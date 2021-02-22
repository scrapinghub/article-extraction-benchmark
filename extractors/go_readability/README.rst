Go-Readability
==============

Open Source article extractor written on golang: https://github.com/go-shiori/go-readability . Based from `Readability.js <https://github.com/mozilla/readability>`_ by Mozilla, and written line by line to make sure it looks and works as similar as possible.

Usage
-----

To use the library I'm wrote a simple cli-module that reads the contents of the file passed in the arguments and outputs the parsing result to stdout.


Installation
------------

1. Install golang (I'm used version ``1.15.8``)
2. Go to the folder containing this file
3. Build an executable file:

    go build -o go_readability_cli
