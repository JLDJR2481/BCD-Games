document.getElementById('startButton').addEventListener('click', main);

window.addEventListener('keydown', function (event) {
    switch (event.key) {
        case 'ArrowLeft':
            if (direction != "RIGHT")
                direction = "LEFT";
            break;
        case 'ArrowUp':
            if (direction != "DOWN")
                direction = "UP";
            break;
        case 'ArrowRight':
            if (direction != "LEFT")
                direction = "RIGHT";
            break;
        case 'ArrowDown':
            if (direction != "UP")
                direction = "DOWN";
            break;
    }
});

document.getElementById("retryButton").addEventListener('click', function () {
    location.reload();
});

window.addEventListener('keydown', function (event) {
    if (directionChanged) return; // Ignora las pulsaciones de teclas adicionales hasta que se actualice la posición de la serpiente

    switch (event.key) {
        case 'ArrowLeft':
            if (direction != "RIGHT") {
                nextDirection = "LEFT";
                directionChanged = true;
            }
            break;
        case 'ArrowUp':
            if (direction != "DOWN") {
                nextDirection = "UP";
                directionChanged = true;
            }
            break;
        case 'ArrowRight':
            if (direction != "LEFT") {
                nextDirection = "RIGHT";
                directionChanged = true;
            }
            break;
        case 'ArrowDown':
            if (direction != "UP") {
                nextDirection = "DOWN";
                directionChanged = true;
            }
            break;
    }
});

var box = 20;

var snake = [{
    x: 2 * box,
    y: 10 * box
},
{
    x: 1 * box,
    y: 10 * box
}];

var food = {
    x: Math.floor(Math.random() * 20) * box,
    y: Math.floor(Math.random() * 20) * box
};

var canvas = document.getElementById("gameCanvas");
var ctx = canvas.getContext("2d");
var score = 0;
var game;

var direction = "RIGHT";
var nextDirection = "RIGHT";
var directionChanged = false;

var isGameOver = false;



// Función que printa la serpiente
function drawSnake() {
    for (var i = 0; i < snake.length; i++) {
        ctx.fillStyle = (i == 0) ? "yellow" : "green";
        ctx.fillRect(snake[i].x, snake[i].y, box, box);
    }
}

function drawFood() {
    ctx.fillStyle = "red";
    ctx.fillRect(food.x, food.y, box, box);

}

function checkCollision(head, array) {
    for (let i = 1; i < array.length; i++) {
        if (head.x == array[i].x && head.y == array[i].y) {
            return true;
        }
    }
    return false;
}

function updateSnakePosition() {
    direction = nextDirection;
    directionChanged = false;

    var snakeX = snake[0].x;
    var snakeY = snake[0].y;

    if (direction == "RIGHT") snakeX += box;
    if (direction == "LEFT") snakeX -= box;
    if (direction == "UP") snakeY -= box;
    if (direction == "DOWN") snakeY += box;

    var newHead = {
        x: snakeX,
        y: snakeY
    };

    if (snakeX < 0 || snakeX >= 20 * box || snakeY < 0 || snakeY >= 20 * box || checkCollision(newHead, snake)) {
        clearInterval(game);
        isGameOver = true;
    }

    snake.unshift(newHead);
}

function checkFoodCollision() {
    if (snake[0].x == food.x && snake[0].y == food.y) {
        food = {
            x: Math.floor(Math.random() * 20) * box,
            y: Math.floor(Math.random() * 20) * box
        };
        score++;
        document.getElementById('scoreInGame').innerHTML = "Puntuación: " + score;
    } else {
        snake.pop();
    }

}

function draw() {
    ctx.fillStyle = "black";
    ctx.fillRect(0, 0, 20 * box, 20 * box);

    drawSnake();
    drawFood();

    updateSnakePosition();
    checkFoodCollision();
}


var lastFrameTimeMs = 0;
var maxFPS = 10;

function main(timestamp) {
    document.getElementById('startButton').style.display = 'none';
    document.getElementById("instructions").style.display = "none";
    document.getElementById("scoreInGame").style.display = "";
    if (timestamp < lastFrameTimeMs + (1000 / maxFPS)) {
        window.requestAnimationFrame(main);
        return;
    }
    lastFrameTimeMs = timestamp;

    draw();
    if (!isGameOver) {
        window.requestAnimationFrame(main);
    } else {
        canvas.style.display = "none";
        document.getElementById("scoreInGame").style.display = "none";
        document.getElementById("scoreGameOver").innerHTML = "Puntuación: " + score;
        var gameOverScreen = document.getElementById("gameOverScreen");
        gameOverScreen.style.display = "flex";
        gameOverScreen.style.flexDirection = "column";
        gameOverScreen.style.justifyContent = "center";
        gameOverScreen.style.alignItems = "center";

        document.getElementById("highScores").style.display = "";

        postScore();

    }
}

