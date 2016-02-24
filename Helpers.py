__author__ = 'Joshua Diaddigo'

import signal
from unittest.mock import *
import sys

def fake_input(function, input_items):
    with patch('builtins.input', side_effect=input_items):
        function()

def timeout(function, seconds):
        result = None
        signal.signal(signal.SIGALRM, lambda: sys.stdout.write("Infinite loop?\n") if result is Exception else None)
        signal.alarm(seconds)
        try:
            result = function()
        finally:
            signal.alarm(0)
        return result
