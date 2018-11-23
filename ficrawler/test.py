# coding:utf-8
import re
import csv
import unittest

from query import query_csv


class MyTest(unittest.TestCase):
    # def setUp(self):
    #     # 每个测试用例执行之前做操作
    #     print('StartItem')

    # def tearDown(self):
    #     # 每个测试用例执行之后做操作
    #     print('EndItem')

    # @classmethod
    # def setUpClass(self):
    #     print('Start')

    # @classmethod
    # def tearDownClass(self):
    #     print('End')

    def test_crawl(self):
        with open('t.csv','r') as myFile:
            lines = csv.reader(myFile)
            for line in list(lines)[1:]:
                company, website, symbol, dividend, a_date, r_date, ex_date, pay_date = line
                self.assertNotEqual(company, "")
                if website:
                    self.assertIsNotNone(re.match(r"^http.*", website), website)
                self.assertIsNotNone(re.search(r"^[\:\_\/A-Z]*$", symbol), symbol)
                self.assertIsNotNone(re.search(r"^[\.\d]*$", dividend), dividend)
                self.assertIsNotNone(re.search(r"^[\-\d]*$", a_date), a_date)
                self.assertIsNotNone(re.search(r"^[\-\d]*$", r_date), r_date)
                self.assertIsNotNone(re.search(r"^[\-\d]*$", ex_date), ex_date)
                self.assertIsNotNone(re.search(r"^[\-\d]*$", pay_date), pay_date)
        
    def test_query(self):
        # symbol
        result = query_csv(symbol="WING")
        for item in result:
            self.assertEqual(item[2].lower(), "wing", item[2].lower())
        # company
        result = query_csv(company="inc")
        for item in result:
            self.assertIn("inc", item[0].lower(), item[0].lower())
        # ex_date_start
        result = query_csv(ex_date_start="2018-11-03")
        for item in result:
            ex_date = int(item[6].replace("-", ""))
            self.assertTrue(ex_date >= 20181103, ex_date)
        # ex_date_end
        result = query_csv(ex_date_end="2018-12-20")
        for item in result:
            ex_date = int(item[6].replace("-", ""))
            self.assertTrue(ex_date <= 20181220, ex_date)

def main():
    unittest.main()


if __name__ == '__main__':
    main()