#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 16:28:34 2018

@author: nagasudheerravela
"""

class Extra:
     staticVariable = 'Null'
    
def func():
    Extra.staticVariable = Extra.staticVariable +'1'
    print(Extra.staticVariable)
     
     
     
func()
func()