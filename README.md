Pokemon api
===========
[![Build Status](https://travis-ci.org/magocod/pokemon.svg?branch=master)](https://travis-ci.org/magocod/pokemon)
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

1.1 - Create all virtual environments and activate the py37 virtual environment
(using tox, this command will create two dev environment, use py37, the second environment just to check the code style)
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

## Load initial data

To load the initial database, the following command must be executed, this command takes care of making the correct call to upload documents.
```bash
python manage.py init_db
```

If you look at the available commands, you will see the following (load_pokemons, load_areas, load_regions), in the different applications, although these commands can be called individually these have a restriction, they must be executed strictly in the following order.
```bash
python manage.py load_regions
python manage.py load_pokemons
python manage.py load_areas

```

The init_db command deals with this, prefer to always use this if you want to load all the data and not just a part of it.


## Notes

1 - Currently configuration and credentials (.ini file extension) are saved to repository (should not be done), this is done for testing in travis cl, once this file is successfully removed from repository.

2 - when loading data from json files, no content verification is done

3 - Api doc (available for a limited time, this collection is in source code, pokemon/docs).
https://documenter.getpostman.com/view/13062236/TVRn3SRe

4 - Note that this project may not currently have a configuration optimized for use in a production environment.

## Bugs

1 - A small part of the pokemons cannot be assigned an area correctly, due to the Unicode names, which are currently not verified correctly (about 25)

2 - Currently testing Pokemon exchange service (active team to warehouse, warehouse to active team), it can only be run on sqlite3 (tests/pokemons/test_swap_party_member)

3 - the tests use the data available in the load jsons, so your start may have a delay
