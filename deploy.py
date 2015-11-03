#!/usr/bin/env python
# coding:utf-8

import os
import sys
import glob
import shutil
import subprocess


BLOG_GIT = 'git@github.com:ifels/ifels.blog.git'
GIHUB_IO_GIT = 'git@github.com:ifels/ifels.github.com.git'

BLOG_NAME = 'ifels.blog'

class switchDir:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.newPath = os.path.expanduser(new_path)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, exception_type, exception_value, traceback):
        os.chdir(self.savedPath)


def deploy():
    curDir = os.path.dirname(os.path.abspath(__file__))
    commitMsg = ''

    os.system('rm -rf ifels.blog')
    os.system('git clone --recursive %s %s' % (BLOG_GIT, BLOG_NAME))

    blogDir = curDir + '/' + BLOG_NAME
    publicDir = blogDir + '/public'

    with switchDir(blogDir):
        s = subprocess.Popen('git log -1 --pretty=format:"%s"', shell=True, stdout=subprocess.PIPE)
        commitMsg = s.communicate()[0]
        print("commitMsg", commitMsg)

        os.system('rm -rf public')
        os.system('git clone %s %s' % (GIHUB_IO_GIT, 'public'))
        os.system('hugo -v -b "http://ifels.github.io" -t redlounge')

    with switchDir(publicDir):
        os.system('git add --all')
        os.system('git commit -a -m "%s"' % commitMsg)
        os.system('git push origin master')

if __name__ == '__main__': 
    deploy()

