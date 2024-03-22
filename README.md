# ursuppe

 ursuppe is an open submission and event platform for cultural projects written in Django, with three primary functions:
 - An open submissions platform for image documentation
 - An open events calendar with an integrated map and ical feed
 - Index with highlights
 
## Prerequisities

- python3
- git
- redis-server (optional)

## Installation

Clone this repository:

`$ git clone git@github.com:ursuppeeppusru/ursuppe.git`

Setup and activate virtualenv:

`$ python3 -m venv env`

Install Python packages:

`$ pip install -r requirements.txt`

Create .env file:

`$ cp ./primordialsoup/.env-example ./primordialsoup/.env`

Configure by editing the `.env` file and remember to add `DEBUG=True` for localhost

If production, provision redis cache:

`$ python manage.py createcachetable`

Provision database:

`$ python manage.py migrate`

Create superuser:

`$ python manage.py createsuperuser`

Run development server*:

`$ python manage.py runserver`

Note that for production it is recommended to run the application with [WSGI](https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/).

## Cache

The default cache program is redis and is enabled by default in the production environment. The default cache is set to 1 hour and can be configured in each views found in the `views.py` files under each Django app.

## Styling

CSS `:root` variables for light and dark mode, as well as other styling options can be found in `primodialsoup.css`.  
  
## License

As a worker-owned cooperative that strives to avoid exploitation, discrimination and violence we are using [CNPLv7+ - The Cooperative Non-Violent Public License](https://github.com/ursuppeeppusru/ursuppe/blob/development/LICENSE.md). It aims to ensure basic protections against forms of violence, coercion, and discrimination which creations are frequently leveraged for in the modern world. This license covers several formats of creative work but has extra terms for software given the power it has as a tool outside of its creative capacities. The cooperative layer only allows commercial use of the copyrighted work for individuals and worker-owned organizations. 
