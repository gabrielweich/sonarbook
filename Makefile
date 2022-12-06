lint:
	cd api && poetry run pre-commit install && poetry run pre-commit run -a -v
