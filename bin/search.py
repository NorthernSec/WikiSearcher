#!/usr/bin/env python3
#
# Search script for the WikiPedia sqlite db
#
# Copyright (c) 2016    Pieter-Jan Moreels - pieterjan.moreels@gmail.com

# Imports
import argparse
import os
import sys
runPath = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(runPath, ".."))

from lib.Config import Configuration as conf
from lib.DatabaseConnection import dbConnector

if __name__=='__main__':
  description='''generate sqlite db from wikipedia xml extact'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-db',              help='Location of the wikipedia sqlite db')
  parser.add_argument('index', nargs="?", help='Index of the entry you want to open')
  parser.add_argument('-s',               help='String the title has to contain')
  args = parser.parse_args()

  # Check args
  if not args.index and not args.s:
    sys.exit("Please specify the index of the entry, or use -s to search")
  if args.index and args.s:
    sys.exit('''You cannot specify an index and use -s simultaniously.
                If you search on more than one word, please make sure you put it between quotes.''')
  
  # Parse args
  if args.db:
    db = dbConnector(args.db)
  else:
    db = dbConnector(conf.getDBLocation())

  if args.s:
    print('Index \tTitle \tContent')
    for page in db.searchPages(args.s):
      print('%s \t%s \t%s'%(page['id'], page['title'], page['text'][:30]))
  elif args.index:
    print(args.index)

