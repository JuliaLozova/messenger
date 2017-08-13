
from blessings import Terminal
#from blessed import Terminal
#import fileinput
import sys

term = Terminal()

with term.hidden_cursor(), term.fullscreen():
    while True:
        with term.location(0, term.height - 1):
            print('Me:')
            inp = sys.stdin.readline()
            for word in inp.split('\n'): 
                with term.location(0, (term.height / 2)):
                    print(term.bold_white_on_black(word))

                with term.location(0, (term.height - 2)):
                    print term.clear_eol