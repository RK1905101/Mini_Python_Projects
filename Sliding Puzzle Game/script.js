const puzzle = document.getElementById('puzzle');
const status = document.getElementById('status');
const imageSelect = document.getElementById('image-select');
const uploadInput = document.getElementById('upload');
const startBtn = document.getElementById('start');
const restartBtn = document.getElementById('restart');
const viewOriginalBtn = document.getElementById('view-original');
const originalImage = document.getElementById('original-image');
const elapsedDisplay = document.getElementById('elapsed');
const movesDisplay = document.getElementById('moves');

let timer = null;
let startTime = null;
let moves = 0;

let imgSrc = '';
let useNumbers = false;
let isImageSelected = false;
let board = [];

function initBoard() {
  board = [0,1,2,3,4,5,6,7,8];
  renderTiles();
}

function renderTiles() {
  puzzle.innerHTML = '';

  let emptyCount = board.filter(x => x === 8).length;
  if (emptyCount !== 1) {
    board = [0,1,2,3,4,5,6,7,8];
  }

  for (let pos = 0; pos < 9; pos++) {
    const val = board[pos];
    const tile = document.createElement('div');
    tile.className = 'tile';

    if (val === 8) {
      tile.classList.add('empty');
      tile.textContent = '';
      tile.style.backgroundImage = 'none';
    } else if (useNumbers) {
      tile.textContent = val + 1;
      tile.style.backgroundImage = 'none';
    } else {
      tile.textContent = '';
      tile.style.backgroundImage = `url('${imgSrc}')`;
      tile.style.backgroundPosition = `-${(val % 3) * 100}px -${Math.floor(val / 3) * 100}px`;
    }

    tile.addEventListener('click', () => handleTileClick(pos));
    puzzle.appendChild(tile);
  }
}

function handleTileClick(clickedPos) {
  if (!isImageSelected) return;

  const emptyPos = board.indexOf(8);
  if (isAdjacent(clickedPos, emptyPos)) {
    [board[clickedPos], board[emptyPos]] = [board[emptyPos], board[clickedPos]];
    moves++;
    movesDisplay.textContent = moves;
    renderTiles();
    checkWin();
  }
}

function shuffleBoard() {
  if (!isImageSelected) {
    status.textContent = "Please select an image first.";
    return;
  }

  let temp = board.slice(0,8);
  for (let i = temp.length -1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i+1));
    [temp[i], temp[j]] = [temp[j], temp[i]];
  }

  temp.push(8);
  board = temp;
  renderTiles();
}

function isAdjacent(p1, p2) {
  const r1 = Math.floor(p1 / 3), c1 = p1 % 3;
  const r2 = Math.floor(p2 / 3), c2 = p2 % 3;
  return (Math.abs(r1 - r2) === 1 && c1 === c2) ||
         (Math.abs(c1 - c2) === 1 && r1 === r2);
}

function checkWin() {
  const solved = board.every((val, idx) => val === idx);
  if (solved && timer) {
    clearInterval(timer);
  }
  status.textContent = solved ? "🎉 You Win!" : "";
}

viewOriginalBtn.addEventListener('click', () => {
  if (!isImageSelected) {
    status.textContent = "Please select an image first.";
    return;
  }
  originalImage.src = imgSrc;
  originalImage.style.display = 'block';
  setTimeout(() => {
    originalImage.style.display = 'none';
  }, 3000);
});

imageSelect.addEventListener('change', (e) => {
  status.textContent = '';
  const val = e.target.value;
  useNumbers = (val === 'numbers');

  if (val === 'browse') {
    uploadInput.click();
  } else if (val) {
    imgSrc = useNumbers ? '' : val;
    isImageSelected = true;
    initBoard();
    startBtn.style.display = 'inline-block';
    // resetGame();
  }
});

uploadInput.addEventListener('change', (e) => {
  const file = e.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = () => {
      imgSrc = reader.result;
      isImageSelected = true;
      useNumbers = false;
      initBoard();
      status.textContent = '';
      imageSelect.value = 'browse';
      startBtn.style.display = 'inline-block';
      // resetGame();
    };
    reader.readAsDataURL(file);
  }
});

startBtn.onclick = () => {
  if (!isImageSelected) {
    status.textContent = "Please select an image first.";
    return;
  }
  startGame();
};

restartBtn.onclick = () => {
  if (!isImageSelected) {
    status.textContent = "Please select an image first.";
    return;
  }
  startGame();
};

function startGame() {
  shuffleBoard();
  resetGame();
  startBtn.style.display = 'none';
}

function startTimer() {
  if (timer) clearInterval(timer);
  startTime = Date.now();
  timer = setInterval(() => {
    const now = Date.now();
    const diff = now - startTime;
    const h = String(Math.floor(diff / 3600000)).padStart(2,'0');
    const m = String(Math.floor((diff % 3600000) / 60000)).padStart(2,'0');
    const s = String(Math.floor((diff % 60000) / 1000)).padStart(2,'0');
    elapsedDisplay.textContent = `${h}:${m}:${s}`;
  }, 500);
}

function resetGame() {
  moves = 0;
  movesDisplay.textContent = moves;
  elapsedDisplay.textContent = "00:00:00";
  startTimer();
}

window.onload = () => {
  puzzle.innerHTML = '';
  status.textContent = "Please select an image to begin.";
  startBtn.style.display = 'none';
  restartBtn.style.display = 'inline-block';
  moves = 0;
  movesDisplay.textContent = moves;
  elapsedDisplay.textContent = "00:00:00";
};

initBoard();
