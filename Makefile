init:
	pip install -r requirements.txt

test:
	pytest tests

build:
	python setup.py sdist

upload:
	twine upload dist/*
