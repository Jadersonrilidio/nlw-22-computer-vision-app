const gestureImages = {};
const gestures = ['coracao', 'hangloose', 'joinha', 'ola', 'paz', 'rock', 'spock'];

gestures.forEach(g => {
    const img = new Image();
    img.src = `/assets/images/gestures/${g}.png`;
    img.className = 'pulse-img';
    img.setAttribute('data-gesture', g);
    gestureImages[g] = img;
});

const v = document.getElementById('v');
const c = document.getElementById('c');
const ctx = c.getContext('2d');
const capC = document.createElement('canvas');
capC.width = 640;
capC.height = 480;
const capCtx = capC.getContext('2d');

const ws = new WebSocket('ws://' + window.location.host + '/ws');

ws.onopen = () => console.log('WebSocket connected');
ws.onerror = e => console.error('WebSocket error:', e);
ws.onclose = () => console.log('WebSocket closed');

navigator.mediaDevices.getUserMedia({ video: true }).then(s => {
    v.srcObject = s;
    v.onloadedmetadata = () => {
        v.play();
        console.log('Webcam video playing');
    };
});

ws.onmessage = e => {
    let data;
    try {
        data = JSON.parse(e.data);
    } catch (err) {
        return;
    }

    const img = new Image();
    img.onload = () => {
        ctx.drawImage(img, 0, 0);
    };
    img.src = data.image;

    if (data.fps !== undefined) {
        const fpsEl = document.getElementById('fps');
        if (fpsEl) fpsEl.innerText = `${data.fps} FPS`;
    }

    const gDiv = document.getElementById('gestures');
    if (gDiv) {
        const hands = ['Left', 'Right'];
        gDiv.innerHTML = hands.map(hand => {
            const handData = data.gestures.find(g => g.hand === hand);
            const handClass = handData ? '' : 'dimmed';
            const nameClass = handData ? '' : 'italic';
            return `
                <div class="gesture-badge ${handClass}">
                    <span class="badge-hand">${hand}</span>
                    <span class="badge-name ${nameClass}">
                        ${handData ? handData.gesture : 'detecting...'}
                    </span>
                    <span class="badge-score">
                        ${handData ? (handData.score * 100).toFixed(0) + '%' : '--'}
                    </span>
                </div>`;
        }).join('');
    }

    const matchContainer = document.getElementById('match-container');
    if (matchContainer) {
        if (data.match) {
            const preLoadedImg = gestureImages[data.match];
            if (preLoadedImg && !matchContainer.contains(preLoadedImg)) {
                matchContainer.innerHTML = '';
                matchContainer.appendChild(preLoadedImg);
            }
        } else {
            if (!matchContainer.querySelector('.placeholder-text')) {
                matchContainer.innerHTML = '<div class="placeholder-text">Waiting for match</div>';
            }
        }
    }
};

const initialHands = ['Left', 'Right'];
const gesturesEl = document.getElementById('gestures');
if (gesturesEl) {
    gesturesEl.innerHTML = initialHands.map(hand => `
        <div class="gesture-badge dimmed">
            <span class="badge-hand">${hand}</span>
            <span class="badge-name italic">detecting...</span>
            <span class="badge-score">--</span>
        </div>`).join('');
}
const matchContainerEl = document.getElementById('match-container');
if (matchContainerEl) matchContainerEl.innerHTML = '<div class="placeholder-text">Waiting for match</div>';

setInterval(() => {
    if (ws.readyState === 1 && v.videoWidth > 0) {
        const qualityEl = document.getElementById('quality');
        const q = qualityEl ? parseFloat(qualityEl.value) : 0.5;
        const showLandmarksEl = document.getElementById('show_landmarks');
        const drawLandmarks = showLandmarksEl ? showLandmarksEl.checked : true;

        capCtx.drawImage(v, 0, 0, capC.width, capC.height);
        ws.send(JSON.stringify({
            "image": capC.toDataURL('image/jpeg', q),
            "show_landmarks": drawLandmarks
        }));
    }
}, 100);
