#!/usr/bin/python

import re
import sys
import os
from pyquery import PyQuery as pq
from lxml import etree
import urllib

#List to collect any errors we run into
errorList = []

#Check whether the argument passed is for a directory or a file. Build a fileList of files to iterate over
fileList = []
rootarg = sys.argv[1]
if os.path.isdir(rootarg):
  for root, subFolders, files in os.walk(rootarg):
    for file in files:
        fileList.append(os.path.join(root,file))
else:
  fileList.append(rootarg)

rules = [
{'name':"container",'regex':'container-fluid','rep':"container"},
{'name':"row",'regex':'row-fluid','rep':"row"},
{'name':"span",'regex':'span(?=[1-9|10|11|12])','rep':"col-md-"},
{'name':"offset",'regex':'offset(?=[1-9|10|11|12])','rep':"col-lg-offset-"},
{'name':"btn",'regex':'(?!class=\")btn(?=[\s\"][^\-|btn])','rep':"btn btn-default"},
{'name':"btn-mini",'regex':'btn-mini','rep':"btn-xs"},
{'name':"btn-lg",'regex':'btn-large','rep':"btn-lg"},
{'name':"btn-small",'regex':'btn-small','rep':"btn-sm"},
{'name':"input",'regex':'input-large','rep':"input-lg"},
{'name':"input",'regex':'input-small','rep':"input-sm"},
{'name':"input",'regex':'input-append','rep':"input-group"},
{'name':"input",'regex':'input-prepend','rep':"input-group"},
{'name':"add-on",'regex':'add-on','rep':"input-group-addon"},
{'name':"label",'regex':'(?!class=\")label(?=[\s\"][^\-|label])','rep':"label label-default"},
{'name':"hero",'regex':'hero-unit','rep':"jumbotron"},
{'name':"nav list",'regex':'nav-list','rep':""},
{'name':"affix",'regex':'nav-fixed-sidebar','rep':"affix"},
{'name':"icons",'regex':"(='\bicon-)",'rep':"=glyphicon glyphicon-"},
{'name':"icons",'regex':'(="\bicon-)','rep':"=\"glyphicon glyphicon-"},
{'name':"icons",'regex':'(=\bicon-)','rep':"=glyphicon glyphicon-"},
{'name':"icons",'regex':'\bclass+(\sicon-)','rep':"=\"glyphicon glyphicon-"},
{'name':"brand",'regex':'(?!class=\")brand','rep':"navbar-brand"},
{'name':"btn",'regex':'(?!class=\")btn btn-navbar','rep':"navbar-toggle"},
{'name':"nav",'regex':'nav-collapse','rep':"navbar-collapse"},
{'name':"toggle",'regex':'nav-toggle','rep':"navbar-toggle"},
{'name':"util",'regex':'(?!class=\")-phone','rep':"-sm"},
{'name':"util",'regex':'(?!class=\")-tablet','rep':"-md"},
{'name':"util",'regex':'(?!class=\")-desktop','rep':"-lg"}
]

for file in fileList:
  try:
    with open(file,'r') as f:
      output = f.read()
      f.close()

    #Regular expression replacements
    for rule in rules:
      output = re.sub(rule['regex'], rule['rep'], output)

    #Wrap the output in a form, so we're certain what's the top level
    d = pq(output)
    d.wrap('<form id="ele"></form>')

    #Replace the navbar
    nb = d('#ele').find('.navbar')
    if (nb is not None):
      nb.addClass('navbar-default')
      nb.find('.nav').addClass('navbar-nav')
      nb.find('.btn').addClass('navbar-btn')
      nb_inner = nb.find('.navbar-inner')
      h = nb_inner.html()

      if(h is not None):
        nb.html(h)

    #Wrap the brand and nav-toggle with nav-header
    brand = nb.find(".navbar-brand")
    togg = nb.find(".navbar-toggle")
    navbarheader = d('<div class="navbar-header"></div>')
        
    if (brand and togg):
      brand.appendTo(navbarheader)
      togg.appendTo(navbarheader)
      navbarheader.prependTo(nb)

    #modal structure
    md = d('#ele').find('.modal')
    if (md is not None):
      md.removeClass("hide")
      mdia = d('<div class="modal-dialog"></div>')
      mc = d('<div class="modal-content"></div>')
      mc.appendTo(mdia)
      d('#ele').find(".modal-header").appendTo(mc)
      d('#ele').find(".modal-body").appendTo(mc)
      d('#ele').find(".modal-footer").appendTo(mc)
      mdia.appendTo(md)

    #Images
    d.find('img').addClass("img-responsive")

    #Write file
    f = open(file, "w")
    f.write(d.html())
    f.close()

  except Exception as e:
    fileError = {'file': file, 'exception': e.message}
    errorList.append(fileError)

#If we've encountered any exceptions, print out the errors to help the user.
if(len(errorList)>0):
  print "ERRORS\n"
  print "Errors were encountered when trying to transform the following files. The files may not have been fully updated\n"
  for errorFile in errorList:
    print " -  " + errorFile['file'] + ": (Error message: " + errorFile['exception'] + " )\n\n"
