#!/usr/bin/python3
# encoding: utf-8

import os
def listActions(path):
    if not os.path.exists(path):
        os.mkdir(path)
    pathlist = os.listdir(path)
    actList = []
    for f in pathlist:
        if f[0] == '.':
            pass
        else:
            if f[-4:] == '.d6a':
                f.replace('-','')
                if f:
                    actList.append(f)
            else:
                pass
    return actList


