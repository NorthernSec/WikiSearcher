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

def filterResults(results):
  results = [x for x in results if x['text'][:8] == '#REDIRECT']
  return results

def search(text, unfiltered=False):
  results = db.searchPages(args.arg)
  if not unfiltered: filterResults(results)
  if len(results) == 0:
    print('No results found')
  else:
    print('Index \tTitle \tContent')
    for page in results:
      print('%s \t%s \t%s'%(page['id'], page['title'], page['text'][:100]))


if __name__=='__main__':
  description='''Query the Wikipedia data'''

  parser = argparse.ArgumentParser(description=description)
  parser.add_argument('-db',                metavar="path",      help='Location of the wikipedia sqlite db')
  parser.add_argument('act',                metavar="action",    help='Action to take [(s)earch/(o)pen]')
  parser.add_argument('arg',                metavar="argument",  help='Argument for action (title string for search, entry # for open')
  parser.add_argument('--unfiltered', '-u', action="store_true", help="Don't filter the content")
  args = parser.parse_args()

  # Select DB
  if args.db: db = dbConnector(args.db)
  else:       db = dbConnector(conf.getDBLocation())

  # Parse actions
  action = args.act.lower()
  if   action in ['s', 'search']: search(args.arg, args.unfiltered)
  elif action in ['o', 'open']:   print(args.action)

