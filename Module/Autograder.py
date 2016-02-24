__author__ = "joshua diaddigo"
__email__ = "joshua.diaddigo@gatech.edu"

import os
import re
import imp
from unittest.mock import *
from datetime import *
import traceback
import sys

def run_tests(test_cases, expected_hw_filename, due_date=None, output=sys.stdout, path=os.getcwd()):
    if due_date is None:
        due_date = datetime(2099, 12, 31, 23, 59, 59)
    temp = sys.stdout
    sys.stdout = output
    __automate_tests(test_cases, expected_hw_filename, due_date, path)
    sys.stdout = temp
    return output

def __automate_tests(test_cases, expected_hw_filename, due_date, base_path):
    def print_indent(*args):
        sys.stdout.write("\t{}\n".format(" ".join(map(str, args))))

    print(("-" * 100) + "\n")
    for directory in os.listdir(base_path):
        if directory[0] != "." and directory[0] != "a" and directory != "results.txt":
            print("Student:\n\t {} \n".format(re.sub(r'\([^)]*\)', '', directory)))
            new_dir = os.path.join(base_path, directory)
            os.chdir(new_dir)

            print("Submission Date:")
            try:
                f = open("timestamp.txt")
                timestamp = f.read()
                f.close()
                submitted_date = datetime(int(timestamp[0:4]), int(timestamp[4:6]), int(timestamp[6:8]))
                if submitted_date > due_date:
                    print_indent("THIS ASSIGNMENT IS LATE.\n")
                else:
                    print_indent("Submitted on time\n")
            except Exception:
                print_indent("NO SUBMISSION\n")
                print(("-" * 100) + "\n")
                continue

            new_dir = os.path.join(new_dir, "Submission attachment(s)")
            sys.path.append(new_dir)
            os.chdir(new_dir)

            try:
                print("All Comments:")

                hw_file = open(expected_hw_filename)
                hw_file_contents = hw_file.read().split("\n")
                hw_file.close()

                executable_code = "import math\n"
                executable_code += "from math import pi\n"

                for line in hw_file_contents:
                    if len(line) > 0 and line[0] == "#":
                        print_indent(line)

                    if len(line.strip()) == 0 \
                            or line[0] in ["\'", "\"", " ", "\t"] \
                            or "def " in line:
                        executable_code += line + "\n"
                    else:
                        try:
                            compile(line, expected_hw_filename, "exec")
                        except Exception as ex:
                            if isinstance(ex, SyntaxError):
                                executable_code += line + "\n"

                print("\nTest Results: \n")

                hw = imp.new_module("HW")
                exec(executable_code, hw.__dict__)
                sys.modules["HW"] = hw

                with patch('builtins.print', side_effect=print_indent):
                    test_cases(hw)
            except Exception:
                print_indent(traceback.format_exc().replace("\n", "\n\t"))

            print("\n" + ("-" * 100) + "\n")
            sys.path.remove(new_dir)

