#!/usr/bin/python

import cgi
import datetime
import json
import re

from os         import listdir, stat
from os.path    import exists, isdir, isfile, join

print "Content-Type: application/json"
print

param = cgi.FieldStorage()

def getDirectory(dir):
    originDir = "/var/www/download_files"
    if dir:
        dir = re.sub(r'\\','',dir)
        dir = re.sub(r'\/\.\.\/','',dir)
        if dir.startswith('/'):
            dir = dir[1:]
        dir = re.sub(r'\\','',dir)
        dir = re.sub(r'\/\.\.\/','',dir)
        if dir == "../" or dir == ".." or dir == "/" or dir == "../." :
            dir = ""
    else:
        dir = ""

    dir = join(join(originDir,dir),'','')

    if not exists(dir):
        dir = originDir

    allcontent = listdir(dir)
    dirItem    = [] 

    for item in allcontent:
        hashInfo = {}
        if item.startswith('.'):
            continue
        listInfo = stat(join(dir,item))
        hashInfo['name'] = item
        hashInfo['url']  = re.sub(r''+re.escape(originDir)+'','',dir)+item
        hashInfo['edit'] = datetime.datetime.fromtimestamp(int(listInfo.st_mtime)).strftime('%Y-%m-%d %H:%M:%S')
        hashInfo['size'] = int(listInfo.st_size)
        if isfile(join(dir,item)):
            hashInfo['type'] = 'file'
        if isdir(join(dir,item)):
            hashInfo['type'] = 'dir'
        dirItem.append(hashInfo)
    return dirItem

def getAction():
    action  = param.getvalue("action")
    if action == "getDirectory":
        dir = param.getvalue("dir")
        return getDirectory(dir)
    elif action == "deleteFile":
        file = param.getvalue("file")
        #TODO#
        return {"message": "Not implemented"}
    else:
        return {"message": "Please specify an valid action"}

print json.dumps(getAction())
