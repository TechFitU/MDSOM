

# mdsom

mdsom is a 
simple medical record and appointment tracking and management system. It is built with [Python][0] using the [Django Web Framework][1].

This project has the following basic apps:

* inmediag (Simple handling of medical records and appointments app.)
* accounts (Sign-ups and Log-ins - Basic user registration, log-ins, forgot password etc. styled with crispy forms)
* profiles (User Profiles - extendible user profile with great defaults like profile picture)


## Installation

### Quick start

To set up a development environment quickly, first install Python 3. It
comes with virtualenv built-in. So create a virtual env by:

    1. `$ python3 -m venv mdsom`
    2. `$ . mdsom/bin/activate`

Install all dependencies:

    pip install -r requirements.txt

Run migrations:

    python manage.py migrate
    
### Running demo:
Run the project:

    python manage.py runserver
Browse: http://127.0.0.1:8000/admin

Admin account: _admin@techfitu.com_

Admin Password: _Admin123.!_

### Detailed instructions

Take a look at the docs for more information.

[0]: https://www.python.org/
[1]: https://www.djangoproject.com/
