import xml.etree.ElementTree as ET
import os
import re
import collections
import pandas as pd

_author_ = 'tdhiman@worldquant.com'

"""
PURPOSE: This module will parse the xml files
from the given directory and converted in to
the csv format.

How it will convert:
It will find all the unique possible combinations
from the xml files and used these combinations as
the label for that csv files and assigned values
corresponding values to them
"""

class XML:

    def __init__(self, dir=None, dataset=None, type=None):
        self.output = collections.defaultdict(list)
        self.dir = dir
        self.dataset = dataset
        self.type = type

    def generatorXML(self, parent, pre=None):
        pre = pre[:] if pre else [parent.tag]

        if parent.attrib:
            for k,v in parent.attrib.iteritems():
                yield pre + ['attrib'] + [k] + [v]

        if len(list(parent)) > 0:
            for child in parent:
                for d in self.generatorXML(child, pre + [child.tag]):
                    yield d
        else:
            yield pre + [parent.text]

    def iterateInDir(self):
        output = collections.defaultdict(list)
        for file in [os.path.join(self.dir, filename) for filename in os.listdir(self.dir)]:
            print 'Running for this file: '+str(file)
            with open(file) as f:
                if self.type == '1':
                    data = ET.fromstring(f.read())
                    for op in self.generatorXML(data, None):
                        key = '/'.join(op[:-1])
                        value = op[-1]
                        output[key].append(value)
                else:
                    for line in f:
                        data = ET.fromstring(line)
                        for op in self.generatorXML(data, None):
                            key = '/'.join(op[:-1])
                            value = op[-1]
                            output[key].append(value)
        df = pd.DataFrame()
        for key in output.keys():
            print key, output[key], len(output[key])
            df[key] = pd.Series(output[key])
        df.to_csv(self.dataset+'.csv', encoding='utf-8')

dir = raw_input('Enter the directory\n')
dataset = raw_input('Enter the dataset name\n')
type = raw_input('File type: \n1 - single tag\n2 - Multiple tag\n')
xml = XML(dir, dataset, type)
xml.iterateInDir()
