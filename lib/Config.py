#!/usr/bin/env python3.3
# -*- coding: utf-8 -*-
#
# Read configuration file or return default values
#
# Copyright (c) 2016    NorthernSec
# Copyright (c) 2016    Pieter-Jan Moreels
# This software is licensed under the Original BSD License

# Imports
import os
import sys
runpath=os.path.dirname(os.path.realpath(__file__))

import configparser

class Configuration():
  cp=configparser.ConfigParser()
  cp.read(os.path.join(runpath, '../etc/configuration.ini'))
  default={'db': 'db/wiki.db'}

  @classmethod
  def read(cls, section, item, default):
    result=default
    try:
      if type(default) == bool:
        result=cls.cp.getboolean(section, item)
      elif type(default) == int:
        result=cls.cp.getint(section, item)
      else:
        result=cls.cp.get(section,item)
    except:
      pass
    return result

  @classmethod
  def locate(cls, path):
    if path.startswith('/'):
      return path
    else:
      return os.path.join(runpath, '..', path)

  # Functions
  @classmethod
  def getDBLocation(cls):
    return cls.locate(cls.read("Database", "Path", cls.default['db']))
