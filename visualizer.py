from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

class SudokuVisualizer:
    @staticmethod
    def export_pdf(board, filename="sudoku.pdf", title="Sudoku"):
        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        
        # Draw Title
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 50, title)
        
        # Grid settings
        margin = 100
        grid_size = width - 2 * margin
        cell_size = grid_size / 9
        start_x = margin
        start_y = height - margin - grid_size
        
        # Draw cells and numbers
        c.setFont("Helvetica", 18)
        for r in range(9):
            for col in range(9):
                x = start_x + col * cell_size
                y = start_y + (8 - r) * cell_size
                
                # Draw cell border
                c.setLineWidth(0.5)
                c.rect(x, y, cell_size, cell_size)
                
                # Draw number
                val = board.grid[r][col]
                if val != 0:
                    c.drawCentredString(x + cell_size/2, y + cell_size/3, str(val))
        
        # Draw thick lines for 3x3 boxes
        c.setLineWidth(2)
        for i in range(4):
            # Vertical
            c.line(start_x + i * 3 * cell_size, start_y, 
                   start_x + i * 3 * cell_size, start_y + grid_size)
            # Horizontal
            c.line(start_x, start_y + i * 3 * cell_size, 
                   start_x + grid_size, start_y + i * 3 * cell_size)
            
        c.showPage()
        c.save()
        print(f"PDF exported to {filename}")

    @staticmethod
    def print_debug_steps(steps):
        print("\n--- Solving Steps (Debug) ---")
        for i, step in enumerate(steps, 1):
            print(f"{i}. {step}")
        print("-----------------------------\n")
