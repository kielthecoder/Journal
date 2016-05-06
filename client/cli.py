import requests
import pprint
import json
import sys

class Server:
	def __init__(self, parent):
		self.parent = parent
		self.host = None

	def __call__(self, fulltext, words):
		name = 'do_' + words[0].lower()
		try:
			method = getattr(self, name)
			method(fulltext, words[1:])
		except AttributeError:
			print('Command not found')

	def do_open(self, fulltext, words):
		"""Connect to a sever"""
		try:
			self.host = words[0]
		except:
			print("Usage: server open <address:port>")

	def do_close(self, fulltext, words):
		"""Close connection to server"""
		self.host = None

class Echo:
	def __init__(self, parent):
		self.parent = parent
		self.host = self.parent.server.host

	def __call__(self, fulltext, words):
		if self.host:
			req = requests.get(self.host + '/api/v1/echo?text=' + words[0])
		else:
			print("Must be connected to server first (use server open)")

class REPL:
	def __init__(self):
		self.running = False
		self.server = Server(self)
		self.echo = Echo(self)

	def run(self):
		self.running = True
		print('Type "help" for a list of available commands.')
		while self.running:
			try:
				text = input('>>> ')
			except EOFError:
				print()
				text = 'quit'
			words = text.split()
			cmd = words[0].lower()
			if cmd == 'help':
				self.do_help()
			elif cmd == 'server':
				self.server(text, words[1:])
			elif cmd == 'echo':
				self.echo(text, words[1:])
			else:
				name = 'do_' + cmd
				try:
					method = getattr(self, name)
					method(text, words[1:])
				except AttributeError:
					print('Command not found')
		print('Goodbye!')

	def do_help(self):
		"""List commands available from the REPL"""
		methods = dir(self)
		commands = []
		for m in methods:
			if m.startswith('do_'):
				commands.append([m[3:], getattr(self, m).__doc__])
		systems = ['server']
		for s in systems:
			if hasattr(self, s):
				methods = dir(self.server)
				for m in methods:
					if m.startswith('do_'):
						commands.append([s + ' ' + m[3:], getattr(self.server, m).__doc__])
		margin = 20
		for cmd in commands:
			pad = len(cmd[0]) + 4
			if pad > margin:
				margin = pad
		for cmd in commands:
			print("%s- %s" % (cmd[0].ljust(margin), cmd[1]))

	def do_quit(self, fulltext, words):
		"""Stop the REPL"""
		self.running = False

if __name__ == '__main__':
	app = REPL()
	app.run()
