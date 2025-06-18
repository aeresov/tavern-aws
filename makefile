.PHONY: tidyup
tidyup:
	poetry run isort .
	poetry run black .
