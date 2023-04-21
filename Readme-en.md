![logo](misc/img/logo.png)

# Online store based on Django and Vue3

### Core technologies

* Frontend: HTML5, CSS3, JS, Vue3
* Backend: python 3.10, django 4.2, django rest framework 3.14
* Working with data is implemented in the PostgreSQL 15.2 DBMS

### Implementation Features

* The database structure is available [here](misc/img/database.png)
* Frontend and backend applications communicate via an API written in DRF
* Basic API get-routes are cached in local memory
* In the admin panel you can create, view, edit, delete and deactivate
  (soft-delete) entities:
    * products and related specifications, tags, reviews, promotions
    * categories, subcategories
    * users, including those with administrator rights
    * orders, payments
* The user's basket is implemented through a browser session, until the order
  is placed, information about it is not added and not stored in the database.
* Calling the site to the API implemented by setting the header in requests
  (X-HERE-I-AM)

### Repository structure

* `misc/` - directory with files needed to display documentation and
  other support files
* `requirements/` - directory with files containing a list of dependencies
* `shop/` - directory with the Django project itself
* `.env.template` - template for declaring environment variables
* `demo.sh` - demo script
* `swagger.yaml` - API contract

### Demo deployment unstructions

You might want to use
[script to install and run](#установка-с-помощью-скрипта)

ATTENTION! The instruction below is written for Unix-like OS users,
all commands must be run in a terminal. It is assumed that at the beginning
installation you are at the root of the project

1. Copy the repository.
2. Rename the [.env.template](.env.template) file to `.env`,
   fill it according the template.

3. Install dependencies.
    ```shell
    pip install -r requirements/base.pip
    ```
4. Go to project root
    ```shell
   cd shop/
   ```
5. Run [PostgreSQL](#start-subd-postrgesql) or your favorite DBMS
   (in this case, change [settings](shop/backend/settings.py#L125))

6. Apply migrations

   **ATTENTION! Before running the following commands, make sure your database
   is ready to go (see paragraph 5)**
    ```shell
    python manage.py migrate
    ```

7. **!Developing**

   Create some demo content by loading fixtures
    ```shell
   python manage.py loaddata fixtures/data.json
   ```
   The following will appear in the database:
    * directories
    * products with reviews, specifications, tags
    * super-user with `admin` as both login and password
    * three regular users (user1, user2, user3) with password 123456

8. And finally start the Django test server
    ```shell
   python manage.py runserver
   ```

9. The site is available at http://localhost:8000/
10. Admin panel http://localhost:8000/admin/

### Starting PostgreSQL

It is assumed that you have already installed
[docker](https://docs.docker.com/desktop/install/linux-install/)

1. From the project root go to the `postgres` directory
    ```shell
   cd shop/postgres/
   ```
2. Enter commands
    ```shell
   docker compose build
   docker compose up -d
   ```

   As a result, the PostgreSQL DBMS will be launched at the
   http://localhost:5432/
3. Don't forget to go back up a level
    ```shell
   cd ..
   ```

[Back to instructions](#инструкция-по-демонстрационному-развертыванию)

### Installation using a script

1. Run demo.sh script from project root
    ```shell 
    source demo.sh
    ```
   All settings will be done automatically (you will still need
   docker pre-installed)

2. The site is available at http://localhost:8000/
3. Admin panel http://localhost:8000/admin/