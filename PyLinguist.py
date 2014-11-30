#!/usr/bin/env python
# encoding: utf-8

import goslate
import xml.etree.ElementTree as ET
import argparse
import sys


class PyLinguist(object):
    """PyLinguist: wrap of goslate and XML parser"""
    gs = goslate.Goslate()
    tree = None

    def __init__(self):
        self.maplist = {}
        self.tree = None

    def parseXML(self, filename):
        """Parse input XML file and parse into list"""
        self.tree = ET.parse(filename)
        root = self.tree.getroot()
        # Add translated text to dict
        for msg in root.iter('message'):
            source = msg.find('source').text
            translation = msg.find('translation').text
            isTranslated = not (msg.find('translation').attrib.get('type') == "unfinished")
            if isTranslated and source not in self.maplist:
                self.maplist[source] = translation

    def translate(self, target_lang):
        """use goslate to translate from source_lang to target_lang

        :text: text to translate
        :source_lang: source language, ex. "en"
        :target_lang: target language, ex. "de"
        :returns: translated text

        """
        root = self.tree.getroot()
        for msg in root.iter('message'):
            source = msg.find('source').text
            isTranslated = not (msg.find('translation').attrib.get('type') == "unfinished")
            if not isTranslated:
                if source in self.maplist:
                    msg.find('translation').text = self.maplist[source]
                    del msg.find('translation').attrib['type']
                else:
                    # print(source)
                    # print(target_lang)
                    try:
                        text = self.gs.translate(source, target_lang)
                        msg.find('translation').text = text
                        self.maplist[source] = text
                        del msg.find('translation').attrib['type']
                    except Exception:
                        pass

        return self.gs.translate(source, target_lang)

    def writeXML(self, filename):
        """Write tree object into file"""
        self.tree.write(filename, xml_declaration=True, encoding="UTF-8", method="html")

    def print(self):
        """print out maplist
        """
        for item in self.maplist:
            print(item)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate Qt tf file')
    parser.add_argument('-i', dest='inputFile',
                        help='specify the input filename')
    parser.add_argument('-o', dest='outputFile',
                        help='specify the output filename')
    parser.add_argument('-t', dest='target', default='en',
                        help='specify the target language')
    args = parser.parse_args()

    if not args.inputFile or not args.outputFile:
        parser.print_help()
        sys.exit(1)

    trans = PyLinguist()
    trans.parseXML(args.inputFile)
    trans.translate(target_lang=args.target)
    trans.writeXML(args.outputFile)
