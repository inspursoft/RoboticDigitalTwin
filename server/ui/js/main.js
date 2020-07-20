var canvas, ctx;
var canvasWidth, canvasHeight;
var color = {
    background: "#FAEBD7",
    linelite: "#DCDCDC",
    lineWeight: "#C0C0C0"
}
var lastFrameTime = 0, deltaFrameTime = 1, fps = 0;
var rotateDegreesBottom = 0, rotateDegreesMiddle = 0, rotateDegreesHead = 0, rotateDegreesClaw = 0, scale = 1;
var ws;

document.body.onload = viewer;
function viewer() {
    init();
    lastFrameTime = Date.now();
    loop();
    getFPS();
    // animate();
}

function init() {
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    canvasWidth = canvas.width;
    canvasHeight = canvas.height;
}

function loop() {
    requestAnimFrame(loop);
    var now = Date.now();
    deltaFrameTime = now - lastFrameTime;
    lastFrameTime = now;
    ctx.resetTransform();
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    drawBackground();
    drawGird(10);
    drawArm();
}

var bottom = 0.1, middle = 0.2, head = 0.3, claw = 0.1, sc = 0.001;
function animate() {
    setInterval(() => {
        rotateDegreesBottom += bottom;
        rotateDegreesMiddle += middle;
        rotateDegreesHead += head;
        rotateDegreesClaw += claw;
        scale += sc;
        if (rotateDegreesBottom > 85 || rotateDegreesBottom < -85) {
            bottom *= -1;
        }
        if (rotateDegreesMiddle > 120 || rotateDegreesMiddle < -120) {
            middle *= -1;
        }
        if (rotateDegreesHead > 105 || rotateDegreesHead < -105) {
            head *= -1;
        }
        if (rotateDegreesClaw > 15 || rotateDegreesClaw < -5) {
            claw *= -1;
        }
        if (scale > 1.5 || scale < 0.5) {
            sc *= -1;
        }
    }, 10);
}

function drawArm() {

    ctx.transform(scale, 0, 0, -scale, 0, canvasHeight); // 设置标准坐标系，以 canve 左下角为坐标远点

    drawArmBase(225, 50);

    drawArmHead(290, 130, rotateDegreesBottom, rotateDegreesMiddle, rotateDegreesHead, rotateDegreesClaw);
    drawArmMiddle();
    drawArmBottom();

}

function drawArmBase(baseX = 0, baseY = 0) {
    ctx.save();
    ctx.translate(baseX, baseY);

    drawLineLength(0, 0, 150, 0, 8);
    drawRectangle(63, 10, 23, 38, 'black', 5);

    drawLineLength(28, 2, 50, -90, 10, 'GoldenRod');
    drawLineLength(74, 2, 50, -90, 10, 'GoldenRod');
    drawLineLength(120, 2, 50, -90, 10, 'GoldenRod');

    var grd = ctx.createLinearGradient(0, 0, 86, 0);
    grd.addColorStop(0, "black");
    grd.addColorStop(0.5, "white");
    grd.addColorStop(1, "black");
    drawRectangle(31, 52, 86, 11, grd);

    drawLineLength(20, 39, 108, undefined, 4, 'blue', 'round');
    drawLineLength(20, 54, 108, undefined, 4, 'blue', 'round');
    drawLineLength(20, 65, 108, undefined, 4, 'blue', 'round');

    drawRectangle(52, 65, 52, 32, 'SlateGray', 3);
    drawRectangle(51, 65, 54, 16, 'blue', 5);
    // drawRectangle(54, 65, 50, 32, 'SlateGray', 3);
    // drawRectangle(53, 65, 52, 16, 'blue', 5);

    drawInfo("--------- Base", 115, -55);
    ctx.restore();
}

// rotateDegrees 逆时针为正
var xScaling = 1, xScalingMin = 0.2, xMovingFast = 0, xMovingSlow = 0, xScalingDirection = 0, xMovingDirection = 0, frontDark = 1, turnRight = -1; //停止轴向旋转
// var xScaling = 1, xScalingMin = 0.2, xMovingFast = 0, xMovingSlow = 0, xScalingDirection = 1, xMovingDirection = -1, frontDark = 1, turnRight = -1;
function drawArmBottom() {
    if (xScaling <= xScalingMin || xScaling >= 1) {
        xScalingDirection = -xScalingDirection;
        xMovingDirection = -xMovingDirection;
        if (xScaling >= 1) {
            turnRight = -turnRight;
        }
        if (xScaling <= xScalingMin) {
            frontDark = -frontDark;
        }
    }
    xScaling += xScalingDirection * 0.00733;
    xMovingFast += (xMovingDirection * 0.33);
    xMovingSlow += (xMovingDirection * 0.11);

    if (frontDark == 1) {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, -xMovingSlow, 0);
        drawRectangle(-13, -12, 25, 118, 'MediumBlue', 12);
        drawFiveCircle(0, 0, 3, 3);
        drawFiveCircle(0, 92, 3, 3);
        ctx.restore();
        drawLineLength(-10 * xScaling - xMovingSlow, 50, xMovingFast + 10, undefined, 4, 'blue')
        drawRectangle(-11 * xScaling - xMovingSlow, -13, xMovingFast + 9, 30, 'SlateGray', 3);

        drawRectangle(-11 * xScaling - xMovingSlow, 80, xMovingFast + 10, 28, 'SlateGray', 3);
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, xMovingFast, 0);
        drawRectangle(-13, -12, 25, 118, 'DarkBlue', 12);
        drawFiveCircle(0, 0, 3, 3);
        drawFiveCircle(0, 92, 3, 3);
        ctx.restore();
    } else {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 24 + xMovingSlow, 0);
        drawRectangle(-13, -12, 25, 118, 'DarkBlue', 12);
        drawFiveCircle(0, 0, 3, 3);
        drawFiveCircle(0, 92, 3, 3);
        ctx.restore();
        drawLineLength(24 - xMovingFast, 50, xMovingFast + 10, undefined, 4, 'blue')
        drawRectangle(27 - xMovingFast, -13, xMovingFast + 9, 30, 'SlateGray', 3);

        drawRectangle(27 - xMovingFast, 80, xMovingFast + 10, 28, 'SlateGray', 3);
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 24 - xMovingFast, 0);
        drawRectangle(-13, -12, 25, 118, 'MediumBlue', 12);
        drawFiveCircle(0, 0, 3, 3);
        drawFiveCircle(0, 92, 3, 3);
        ctx.restore();
    }

    drawInfo("--------- Bottom", 0, -50);
}

function drawArmMiddle() {

    if (frontDark == 1) {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, -xMovingSlow, 0);
        drawRectangle(-13, 15, 25, 65, 'MediumBlue', 0);
        // drawFiveCircle(0, 26, 3, 2);
        // drawFiveCircle(0, 87, 3, 2);

        ctx.restore();
        drawRectangle(-11 * xScaling - xMovingSlow, -13, xMovingFast + 10, 55, 'SlateGray', 3);
        drawLineLength(-10 * xScaling - xMovingSlow, 40, xMovingFast + 10, undefined, 4, 'blue');
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, xMovingFast, 0);
        drawRectangle(-13, 15, 25, 83, 'DarkBlue', 12);
        drawFiveCircle(0, 26, 3, 2);
        drawFiveCircle(0, 87, 3, 2);
        ctx.restore();
    } else {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 24 + xMovingSlow, 0);
        drawRectangle(-13, 15, 25, 65, 'DarkBlue', 0);
        // drawFiveCircle(0, 26, 3, 2);
        // drawFiveCircle(0, 87, 3, 2);
        ctx.restore();
        drawRectangle(27 - xMovingFast, -13, xMovingFast + 10, 55, 'SlateGray', 3);
        drawLineLength(24 - xMovingFast, 40, xMovingFast + 10, undefined, 4, 'blue');
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 24 - xMovingFast, 0);
        drawRectangle(-13, 15, 25, 83, 'MediumBlue', 12);
        drawFiveCircle(0, 26, 3, 2);
        drawFiveCircle(0, 87, 3, 2);
        ctx.restore();
    }





    // drawRectangle(-12, 1, 22, 65, 'SlateGray', 0);
    // drawRectangle(-13, 15, 25, 83, 'MediumBlue', 12);

    // drawFiveCircle(0, 26, 3, 2);
    // drawFiveCircle(0, 87, 3, 2);

    drawInfo("--------- Middle", 0, -50);

    ctx.restore();
}

function drawArmHead(baseX = 0, baseY = 0, rotateDegreesBottom = 0, rotateDegreesMiddle = 0, rotateDegreesHead = 0, rotateDegreesClaw = 0) {
    var sin, cos;
    // for bottom
    sin = Math.sin(rotateDegreesBottom * Math.PI / 180);
    cos = Math.cos(rotateDegreesBottom * Math.PI / 180);
    // ctx.transform(cos, sin, -sin, cos, baseX, baseY);
    if (frontDark == 1) {
        ctx.transform(cos, sin, -sin, cos, baseX + xMovingFast, baseY);
    } else {
        ctx.transform(cos, sin, -sin, cos, baseX + 24 + xMovingSlow, baseY);
    }

    ctx.save();
    // for middle
    sin = Math.sin(rotateDegreesMiddle * Math.PI / 180);
    cos = Math.cos(rotateDegreesMiddle * Math.PI / 180);
    ctx.transform(cos, sin, - sin, cos, 0, 92);

    ctx.save();
    // for head
    sin = Math.sin(rotateDegreesHead * Math.PI / 180);
    cos = Math.cos(rotateDegreesHead * Math.PI / 180);
    ctx.transform(cos, sin, -sin, cos, 0, 87);


    if (frontDark == 1) {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, -xMovingSlow, 0);
        // back
        drawRectangle(-38, -8, 58, 25, 'RoyalBlue', 3);
        drawRectangle(-35, -6, 52, 19, 'black', 3);
        drawCircle(-31, -1, 4, 'SlateGray');
        drawCircle(-31, 9, 4, 'SlateGray');
        drawCircle(13, -1, 4, 'SlateGray');
        drawCircle(13, 9, 4, 'SlateGray');
        drawRectangle(-38, 22, 57, 27, 'RoyalBlue', 3);
        drawRectangle(-30, 16, 40, 40, 'black', 3);
        drawRectangle(-10, 30, 12, 35, 'black', 3);
        drawHexagon(-14, 62, 20, 'SlateGray', 8);
        // back end
        ctx.restore();

        drawRectangle(-11 * xScaling - xMovingSlow, 0, xMovingFast + 10, 60, 'black', 0);
        drawRectangle(-40 * xScaling - xMovingSlow, -8, xMovingFast + 25, 25, 'RoyalBlue', 3);
        drawRectangle(-32 * xScaling - xMovingSlow, 22, xMovingFast + 10, 27, 'RoyalBlue', 3);
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, xMovingFast / 2, 0);
        drawClaw(-4, 75, undefined, rotateDegreesClaw);
        ctx.restore();
        drawRectangle(-11 * xScaling - xMovingSlow, 60, xMovingFast + 10, 35, 'SlateGray', 3);


        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, xMovingFast, 0);
        // front
        drawRectangle(-38, -8, 58, 25, 'RoyalBlue', 3);
        drawRectangle(-35, -6, 52, 19, 'black', 3);
        drawCircle(-31, -1, 4, 'SlateGray');
        drawCircle(-31, 9, 4, 'SlateGray');
        drawCircle(13, -1, 4, 'SlateGray');
        drawCircle(13, 9, 4, 'SlateGray');
        drawRectangle(-38, 22, 57, 27, 'RoyalBlue', 3);
        drawRectangle(-30, 16, 40, 40, 'black', 3);
        drawRectangle(-10, 30, 12, 35, 'black', 3);
        // drawClaw(-4, 75, undefined, rotateDegreesClaw);
        drawHexagon(-14, 62, 20, 'SlateGray', 8);
        // front end
        ctx.restore();
    } else {
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 20 + xMovingSlow + 20 * xScaling, 0);
        // back
        drawRectangle(-38, -8, 58, 25, 'RoyalBlue', 3);
        drawRectangle(-35, -6, 52, 19, 'black', 3);
        drawCircle(-31, -1, 4, 'SlateGray');
        drawCircle(-31, 9, 4, 'SlateGray');
        drawCircle(13, -1, 4, 'SlateGray');
        drawCircle(13, 9, 4, 'SlateGray');
        drawRectangle(-38, 22, 57, 27, 'RoyalBlue', 3);
        drawRectangle(-30, 16, 40, 40, 'black', 3);
        drawRectangle(-20, 30, 12, 35, 'black', 3);
        // drawClaw(-14, 75, undefined, rotateDegreesClaw);
        drawHexagon(-24, 62, 20, 'SlateGray', 8);
        // back end
        ctx.restore();
        drawRectangle(27 - xMovingFast, 0, xMovingFast + 5, 60, 'black', 0);
        drawRectangle(27 - xMovingFast, -8, xMovingFast + 10 + 20 * xScaling, 25, 'RoyalBlue', 3);
        drawRectangle(27 - xMovingFast, 22, xMovingFast + 10 + 20 * xScaling, 27, 'RoyalBlue', 3);
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, (20 + xMovingSlow + 20 * xScaling) / 2, 0);
        drawClaw(4, 75, undefined, rotateDegreesClaw);
        ctx.restore();
        drawRectangle(24 - xMovingFast, 60, xMovingFast + 7, 35, 'SlateGray', 3);
        ctx.save();
        ctx.transform(xScaling, 0, 0, 1, 20 - xMovingFast + 20 * xScaling, 0);
        // front
        drawRectangle(-38, -8, 58, 25, 'RoyalBlue', 3);
        drawRectangle(-35, -6, 52, 19, 'black', 3);
        drawCircle(-31, -1, 4, 'SlateGray');
        drawCircle(-31, 9, 4, 'SlateGray');
        drawCircle(13, -1, 4, 'SlateGray');
        drawCircle(13, 9, 4, 'SlateGray');
        drawRectangle(-38, 22, 57, 27, 'RoyalBlue', 3);
        drawRectangle(-30, 16, 40, 40, 'black', 3);
        drawRectangle(-20, 30, 12, 35, 'black', 3);
        drawHexagon(-24, 62, 20, 'SlateGray', 8);
        // front end
        ctx.restore();
    }


    // 原本
    // drawRectangle(-38, -8, 58, 25, 'RoyalBlue', 3);
    // drawRectangle(-35, -6, 52, 19, 'black', 3);

    // drawCircle(-31, -1, 4, 'SlateGray');
    // drawCircle(-31, 9, 4, 'SlateGray');
    // drawCircle(13, -1, 4, 'SlateGray');
    // drawCircle(13, 9, 4, 'SlateGray');

    // drawRectangle(-38, 22, 57, 27, 'RoyalBlue', 3);
    // drawRectangle(-30, 16, 40, 40, 'black', 3);

    // drawRectangle(-10, 30, 12, 35, 'black', 3);

    // drawClaw(-4, 75, undefined, rotateDegreesClaw);
    // drawHexagon(-14, 62, 20, 'SlateGray', 8);

    drawInfo("--------- Claw", 0, -70);
    drawInfo("--------- Head", 0, -30);
    ctx.restore();

}

function drawClaw(startX, startY, fillcolor = 'black', rotateDegrees = 0, scale = 1) {
    drawClawRight(startX, startY, fillcolor, rotateDegrees, scale);
    drawClawRight(startX, startY, fillcolor, rotateDegrees, scale, true);

    // drawInfo("--------- Claw", 0, -70);
}


function drawFiveCircle(centerX, centerY, centerRadius, edgeRadius, centerColor = 'LightGrey', edgeColor = 'white', space = 1) {
    drawCircle(centerX, centerY, centerRadius, centerColor);
    drawCircle(centerX, centerY - centerRadius - edgeRadius - space, edgeRadius, edgeColor);
    drawCircle(centerX, centerY + centerRadius + edgeRadius + space, edgeRadius, edgeColor);
    drawCircle(centerX - centerRadius - edgeRadius - space, centerY, edgeRadius, edgeColor);
    drawCircle(centerX + centerRadius + edgeRadius + space, centerY, edgeRadius, edgeColor);
}


function drawBackground() {
    ctx.save();
    roundedRect(0, 0, canvasWidth, canvasHeight, color.background);
    ctx.restore();
}



function getFPS(space = 100) {
    space = space < 100 ? 100 : space
    setInterval(() => {
        fps = (1000 / deltaFrameTime).toFixed(1);
    }, space);
}


