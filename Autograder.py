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
    def print_html(content="", tag_name="div", id=None, class_name="", indent_level=0, closing=True):
        id_section = "" if id is None else " id='" + id + "'"
        out_str = "<" + tag_name + id_section + " class='" + class_name + "'>" + content
        out_str += ("</" + tag_name + ">") if closing else ""
        sys.stdout.write(("\t" * indent_level) + out_str + "\n")

    def print_formatted(*args, indent_level=3):
        tabs = "\t" * indent_level
        content = (tabs + "{}").format(" ".join(map(str, args)))
        sys.stdout.write(("<br>\n" + tabs).join(content.split("\n")) + "\n")

    print("<!DOCTYPE html>")
    for directory in os.listdir(base_path):
        if directory[0] != "." and directory[0] != "a" and directory != "results.txt":
            student_name = re.sub(r'\([^)]*\)', '', directory)
            print_html(id=re.sub(r',', '', re.sub(r' ', '_', student_name)), class_name="student", closing=False,
                       indent_level=1)
            print_html(class_name="student_name", content=student_name, indent_level=2)
            new_dir = os.path.join(base_path, directory)
            os.chdir(new_dir)

            try:
                f = open("timestamp.txt")
                timestamp = f.read()
                f.close()
                submitted_date = datetime(int(timestamp[0:4]), int(timestamp[4:6]), int(timestamp[6:8]))

                print_html(class_name='student_submission_time',
                           content="THIS ASSIGNMENT IS LATE." if submitted_date > due_date else "Submitted on time",
                           indent_level=2)
            except Exception:
                print_html(class_name='submission_time', content="NO SUBMISSION", indent_level=2)
                print("\t</div>")
                continue

            new_dir = os.path.join(new_dir, "Submission attachment(s)")
            sys.path.append(new_dir)
            os.chdir(new_dir)

            try:
                print_html(class_name="student_comments", closing=False, indent_level=2)

                hw_file = open(expected_hw_filename)
                hw_file_contents = hw_file.read().split("\n")
                hw_file.close()

                executable_code = "import math\n"
                executable_code += "from math import pi\n"

                for line in hw_file_contents:
                    if len(line) > 0 and line[0] == "#":
                        print_formatted(line, indent_level=3)

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
                print("\t\t</div>")

                print_html(class_name="student_test_results", closing=False, indent_level=2)

                hw = imp.new_module("hw")
                exec(executable_code, hw.__dict__)
                sys.modules["hw"] = hw

                with patch('builtins.print', side_effect=print_formatted):
                    test_cases(hw)

                print("\t\t</div>")
            except Exception:
                print_formatted(traceback.format_exc(), indent_level=3)
                print("\t\t</div>")

            sys.path.remove(new_dir)

            print("\t</div>")
    print("</html>")