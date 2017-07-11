
#!/usr/bin/python
import curses 
import socket

def get_info(host, port=25565):
	# Cheers barneygale
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5.0)
	s.connect((host, port))
	s.send('\xfe')
	d = s.recv(256)
	s.close()
	assert d[0] == '\xff'
	d = d[3:].decode('utf-16be').split(u'\xa7')
	return {'motd':        str(d[0]),'players':     str(d[1]),'max_players': str(d[2])}

def formatter(screenob):
	screenob.addstr(0,0,"Server".ljust(25) + "Players".ljust(8) + "Max\n",curses.A_UNDERLINE)
	screenob.refresh()
	fancy_get_info(screenob,'c.nerd.nu',1)
	fancy_get_info(screenob,'s.nerd.nu',2)
	fancy_get_info(screenob,'p.nerd.nu',3)
	fancy_get_info(screenob,'x.nerd.nu',4)

def fancy_get_info(screenob,serv,line=0):
	try:
		stat = get_info(serv)
	except:
		stat = {'motd': serv, 'players': "?",'max_players': "?"}
	screenob.addstr(line,0,stat['motd'].ljust(25) + stat['players'].ljust(8) + stat['max_players'] + "\n")
	screenob.refresh()

def main():
	screen = curses.initscr() 
	curses.noecho() 
	curses.curs_set(0) 
	screen.keypad(1) 
	screen.addstr("Welcome to the nerd.nu status tool.\n\n")
	screen.addstr("Press UP for a status check.\n")
	screen.addstr("Press Q to quit.\n")
	while True: 
		event = screen.getch() 
		if event == ord("q"): break 
		elif event == curses.KEY_UP:
			screen.clear() 
			screen.addstr(6,0,"Updating...\n")
			screen.refresh()
			formatter(screen)
			screen.addstr(6,0,"Updated.\n")
	curses.endwin()

if __name__ == "__main__":
	main()