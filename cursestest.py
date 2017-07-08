import curses, sys, time

def test_streams(wot):
    print wot, "stdout"
    print >>sys.stderr, wot, "stderr"

def curses_mode(stdscr):
    test_streams("wrap")
    time.sleep(1.0)

test_streams("before")
curses.wrapper(curses_mode)
test_streams("after")