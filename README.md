# TAXMAN

## Development

Setup development environment:

```
python -m venv venv
pip install requirements/dev.txt
pip install lint.txt
pip install test.txt
```

Running the app in development mode:

```
flask --app taxman.app run --debug
```

Once running, interactive documentation is available at:

`http://127.0.0.1:5000/apidocs/`


### Testing

Running the Unit tests:

```
pytest --cov=taxman
```

Running the linting tools:

```
ruff check .
ruff format
pyright
```
