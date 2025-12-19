#!/bin/bash

set -x
emacs --batch --eval "(require 'package)" --eval "(package-initialize)" README.org -f org-html-export-to-html
