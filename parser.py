class PuzzleError(Exception):
	err_msg = ""

	def __init__(self, msg):
		self.err_msg = f"Error: {msg}"


def load_puzzle(filename : str) -> tuple:
	size = -1
	array = []
	try:
		with open(filename, 'r') as f:
			for line in f:
				line = line.strip(' \n').partition('#')
				split_line = line[0].split()
				try:
					if len(split_line) == 1 and split_line[0].isdigit() and size < 0:
						size = int(split_line[0])
					elif len(split_line) == size:
						array.extend(list(map(int, split_line)))
					elif len(split_line) > 0:
						raise PuzzleError(msg='invalid puzzle input')
						#exit('Error: invalid puzzle input')
				except ValueError:
					raise PuzzleError(msg='invalid puzzle input')
				#exit('Error: invalid puzzle input')
	except OSError:
		raise PuzzleError(msg=f"can't open file: {filename}")
		#exit(f'Error: error open file: {filename}')
	
	check = [n < size * size and n >= 0 for n in array]
	if size < 1 or len(array) != size ** 2 or False in check or len(array) != len(set(array)):
		raise PuzzleError(msg='invalid puzzle input')
		#exit('Error: invalid puzzle input')
	return array
