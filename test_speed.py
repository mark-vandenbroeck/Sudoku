import time
from sudoku_engine import PuzzleGenerator

def test_speed():
    gen = PuzzleGenerator()
    for diff in ["Easy", "Medium", "Hard"]:
        start = time.time()
        puzzle, score, steps = gen.generate(diff)
        end = time.time()
        print(f"Generated {diff} Sudoku (Score: {score}) in {end - start:.2f} seconds")

if __name__ == "__main__":
    test_speed()
