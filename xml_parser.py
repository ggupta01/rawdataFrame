import xml.etree.ElementTree as ET
import re
import collections
import pandas as pd

def generatorXML(parent, pre=None):
    pre = pre[:] if pre else [parent.tag]

    if parent.attrib:
        for k,v in parent.attrib.iteritems():
            yield pre + ['attrib'] + [k] + [v]

    if len(list(parent)) > 0:
        for child in parent:
            for d in generatorXML(child, pre + [child.tag]):
                yield d
    else:
        yield pre + [parent.text]

output = collections.defaultdict(list)
with open(raw_input("Please enter the file name: "),"rb") as f:
    for line in f:
        data = ET.fromstring(line)
        for op in generatorXML(data, None):
            print op
            key = '/'.join(op[:-1])
            value = op[-1]
            output[key] = value

pd.DataFrame(output.keys(), output.values()).to_csv('abc.csv')
