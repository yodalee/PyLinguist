# PyLinguist
This is a Python Qt tf file translator using Google Translation

## Pre-request
PyLinguist require python package Goslate  
https://pypi.python.org/pypi/goslate  
Can be installed by pip:  
$ pip install goslate  

## Usage
python PyLinguist.py input\_ts\_file target\_language  
ex: python PyLinguist.py en.ts de  

available option:  
-B: close automatic backup  
-v: open verbose translate, result will be print out  

## Language Support
The language that google translate supportted can be found at:  
https://cloud.google.com/translate/v2/using\_rest#language-params

## Bugs
* Please report bugs to the Github issue tracker.
