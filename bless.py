import fileinput
import signal
import sys
import time
from blessings import Terminal # $ pip install blessings

def signal_handler(*args):
    raise SystemExit

for signal_name in "SIGHUP SIGINT SIGTERM".split():
    signal.signal(getattr(signal, signal_name), signal_handler)

term = Terminal()
with term.hidden_cursor(), term.fullscreen():
    for line in fileinput.input(): # read from files on the command-line and/or stdin
        for word in line.split(): # whitespace-separated words
            # use up to date width/height (SIGWINCH support)
            with term.location((term.width - len(word)) // 2, term.height // 2):
                print(term.bold_white_on_black(word))
                time.sleep(1)
                print(term.clear)