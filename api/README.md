# Sonarbook



## Local execution

- After clone the project install dependencies with poetry

```sh
$ poetry install
```

- Use docker compose to start PostgreSQL

```sh
$ docker-compose up -d --build postgres
```

- Configure environment variables

```sh
$ cp .env.development .env
```

- Run migrations to update the database

```sh
$ poetry run alembic upgrade head
```

- Start the API

```sh
$ poetry run uvicorn src.main:app --reload --port 8000
```


## Authentication Keys

Asymmetric keys are used for encryption/decryption of the access token, enabling other services to validate the token using the public key. For development pourposes, keys are provided in .env.development, although is recommended to generate new ones for production, this can be done with the following commands:

```sh
$ openssl genrsa -out private.pem 2048
$ openssl rsa -in private.pem -pubout -out public.pem
```

- Transform the keys in single lines and copy it's values to PRIVATE_KEY and PUBLIC_KEY env variables in .env:
```sh
$ awk -v ORS='\\n' '1' private.pem
$ awk -v ORS='\\n' '1' public.pem
```

