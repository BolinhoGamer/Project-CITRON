# This is the interpreter class
class Interpreter:
	def __init__(self, code, generate=True):
		self.code = code
		self.tokens = []
		self.ast = []
		
		self.error_msg = (
			'',  # Error type
			'',  # Message
			'',  # Base word
			0,   # Line offset
			0,   # Line number
		)
		
		self.running = False
		self.error = False
		self.warning = False
		self.building = True
		
		if generate:
			self.tokenize(code)
	
	
	def abort(self, mode, msg, x, y, base):
		'''
		Halts the program and stores the error
		message at 'Interpreter.error_msg'
		Check 'Interpreter.error' to see if an
		error has occurred
		Check 'Interpreter.warning' to see if a
		warning has occured
		
		An error should have preference over a
		warning
		The warning flag will reset when the
		interpreter steps again
		
		(Do not call this method, it is reserved
		to the interpreter error handling system)
		'''
		
		line = self.code.split('\n')[y]
		tabs = line.count('\t')
		line = line.replace('\t', '  ')
		
		m = {
			'e': 'ERROR',
			'w': 'WARNING',
			'i': 'NOT IMPLEMENTED'
		}[mode]
		self.error_msg = f'''[{m}]: {msg}
{line}
{' '*(x+tabs)}{'^'*len(base)}
Line: {y+1}, Offset: {x}
''', base, x, y

		if mode == 'w': self.warning
		else:
			self.running = False
			self.building = False
			self.error = True
	
	
	def tokenize(self, code):
		'''
		Breaks given code into smaller pieces
		that are stored in 'Interpreter.tokens'
		'''
		buffer_x = 0
		x = 0
		y = 0
		
		# Tokenization loop
		buffer = ''
		for char in code + ' ':
			if char in '\n ':
				self.match_buffer(buffer, buffer_x, y)
				buffer = ''
			
				match char:
					case '\n':  # New line
						x = 0
						y += 1
	
	
	def match_buffer(self, buffer, x, y):
		'''
		Matches the given buffer string to the
		correct token
		
		(Do not call this method directly, use
		'Interpreter.tokenize')
		'''
		
		# Empty buffer
		if not buffer:
			return
		
		match buffer:
			case _:
				if buffer[0].isdigit():
					# Number token
					
					if buffer.startswith('0x'):
						try:
							val = int(buffer[2:].replace('_', ''), 16)
						except:
							self.abort('e', 'Invalid syntax: Invalid hexadecimal literal', x, y, buffer)
					
					elif buffer.startswith('0b'):
						try:
							val = int(buffer[2:].replace('_', ''), 2)
						except:
							self.abort('e', 'Invalid syntax: Invalid binary literal', x, y, buffer)
					
					elif buffer.startswith('0o'):
						try:
							val = int(buffer[2:].replace('_', ''), 8)
						except:
							self.abort('e', 'Invalid syntax: Invalid octal literal', x, y, buffer)
							
					else:
						try:
							val = float(buffer.replace('_', ''))
						except:
							self.abort('e', 'Invalid syntax: Invalid number literal', x, y, buffer)
				
				
				else:
					# Default case
					self.tokens.append(('identifier', buffer, buffer, x, y))



help(Interpreter)
