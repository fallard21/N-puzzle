from sys import exit
from parser import load_puzzle, is_solvable
from common import PuzzleError, PuzzleSolver
from argparse import ArgumentParser
from gui_puzzle import GuiPuzzle


if __name__ == "__main__":
	parser = ArgumentParser()

	parser.add_argument("filename", type=str, help="File with puzzle")
	parser.add_argument("-heruistic", type=int, default=1, 
		help="Select heuristic (1 - manhattan, 2 - text1, 3 - text2)")
	parser.add_argument("-v", action='store_true', help="Run program with GUI (Algorithm mode)")
	parser.add_argument("-f", action='store_true', help="Run program with GUI (FreePlay mode)")
	args = parser.parse_args()

	if args.v and args.f:
		print("Can't be both free-mode AND algorithm-mode")
		exit(1)
	
	try:
		size, start, goal = load_puzzle(args)
		is_solvable(start, goal, size)

		solver = PuzzleSolver(start, goal)
		solver.run()
		path = solver.get_path()

		if args.v or args.f:
			mode = True if args.f else False
			gui = GuiPuzzle(path, size, freemode=mode)
			gui.run()
	except PuzzleError as pe:
		print(pe)
		exit(1)


# Если -u и size - нечетное -> РЕШАЕТСЯ
# Если -s и size - четное -> НЕ РЕШАЕТСЯ