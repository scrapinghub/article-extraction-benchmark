Article extraction benchmark
============================

This repo allows to reproduce results of article extraction benchmark.

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
Ground truth is in ``groud-truth.json``,
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

Output from these libraries is already present in the repo in ``output/*.json`` files.
They were generated with ``run_*.py`` files.

All dependencies are in ``requirements.txt``.
Note that dragnet may fail to install at first try, as
you need to have ``numpy`` and ``Cython`` installed, and have ``libxml2`` headers
(``libxml2-dev`` on Ubuntu).

boilerpipe requires a custom installation: use python2, you also need Java
(e.g. install ``default-jre`` in Ubuntu), install it with
``pip install -e git+https://github.com/misja/python-boilerpipe.git@ab3694d7bf695b73f0684a028e70aa816d63e6cb#egg=boilerpipe``

Evaluation
----------

For evaluation, run::

    python3 evaluation.py

We report precision, recall, F1, accuracy and their standard deviation estimated with bootstrap.
Please refer to the technical report for more details.

License
-------

License is MIT.
