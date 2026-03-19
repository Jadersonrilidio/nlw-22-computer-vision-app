const v = document.getElementById('v');
const c = document.getElementById('c');
const ctx = c.getContext('2d');
const capC = document.createElement('canvas'); // Offscreen canvas
capC.width = 640;
capC.height = 480;
const capCtx = capC.getContext('2d');

const ws = new WebSocket('ws://' + window.location.host + '/ws');

navigator.mediaDevices.getUserMedia({video:true}).then(s => v.srcObject = s);

ws.onmessage = e => {
    const img = new Image();
    img.onload = () => ctx.drawImage(img, 0, 0);
    img.src = e.data;
};

setInterval(() => {
    if (ws.readyState === 1) {
        capCtx.drawImage(v, 0, 0, capC.width, capC.height);
        ws.send(JSON.stringify({"image": capC.toDataURL('image/jpeg', 0.5)}));
    }
}, 100);
