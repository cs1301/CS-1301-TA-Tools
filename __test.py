import autograder

print("Running test cases...")


def test_cases(hw):
    hw.test()

filestream = open("output.html", "w")
autograder.run_tests(test_cases, "hw1.py",
                     path="/Users/joshua/Library/Mobile Documents/com~apple~CloudDocs/School/2015-2016/CS 1301/Spring/Week 3/HW 1 - Simple Functions & Drawing",
                     output=filestream)
filestream.close()

print("Test cases succeeded!")
