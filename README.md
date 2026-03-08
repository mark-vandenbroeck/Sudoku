# Sudoku Architect

[![GitHub Repo](https://img.shields.io/badge/GitHub-Sudoku-blue?logo=github)](https://github.com/mark-vandenbroeck/Sudoku)

Sudoku Architect is a Python-based Sudoku generator and solver that focuses on **logical solvability** rather than brute force. It generates puzzles with a specific difficulty level by simulating human-like solving techniques and assigning a score based on the complexity of the required steps.

## Features

- **Logic-Based Generation**: Puzzles are guaranteed to be solvable using human-readable logic.
- **Difficulty Scoring**: A precise score is calculated based on the techniques used (e.g., Naked Singles, Hidden Singles, etc.).
- **Dual Interface**:
  - **Premium Web App**: A modern Flask-based interface with Glassmorphism and dark mode.
  - **CLI Tool**: A terminal-based generator for quick puzzle creation.
- **Performance Optimized**: High-speed generation using bitmasks and optimized backtracking.
- **Docker Ready**: Fully containerized for easy deployment.
- **PDF Export**: Generate high-quality, printable PDFs of any puzzle.

## Solving Techniques & Scoring

The difficulty of a puzzle is determined by the total score of the steps required to solve it. The following techniques are integrated into the solver:

| Technique | Type | Score | Description |
| :--- | :--- | :--- | :--- |
| **Naked Single** | Placement | 1 | A cell where only one number is possible after checking its row, column, and box. |
| **Hidden Single**| Placement | 2 | A number that can only fit in one specific cell within a row, column, or box. |
| **Pointing Tuple**| Reduction | 8 | A set of numbers in a box that point to a candidates in a row/column outside the box. |
| **Naked Tuple**   | Reduction | 15 | Two or three cells in a unit that contain only the same two or three candidates. |

*Note: The generator uses these scores to hit target difficulty thresholds (e.g., Easy: 40, Medium: 80, Hard: 150).*

## How to Run

### Web Application (Recommended)
1. Ensure you have Flask installed: `pip install flask`.
2. Run the application:
   ```bash
   python3 app.py
   ```
3. Open your browser and navigate to `http://127.0.0.1:5090`.

### Docker (Preferred)
1. Build and start the container:
   ```bash
   docker compose up --build
   ```
2. Open `http://localhost:5090`.

### CLI Tool
1. Run the main script:
   ```bash
   python3 main.py
   ```
2. Follow the interactive prompts to select difficulty and toggle debug mode.

## Project Structure

- `sudoku_engine.py`: The core engine containing the board logic, logic solver, and puzzle generator.
- `visualizer.py`: Utility for PDF export and debug console output.
- `app.py`: Flask server for the web interface.
- `templates/` & `static/`: Frontend assets for the web app.
- `main.py`: Entry point for the CLI version.

## Dependencies

- **Python 3.x**
- **Flask**: For the web interface.
- **ReportLab**: For generating printable PDFs.
