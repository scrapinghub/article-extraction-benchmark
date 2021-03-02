Article extraction benchmark: open-source libraries and commercial services
===========================================================================

We evaluate the quality of article body
extraction for commercial services
`Zyte Automatic Extraction (ours) <https://www.zyte.com/data-types/news-scraping-api/>`_,
`Diffbot <https://www.diffbot.com/>`_
and open-source libraries
`newspaper3k <https://newspaper.readthedocs.io/en/latest/>`_,
`readability-lxml <https://github.com/buriy/python-readability>`_,
`dragnet <https://github.com/dragnet-org/dragnet>`_,
`boilerpipe <https://github.com/misja/python-boilerpipe>`_,
`html-text <https://github.com/TeamHG-Memex/html-text>`_,
`trafilatura <https://github.com/adbar/trafilatura>`_,
`go-readability <https://github.com/go-shiori/go-readability>`_,
`Readability.js <https://github.com/mozilla/readability>`_,
`Go-DomDistiller <https://github.com/markusmobius/go-domdistiller>`_.
`news-please <https://github.com/fhamborg/news-please>`_.
`Goose3 <https://github.com/goose3/goose3>`_,
`inscriptis <https://github.com/weblyzard/inscriptis>`_.
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

Results of the initial evaluation::

    AutoExtract          precision=0.984 ± 0.002  recall=0.956 ± 0.010  F1=0.970 ± 0.005 accuracy=0.470 ± 0.037
    Diffbot              precision=0.958 ± 0.009  recall=0.944 ± 0.013  F1=0.951 ± 0.010 accuracy=0.348 ± 0.038
    boilerpipe           precision=0.850 ± 0.016  recall=0.870 ± 0.020  F1=0.860 ± 0.016 accuracy=0.006 ± 0.006
    dragnet              precision=0.925 ± 0.013  recall=0.889 ± 0.019  F1=0.907 ± 0.014 accuracy=0.221 ± 0.030
    html-text            precision=0.500 ± 0.017  recall=0.994 ± 0.001  F1=0.665 ± 0.015 accuracy=0.000 ± 0.000
    newspaper            precision=0.917 ± 0.014  recall=0.906 ± 0.018  F1=0.912 ± 0.014 accuracy=0.260 ± 0.032
    readability          precision=0.913 ± 0.014  recall=0.931 ± 0.016  F1=0.922 ± 0.014 accuracy=0.315 ± 0.035
    xpath-text           precision=0.246 ± 0.016  recall=0.992 ± 0.001  F1=0.394 ± 0.020 accuracy=0.000 ± 0.000

Result of packages added after original evaluation::

    trafilatura          precision=0.925 ± 0.011  recall=0.966 ± 0.009  F1=0.945 ± 0.009 accuracy=0.221 ± 0.031
    go_readability       precision=0.912 ± 0.009  recall=0.975 ± 0.007  F1=0.943 ± 0.007 accuracy=0.210 ± 0.030
    readability_js       precision=0.853 ± 0.013  recall=0.924 ± 0.012  F1=0.887 ± 0.012 accuracy=0.149 ± 0.026
    go_domdistiller      precision=0.901 ± 0.010  recall=0.956 ± 0.010  F1=0.927 ± 0.007 accuracy=0.066 ± 0.018
    news_please          precision=0.917 ± 0.013  recall=0.906 ± 0.018  F1=0.911 ± 0.014 accuracy=0.249 ± 0.032
    goose3               precision=0.930 ± 0.015  recall=0.847 ± 0.021  F1=0.887 ± 0.016 accuracy=0.227 ± 0.032
    inscriptis           precision=0.517 ± 0.017  recall=0.993 ± 0.001  F1=0.679 ± 0.015 accuracy=0.000 ± 0.000

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

- newspaper3k: https://github.com/codelucas/newspaper
- readability-lxml: https://github.com/buriy/python-readability
- dragnet: https://github.com/dragnet-org/dragnet
- boilerpipe: https://github.com/misja/python-boilerpipe
- html-text: https://github.com/TeamHG-Memex/html-text -
  this is a baseline which extracts the full text of HTML page
- trafilatura: https://github.com/adbar/trafilatura contributed by the author
  at https://github.com/scrapinghub/article-extraction-benchmark/pull/4
- go-readability: https://github.com/go-shiori/go-readability
- Readability.js: https://github.com/mozilla/readability
- Go-DomDistiller: https://github.com/markusmobius/go-domdistiller
- news-please: https://github.com/fhamborg/news-please
- Goose3: https://github.com/goose3/goose3
- inscriptis: https://github.com/weblyzard/inscriptis -
  converts HTML to text with a particular emphasis on nested tables

Output from these libraries is already present in the repo in ``output/*.json`` files.
They were generated with ``extractors/run_*.py`` files.

All dependencies are in ``requirements.txt``.
Note that dragnet may fail to install at first try, as
you need to have ``numpy`` and ``Cython`` installed, and have ``libxml2`` headers
(``libxml2-dev`` on Ubuntu).

boilerpipe requires a custom installation: use python2, you also need Java
(e.g. install ``default-jre`` in Ubuntu), install it with
``pip install -e git+https://github.com/misja/python-boilerpipe.git@ab3694d7bf695b73f0684a028e70aa816d63e6cb#egg=boilerpipe``

go-readability requires a custom installation: see README in ``extractors/go_readability``.

Readability.js require a custom installation: install nodejs and install cli tool:
``npm install -g readability-cli@2.2.1-pre``

Go-DomDistiller requires a custom installation: see README in ``extractors/go_domdistiller``.

Evaluation
----------

For evaluation, run::

    python3 evaluation.py

We report precision, recall, F1, accuracy and their standard deviation estimated with bootstrap.
Please refer to the technical report for more details.

License
-------

License is MIT.
