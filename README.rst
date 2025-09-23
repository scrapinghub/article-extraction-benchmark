Article extraction benchmark: open-source libraries and commercial services
===========================================================================

We evaluate the quality of article body
extraction for commercial services
`Zyte Automatic Extraction (ours) <https://www.zyte.com/data-types/news-scraping-api/>`_,
`Diffbot <https://www.diffbot.com/>`_
and open-source libraries
`newspaper4k <https://github.com/AndyTheFactory/newspaper4k>`_,
`readability-lxml <https://github.com/buriy/python-readability>`_,
`dragnet <https://github.com/dragnet-org/dragnet>`_,
`boilerpipe <https://github.com/misja/python-boilerpipe>`_,
`html-text <https://github.com/TeamHG-Memex/html-text>`_,
`trafilatura <https://github.com/adbar/trafilatura>`_,
`go-trafilatura <https://github.com/markusmobius/go-trafilatura>`_,
`go-readability <https://github.com/go-shiori/go-readability>`_,
`readeck/go-readability <https://codeberg.org/readeck/go-readability>`_,
`Readability.js <https://github.com/mozilla/readability>`_,
`Go-DomDistiller <https://github.com/markusmobius/go-domdistiller>`_.
`news-please <https://github.com/fhamborg/news-please>`_.
`Goose3 <https://github.com/goose3/goose3>`_,
`inscriptis <https://github.com/weblyzard/inscriptis>`_,
`html2text <https://github.com/Alir3z4/html2text>`_,
`jusText <https://github.com/miso-belica/jusText>`_,
`BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>`_.
We release evaluation datasets and scripts,
and provide more details in a whitepaper.

Article extraction is a task of extracting certain fields of an article
(e.g. news or blog post), such as headline, article body, publication date,
authors, etc. Article extraction systems must work on any web-site.
Here we evaluate only the article body field, as this is one of the most important fields
and one of the hardest to get right.

.. contents::

Results
-------

Results of the initial evaluation, done in November 2019::

                      version   F1             precision      recall         accuracy
    AutoExtract       Nov 2019  0.970 ± 0.005  0.984 ± 0.002  0.956 ± 0.010  0.470 ± 0.037
    Diffbot           Nov 2019  0.951 ± 0.010  0.958 ± 0.009  0.944 ± 0.013  0.348 ± 0.038
    boilerpipe        ab3694d   0.860 ± 0.016  0.850 ± 0.016  0.870 ± 0.020  0.006 ± 0.006
    dragnet           1b65e7b   0.907 ± 0.014  0.925 ± 0.013  0.889 ± 0.019  0.221 ± 0.030
    html-text         0.5.1     0.665 ± 0.015  0.500 ± 0.017  0.994 ± 0.001  0.000 ± 0.000
    newspaper3k       0.2.8     0.912 ± 0.014  0.917 ± 0.014  0.906 ± 0.018  0.260 ± 0.032
    readability-lxml  0.7.1     0.922 ± 0.014  0.913 ± 0.014  0.931 ± 0.016  0.315 ± 0.035
    xpath-text        4.4.2     0.394 ± 0.020  0.246 ± 0.016  0.992 ± 0.001  0.000 ± 0.000

Results of the latest evaluation with open source libraries added::

                         version    F1             precision      recall         accuracy
    go-trafilatura       ae7ea06    0.960 ± 0.007  0.940 ± 0.009  0.980 ± 0.006  0.287 ± 0.033
    trafilatura          2.0.0      0.958 ± 0.006  0.938 ± 0.009  0.978 ± 0.006  0.293 ± 0.033
    newspaper4k          0.9.3.1    0.949 ± 0.008  0.964 ± 0.008  0.934 ± 0.011  0.326 ± 0.033
    news_please          1.6.16     0.948 ± 0.008  0.964 ± 0.008  0.933 ± 0.011  0.326 ± 0.034
    readability_js       0.6.0      0.947 ± 0.005  0.914 ± 0.008  0.982 ± 0.003  0.166 ± 0.028
    go_readability_fork  fb0fbc5    0.947 ± 0.005  0.914 ± 0.008  0.982 ± 0.003  0.166 ± 0.028
    go_readability       9f5bf5c    0.934 ± 0.009  0.900 ± 0.011  0.971 ± 0.009  0.188 ± 0.029
    go_domdistiller      25b8d04    0.927 ± 0.007  0.901 ± 0.010  0.956 ± 0.009  0.061 ± 0.017
    readability-lxml     0.8.4.1    0.922 ± 0.013  0.913 ± 0.014  0.931 ± 0.015  0.315 ± 0.034
    goose3               3.1.20     0.896 ± 0.015  0.940 ± 0.013  0.856 ± 0.020  0.232 ± 0.031
    beautifulsoup        4.13.5     0.860 ± 0.016  0.850 ± 0.016  0.870 ± 0.020  0.006 ± 0.006
    justext              3.0.2      0.804 ± 0.018  0.858 ± 0.016  0.756 ± 0.027  0.088 ± 0.021
    inscriptis           2.6.0      0.679 ± 0.015  0.517 ± 0.018  0.992 ± 0.001  0.000 ± 0.000
    html2text            2025.4.15  0.662 ± 0.015  0.499 ± 0.017  0.983 ± 0.002  0.000 ± 0.000

Earlier results from April 2021::

                      version   F1             precision      recall         accuracy
    trafilatura       0.5.1     0.945 ± 0.009  0.925 ± 0.011  0.966 ± 0.009  0.221 ± 0.031
    go_readability    bdc8717   0.943 ± 0.007  0.912 ± 0.009  0.975 ± 0.007  0.210 ± 0.030
    readability_js    Feb 2021  0.887 ± 0.012  0.853 ± 0.013  0.924 ± 0.012  0.149 ± 0.026
    go_domdistiller   1c90a88   0.927 ± 0.007  0.901 ± 0.010  0.956 ± 0.010  0.066 ± 0.018
    news_please       1.5.17    0.911 ± 0.014  0.917 ± 0.013  0.906 ± 0.018  0.249 ± 0.032
    goose3            3.1.8     0.887 ± 0.016  0.930 ± 0.015  0.847 ± 0.021  0.227 ± 0.032
    inscriptis        1.1.2     0.679 ± 0.015  0.517 ± 0.017  0.993 ± 0.001  0.000 ± 0.000
    html2text         2020.1.16 0.662 ± 0.015  0.499 ± 0.017  0.983 ± 0.002  0.000 ± 0.000
    justext           2.2.0     0.802 ± 0.018  0.858 ± 0.017  0.754 ± 0.028  0.088 ± 0.021
    beautifulsoup     4.9.3     0.665 ± 0.015  0.499 ± 0.017  0.994 ± 0.001  0.000 ± 0.000

Below you can find more details about the packages and result reproduction.

More details
------------

More details are available:

- In the whitepaper at https://www.zyte.com/whitepaper-ebook/in-depth-analysis-and-evaluation-on-the-quality-of-article-body-extraction/
- In a technical report attached to the v1.0.0 release at
  https://github.com/scrapinghub/article-extraction-benchmark/releases/tag/v1.0.0

Installation
------------

Clone this repo, and use Python 3.6+.

Evaluation does not require any dependencies.
Dependencies listed in ``requirements.txt`` are only for re-generating
output files for open-source article extraction libraries.
See below for their installation details.

Data
----

JSON data format: a dictionary which maps item ids to dictionaries,
with the following fields:

- ``articleBody``: text of the article
- ``url``: page url (optional)

All files should have the same keys.
Ground truth is in ``ground-truth.json``,
predictions from different systems is in ``output/*.json`` files.

HTML files are in ``html`` folder. They were fetched with Splash headless
browser with JS disabled by default. They are gzip-compressed and utf-8 encoded.

Screenshots of all pages are not in the repo, they are available on github
in the "Releases" section: https://github.com/scrapinghub/article-extraction-benchmark/releases

Open-source libraries
---------------------

In addition to benchmarking AutoExtract and Diffbot services, we also benchmark several
open-source libraries that work directly on HTML files without a need for rendering
or external resources:

- newspaper4k: https://github.com/AndyTheFactory/newspaper4k
- readability-lxml: https://github.com/buriy/python-readability
- dragnet: https://github.com/dragnet-org/dragnet
- boilerpipe: https://github.com/misja/python-boilerpipe
- html-text: https://github.com/TeamHG-Memex/html-text -
  this is a baseline which extracts the full text of HTML page
- trafilatura: https://github.com/adbar/trafilatura contributed by the author
  at https://github.com/scrapinghub/article-extraction-benchmark/pull/4
- go-trafilatura: https://github.com/markusmobius/go-trafilatura
- go-readability: https://github.com/go-shiori/go-readability
- readeck/go-readability: https://codeberg.org/readeck/go-readability/src/branch/main/FORK.md
- Readability.js: https://github.com/mozilla/readability
- Go-DomDistiller: https://github.com/markusmobius/go-domdistiller
- news-please: https://github.com/fhamborg/news-please
- Goose3: https://github.com/goose3/goose3
- inscriptis: https://github.com/weblyzard/inscriptis -
  converts HTML to text with a particular emphasis on nested tables
- html2text: https://github.com/Alir3z4/html2text -
  converts HTML pages to Markup language
- jusText: https://github.com/miso-belica/jusText -
  Heuristic based boilerplate removal tool
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/ -
  Python library for pulling data out of HTML and XML files.

Output from these libraries is already present in the repo in ``output/*.json`` files.
They were generated with ``extractors/run_*.py`` files.

You can re-generate output JSON files with:

    python3 -m venv ./venv
    source ./venv/bin/activate
    make run-all

This will install Python dependencies from ``requirements.txt`` into a
`virtual environment <https://docs.python.org/3/library/venv.html>`_

Evaluation
----------

For evaluation, run::

    python3 evaluate.py

We report precision, recall, F1, accuracy and their standard deviation estimated with bootstrap.
Please refer to the technical report for more details.

License
-------

License is MIT.
