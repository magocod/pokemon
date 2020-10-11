Pokemon api
===========
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Framework

* Django -> https://www.djangoproject.com/

## third-party

* Django-rest-framework -> https://www.django-rest-framework.org/
* black -> https://black.readthedocs.io/en/latest/
* isort -> https://timothycrosley.github.io/isort/

## Tox env

* Python 3.7
* Python lint (flake8)

## Tests

* Pytest -> https://docs.pytest.org/en/latest/
* coverage -> https://coverage.readthedocs.io/en/latest/

## Instructions

1 - Create a virtual python environment and install libraries with pip
```bash
pip install -r requirements/py37.txt
```

1.1 - Create all virtual environments (using tox)
```bash
tox
```

2 - Migrate the database
```bash
python manage.py migrate
```

3 - Run tests (verify successful installation)
```bash
pytest
```

3.1 - Run tests (verify coverage)
```bash
coverage run -m pytest
coverage report
coverage html
```

4 - Run development server
```bash
python manage.py runserver
```

5 - Enter the address
```bash
http://localhost:8000
```
