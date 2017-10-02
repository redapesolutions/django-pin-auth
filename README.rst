=============================
Django pin authentication
=============================

.. image:: https://badge.fury.io/py/django-pin-auth.svg
    :target: https://badge.fury.io/py/django-pin-auth

.. image:: https://travis-ci.org/matiboy/django-pin-auth.svg?branch=master
    :target: https://travis-ci.org/matiboy/django-pin-auth

.. image:: https://codecov.io/gh/matiboy/django-pin-auth/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/matiboy/django-pin-auth

.. image:: https://img.shields.io/badge/commitizen-friendly-brightgreen.svg
    :target: http://commitizen.github.io/cz-cli/

Django pin based authentication

Documentation
-------------

The full documentation is at https://django-pin-auth.readthedocs.io.

Quickstart
----------

Install Django pin authentication::

    pip install django-pin-auth

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pin_auth.apps.DjangoPinAuthConfig',
        ...
    )

Add Django pin authentication's URL patterns:

.. code-block:: python

    from django_pin_auth import urls as django_pin_auth_urls


    urlpatterns = [
        ...
        url(r'^pinauth', include(django_pin_auth_urls, namespace='django_pin_auth')),
        ...
    ]

Requirements
------------

You must have sessions enabled.

Development
-----------

You can get an environment with a dev project set up very quickly with Docker:

::

    export COMPOSE_FILE=dev.yml
    docker-compose up

If need be, you can modify the environment variables as declared in the ``.env`` file

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
