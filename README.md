# String Reversal Web Service

A web service for reversing strings, where reversing a string takes 5 seconds of CPU-bound work.

## Introduction

In this project, we are solving the problem of string reversal, which involves reversing a string (e.g., turning "ABC" into "CBA").
However, in our fictional world, reversing any string takes exactly 5 seconds of CPU-bound work.

To address this, we will be building a string-reversal web service.
This service will allow users to submit a string of their choice via a REST API.
The reversal will be computed, and the result made available to users.

Users are aware that reversing a string is a time-consuming task, so they are okay with not receiving the result immediately.
They can come back later to see their results.

To address the computational complexity of string reversal, we will be splitting the work into two separate services.

### User Service

- User-facing via a simple REST API.
- Provides a POST endpoint that allows users to submit a string for reversal.
    - Generates a unique request ID and returns it to the user.
    - Responds with HTTP status 202 Accepted.
- Offers a GET endpoint that takes the request ID and returns the request's status.
    - Possible statuses: Pending, Done, Failed.
    - If the status is Done, it returns the reversed string to the user.
- Users submit requests and poll the GET endpoint to retrieve their results.
- To ensure the availability of the API, the reversal is not computed directly in the user service. Instead, a reversal request is published into an internal event bus, and the result is delivered back to the user asynchronously.

### Reversal Service

- Not directly accessible to the user.
- Subscribes to reversal requests on the internal event bus. When a reversal request is received, it computes the reversal and publishes the result back into the event bus.
- Only communicates with the rest of the system via the event bus.

## Main tools & libs used in project
- [Python 3.11](https://www.python.org/downloads/release/python-3116/)
- [Poetry](https://python-poetry.org/) modern and powerful package manager
- [FastAPI](https://fastapi.tiangolo.com/) backend framework
- [Alembic](https://pypi.org/project/alembic/) library for database migration 
- [Postgres](https://www.postgresql.org/) main project database
- [RabbitMQ](https://www.rabbitmq.com/) message broker
- [Docker]() & [Docker Compose]() Containerized development tools
- [Pytest](https://docs.pytest.org/en/7.1.x/) modern, flexible python framework for testing

## Development
To run the app locally, you can use the features provided by containerization using `Docker` and
`Docker Compose`. They can greatly isolate the development process and unify the development result across all dev's
machines, but before using `Docker` you have to do a few steps:

**Install poetry package manager to your machine**
```shell
pip install poetry
```
**Activate poetry**
```shell
poetry shell
```
**Install dependencies to venv**
```shell
poetry install
```

Next step is build Docker image and start docker containers:

#### Via `docker-compose`
```shell
docker-compose up -d
```

The final step is accepting exist alembic migration to the Postgres instance.

**Open a new terminal session and type the command:**

```shell
docker exec -t user_service poetry run alembic upgrade head
```

## Database migrations

As mentioned above to apply migration is necesseary to start docker containers and than execute migration command in new teminal session.

### Revert migrations

Sometimes may happen that we have some corrupted migrations in database so we need to revert them. For this purpose exists following command:

```shell
docker exec -t user_service poetry run alembic downgrade -1
```
Note: The number at the end of the command (`-1`) specifies how many migrations we want to revert.

### New migration
Alemic works based on automatically generated migrations from changes in the database schema in the code and the current state of the database itself. To create a new migration, you need to do the following steps:

- Make sure that databases schema is up to date (all migrations are applied)
- Make desired change of database schema in code (add new table, change column, etc.)
- Execute following command to generate new migration:

```shell
docker exec -t user_service poetry run alembic revision --autogenerate -m "<NAME_OF_MIGRATION>"
```

## Tests

We use `pytest` library for writing unit tests on BE. To run tests execute following command:

```shell
docker-compose -f docker-compose.test.yml run tests
```

Note: Tests have separated postgres instance started by test docker-compose file.