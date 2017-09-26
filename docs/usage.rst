=====
Usage
=====

To use Django pin authentication in a project, add it to your `INSTALLED_APPS`:

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
        url(r'^', include(django_pin_auth_urls)),
        ...
    ]
