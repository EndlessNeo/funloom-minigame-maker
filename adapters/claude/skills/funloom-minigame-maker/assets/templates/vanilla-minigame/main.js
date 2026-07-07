const TARGET_SCORE = 8;
const START_LIVES = 3;
const START_TIME = 20;

const scoreEl = document.getElementById("score");
const livesEl = document.getElementById("lives");
const timeEl = document.getElementById("time");
const stage = document.getElementById("stage");
const target = document.getElementById("target");
const message = document.getElementById("message");
const startButton = document.getElementById("startButton");
const tapButton = document.getElementById("tapButton");

let score = 0;
let lives = START_LIVES;
let timeLeft = START_TIME;
let running = false;
let timer = 0;

function render() {
  scoreEl.textContent = String(score);
  livesEl.textContent = String(lives);
  timeEl.textContent = String(timeLeft);
}

function placeTarget() {
  const rect = stage.getBoundingClientRect();
  const size = target.offsetWidth || 72;
  const x = Math.max(size, Math.random() * (rect.width - size * 2) + size);
  const y = Math.max(size, Math.random() * (rect.height - size * 2) + size);
  target.style.left = `${x}px`;
  target.style.top = `${y}px`;
}

function finish(result, title, body) {
  if (!running) return;
  running = false;
  window.clearInterval(timer);
  target.style.display = "none";
  message.innerHTML = `<h1>${title}</h1><p>${body}</p>`;
  message.style.display = "grid";
  window.completeFunloomMinigame(result);
}

function scorePoint() {
  if (!running) return;
  score += 1;
  render();
  if (score >= TARGET_SCORE) {
    finish("success", "挑战成功", "你已达到目标分数。");
    return;
  }
  placeTarget();
}

function loseLife() {
  if (!running) return;
  lives -= 1;
  render();
  if (lives <= 0) {
    finish("failure", "挑战失败", "生命值已经归零。");
  }
}

function startGame() {
  score = 0;
  lives = START_LIVES;
  timeLeft = START_TIME;
  running = true;
  render();
  message.style.display = "none";
  target.style.display = "block";
  placeTarget();
  window.clearInterval(timer);
  timer = window.setInterval(() => {
    if (!running) return;
    timeLeft -= 1;
    render();
    if (timeLeft <= 0) {
      finish("failure", "挑战失败", "时间耗尽。");
    }
  }, 1000);
}

target.addEventListener("click", (event) => {
  event.stopPropagation();
  scorePoint();
});

target.addEventListener("touchstart", (event) => {
  event.preventDefault();
  event.stopPropagation();
  scorePoint();
}, { passive: false });

stage.addEventListener("click", (event) => {
  if (event.target === target || event.target === startButton || !running) return;
  loseLife();
});

tapButton.addEventListener("click", scorePoint);
startButton.addEventListener("click", startGame);
window.addEventListener("resize", () => {
  if (running) placeTarget();
});

render();
