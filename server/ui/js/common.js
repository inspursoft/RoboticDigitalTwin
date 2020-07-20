
window.requestAnimFrame = (function () {
    return window.requestAnimationFrame ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame ||
        window.oRequestAnimationFrame ||
        window.msRequestAnimationFrame ||
        function (/* function */ callback, /* DOMElement */ element) {
            window.setTimeout(callback, 1000 / 60);
        };
})();


function drawClawRight(startX, startY, fillcolor = 'black', rotateDegrees = 0, scale = 1, reverse = false) {
    ctx.save();
    var sin = Math.sin(rotateDegrees * Math.PI / 180);
    var cos = Math.cos(rotateDegrees * Math.PI / 180);
    ctx.translate(startX, startY);

    if (reverse) {
        ctx.transform(-1, 0, 0, 1, 0, 0);
    }
    ctx.transform(cos, sin, -sin, cos, 0, 0);


    ctx.fillStyle = fillcolor;
    ctx.beginPath();

    var x1 = 15 * scale;
    var x2 = 21 * scale;
    var x3 = 30 * scale;

    var y1 = 9 * scale;
    var y2 = 40 * scale;
    var y3 = 46 * scale;
    var y4 = 53 * scale;

    ctx.moveTo(0, 0);
    ctx.lineTo(x3, y2);
    ctx.lineTo(x1, y4);
    ctx.lineTo(x1, y3);
    ctx.lineTo(x2, y2);
    ctx.lineTo(0, y1);

    ctx.closePath();
    ctx.fill();
    ctx.restore();
}

function drawHexagon(startX, startY, length, fillcolor = 'black', radius = 0, rotateDegrees = 0) {
    ctx.save();
    var sin = Math.sin(rotateDegrees * Math.PI / 180);
    var cos = Math.cos(rotateDegrees * Math.PI / 180);
    ctx.translate(startX, startY);
    ctx.transform(cos, sin, -sin, cos, 0, 0);

    ctx.fillStyle = fillcolor;
    ctx.beginPath();

    var sin60 = Math.sin(60 * Math.PI / 180);
    var x4 = radius * Math.tan(30 * Math.PI / 180);
    var x5 = length - x4;
    var x0 = -length / 2;
    var x1 = - x5 / 2;
    var x2 = -x4 / 2;
    var x3 = 0;
    var x6 = length;
    var x7 = length - x2;
    var x8 = length - x1;
    var x9 = length - x0;

    var y0 = 0;
    var y1 = x4 * sin60;
    var y2 = x5 * sin60;
    var y3 = length * sin60;
    var y4 = y2 + radius;
    var y5 = y3 * 2 - y1;
    var y6 = y3 * 2;

    ctx.moveTo(x4, y0);
    ctx.lineTo(x5, y0);
    ctx.arcTo(x6, y0, x7, y1, radius);

    ctx.lineTo(x8, y2);
    ctx.arcTo(x9, y3, x8, y4, radius);

    ctx.lineTo(x7, y5);
    ctx.arcTo(x6, y6, x5, y6, radius);

    ctx.lineTo(x4, y6);
    ctx.arcTo(x3, y6, x2, y5, radius);

    ctx.lineTo(x1, y4);
    ctx.arcTo(x0, y3, x1, y2, radius);

    ctx.lineTo(x2, y1);
    ctx.arcTo(x3, y0, x4, y0, radius);

    ctx.closePath();
    ctx.fill();
    ctx.resetTransform();
    ctx.restore();
}

function drawCircle(centerX, centerY, radius, color = 'black') {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fill();
}

// style = butt | round | square
function drawLine(startX, startY, endX, endY, lineWidth = 1, color = "black", style = 'butt') {
    ctx.beginPath();
    ctx.lineWidth = lineWidth;
    ctx.strokeStyle = color;
    ctx.lineCap = style;
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
    ctx.lineWeight = 1;
}

function drawLineLength(startX, startY, length, rotateDegrees = 0, lineWidth = 1, color = "black", style = 'butt', scale = 1) {
    var endX = startX + length * Math.cos(rotateDegrees * Math.PI / 180) * scale;
    var endY = startY - length * Math.sin(rotateDegrees * Math.PI / 180) * scale;
    drawLine(startX, startY, endX, endY, lineWidth * scale, color, style);
}


function drawGird(space = 5) {
    ctx.save();
    space = Math.floor(space);
    space = 5 > space ? 5 : space;
    for (var i = space; i < canvasWidth; i = i + space) {
        chooseLine(i, space);
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvasHeight);
        ctx.stroke();
        ctx.beginPath(); // 必须的，表明从新开始一个新任务
    }
    for (var i = space; i < canvasHeight; i = i + space) {
        chooseLine(i, space);
        ctx.moveTo(0, i);
        ctx.lineTo(canvasWidth, i);
        ctx.stroke();
        ctx.beginPath(); // 必须的，表明从新开始一个新任务
    }
    ctx.fillStyle = 'green';
    ctx.font = "18px Arial";
    ctx.fillText(fps + "fps", 20, 20);
    ctx.restore();
}

function chooseLine(current, space) {
    if (current % (space * 5) === 0) {
        ctx.strokeStyle = color.lineWeight;
        ctx.lineWidth = 2;
    } else {
        ctx.strokeStyle = color.linelite;
        ctx.lineWidth = 1;
    }
}

//圆角矩形画法
function roundedRect(startX, startY, width, height, fillcolor = 'black', radius = 0, rotateDegrees = 0, scale = 1) {
    var sin = Math.sin(rotateDegrees * Math.PI / 180);
    var cos = Math.cos(rotateDegrees * Math.PI / 180);
    ctx.transform(scale * cos, scale * sin, scale * (-sin), scale * cos, startX, startY);

    ctx.fillStyle = fillcolor;
    ctx.beginPath();

    ctx.moveTo(radius, 0);

    // top right
    ctx.lineTo(width - radius, 0);
    ctx.arcTo(width, 0, width, radius, radius);
    ctx.lineTo(width, radius);

    // down right
    ctx.lineTo(width, height - radius);
    ctx.arcTo(width, height, width - radius, height, radius);
    ctx.lineTo(width - radius, height);

    // down left
    ctx.lineTo(radius, height);
    ctx.arcTo(0, height, 0, height - radius, radius);
    ctx.lineTo(0, height - radius);

    // top left
    ctx.lineTo(0, radius);
    ctx.arcTo(0, 0, radius, 0, radius);
    ctx.lineTo(radius, 0);
    ctx.fill();

    ctx.resetTransform();
}

function drawRectangle(startX, startY, width, height, fillcolor = 'black', radius = 0) {
    ctx.fillStyle = fillcolor;
    ctx.beginPath();
    ctx.translate(startX, startY);

    ctx.moveTo(radius, 0);

    // top right
    ctx.lineTo(width - radius, 0);
    ctx.arcTo(width, 0, width, radius, radius);

    // down right
    ctx.lineTo(width, height - radius);
    ctx.arcTo(width, height, width - radius, height, radius);

    // down left
    ctx.lineTo(radius, height);
    ctx.arcTo(0, height, 0, height - radius, radius);

    // top left
    ctx.lineTo(0, radius);
    ctx.arcTo(0, 0, radius, 0, radius);
    ctx.closePath();
    ctx.fill();

    ctx.translate(-startX, -startY);
}

function drawInfo(text = '', x = 0, y = 0,color = 'red', font = '18px Arial') {
    ctx.save();
    ctx.transform(1, 0, 0, -1, 0, 0);
    ctx.fillStyle = color;
    ctx.font = font;
    ctx.fillText(text, x, y);
    ctx.restore();
}