#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPM Repository clean

Deletes files not listed in the repository metainfo from its local clone. Only repo
subdir contents are cleaned, any additional top level objects remains unchanged.

@author: Andrey Novikov aka NovA
"""

import argparse
import pathlib
import xml.etree.ElementTree as ET
import gzip

# program context (repo dir, ...)
class Ctx:
    repofiles = set()
    repodirs = set()

ctx = Ctx()

def parse_cmdline():
    """Parse command line arguments and update `ctx`"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument('basedir', metavar="/repo/clone/dir/",
                        help="Path where a repository was clonned")
    parser.parse_args(namespace=ctx)
#


def accfile(fn: str, size: int = -1):
    """Account file in the repo and return full path"""
    ctx.repofiles.add(fn)
    ctx.repodirs.add(str(pathlib.Path(fn).parent))
    print(f"Accounting files in the repo... {len(ctx.repofiles)}", end='\r')
    return str(pathlib.Path(ctx.basedir, fn))
#


if __name__ == "__main__":
    parse_cmdline()

    print("---\n"
         f"--- Cleaning old files in RPM repo {ctx.basedir}\n"
          "---")

    # Obtain metadata files
    metafile: str = ''
    repomd = ET.parse(accfile('repodata/repomd.xml'))
    ns = '{http://linux.duke.edu/metadata/repo}'  # xml namespace
    for e in repomd.findall(f'{ns}data/{ns}location'):
        fn = e.get('href')
        path = accfile(fn)
        if fn.endswith('primary.xml.gz'):
            metafile = path
    accfile('repodata/repomd.xml.asc')
    accfile('repodata/repomd.xml.key')

    # Parse metafile to list RPMs
    ns = '{http://linux.duke.edu/metadata/common}'  # xml namespace
    with gzip.open(metafile, 'rb') as f:
        for _, e in ET.iterparse(f):
            if e.tag == f'{ns}package':
                fn = e.find(f'{ns}location').get('href')
                sz = int(e.find(f'{ns}size').get('package'))
                accfile(fn, sz)
                e.clear()  # !!! a must, memory hog otherwise
    print('')

    print(f"Processing subdirs: {sorted(ctx.repodirs)}...")
    ndelfiles = 0
    for d in ctx.repodirs:
        dd = pathlib.Path(ctx.basedir, d)
        if not dd.is_dir():
            continue;
        for f in dd.iterdir():
            if not f.is_file():
                continue
            fn = str(f.relative_to(ctx.basedir))
            if not fn in ctx.repofiles:
                f.unlink()
                print(f'  {fn} deleted')
                ndelfiles += 1
    
    print("---")
    print(f"{ndelfiles} old files have been deleted")
#
