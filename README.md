Pokemon api
===========
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Framework

* Django -> https://www.djangoproject.com/

## third-party

* Django-rest-framework -> https://www.django-rest-framework.org/
* black -> https://black.readthedocs.io/en/stable/
* isort -> https://timothycrosley.github.io/isort/

## Tox env

* Python 3.7
* Python lint (flake8)

## Tests

* Pytest -> https://docs.pytest.org/en/latest/
* coverage -> https://coverage.readthedocs.io/en/coverage-5.0.3/

## Instructions

Create a virtual python environment and install libraries with pip

```bash
pip install -r requirements.txt
```

Create all virtual environments (using tox)
```bash
tox
```

Migrate the database

```bash
python manage.py migrate
```

run tests (verify successful installation)
```bash
pytest
```

run tests (verify coverage)
```bash
pytest --cov
```

Run development server

```bash
python manage.py runserver
```

Enter the address

```bash
http://localhost:8000
```
