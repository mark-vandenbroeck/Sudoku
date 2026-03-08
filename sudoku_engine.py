import copy

class SudokuBoard:
    def __init__(self, grid=None):
        if grid is None:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]
        else:
            self.grid = [row[:] for row in grid]
        self.candidates = [[set(range(1, 10)) if self.grid[r][c] == 0 else set() 
                           for c in range(9)] for r in range(9)]
        self._update_all_candidates()

    def _update_all_candidates(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != 0:
                    self._remove_candidate_from_peers(r, c, self.grid[r][c])

    def _remove_candidate_from_peers(self, row, col, val):
        # Remove from row
        for c in range(9):
            self.candidates[row][c].discard(val)
        # Remove from column
        for r in range(9):
            self.candidates[r][col].discard(val)
        # Remove from 3x3 box
        start_r, start_c = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_r, start_r + 3):
            for c in range(start_c, start_c + 3):
                self.candidates[r][c].discard(val)

    def set_cell(self, row, col, val):
        self.grid[row][col] = val
        self.candidates[row][col] = set()
        self._remove_candidate_from_peers(row, col, val)

    def is_solved(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    return False
        return True

    def is_valid(self):
        # Check rows
        for r in range(9):
            vals = [v for v in self.grid[r] if v != 0]
            if len(vals) != len(set(vals)): return False
        # Check cols
        for c in range(9):
            vals = [self.grid[r][c] for r in range(9) if self.grid[r][c] != 0]
            if len(vals) != len(set(vals)): return False
        # Check boxes
        for box_r in range(0, 9, 3):
            for box_c in range(0, 9, 3):
                vals = []
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        if self.grid[r][c] != 0:
                            vals.append(self.grid[r][c])
                if len(vals) != len(set(vals)): return False
        return True

    def copy(self):
        return SudokuBoard(self.grid)

    def solve_backtracking(self, limit=1):
        solutions = []
        grid = self.grid
        
        # Use bitmasks for fast checking
        rows = [0] * 9
        cols = [0] * 9
        boxes = [0] * 9
        
        empty_cells = []
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                if val != 0:
                    mask = 1 << val
                    rows[r] |= mask
                    cols[c] |= mask
                    boxes[3*(r//3) + (c//3)] |= mask
                else:
                    empty_cells.append((r, c))

        def solve(idx):
            if idx == len(empty_cells):
                solutions.append([row[:] for row in grid])
                return
            
            r, c = empty_cells[idx]
            box_idx = 3*(r//3) + (c//3)
            
            # Combine masks: 1s are occupied numbers
            occupied = rows[r] | cols[c] | boxes[box_idx]
            
            for n in range(1, 10):
                mask = 1 << n
                if not (occupied & mask):
                    # Place
                    grid[r][c] = n
                    rows[r] |= mask
                    cols[c] |= mask
                    boxes[box_idx] |= mask
                    
                    solve(idx + 1)
                    
                    if len(solutions) >= limit:
                        return
                    
                    # Backtrack
                    grid[r][c] = 0
                    rows[r] &= ~mask
                    cols[c] &= ~mask
                    boxes[box_idx] &= ~mask

        solve(0)
        return solutions

    def __str__(self):
        res = ""
        for r in range(9):
            if r % 3 == 0 and r != 0:
                res += "-" * 21 + "\n"
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    res += "| "
                res += str(self.grid[r][c]) if self.grid[r][c] != 0 else "."
                res += " "
            res += "\n"
        return res

class LogicSolver:
    def __init__(self, board):
        self.board = board.copy()
        self.steps = []
        self.total_score = 0
        self.techniques = [
            (self.find_naked_single, "Naked Single", 1),
            (self.find_hidden_single, "Hidden Single", 2),
            (self.find_pointing_tuple, "Pointing Tuple", 8),
            (self.find_naked_tuple, "Naked Tuple", 15),
        ]

    def solve(self):
        while not self.board.is_solved():
            found = False
            for technique_fn, name, score in self.techniques:
                changes = technique_fn()
                if changes:
                    for r, c, val, desc in changes:
                        if val is not None:
                            if self.board.grid[r][c] == 0:
                                self.board.set_cell(r, c, val)
                                self.steps.append(f"{name}: {desc}")
                                self.total_score += score
                        else:
                            # It's a candidate removal (for tuple techniques)
                            # For now, let's just implement placement techniques
                            pass
                    found = True
                    break
            if not found:
                break
        return self.board.is_solved()

    def find_naked_single(self):
        for r in range(9):
            for c in range(9):
                if self.board.grid[r][c] == 0:
                    cands = self.board.candidates[r][c]
                    if len(cands) == 1:
                        val = list(cands)[0]
                        return [(r, c, val, f"Cell ({r+1},{c+1}) only allows {val}")]
        return []

    def find_hidden_single(self):
        # ... (keep existing implementation) ...
        # [Simplified version for now to save space, but logically correct]
        for unit_type in ['row', 'col', 'box']:
            for i in range(9):
                cells = self._get_unit_cells(unit_type, i)
                for val in range(1, 10):
                    possible = [rc for rc in cells if self.board.grid[rc[0]][rc[1]] == 0 and val in self.board.candidates[rc[0]][rc[1]]]
                    if len(possible) == 1:
                        r, c = possible[0]
                        return [(r, c, val, f"Value {val} only possible in ({r+1},{c+1}) for {unit_type} {i+1}")]
        return []

    def _get_unit_cells(self, unit_type, i):
        if unit_type == 'row': return [(i, c) for c in range(9)]
        if unit_type == 'col': return [(r, i) for r in range(9)]
        # box
        r_start, c_start = 3 * (i // 3), 3 * (i % 3)
        return [(r, c) for r in range(r_start, r_start + 3) for c in range(c_start, c_start + 3)]

    def find_pointing_tuple(self):
        # Placeholder for pointing pair/triple
        return []

    def find_naked_tuple(self):
        # Placeholder for naked pair/triple
        return []

import random

class PuzzleGenerator:
    def __init__(self):
        pass

    def generate(self, difficulty="Medium"):
        # 1. Generate full board
        base_board = SudokuBoard()
        # Fill diagonal boxes first (they are independent)
        for i in range(0, 9, 3):
            self._fill_box(base_board, i, i)
        
        # Solve the rest with backtracking
        sols = base_board.solve_backtracking()
        full_grid = sols[0]
        puzzle = SudokuBoard(full_grid)
        
        # 2. Remove numbers and check difficulty
        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells)
        
        target_score = {"Easy": 40, "Medium": 80, "Hard": 150, "Expert": 300}[difficulty]
        
        for r, c in cells:
            val = puzzle.grid[r][c]
            puzzle.grid[r][c] = 0
            
            # Check uniqueness - stop at 2
            test_board = SudokuBoard(puzzle.grid)
            if len(test_board.solve_backtracking(limit=2)) > 1:
                puzzle.grid[r][c] = val 
                continue
                
            # Check difficulty
            solver = LogicSolver(puzzle)
            solver.solve()
            if solver.total_score >= target_score:
                break
                
        return puzzle, solver.total_score, solver.steps

    def _fill_box(self, board, start_r, start_c):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board.set_cell(start_r + i, start_c + j, nums.pop())
