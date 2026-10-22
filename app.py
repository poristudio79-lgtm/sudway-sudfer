import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Head Soccer 2D Battle", page_icon="⚽", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; margin: 0; padding: 0; }
    iframe { border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
    </style>
""", unsafe_allow_html=True)

HEAD_SOCCER_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body, html { width: 100%; height: 100%; overflow: hidden; background: #070b12; font-family: 'Arial Black', sans-serif; display: flex; justify-content: center; align-items: center; }
  
  #gameContainer { position: relative; width: 900px; height: 500px; background: linear-gradient(to bottom, #1a2a6c, #b21f1f, #fdbb2d); border-radius: 12px; overflow: hidden; border: 4px solid #fff; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
  canvas { display: block; width: 100%; height: 100%; }

  /* UI HUD */
  #hud { position: absolute; top: 15px; left: 0; right: 0; display: flex; justify-content: space-around; align-items: center; z-index: 10; pointer-events: none; }
  .score-board { background: rgba(0, 0, 0, 0.6); padding: 8px 25px; border-radius: 20px; border: 2px solid #fff; color: #fff; font-size: 28px; font-weight: 900; letter-spacing: 3px; text-shadow: 2px 2px 0 #000; }
  .timer-board { background: rgba(255, 215, 0, 0.8); color: #000; padding: 6px 18px; border-radius: 15px; border: 2px solid #fff; font-size: 22px; font-weight: 900; }

  /* Power Bar HUD */
  .power-container { position: absolute; bottom: 15px; width: 220px; height: 16px; background: rgba(0,0,0,0.6); border: 2px solid #fff; border-radius: 10px; overflow: hidden; z-index: 10; }
  #p1PowerBar { left: 30px; }
  #p2PowerBar { right: 30px; }
  .power-fill { height: 100%; width: 0%; background: linear-gradient(90deg, #ff9800, #ffeb3b); transition: width 0.1s; }

  /* Screens */
  .screen { position: absolute; inset: 0; background: rgba(10, 15, 25, 0.92); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 20; transition: opacity 0.3s; }
  .hidden { display: none !important; }

  h1 { font-size: 42px; color: #ffeb3b; text-shadow: 3px 3px 0 #ff5722, -3px -3px 0 #ff5722; margin-bottom: 10px; text-align: center; }
  p { color: #fff; font-size: 16px; margin-bottom: 25px; text-align: center; }
  
  .btn-group { display: flex; gap: 15px; }
  .menu-btn { background: linear-gradient(135deg, #00e676, #00b0ff); color: #fff; font-size: 20px; font-weight: 900; padding: 12px 30px; border-radius: 25px; border: 3px solid #fff; cursor: pointer; box-shadow: 0 6px 20px rgba(0,230,118,0.5); transition: transform 0.2s; }
  .menu-btn:hover { transform: scale(1.08); }
  .btn-p2 { background: linear-gradient(135deg, #ff3d00, #ffea00); box-shadow: 0 6px 20px rgba(255,61,0,0.5); }
</style>
</head>
<body>

<div id="gameContainer">
  <!-- HUD -->
  <div id="hud">
    <div class="score-board" id="scoreP1">0 - 0</div>
    <div class="timer-board" id="timerDisplay">60</div>
    <div class="score-board" id="scoreP2">0 - 0</div>
  </div>

  <div class="power-container" id="p1PowerBar"><div class="power-fill" id="p1Fill"></div></div>
  <div class="power-container" id="p2PowerBar"><div class="power-fill" id="p2Fill"></div></div>

  <!-- CANVAS GAME 2D -->
  <canvas id="gameCanvas" width="900" height="500"></canvas>

  <!-- START MENU -->
  <div id="menuScreen" class="screen">
    <h1>⚽ HEAD SOCCER 2D</h1>
    <p>Dùng đầu & chân sút tung lưới đối thủ!<br><b>P1:</b> A/D (Di chuyển), W (Nhảy), S (Sút), Space (Tuyệt chiêu)<br><b>P2:</b> Phím Mũi Tên (Di chuyển/Nhảy/Sút)</p>
    <div class="btn-group">
      <button class="menu-btn" onclick="startGame(1)">1 PLAYER (VS AI)</button>
      <button class="menu-btn btn-p2" onclick="startGame(2)">2 PLAYERS</button>
    </div>
  </div>

  <!-- GAME OVER SCREEN -->
  <div id="overScreen" class="screen hidden">
    <h1 id="winnerText">TRẬN ĐẤU KẾT THÚC</h1>
    <p id="finalScoreText" style="font-size: 24px; color: #ffeb3b; margin: 15px 0;">Tỷ số: 0 - 0</p>
    <button class="menu-btn" onclick="location.reload()">CHƠI LẠI</button>
  </div>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let gameMode = 1; // 1: VS AI, 2: 2 Players
let gameState = 'MENU'; // MENU, PLAYING, GAMEOVER
let timeLeft = 60;
let gameTimerInterval = null;

// Game Objects
const groundY = 410;

let p1 = {
  x: 200, y: groundY, vx: 0, vy: 0, r: 35, 
  color: '#00e676', hatColor: '#1b5e20', score: 0, power: 0, facing: 1
};

let p2 = {
  x: 700, y: groundY, vx: 0, vy: 0, r: 35, 
  color: '#ff3d00', hatColor: '#b71c1c', score: 0, power: 0, facing: -1
};

let ball = {
  x: 450, y: 250, vx: 0, vy: 0, r: 20
};

// Input Controls
let keys = {};
window.addEventListener('keydown', e => { keys[e.key.toLowerCase()] = true; });
window.addEventListener('keyup', e => { keys[e.key.toLowerCase()] = false; });

function startGame(mode) {
  gameMode = mode;
  gameState = 'PLAYING';
  document.getElementById('menuScreen').classList.add('hidden');
  
  p1.score = 0; p2.score = 0; p1.power = 0; p2.power = 0;
  resetPositions();

  timeLeft = 60;
  if(gameTimerInterval) clearInterval(gameTimerInterval);
  gameTimerInterval = setInterval(() => {
    timeLeft--;
    document.getElementById('timerDisplay').innerText = timeLeft;
    if (timeLeft <= 0) {
      clearInterval(gameTimerInterval);
      endGame();
    }
  }, 1000);
}

function resetPositions() {
  p1.x = 200; p1.y = groundY; p1.vx = 0; p1.vy = 0;
  p2.x = 700; p2.y = groundY; p2.vx = 0; p2.vy = 0;
  ball.x = 450; ball.y = 180; ball.vx = 0; ball.vy = -4;
}

function endGame() {
  gameState = 'GAMEOVER';
  document.getElementById('overScreen').classList.remove('hidden');
  let text = "HÒA NHAU!";
  if (p1.score > p2.score) text = "🏆 PLAYER 1 (XANH) CHIẾN THẮNG!";
  else if (p2.score > p1.score) text = gameMode === 1 ? "🤖 MÁY (AI) CHIẾN THẮNG!" : "🏆 PLAYER 2 (ĐỎ) CHIẾN THẮNG!";
  document.getElementById('winnerText').innerText = text;
  document.getElementById('finalScoreText').innerText = `Tỷ số: ${p1.score} - ${p2.score}`;
}

// --- GAME LOOP UPDATE ---
function update() {
  if (gameState !== 'PLAYING') return;

  // --- PLAYER 1 CONTROLS (WASD + Space) ---
  if (keys['a']) { p1.vx = -5; p1.facing = -1; }
  else if (keys['d']) { p1.vx = 5; p1.facing = 1; }
  else { p1.vx *= 0.8; }

  if (keys['w'] && p1.y >= groundY) { p1.vy = -14; }
  
  // Power Shot P1 (Space)
  if (keys[' ' ] && p1.power >= 100) {
    p1.power = 0;
    if (Math.hypot(ball.x - p1.x, ball.y - p1.y) < 70) {
      ball.vx = 18 * p1.facing;
      ball.vy = -12;
    }
  }

  // --- PLAYER 2 CONTROLS ---
  if (gameMode === 2) {
    if (keys['arrowleft']) { p2.vx = -5; p2.facing = -1; }
    else if (keys['arrowright']) { p2.vx = 5; p2.facing = 1; }
    else { p2.vx *= 0.8; }

    if (keys['arrowup'] && p2.y >= groundY) { p2.vy = -14; }
    
    if (keys['enter'] && p2.power >= 100) {
      p2.power = 0;
      if (Math.hypot(ball.x - p2.x, ball.y - p2.y) < 70) {
        ball.vx = 18 * p2.facing;
        ball.vy = -12;
      }
    }
  } else {
    // AI LOGIC
    let targetX = ball.x + (ball.vx * 5);
    if (targetX < 480) targetX = 520; // Giữ sân nhà
    if (p2.x < targetX - 15) { p2.vx = 4.2; p2.facing = -1; }
    else if (p2.x > targetX + 15) { p2.vx = -4.2; p2.facing = 1; }
    else { p2.vx *= 0.8; }

    if (ball.y < 300 && ball.x > 450 && p2.y >= groundY && Math.random() < 0.08) {
      p2.vy = -13;
    }
  }

  // Physics Gravity for Players
  [p1, p2].forEach(p => {
    p.vy += 0.6; // Trọng lực
    p.y += p.vy;
    p.x += p.vx;

    if (p.y > groundY) { p.y = groundY; p.vy = 0; }
    // Giới hạn biên sân
    if (p === p1) {
      if (p.x < p.r) p.x = p.r;
      if (p.x > 430) p.x = 430;
    } else {
      if (p.x < 470) p.x = 470;
      if (p.x > 900 - p.r) p.x = 900 - p.r;
    }
  });

  // Ball Physics
  ball.vy += 0.45; // Trọng lực bóng
  ball.x += ball.vx;
  ball.y += ball.vy;
  ball.vx *= 0.99; // Ma sát không khí

  // Va chạm biên sân bóng
  if (ball.x - ball.r < 0) { ball.x = ball.r; ball.vx *= -0.7; }
  if (ball.x + ball.r > 900) { ball.x = 900 - ball.r; ball.vx *= -0.7; }
  if (ball.y - ball.r < 0) { ball.y = ball.r; ball.vy *= -0.7; }

  // Va chạm mặt đất
  if (ball.y + ball.r > groundY + 20) {
    ball.y = groundY + 20 - ball.r;
    ball.vy *= -0.75;
  }

  // --- VA CHẠM CẦU THỦ & BÓNG ---
  [p1, p2].forEach(p => {
    let dx = ball.x - p.x;
    let dy = ball.y - p.y;
    let dist = Math.hypot(dx, dy);
    let minDist = p.r + ball.r;

    if (dist < minDist) {
      let angle = Math.atan2(dy, dx);
      let hitSpeed = Math.hypot(p.vx, p.vy) + 6;
      ball.vx = Math.cos(angle) * hitSpeed + p.vx * 0.5;
      ball.vy = Math.sin(angle) * hitSpeed + p.vy * 0.5;
      
      // Tăng năng lượng tuyệt chiêu
      p.power = Math.min(100, p.power + 15);
    }
  });

  // --- GHI BÀN (LUẬT LƯỚI & KHUNG THÀNH) ---
  // Khung thành trái (x: 0-70, y: 260-410) -> P2 ghi bàn
  if (ball.x - ball.r < 70 && ball.y > 250) {
    p2.score++;
    updateScoreUI();
    resetPositions();
  }
  // Khung thành phải (x: 830-900, y: 260-410) -> P1 ghi bàn
  if (ball.x + ball.r > 830 && ball.y > 250) {
    p1.score++;
    updateScoreUI();
    resetPositions();
  }

  // Cập nhật thanh Power Bar UI
  document.getElementById('p1Fill').style.width = p1.power + '%';
  document.getElementById('p2Fill').style.width = p2.power + '%';
}

function updateScoreUI() {
  document.getElementById('scoreP1').innerText = `${p1.score} - ${p2.score}`;
  document.getElementById('scoreP2').innerText = `${p2.score} - ${p1.score}`;
}

// --- RENDER HỌA TIẾT ĐỒ HỌA 2D ---
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Vẽ Khán đài & Sân vận động nền
  ctx.fillStyle = '#141e30';
  ctx.fillRect(0, 0, canvas.width, groundY + 20);

  // Vạch sân cỏ
  ctx.fillStyle = '#2e7d32';
  ctx.fillRect(0, groundY + 20, canvas.width, canvas.height - (groundY + 20));
  
  // Vòng tròn giữa sân
  ctx.strokeStyle = 'rgba(255,255,255,0.3)';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.arc(450, groundY + 20, 70, Math.PI, 0, false);
  ctx.stroke();

  // Khung thành trái & phải
  ctx.fillStyle = 'rgba(255,255,255,0.15)';
  ctx.fillRect(0, 250, 70, 160);
  ctx.fillRect(830, 250, 70, 160);

  // Cột lưới khung thành
  ctx.strokeStyle = '#fff';
  ctx.lineWidth = 6;
  ctx.strokeRect(0, 250, 70, 160);
  ctx.strokeRect(830, 250, 70, 160);

  // Vẽ Cầu thủ 1 (Đầu to chân ngắn)
  drawPlayer(p1);
  // Vẽ Cầu thủ 2
  drawPlayer(p2);

  // Vẽ Quả bóng đá
  ctx.save();
  ctx.translate(ball.x, ball.y);
  ctx.rotate(Date.now() * 0.003);
  ctx.fillStyle = '#fff';
  ctx.beginPath(); ctx.arc(0, 0, ball.r, 0, Math.PI * 2); ctx.fill();
  ctx.lineWidth = 2; ctx.strokeStyle = '#000'; ctx.stroke();
  // Họa tiết quả bóng
  ctx.fillStyle = '#000';
  ctx.beginPath(); ctx.arc(0, 0, 6, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}

function drawPlayer(p) {
  ctx.save();
  ctx.translate(p.x, p.y);

  // Thân áo nhỏ dưới đầu
  ctx.fillStyle = p.color;
  ctx.fillRect(-14, -5, 28, 35);
  ctx.lineWidth = 2; ctx.strokeStyle = '#fff'; ctx.strokeRect(-14, -5, 28, 35);

  // Đôi giày / Chân
  ctx.fillStyle = '#111';
  ctx.beginPath();
  ctx.arc(p.facing * 12, 35, 10, 0, Math.PI * 2);
  ctx.fill();

  // Đầu to đặc trưng Head Soccer
  ctx.fillStyle = '#ffdbac'; // Màu da
  ctx.beginPath();
  ctx.arc(0, -35, p.r, 0, Math.PI * 2);
  ctx.fill();
  ctx.lineWidth = 3; ctx.strokeStyle = '#222'; ctx.stroke();

  // Mắt & Miệng biểu cảm
  ctx.fillStyle = '#222';
  ctx.beginPath();
  ctx.arc(p.facing * 12, -42, 5, 0, Math.PI * 2);
  ctx.fill();

  // Nón / Tóc cầu thủ
  ctx.fillStyle = p.hatColor;
  ctx.beginPath();
  ctx.arc(0, -45, p.r, Math.PI, 0, false);
  ctx.fill();

  ctx.restore();
}

// Loop
function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();
</script>
</body>
</html>
"""

components.html(HEAD_SOCCER_HTML, height=530)
