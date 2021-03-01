Go-DomDistiller
===============

Open Source article extractor written on golang: https://github.com/markusmobius/go-domdistiller.
Based on `DOM Distiller <https://chromium.googlesource.com/chromium/dom-distiller>`_ which is part of the Chromium project that is built using Java language.
The structure of this package follows the structure of the original Java code

Usage
-----

To use the library I'm wrote a simple cli-module that reads the contents of the file passed in the arguments and outputs the parsing result to stdout.


Installation
------------

1. Install golang (I'm used version ``1.15.8``)
2. Go to the folder containing this file
3. Build an executable file:

    go build -o go_domdistiller_cli
