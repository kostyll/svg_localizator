print data
import xml.etree.ElementTree as ET
tree = ET.parse('svg')
root = tree.getroot()
root
root.items
root.items()
root.getchildren()
root
root.getchildren()
root.text
def parseNode(node):
    for item in node.getchildren():
        parseNode(item)
    print node.text


parseNode(root)

#http://stackoverflow.com/questions/17437103/replacing-xml-element-in-python
#tree.write('output.xml')