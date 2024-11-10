Introduction
============
This is introduction how to setup this project

## Prerequisite
- Python3 (pip)
- Git


## Setup project environment
Clone this repository
```
$ git clone 
```
Move to Task Management API folder `cd Task Management API`
Init virtual environment and activate 
```
$ pip install virtualenv
$ python -m virtualenv env
$ source env/Scripts/activate
```

Install all dependencies and module
```
$ pip install -r requirements.txt
``` 

## Setup database
There are many way to set up posgresql the database
- Docker
```
$ docker run --name some-postgres -e POSTGRES_PASSWORD=yoursecretpassword -d postgres
```
- Local database (https://www.postgresql.org/download/)
- Cloud database (https://customer.elephantsql.com/)

## Integrate database with our project
At Task Management API folder, create `.env` file, add database config to file with format
```
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host_or_localhost
DB_PORT=your_database_port_default_is_5432
```

After setup database config successfully, migrate data and connect to our database is neccessary
At Task Management API folder:
```
$ python manage.py migrate
```
By type this comment, django will init table, relation, and default data (via `0001_initial.py`)

## Run project

Launch server on port 8000
```
$ python manage.py runserver
```

Api provide endpoints:

```
GET localhost:8000/tasks/
POST localhost:8000/tasks/
GET localhost:8000/tasks/:id
PUT localhost:8000/tasks/:id
DELETE localhost:8000/tasks/:id
```

## API Testing
Requires: rest client extension on VS code
Open file `api_testing.http` on VS code
Click on send request for each end point
