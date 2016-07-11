.PHONY: test doc

all:   # Do nothing

clean:
	python setup.py clean
	rm -f MANIFEST
	rm -rf dist
	rm -rf asr_tools.egg-info/
	rm -rf build
	find . -name *.pyc -exec rm -rf '{}' \;
	rm -rf htmlcov
	rm -rf doc

test:
	python3 setup.py test

coverage:
	python3 -m coverage erase
	python3 -m coverage run --source asr_tools setup.py test
	python3 -m coverage report
	python3 -m coverage html

doc:
	mkdir -p doc
	pydoc -w `find asr_tools -name '*.py'`
	mv *.html doc

showdoc:
	pydoc `find asr_tools -name '*.py'`

style:
	pep8 --max-line-length=120 --ignore=E701,E302
