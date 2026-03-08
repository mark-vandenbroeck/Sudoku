from flask import Flask, render_template, request, jsonify, send_file, session
import os
import uuid
from sudoku_engine import PuzzleGenerator, SudokuBoard
from visualizer import SudokuVisualizer

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Directory for temporary PDF files
TEMP_DIR = "/tmp/sudoku_web"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    difficulty = data.get('difficulty', 'Medium')
    
    gen = PuzzleGenerator()
    puzzle, score, steps = gen.generate(difficulty)
    
    # Store puzzle in session (as nested list)
    session['current_puzzle'] = puzzle.grid
    session['difficulty'] = difficulty
    
    return jsonify({
        'grid': puzzle.grid,
        'score': score,
        'steps': steps
    })

@app.route('/download', methods=['GET'])
def download():
    grid = session.get('current_puzzle')
    difficulty = session.get('difficulty', 'Sudoku')
    
    if not grid:
        return "No puzzle generated yet", 400
        
    board = SudokuBoard(grid)
    filename = f"sudoku_{uuid.uuid4().hex}.pdf"
    filepath = os.path.join(TEMP_DIR, filename)
    
    SudokuVisualizer.export_pdf(board, filename=filepath, title=f"Sudoku - {difficulty}")
    
    return send_file(filepath, as_attachment=True, download_name=f"sudoku_{difficulty.lower()}.pdf")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5090)
