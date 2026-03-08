from sudoku_engine import PuzzleGenerator
from visualizer import SudokuVisualizer

def test_generation():
    print("Testing Easy Sudoku generation...")
    gen = PuzzleGenerator()
    puzzle, score, steps = gen.generate("Easy")
    
    print("\nPuzzle Generated!")
    print(puzzle)
    print(f"Logical Difficulty Score: {score}")
    
    SudokuVisualizer.print_debug_steps(steps)
    SudokuVisualizer.export_pdf(puzzle, filename="test_sudoku.pdf", title="Test Sudoku - Easy")
    print("Verification complete.")

if __name__ == "__main__":
    test_generation()
