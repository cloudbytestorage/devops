import fileinput
import xml.sax.xmlreader
from xml.dom import minidom
from xml.etree.ElementTree import ElementTree

#!/usr/bin/env python
_author_ = 'naveenkumar b'
_email_ = 'naveen.b@emc.com'

class XMLUtilities:

    '''
    @staticmethod
    def add_text(filepath, uniquestring, texttoreplace):
        texttoreplace = str(texttoreplace)
        with fileinput.FileInput(filepath, inplace=True) as file:
            for line in file:
                print line.replace(uniquestring, texttoreplace, end='')
            # file.close()
    '''

    @staticmethod
    def add_text(filepath, uniquestring, texttoreplace):
        filedata = None
        with open(filepath, 'r') as file:
            filedata = file.read()

        # Replace the target string
        filedata = filedata.replace(uniquestring, texttoreplace)

        # Write the file out again
        with open(filepath, 'w') as file:
            file.write(filedata)

    @staticmethod
    def add_table_data(htmlFilePath, tr_tag, td_text):
        htmlFile = minidom.parse(htmlFilePath)
        td_tag = tr_tag.appendChild(htmlFile.createElement("td"))
        td_content = htmlFile.createTextNode(td_text)
        td_tag.appendChild(td_content)
        tr_tag.appendChild(td_tag)
        with open(htmlFilePath, 'w') as f:
            f.write(htmlFilePath.toxml())
            f.close()

    @staticmethod
    def add_node_with_text(strxmlfilepath, strxpath, strnodename, strtext):
        tree = ElementTree()
        tree.parse(strxmlfilepath)
        tree.findall("id=name")


    @staticmethod
    def add_node_with_attributes(strxmlfilepath, strxpath, strnodename, attributesListMap):
        reader = xml.sax.xmlreader.XMLReader()
        document = xml.sax.parse(strxmlfilepath)



