#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import bisect
import faker
import humanfriendly
import itertools
import random
import sys
import progressbar

def write_row(file, fields):
    row = '\t'.join([f.replace('\t', ' ') for f in fields]) + '\n'
    return file.write(row)

def generate_data(file, rows, size, seed):
    
    weightedLocales = [
        ('de_DE', 10),
        ('en_US', 10),
        ('cs_CZ', 1),
        ('el_GR', 1),
        ('fa_IR', 1),
        ('hi_IN', 1),
        ('ja_JP', 1),
        ('zh_CN', 1)
    ]
    
    header = [
        'ID',
        'FIRST_NAME',
        'LAST_NAME',
        'LOCALE',
        'CITY'
    ]
    
    randomGenerator = random.Random(seed)
    
    factories = [faker.Factory.create(l[0]) for l in weightedLocales]
    for f in factories:
        f.seed(randomGenerator.randint(0, sys.maxsize))
    
    choices, weights = zip(*weightedLocales)
    cumdist = list(itertools.accumulate(weights))
    
    if rows is not None:
        barMaxValue = rows;
    elif size is not None:
        barMaxValue = size;
    else:
        raise Exception('Require either rows or size to be not None')
    
    widgets = [
        ' ', progressbar.AnimatedMarker(markers='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'),
        ' ', progressbar.Bar(marker='▰', left='', right='', fill='▱'),
        ' ', progressbar.Percentage(),
        ' ', progressbar.ETA()
    ]
    pbar = progressbar.ProgressBar(widgets=widgets, max_value=barMaxValue)
    
    
    totalBytes = write_row(file, header)
    
    rowId = 1
    while True:
        if (rows is not None and rowId > rows) or (size is not None and totalBytes > size):
            break
    
        x = randomGenerator.random() * cumdist[-1]
        localeIndex = bisect.bisect(cumdist, x)
        
        fake = factories[localeIndex]
        
        fields = [
            str(rowId),
            fake.first_name(),
            fake.last_name(),
            choices[localeIndex],
            fake.city()
        ]
        
        totalBytes += write_row(file, fields)
        
        if rows is not None:
            pbar.update(rowId)
        elif size is not None:
            # we will overshot the max by a few bytes
            # progressbar does not like that
            pbar.update(min(totalBytes, barMaxValue))
        
        rowId += 1
    
    pbar.finish()
    file.close()
    
    print("Generated {} rows using {} ({} bytes)".format(rowId, humanfriendly.format_size(totalBytes), totalBytes))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generator for test tables")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-r', '--rows', type=int, help="Generated rows count")
    group.add_argument('-s', '--size', type=str, help="Generated file size")
    
    parser.add_argument('--seed', type=int, help="A fixed seed for random")
    parser.add_argument('file', type=argparse.FileType(mode='w', encoding='UTF-8'), help="output TSV file")
    
    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)
    
    if args.size is not None:
        maxBytes = humanfriendly.parse_size(args.size)
    else:
        maxBytes = None
    
    generate_data(args.file, args.rows, maxBytes, args.seed)
    
