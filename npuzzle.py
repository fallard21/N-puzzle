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
	parser.add_argument("-v", action='store_true', help="Run program with GUI")
	args = parser.parse_args()

	try:
		size, start, goal = load_puzzle(args)
		is_solvable(start, goal, size)

		solver = PuzzleSolver(start, goal)
		solver.run_Astar()
		path = solver.get_path()

		if args.v:
			gui = GuiPuzzle()
			gui.run(path, size)
	except PuzzleError as pe:
		print(pe.err_msg)
		exit(1)


# Если -u и size - нечетное -> РЕШАЕТСЯ
# Если -s и size - четное -> НЕ РЕШАЕТСЯ