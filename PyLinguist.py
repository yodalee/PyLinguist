#!/usr/bin/env python
# encoding: utf-8

import goslate
import xml.etree.ElementTree as ET
import argparse
import time
import os.path
import shutil


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

        :target_lang: target language, ex. "de"

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

    def printTranslatedMap(self):
        """print out maplist
        """
        for key, val in self.maplist.items():
            print(key, val)


def generateName(filename):
    """Generate backup filename

    :filename: the input filename
    :returns: the output filename
    """
    dirname = os.path.dirname(filename)
    basename = os.path.basename(filename)
    noext = os.path.splitext(basename)[0]
    genName = noext + "_backup" + time.strftime("%H%M.ts")
    return os.path.join(dirname, genName)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Translate Qt tf file')
    parser.add_argument('filename', metavar=".tsfile", type=str,
                        help='file to be translate')
    parser.add_argument('lang', metavar="lang", type=str,
                        help='target translate language')
    args = parser.parse_args()

    backupFile = generateName(args.filename)
    print("Translate file: " + args.filename)
    print("Target Language: " + args.lang)
    print("Backup file: copy to " + backupFile)

    shutil.copy(args.filename, backupFile)

    print("Start Translate: ")
    trans = PyLinguist()
    trans.parseXML(args.filename)
    trans.translate(target_lang=args.lang)
    trans.writeXML(args.filename)
