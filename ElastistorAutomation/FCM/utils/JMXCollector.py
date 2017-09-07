#!/usr/bin/env python
#title           :NHCQA-330.py
#description     : XML parser of JMX data file
#author          :Alok
#date            :20160831
#version         :1
#usage           :
#notes           :
#python_version  :2.7
#==============================================================================



#!/usr/bin/python

import xml.sax
import sys
#status=0

class MovieHandler( xml.sax.ContentHandler ):
   status=1
   def __init__(self):
      self.CurrentData = ""
      self.name = ""
      self.password = ""
      self.status=1
      self.upassword = ""
      self.uname = ""

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag

   # Call when an elements ends
   def endElement(self, tag):
      if self.CurrentData == "login":
         #print "name:", self.name
         self.uname = self.name
      if self.CurrentData == "password":
         #print "password:", self.password
         self.upassword=self.password
  	 
      #if self.name != "jmxadmin" :
      if self.uname == "jmxadmin" and  self.upassword == "password":
         #print self.uname
         #print self.upassword
         self.status=0  

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "login":
         self.name = content
      elif self.CurrentData == "password":
         self.password = content

if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)
   # override the default ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )
   #parser.parse("jmx-collector.xml")
   parser.parse("/opt/APG/Collecting/JMX-Collector/JMX-Collector/conf/jmx-collector.xml")
   print Handler.status
   if(Handler.status==0):
	sys.exit(0)
   else:
    
        sys.exit(1)
