all : test

.PHONY: all test mypy pylint django-check django-test

test: django-check django-test mypy pylint

django-check:
	python manage.py check

django-test:
	python manage.py test

mypy:
	mypy --version && mypy -m squaresdb

pylint:
	pylint --version && pylint --rcfile=pylintrc.ini squaresdb/

runserver:
	python manage.py runserver 8007
