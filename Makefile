.PHONY: install test lint serve doctor

install:
	pip install -e ".[server]"

test:
	pytest -q

lint:
	ruff check roadmind

serve:
	roadmind --config configs/roadmind.mock.yaml serve --port 8000

doctor:
	roadmind doctor
