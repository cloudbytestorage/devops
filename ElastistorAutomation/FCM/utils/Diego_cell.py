#!/usr/bin/python

import xml.sax
import sys
#status=1
class MovieHandler( xml.sax.ContentHandler ):
   status=1
   def __init__(self):
      self.CurrentData = ""
      self.type = ""
      self.format = ""
      self.year = ""
      self.rating = ""
      self.stars = ""
      self.description = ""
      self.status=1

   # Call when an element starts
   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "mbean":
         #print "*****Mbean*****"
         job = attributes["query"]
         #print "Title:", job

   def startElement(self, tag, attributes):
      self.CurrentData = tag
      if tag == "custom":
         #print "*****Mbean*****"
         value = attributes["value"]
	 #self.status=10
	 #if job!="CFDeplID" or job!="objname" or job!="location" or job!="device" or job!="devtype" or job!="index" or job!="Job" or job!="IPAddr":
	 #    print "Not match"+job
	 #print value
	 if value in ("Diego_cellVM-1","Diego_cellVM-0"):
  	     #print value
	     self.status=0
   # Call when an elements ends
   def endElement(self, tag):
       if self.CurrentData == "property":
         print "Type:", self.type
     #    print "Year:", self.year
     # elif self.CurrentData == "rating":
     #    print "Rating:", self.rating
     # elif self.CurrentData == "stars":
     #    print "Stars:", self.stars
     # elif self.CurrentData == "description":
     #    print "Description:", self.description
     # self.CurrentData = ""

   # Call when a character is read
   def characters(self, content):
      if self.CurrentData == "type":
         self.type = content
    #  elif self.CurrentData == "format":
     #    self.format = content
     # elif self.CurrentData == "year":
     #    self.year = content
     # elif self.CurrentData == "rating":
     #    self.rating = content
     # elif self.CurrentData == "stars":
     #    self.stars = content
     # elif self.CurrentData == "description":
     #    self.description = content

if ( __name__ == "__main__"):
   
   # create an XMLReader
   parser = xml.sax.make_parser()
   # turn off namepsaces
   parser.setFeature(xml.sax.handler.feature_namespaces, 0)

   # override the default ContextHandler
   Handler = MovieHandler()
   parser.setContentHandler( Handler )
   #global status  
   parser.parse("/opt/APG/Collecting/JMX-Collector/JMX-Collector/conf/jmx-collector-data.xml")
   #Handler.startElement(self, tag, attributes)
   #parser.parse("jmx-collector-data.xml")
   print Handler.status
   if(Handler.status==0):
	#print "hello"
	sys.exit(0)
