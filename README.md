# Django CRM Panel

A simple CRM panel built to demonstrate  some of the important features of Django (forms, signals and more).

## Setup

1. Create virtual environment:
    ```
    python3 -m venv venv
    ```
    Windows:
    ```
    py -m venv venv
    ```

2. Activate environment:
    ```
    source venv/bin/activate
    ```
    Windows:
    ```
    source venv/Scripts/activate
    ```

3. Install requirements:
    ```
    pip install -r requirements.txt
    ```

4. Create database and update database settings (settings.py); or use dafault sqlite3 database

5. Generate a new secret key. The quickest way is to use Django Secret Key Generatos like [djecrety](https://djecrety.ir/)

6. Make & run migrations:
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```
    Windows
    ```
    py manage.py makemigrations
    py manage.py migrate
    ```

7. (Optional) Use Django fixtures to prepopulate database:
    Load fixtures in this order:
    ```
    ./manage.py loaddata group_data.json
    ./manage.py loaddata user_data.json
    ./manage.py loaddata customer_data.json
    ./manage.py loaddata tag_data.json
    ./manage.py loaddata product_data.json
    ./manage.py loaddata order_data.json
    ```

7. If you don't use fixtures, manually create superuser :
    ```
    python manage.py createsuperuser
    ```
    Windows
    ```
    py manage.py createsuperuser
    ```
    - After login in admin panel create two groups: 'admin' and 'customer'
    - Add your superuser to 'admin' group

        > If you want to use build in user permissions (user type) in place of groups - allowed_users decorator must be modified (accounts/decorators.py).
        > Currently it takes one argument: groups array , which should be removed and group related code in wrapper func replaced with user permissions.

8. Start the development server:
    ```
    python manage.py runserver
    ```
    Windows
    ```
    py manage.py runserver
    ```