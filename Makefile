.PHONY: setup
setup:
	pip install -r requirements.txt
# for news_please:
	python -m nltk.downloader --dir "${VIRTUAL_ENV}"/nltk_data punkt_tab
	cd extractors/readability_js && npm install --no-audit --no-fund
	make -C extractors/go_domdistiller
	make -C extractors/go_readability
	make -C extractors/go_readability_readeck
	make -C extractors/go_trafilatura

.PHONY: run-all
run-all: run-go run-python
	python extractors/run_readability_js.py

.PHONY: run-go
run-go: setup
	python extractors/go_domdistiller.py
	python extractors/run_go_readability_readeck.py
	python extractors/run_go_readability.py
	python extractors/run_go_trafilatura.py

.PHONY: run-python
run-python: setup
	python extractors/run_beautifulsoup.py
# PYTHON2	extractors/run_boilerpipe.py
# ERRORED	extractors/run_dragnet.py
	python extractors/run_goose3.py
	python extractors/run_html_text.py
	python extractors/run_html2text.py
	python extractors/run_inscriptis.py
	python extractors/run_justext.py
	python extractors/run_readability.py
	python extractors/run_trafilatura.py
	python extractors/run_xpath_text.py

.PHONY: run-slow
# These libraries use machine learning inference, so they can be extremely slow
run-slow: setup
	python extractors/run_news_please.py
	python extractors/run_newspaper.py
