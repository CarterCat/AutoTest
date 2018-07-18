import unittest
from config import headers, search_url, my_post
from testcases.search_checker import *
from testcases.search_plans import *

class run_test(unittest.TestCase):

    def test1(self):
        test1 = my_post.result(search_url, plans_case1, headers)



    def test2(self):
        test2 = my_post.result(search_url, checker_case1, headers)
