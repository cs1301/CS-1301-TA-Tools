__author__ = 'Joshua Diaddigo'

import signal
from unittest.mock import *

class __TA_Tools_Error(Exception):
    def __init__(self, value=""):
        self.value = value

    def __str__(self):
        return repr(self.value)

def fake_input(function, input_items):
    with patch('builtins.input', side_effect=input_items):
        function()

def timeout(function, seconds):
        def handler(signum, frame):
            raise __TA_Tools_Error()

        result = None
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(seconds)
        try:
            result = function()
        except __TA_Tools_Error:
            print("Infinite loop?")
        finally:
            signal.alarm(0)
        return result
