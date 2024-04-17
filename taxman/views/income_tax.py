from flask import abort, Blueprint, request
from loguru import logger
import requests
from requests.adapters import HTTPAdapter, Retry

from ..calculate_taxes import calculate_tax_info

session = requests.Session()

# Handle intermittent issues with the tax bracket API.
retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504],
)

session.mount("http://", HTTPAdapter(max_retries=retries))

SUPPORTED_YEARS = [2019, 2020, 2021, 2022]

income_tax = Blueprint("income_tax", __name__, url_prefix="/v1/income-tax")


@income_tax.route("/year/<int:year>", methods=["POST"])
def income_tax_year(year: int):
    """For the given year, get total income tax for an amount.
    ---
    parameters:
        - name: year
          in: path
          type: integer
          required: true
        - name: data
          in: body
          schema:
              type: object
              properties:
                income:
                    type: integer
                    example: 100000
                    required: true
    responses:
        200:
            description: Total income tax for the given amount.
    """
    if year not in SUPPORTED_YEARS:
        abort(404, description=f"Year {year} is not supported.")

    income = request.json.get("income")  # type: ignore
    if income is None:
        abort(400, description="income parameter not in request body.")

    # Get tax brackets.
    tax_bracket_url = f"http://localhost:5001/tax-calculator/tax-year/{year}"
    try:
        response = session.get(tax_bracket_url)
        tax_brackets = response.json()["tax_brackets"]
    except Exception:  # NOQA BLE001
        logger.exception("Tax Bracket API did not return a response.")
        abort(
            503,
            description=(
                "Service unavailable, please try unplugging your modem, waiting "
                "for 30 seconds, and plugging it back in."
            ),
        )

    try:
        rv = calculate_tax_info(tax_brackets, income)
        status_code = 200

    except TypeError as e:
        abort(422, description=f"{e}")

    else:
        return rv, status_code
