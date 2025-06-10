.PHONY: dev tests lint fmt

dev:            
	poetry install
	pre-commit install
	uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000

tests:        
	pytest -q

lint:           
	ruff check .
	mypy .

fmt:           
	ruff format .

help:
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*##"}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
