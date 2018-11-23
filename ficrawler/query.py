# coding:utf-8
import csv
import argparse


def query_csv(symbol=None, company=None, ex_date_start=None, ex_date_end=None):
    symbol = symbol.lower() if symbol else None
    company = company.lower() if company else None
    ex_date_start = int(ex_date_start.replace("-", "")) if ex_date_start else None
    ex_date_end = int(ex_date_end.replace("-", "")) if ex_date_end else None
    
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

        return result

def main():
    parser = argparse.ArgumentParser(description='Query csv')
    parser.add_argument('--symbol', help='display an symbol')
    parser.add_argument('--company', help='display an company')
    parser.add_argument('--ex_date_start', help='display an ex_date_start')
    parser.add_argument('--ex_date_end', help='display an ex_date_end')

    args = parser.parse_args()
    result = query_csv(args.symbol, args.company, args.ex_date_start, args.ex_date_end)
    for item in result:
        print(item)


if __name__ == "__main__":
    main()