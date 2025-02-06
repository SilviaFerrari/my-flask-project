// DESIGN FOR CANVAS //

document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('myCanvas');
    const ctx = canvas.getContext('2d');

    // Corpo della casetta
    ctx.fillStyle = 'burlywood';
    ctx.fillRect(100, 150, 200, 200);  // x, y, larghezza, altezza

    // Tetto
    ctx.fillStyle = 'saddlebrown';
    ctx.beginPath();
    ctx.moveTo(90, 150);   // Punto sinistro del tetto
    ctx.lineTo(200, 50);   // Punta superiore
    ctx.lineTo(310, 150);  // Punto destro del tetto
    ctx.closePath();
    ctx.fill();

    // Porta
    ctx.fillStyle = 'peru';
    ctx.fillRect(180, 250, 40, 100);

    // Finestra
    ctx.fillStyle = 'skyblue';
    ctx.fillRect(130, 180, 40, 40);
    ctx.fillRect(230, 180, 40, 40);

    // Sole
    ctx.beginPath();
    ctx.arc(50, 50, 30, 0, 2 * Math.PI);
    ctx.fillStyle = "#f1c40f";
    ctx.fill();
})
