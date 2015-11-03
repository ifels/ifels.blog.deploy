#!/usr/bin/env python
# coding:utf-8

import os
import sys
import codecs
import re

conf = 'hooks.json'

def deamon():
    curDir = os.path.dirname(os.path.abspath(__file__))
    f=codecs.open(conf,'r','utf-8') 
    content = f.read()
    f.close() 
    cmd = curDir + '/' + 'deploy.sh'
    content = re.sub('"execute-command"\s*:\s*".*"', '"execute-command":"' + cmd + '"', content)
    content = re.sub('"command-working-directory"\s*:\s*".*"', '"command-working-directory":"' + curDir + '"', content)
    f=codecs.open(conf,'w','utf-8') 
    f.write(content) 
    f.close()
    
    os.system('killall -9 webhook')
    os.system('webhook -hooks hooks.json -port=7099 -verbose &')

if __name__ == '__main__': 
    deamon()

