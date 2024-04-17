import pytest

from taxman.app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        {
            "TESTING": True,
        },
    )

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


def test_income_tax_200(client):
    response = client.post("/v1/income-tax/year/2022", json={"income": 5000})
    assert response.status == "200 OK"


def test_income_tax_400(client):
    response = client.post("/v1/income-tax/year/2022", json={})
    assert response.status == "400 BAD REQUEST"


def test_income_tax_404(client):
    response = client.post("/v1/income-tax/year/1022", json={})
    assert response.status == "404 NOT FOUND"


def test_income_tax_422(client):
    response = client.post("/v1/income-tax/year/2022", json={"income": "banana"})
    assert response.status == "422 UNPROCESSABLE ENTITY"


def test_income_tax_503(client, mocker):
    mocker.patch(
        "taxman.views.income_tax.requests.Session.get",
        side_effect=Exception,
    )

    response = client.post("/v1/income-tax/year/2022", json={"income": 5000})
    assert response.status == "503 SERVICE UNAVAILABLE"
