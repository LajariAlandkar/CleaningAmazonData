# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 07:37:35 2020

@author: Lajari
"""

import setuptools

setuptools.setup(name = 'CleaningAmazonData',
      version = '0.0.1',
      description = 'Package to clean Amazon scraped data',
      author = 'Lajari Alandkar',
      packages = setuptools.find_packages(),
      url = 'https://gitlab.com/medicinalfoodsandherbsforstresssleepanxiety/Data-Analysis-EDA.git',
      install_requires =['pandas>=1.0.3', 
                         'nltk>=3.4.5', 
                         're>=2.2.1', 
                         'sklearn>=0.22.1']
      
      )



