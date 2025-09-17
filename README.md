# mini-forum

this is a mini-forum application built with django (backend) and vue 3 (frontend). the backend uses django rest framework and jwt authentication. the frontend communicates with the backend through a rest api. the project is containerized using docker and can be run on vds/vps servers.

## features

* user registration and login with jwt authentication
* post and reply to comments
* captcha validation when posting comments
* file attachments for comments
* simple frontend interface with login/register modals

## requirements

* vds or vps with ubuntu 22.04+
* docker and docker compose installed
* git installed

## setup instructions

### install dependencies on server

```bash
apt update && apt upgrade -y
apt install -y git docker.io docker-compose postgresql-client
```

### clone the repository

```bash
git clone https://github.com/your-username/comments_project.git
cd comments_project
```

### create .env file

create a `.env` file in the project root:

```env
POSTGRES_DB=comments_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=jdth,fath
VITE_API_URL=http://localhost:8000/api/
```

### build and run with docker compose

```bash
docker compose up --build
```

this will start three services:

* **db** (postgres)
* **web** (django backend)
* **frontend** (vue app)

backend will be available at `http://localhost:8000/api/` and frontend at `http://localhost:5173/`.

### run migrations and collect static files

inside the running container:

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py collectstatic --noinput
```

## database schema

an erd (entity-relationship diagram) for the database is provided in `db_schema.mwb`, which can be opened in mysql workbench to compare the planned and actual schema.

## usage

* open the frontend in browser: `http://localhost:5173/`
* register or log in
* post comments and replies
* attach files and solve captcha before submitting

## testing

for self-check:

1. clone repo on a clean machine
2. create `.env` file as shown above
3. run `docker compose up --build`
4. apply migrations
5. verify registration, login, posting comments

## additional notes

* the database password is set to `jdth,fath` in this project for testing purposes
* for production, update `.env` with a strong password
* if using vds with a domain, replace `localhost` with your domain/ip in `.env` file
