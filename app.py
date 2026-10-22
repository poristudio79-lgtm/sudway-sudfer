import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Subway Surfers 3D Runner", page_icon="🏃", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; margin: 0; padding: 0; }
    iframe { border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); }
    </style>
""", unsafe_allow_html=True)

SUBWAY_3D_HTML = """
<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; }
  body, html { width: 100%; height: 100%; overflow: hidden; background: #000; font-family: 'Arial Black', -apple-system, sans-serif; }
  #canvas-container { position: relative; width: 100vw; height: 100vh; max-width: 900px; max-height: 550px; margin: 0 auto; overflow: hidden; background: #000; }
  canvas { display: block; width: 100%; height: 100%; }

  /* HUD Top Bar */
  #hud { position: absolute; top: 12px; left: 12px; right: 12px; display: flex; justify-content: space-between; align-items: flex-start; pointer-events: none; z-index: 10; }
  .pause-btn { width: 44px; height: 44px; background: #0088cc; border: 3px solid #fff; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; pointer-events: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.5); }
  .pause-btn::before, .pause-btn::after { content: ''; width: 6px; height: 18px; background: #fff; margin: 0 2px; border-radius: 2px; }
  .stats-container { display: flex; flex-direction: column; align-items: flex-end; gap: 6px; }
  .score-box { display: flex; align-items: center; gap: 8px; }
  .multiplier-tag { background: #ffaa00; color: #fff; font-size: 16px; font-weight: 900; padding: 2px 8px; border-radius: 6px; border: 2px solid #fff; text-shadow: 1px 1px 2px #000; }
  .score-val { color: #fff; font-size: 26px; font-weight: 900; letter-spacing: 2px; text-shadow: 2px 2px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000; }
  .coins-box { display: flex; align-items: center; gap: 6px; background: rgba(0,0,0,0.4); padding: 4px 10px; border-radius: 20px; border: 2px solid rgba(255,255,255,0.3); }
  .coin-icon { width: 22px; height: 22px; background: gold; border-radius: 50%; border: 2px solid #fff; display: flex; align-items: center; justify-content: center; font-size: 11px; color: #b8860b; font-weight: bold; box-shadow: 0 0 5px gold; }
  .coin-val { color: #fff; font-size: 18px; font-weight: 900; text-shadow: 1px 1px 2px #000; }

  /* Powerup HUD Active Timers */
  #active-powerups { position: absolute; top: 70px; left: 12px; display: flex; flex-direction: column; gap: 6px; pointer-events: none; z-index: 10; }
  .pwr-bar-item { display: flex; align-items: center; gap: 6px; background: rgba(0,0,0,0.6); padding: 4px 8px; border-radius: 12px; border: 1.5px solid #fff; }
  .pwr-ico { font-size: 16px; }
  .pwr-progress-bg { width: 60px; height: 8px; background: #333; border-radius: 4px; overflow: hidden; }
  .pwr-progress-fill { height: 100%; width: 100%; background: #00ffcc; transition: width 0.1s linear; }

  /* Hoverboard Button HUD */
  #board-hud { position: absolute; bottom: 20px; left: 20px; pointer-events: auto; z-index: 10; display: flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.5); padding: 8px 14px; border-radius: 25px; border: 2px solid #00ffff; cursor: pointer; }
  .board-icon { font-size: 22px; }
  .board-text { color: #fff; font-size: 14px; font-weight: bold; }

  /* UI Screens */
  .overlay-screen { position: absolute; inset: 0; background: rgba(0,0,0,0.7); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 20; transition: opacity 0.3s ease; }
  .hidden { display: none !important; }

  #start-screen h1 { font-size: 42px; color: #ffea00; text-shadow: 3px 3px 0 #d32f2f, -3px -3px 0 #d32f2f, 3px -3px 0 #d32f2f, -3px 3px 0 #d32f2f; margin-bottom: 8px; font-style: italic; }
  #start-screen p { color: #fff; font-size: 16px; margin-bottom: 25px; text-shadow: 1px 1px 2px #000; }
  .tap-to-play-btn { background: linear-gradient(135deg, #00e676, #00b0ff); color: #fff; font-size: 24px; font-weight: 900; padding: 14px 45px; border-radius: 30px; border: 4px solid #fff; box-shadow: 0 8px 25px rgba(0,230,118,0.6); cursor: pointer; transform: scale(1); animation: pulse 1.5s infinite; }
  @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.06); } }

  /* GAME OVER NOTEBOOK OVERLAY */
  .notebook-container { position: relative; width: 340px; background: #e0e0e0; border-radius: 12px; padding: 16px; box-shadow: 0 20px 50px rgba(0,0,0,0.9); border: 3px solid #ccc; background-image: repeating-linear-gradient(#e0e0e0, #e0e0e0 24px, #a0c0e0 25px); display: flex; flex-direction: column; align-items: center; }
  .notebook-rings { position: absolute; top: -14px; left: 20px; right: 20px; display: flex; justify-content: space-between; }
  .ring { width: 12px; height: 26px; background: linear-gradient(#aaa, #fff, #888); border-radius: 6px; border: 1px solid #555; }
  
  .nb-header { display: flex; justify-content: space-between; width: 100%; margin-top: 10px; padding: 0 10px; }
  .nb-stat { display: flex; align-items: center; gap: 4px; font-size: 14px; font-weight: 900; color: #333; }
  
  .nb-score-title { font-size: 20px; color: #0055aa; margin-top: 5px; font-weight: 900; font-style: italic; }
  .nb-score-banner { background: linear-gradient(#0066cc, #003388); color: #fff; width: 100%; text-align: center; font-size: 32px; font-weight: 900; padding: 6px 0; border-radius: 6px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border: 2px dashed #fff; margin: 4px 0 10px; }
  
  .nb-double-btn { background: linear-gradient(#00c853, #00897b); border: 2px solid #fff; border-radius: 8px; width: 100%; padding: 8px; color: #fff; font-size: 14px; font-weight: 900; display: flex; align-items: center; justify-content: space-between; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }
  
  .nb-leaderboard { width: 100%; background: #fff; border-radius: 8px; margin-top: 10px; padding: 6px; border: 1px solid #bbb; }
  .lb-row { display: flex; align-items: center; justify-content: space-between; padding: 4px 6px; font-size: 11px; font-weight: 900; border-bottom: 1px solid #eee; }
  .lb-row:last-child { border-bottom: none; }
  .lb-rank { width: 16px; color: #555; }
  .lb-name { flex: 1; margin-left: 6px; color: #222; }
  .lb-score { color: #000; }

  .nb-bottom-nav { display: flex; gap: 12px; margin-top: 14px; width: 100%; justify-content: center; }
  .nb-btn { flex: 1; padding: 10px; border-radius: 10px; border: 2px solid #fff; font-size: 16px; font-weight: 900; color: #fff; cursor: pointer; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
  .btn-home { background: linear-gradient(#757575, #424242); }
  .btn-play { background: linear-gradient(#76ff03, #33691e); color: #000; }
</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>

<div id="canvas-container">
  <!-- HUD Top -->
  <div id="hud">
    <div class="pause-btn" id="pauseBtn"></div>
    <div class="stats-container">
      <div class="score-box">
        <span class="multiplier-tag" id="multTag">x3</span>
        <span class="score-val" id="scoreDisplay">000000</span>
      </div>
      <div class="coins-box">
        <div class="coin-icon">★</div>
        <span class="coin-val" id="coinDisplay">0</span>
      </div>
    </div>
  </div>

  <!-- Active Powerups List -->
  <div id="active-powerups"></div>

  <!-- Board HUD -->
  <div id="board-hud" onclick="activateBoard()">
    <span class="board-icon">🛹</span>
    <span class="board-text" id="boardCountText">VÁN TRƯỢT (x3)</span>
  </div>

  <!-- Start Screen -->
  <div id="start-screen" class="overlay-screen">
    <h1>SUBWAY SURFERS</h1>
    <p>Né tránh chướng ngại vật & Thu thập xu!</p>
    <button class="tap-to-play-btn" onclick="startGame()">BẮT ĐẦU</button>
  </div>

  <!-- Game Over Notebook Screen -->
  <div id="gameover-screen" class="overlay-screen hidden">
    <div class="notebook-container">
      <div class="notebook-rings">
        <div class="ring"></div><div class="ring"></div><div class="ring"></div><div class="ring"></div><div class="ring"></div>
      </div>
      
      <div class="nb-header">
        <div class="nb-stat">🔑 0</div>
        <div class="nb-stat">🪙 <span id="nbTotalCoins">0</span></div>
      </div>

      <div class="nb-score-title">★ Score ★</div>
      <div class="nb-score-banner" id="nbFinalScore">0</div>
      <div style="font-size:12px; font-weight:bold; color:#ff6d00; margin-bottom:6px;">🪙 <span id="nbRunCoins">0</span> Coins Collected</div>

      <div class="nb-double-btn">
        <span>Free Double Up!</span>
        <span style="background:#ffea00; color:#000; padding:2px 8px; border-radius:4px; font-size:12px;">▶</span>
      </div>

      <div class="nb-leaderboard">
        <div class="lb-row"><span class="lb-rank">1</span><span class="lb-name">Yutani</span><span class="lb-score">999999</span></div>
        <div class="lb-row"><span class="lb-rank">2</span><span class="lb-name">Spike</span><span class="lb-score">810312</span></div>
        <div class="lb-row"><span class="lb-rank">3</span><span class="lb-name">Fresh</span><span class="lb-score">555555</span></div>
        <div class="lb-row"><span class="lb-rank">4</span><span class="lb-name">Tricky</span><span class="lb-score">345678</span></div>
        <div class="lb-row"><span class="lb-rank">5</span><span class="lb-name">Ninja</span><span class="lb-score">123456</span></div>
      </div>

      <div class="nb-bottom-nav">
        <div class="nb-btn btn-home" onclick="resetToMenu()">MENU</div>
        <div class="nb-btn btn-play" onclick="startGame()">PLAY</div>
      </div>
    </div>
  </div>
</div>

<script>
// --- GAME STATE ---
let gameState = 'START'; // START, INTRO, RUNNING, CAUGHT, GAMEOVER
let score = 0, coins = 0, multiplier = 3;
let runTime = 0;
let boardsCount = 3;
let boardActive = false, boardTime = 0;

// Lanes: -1 (Left), 0 (Center), 1 (Right)
let currentLane = 0;
const laneX = [-2.2, 0, 2.2];
let playerPos = { x: 0, y: 0, z: 0 };
let playerVelY = 0;
let isJumping = false, isSliding = false;
let slideTimer = 0;

// Active Powerups: { magnet: 0, sneakers: 0, jetpack: 0, mult2x: 0 }
let powerups = { magnet: 0, sneakers: 0, jetpack: 0, mult2x: 0 };

// THREE.JS SETUP
const container = document.getElementById('canvas-container');
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x0a151d);
scene.fog = new THREE.FogExp2(0x0a151d, 0.025);

const camera = new THREE.PerspectiveCamera(60, 900 / 550, 0.1, 100);
camera.position.set(0, 3.2, 5.5);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
renderer.shadowMap.enabled = true;
container.appendChild(renderer.domElement);

// LIGHTS
const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
scene.add(ambientLight);

const dirLight = new THREE.DirectionalLight(0xfffaed, 0.8);
dirLight.position.set(5, 15, 5);
dirLight.castShadow = true;
scene.add(dirLight);

// --- ENVIRONMENT BUILDER ---
const tunnelGroup = new THREE.Group();
scene.add(tunnelGroup);

function createTunnelSegment(zPos) {
  const seg = new THREE.Group();
  seg.position.z = zPos;

  // Ground Turquoise Track
  const groundGeo = new THREE.PlaneGeometry(8, 20);
  const groundMat = new THREE.MeshStandardMaterial({ color: 0x009988, roughness: 0.5 });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.rotation.x = -Math.PI / 2;
  seg.add(ground);

  // Rails
  [-2.2, 0, 2.2].forEach(rx => {
    const railGeo = new THREE.BoxGeometry(0.1, 0.08, 20);
    const railMat = new THREE.MeshStandardMaterial({ color: 0x888888, metalness: 0.8 });
    const r1 = new THREE.Mesh(railGeo, railMat); r1.position.set(rx - 0.4, 0.04, 0);
    const r2 = new THREE.Mesh(railGeo, railMat); r2.position.set(rx + 0.4, 0.04, 0);
    seg.add(r1, r2);
  });

  // Tunnel Side Walls (Arched Green-Grey Brick)
  const wallMat = new THREE.MeshStandardMaterial({ color: 0x4a5d4e, roughness: 0.8 });
  const leftWall = new THREE.Mesh(new THREE.BoxGeometry(1, 6, 20), wallMat);
  leftWall.position.set(-4.5, 3, 0);
  const rightWall = new THREE.Mesh(new THREE.BoxGeometry(1, 6, 20), wallMat);
  rightWall.position.set(4.5, 3, 0);
  
  // Ceiling
  const ceil = new THREE.Mesh(new THREE.BoxGeometry(10, 1, 20), wallMat);
  ceil.position.set(0, 6.5, 0);

  seg.add(leftWall, rightWall, ceil);
  tunnelGroup.add(seg);
  return seg;
}

let tunnelSegments = [];
for (let i = 0; i < 6; i++) {
  tunnelSegments.push(createTunnelSegment(-i * 20));
}

// --- CHARACTER MODELS ---
// Player (Jake)
const playerGroup = new THREE.Group();
const shirtMat = new THREE.MeshStandardMaterial({ color: 0xffffff });
const skinMat = new THREE.MeshStandardMaterial({ color: 0xffdbac });
const capMat = new THREE.MeshStandardMaterial({ color: 0xd32f2f });

const pBody = new THREE.Mesh(new THREE.BoxGeometry(0.5, 0.7, 0.3), shirtMat); pBody.position.y = 0.85;
const pHead = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), skinMat); pHead.position.y = 1.35;
const pCap = new THREE.Mesh(new THREE.BoxGeometry(0.38, 0.1, 0.38), capMat); pCap.position.set(0, 1.48, 0.02);

// Hoverboard Mesh
const boardMesh = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.08, 1.4), new THREE.MeshStandardMaterial({ color: 0x00ffff, emissive: 0x004466 }));
boardMesh.position.y = 0.1;
boardMesh.visible = false;

playerGroup.add(pBody, pHead, pCap, boardMesh);
scene.add(playerGroup);

// Inspector & Dog
const chaserGroup = new THREE.Group();
const inspBody = new THREE.Mesh(new THREE.BoxGeometry(0.7, 0.8, 0.4), new THREE.MeshStandardMaterial({ color: 0xeeeeee })); inspBody.position.y = 0.9;
const inspHead = new THREE.Mesh(new THREE.SphereGeometry(0.22, 16, 16), skinMat); inspHead.position.y = 1.45;
const dogMesh = new THREE.Mesh(new THREE.BoxGeometry(0.3, 0.35, 0.5), new THREE.MeshStandardMaterial({ color: 0x888888 })); dogMesh.position.set(0.6, 0.2, 0);

chaserGroup.add(inspBody, inspHead, dogMesh);
chaserGroup.position.set(0, 0, 1.8);
scene.add(chaserGroup);

// --- OBSTACLES & COINS DYNAMIC SYSTEM ---
const obstacles = [];
const coinsList = [];
const powerupItems = [];

function spawnObstacleCluster(zPos) {
  const lane = [-1, 0, 1][Math.floor(Math.random() * 3)];
  const type = Math.random();

  if (type < 0.5) {
    // Train (Cream/Orange)
    const trainGroup = new THREE.Group();
    trainGroup.position.set(laneX[lane + 1], 0, zPos);

    const bodyGeo = new THREE.BoxGeometry(1.8, 2.4, 8);
    const bodyMat = new THREE.MeshStandardMaterial({ color: 0xe0d8c8, roughness: 0.4 });
    const body = new THREE.Mesh(bodyGeo, bodyMat); body.position.y = 1.2;

    const stripe = new THREE.Mesh(new THREE.BoxGeometry(1.82, 0.3, 8), new THREE.MeshStandardMaterial({ color: 0xff5500 }));
    stripe.position.y = 0.8;

    trainGroup.add(body, stripe);
    trainGroup.userData = { type: 'TRAIN', box: new THREE.Box3() };
    scene.add(trainGroup);
    obstacles.push(trainGroup);
  } else {
    // Barrier
    const bar = new THREE.Mesh(new THREE.BoxGeometry(1.6, 1.0, 0.2), new THREE.MeshStandardMaterial({ color: 0xd32f2f }));
    bar.position.set(laneX[lane + 1], 0.5, zPos);
    bar.userData = { type: 'BARRIER', box: new THREE.Box3() };
    scene.add(bar);
    obstacles.push(bar);
  }

  // Spawn Coins Trail
  for (let c = 0; c < 5; c++) {
    const coin = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.05, 16), new THREE.MeshStandardMaterial({ color: 0xffd700, metalness: 0.8 }));
    coin.rotation.x = Math.PI / 2;
    coin.position.set(laneX[lane + 1], 0.6, zPos - 3 - c * 1.2);
    scene.add(coin);
    coinsList.push(coin);
  }
}

// --- CONTROLS ---
window.addEventListener('keydown', (e) => {
  if (gameState !== 'RUNNING') return;
  if (e.key === 'ArrowLeft' || e.key === 'a') { if (currentLane > -1) currentLane--; }
  if (e.key === 'ArrowRight' || e.key === 'd') { if (currentLane < 1) currentLane++; }
  if ((e.key === 'ArrowUp' || e.key === 'w') && !isJumping) {
    isJumping = true;
    playerVelY = powerups.sneakers > 0 ? 0.22 : 0.16;
  }
  if (e.key === 'ArrowDown' || e.key === 's') {
    isSliding = true; slideTimer = 0.6;
    if (isJumping) playerVelY = -0.2;
  }
  if (e.key === ' ' || e.key === 'Spacebar') { activateBoard(); }
});

function activateBoard() {
  if (boardsCount > 0 && !boardActive && gameState === 'RUNNING') {
    boardsCount--;
    boardActive = true;
    boardTime = 8.0; // 8 seconds protection
    boardMesh.visible = true;
    document.getElementById('boardCountText').innerText = `VÁN TRƯỢT (x${boardsCount})`;
  }
}

function startGame() {
  gameState = 'RUNNING';
  score = 0; coins = 0; runTime = 0; currentLane = 0;
  playerPos = { x: 0, y: 0, z: 0 };
  
  document.getElementById('start-screen').classList.add('hidden');
  document.getElementById('gameover-screen').classList.add('hidden');
  
  chaserGroup.position.set(0, 0, 1.8);
  chaserGroup.visible = true;
}

function resetToMenu() {
  gameState = 'START';
  document.getElementById('start-screen').classList.remove('hidden');
  document.getElementById('gameover-screen').classList.add('hidden');
}

// --- GAME LOOP ---
const clock = new THREE.Clock();

function animate() {
  requestAnimationFrame(animate);
  const delta = clock.getDelta();

  if (gameState === 'RUNNING') {
    runTime += delta;
    score += Math.floor(delta * 60 * (powerups.mult2x > 0 ? 2 : 1));
    document.getElementById('scoreDisplay').innerText = String(score).padStart(6, '0');
    document.getElementById('coinDisplay').innerText = coins;

    // 1-Second Disappear Chaser Mechanic
    if (runTime >= 1.0 && chaserGroup.visible) {
      chaserGroup.visible = false;
    }

    // Lane Smooth Movement
    playerPos.x += (laneX[currentLane + 1] - playerPos.x) * 0.2;

    // Jump / Gravity Physics
    if (isJumping) {
      playerPos.y += playerVelY;
      playerVelY -= 0.008;
      if (playerPos.y <= 0) { playerPos.y = 0; isJumping = false; }
    }

    playerGroup.position.set(playerPos.x, playerPos.y, playerPos.z);

    // Update Tunnel Scrolling
    tunnelSegments.forEach(seg => {
      seg.position.z += 0.28;
      if (seg.position.z > 10) seg.position.z -= 120;
    });

    // Spawn New Obstacles
    if (Math.random() < 0.03 && obstacles.length < 8) {
      spawnObstacleCluster(-40 - Math.random() * 20);
    }

    // Move & Collision Check Obstacles
    const pBox = new THREE.Box3().setFromObject(pBody);

    for (let i = obstacles.length - 1; i >= 0; i--) {
      const obs = obstacles[i];
      obs.position.z += 0.28;

      const oBox = new THREE.Box3().setFromObject(obs);
      if (pBox.intersectsBox(oBox)) {
        if (boardActive) {
          // Board protects from crash!
          boardActive = false;
          boardMesh.visible = false;
          scene.remove(obs);
          obstacles.splice(i, 1);
        } else {
          // CRASH! Caught State
          gameState = 'CAUGHT';
          chaserGroup.position.set(playerPos.x, 0, playerPos.z + 0.8);
          chaserGroup.visible = true;
          
          setTimeout(() => {
            gameState = 'GAMEOVER';
            document.getElementById('nbFinalScore').innerText = score;
            document.getElementById('nbRunCoins').innerText = coins;
            document.getElementById('nbTotalCoins').innerText = coins;
            document.getElementById('gameover-screen').classList.remove('hidden');
          }, 1200);
        }
      }

      if (obs.position.z > 10) { scene.remove(obs); obstacles.splice(i, 1); }
    }

    // Coins Collection
    for (let i = coinsList.length - 1; i >= 0; i--) {
      const c = coinsList[i];
      c.position.z += 0.28;
      c.rotation.z += 0.05;

      if (c.position.distanceTo(playerGroup.position) < 0.8) {
        coins++;
        scene.remove(c);
        coinsList.splice(i, 1);
      } else if (c.position.z > 10) {
        scene.remove(c);
        coinsList.splice(i, 1);
      }
    }
  }

  renderer.render(scene, camera);
}

animate();
</script>
</body>
</html>
"""

components.html(SUBWAY_3D_HTML, height=580)
