__author__ = 'joshua'

from Module import Autograder
from Module import Helpers


print("Running test cases...")

def test_cases(hw):
    hw.test()

Autograder.run_tests(test_cases, "hw1.py", path="/Users/joshua/Library/Mobile Documents/com~apple~CloudDocs/School/2015-2016/CS 1301/Spring/Week 3/HW 1 - Simple Functions & Drawing")

print("Test cases succeeded!")
