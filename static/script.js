async function generateSudoku(difficulty) {
    const gridContainer = document.getElementById('sudoku-grid');
    const stepsList = document.getElementById('steps-list');
    const downloadBtn = document.getElementById('download-btn');
    const scoreVal = document.getElementById('score-val');

    // Show loader
    gridContainer.innerHTML = '<div class="loader">Generating ' + difficulty + ' puzzle...</div>';
    stepsList.innerHTML = '<p class="placeholder">Analyzing logic...</p>';
    downloadBtn.disabled = true;
    scoreVal.innerText = '--';

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ difficulty })
        });

        const data = await response.json();
        renderGrid(data.grid);
        renderSteps(data.steps);
        scoreVal.innerText = data.score;
        downloadBtn.disabled = false;
    } catch (error) {
        console.error('Error generating Sudoku:', error);
        gridContainer.innerHTML = '<div class="loader error">Failed to generate puzzle. Please try again.</div>';
    }
}

function renderGrid(grid) {
    const gridContainer = document.getElementById('sudoku-grid');
    gridContainer.innerHTML = '';

    const table = document.createElement('div');
    table.className = 'sudoku-grid';

    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            const val = grid[r][c];
            if (val !== 0) {
                cell.innerText = val;
                cell.classList.add('generated');
            }
            table.appendChild(cell);
        }
    }
    gridContainer.appendChild(table);
}

function renderSteps(steps) {
    const stepsList = document.getElementById('steps-list');
    stepsList.innerHTML = '';

    if (steps.length === 0) {
        stepsList.innerHTML = '<p class="placeholder">No steps recorded.</p>';
        return;
    }

    steps.forEach((step, index) => {
        const item = document.createElement('div');
        item.className = 'step-item';
        item.style.animationDelay = `${index * 0.05}s`;
        item.innerText = `${index + 1}. ${step}`;
        stepsList.appendChild(item);
    });
}

function downloadPDF() {
    window.location.href = '/download';
}
