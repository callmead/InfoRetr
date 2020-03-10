#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 28 21:24:51 2018

@author: afarhan
"""

import csv

v = open('people.csv')
r = csv.reader(v)
row0 = r.next()
row0.append('berry')
print(row0)