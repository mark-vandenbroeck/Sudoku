import sys
from sudoku_engine import PuzzleGenerator
from visualizer import SudokuVisualizer

def main():
    print("=== Sudoku Generator & Logical Solver ===")
    difficulty = input("Enter difficulty (Easy, Medium, Hard, Expert) [Medium]: ") or "Medium"
    
    if difficulty not in ["Easy", "Medium", "Hard", "Expert"]:
        print("Invalid difficulty. Defaulting to Medium.")
        difficulty = "Medium"
        
    print(f"\nGenerating {difficulty} Sudoku... (This might take a moment)")
    
    gen = PuzzleGenerator()
    puzzle, score, steps = gen.generate(difficulty)
    
    print("\nPuzzle Generated!")
    print(puzzle)
    print(f"Logical Difficulty Score: {score}")
    
    debug = input("\nShow logical solving steps? (y/n) [n]: ").lower() == 'y'
    if debug:
        SudokuVisualizer.print_debug_steps(steps)
        
    export = input("Export to PDF? (y/n) [y]: ").lower() != 'n'
    if export:
        filename = f"sudoku_{difficulty.lower()}.pdf"
        SudokuVisualizer.export_pdf(puzzle, filename=filename, title=f"Sudoku - {difficulty}")
        
        # Also export solution
        export_sol = input("Export solution to PDF? (y/n) [n]: ").lower() == 'y'
        if export_sol:
            # We need to solve it completely for the export
            # The steps we have might not be complete if we stopped at target score
            # But the puzzle is guaranteed to have a unique solution
            sols = puzzle.solve_backtracking()
            if sols:
                from sudoku_engine import SudokuBoard
                sol_board = SudokuBoard(sols[0])
                SudokuVisualizer.export_pdf(sol_board, filename=f"sudoku_{difficulty.lower()}_solution.pdf", title=f"Sudoku Solution - {difficulty}")

if __name__ == "__main__":
    main()
