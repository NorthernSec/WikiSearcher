#!/usr/bin/env python3
#
# Import script for the WikiPedia data
#
# Copyright (c) 2016 	Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import argparse
import copy
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from xml.etree import ElementTree as ET
from lib.DatabaseConnection import dbConnector

if __name__=='__main__':
  description='''generate sqlite db from wikipedia xml extact'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('inp', help='Location of the wikipedia xml')
  parser.add_argument('out', help='Location for the sqlite db')
  args = parser.parse_args()

  # make parser
  parser = ET.iterparse(args.inp)

  # parse xml and store in database

  db = dbConnector(args.out)
  elemContent = {'title': None, 'text': None, 'sha1': None}
  entry = copy.copy(elemContent)
  
  for event, element in parser:
    lock=False
    tag = element.tag.split("}")[1]
    if   tag == 'page':  entry = copy.copy(elemContent)
    elif tag == 'title': entry['title']=element.text
    elif tag == 'text':  entry['text']=element.text
    elif tag == 'sha1':  entry['sha1']=element.text
    if not None in entry.values():
      lock=True
      db.addPage(entry)
      entry = copy.copy(elemContent)
      lock=False
    element.clear()
