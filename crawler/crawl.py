# coding:utf-8
import threading
import time
import datetime
import re
import sys
import traceback
import csv

try:
    from HTMLParser import HTMLParser
    from urllib2 import urlopen
except:
    from urllib.request import urlopen
    from html.parser import HTMLParser


html_parser = HTMLParser()
RESULT = []
lock = threading.RLock()


class HtmlSpider(threading.Thread):
    def __init__(self, url, sem):
        super(HtmlSpider, self).__init__()
        self.url = url
        self.sem = sem

    def run(self):
        parse_html(self.url)
        self.sem.release()

def format_date(date):
    try:
        return datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
    except:
        return None

def parse_html(url):
    result = []
    body = urlopen(url).read().decode("utf-8")
    tbody = re.search(r".*events-calender-table-three.*?<tbody>(.*?)<\/tbody>", body, re.M|re.S).group(1)
    for item in tbody.split("<tr>")[1:]:
        try:
            content = re.search(r".*?<strong>(.*?)</strong>(.*)", item, re.M|re.S)
            company = html_parser.unescape(content.group(1))

            content_2 = re.search(r".*?<div class=\"indent-left-smaller\">(.*?)</div>(.*)", content.group(2), re.M|re.S)
            raw_website = re.search(r".*?'(http.*)'", content_2.group(1), re.M|re.S)
            if raw_website:
                website = raw_website.group(1)
            else:
                website = None

            content_3 = re.search(r".*<td class=\"lft-rt-border center blue-links\">[\n\t]+(.*?)[\n\t]+</td>(.*)", content_2.group(2), re.M|re.S)
            raw_symbol = re.search(r"<a.*>(.*)</a>", content_3.group(1))
            if raw_symbol:
                symbol = raw_symbol.group(1)
            else:
                symbol = content_3.group(1)

            content_4 = re.search(r".*<td class=\"right\">(.*?)</td>(.*)", content_3.group(2), re.M|re.S)
            dividend = content_4.group(1)

            content_5 = re.search(r".*?<td class=\"lft-rt-border\">(.*?)</td>(.*)", content_4.group(2), re.M|re.S)
            anouncement_date = html_parser.unescape(content_5.group(1))

            content_6 = re.search(r".*?<td>(.*?)</td>(.*)", content_5.group(2), re.M|re.S)
            record_date = html_parser.unescape(content_6.group(1))

            content_7 = re.search(r".*?<td class=\"lft-rt-border\">(.*?)</td>(.*)", content_6.group(2), re.M|re.S)
            ex_date = html_parser.unescape(content_7.group(1))

            content_8= re.search(r".*?<td>(.*?)</td>(.*)", content_7.group(2), re.M|re.S)
            pay_date = html_parser.unescape(content_8.group(1))

            result.append((company, website, symbol, dividend, format_date(anouncement_date), format_date(record_date), format_date(ex_date), format_date(pay_date)))
        except Exception as e:
            if not re.search(r".*No Dividends for this date.*", item, re.M|re.S):
                print(url, item, traceback.format_exc())

    lock.acquire()
    RESULT.extend(result)
    lock.release()


if __name__ == "__main__":
    start_time = time.time()
    sem = threading.Semaphore(30) #设置同时最多3个
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(30)
    date = start_date
    thread_box = []
    while date <= end_date:
        date_string = date.strftime("%m/%d/%Y")
        sem.acquire() # 内部维护的计数器减1，到0就会阻塞
        html_thread = HtmlSpider("https://eresearch.fidelity.com/eresearch/conferenceCalls.jhtml?tab=dividends&begindate={}".format(date_string), sem)
        thread_box.append(html_thread)
        html_thread.start()
        date += datetime.timedelta(1)
    for item in thread_box:
        item.join()
    end_time = time.time()
    print(end_time - start_time)
    print("total:", len(RESULT))
    with open('t.csv','w') as myFile:
        myWriter = csv.writer(myFile)
        myWriter.writerow(("company", "website", "symbol", "dividend", "anouncement_date", "record_date", "ex_date", "pay_date"))
        myWriter.writerows(RESULT)