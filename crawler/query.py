# coding:utf-8
import csv
import argparse

parser = argparse.ArgumentParser(description='Query csv')
parser.add_argument('--symbol', help='display an symbol')
parser.add_argument('--company', help='display an company')
parser.add_argument('--ex_date_start', help='display an ex_date_start')
parser.add_argument('--ex_date_end', help='display an ex_date_end')

args = parser.parse_args()
symbol = args.symbol.lower() if args.symbol else None
company = args.company.lower() if args.company else None
ex_date_start = int(args.ex_date_start.replace("-", "")) if args.ex_date_start else None
ex_date_end = int(args.ex_date_end.replace("-", "")) if args.ex_date_end else None

with open('t.csv','r') as myFile:
    lines = csv.reader(myFile)
    result = []
    for line in list(lines)[1:]:
        ex_date = int(line[6].replace("-", ""))

        if symbol and symbol != line[2].lower():
            continue

        if company and company not in line[1].lower():
            continue

        if ex_date_start and ex_date_start > ex_date:
            continue

        if ex_date_end and ex_date_end < ex_date:
            continue

        result.append(line)

    for item in result:
        print(item)