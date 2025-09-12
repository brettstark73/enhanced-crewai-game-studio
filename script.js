class PixelSnakeGame {
    constructor() {
        this.canvas = document.getElementById('game-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.gridSize = 20;
        this.tileCount = this.canvas.width / this.gridSize;
        
        // Game state
        this.snake = [{ x: 10, y: 10 }];
        this.food = { x: 15, y: 15 };
        this.direction = { x: 0, y: 0 };
        this.score = 0;
        this.level = 1;
        this.gameRunning = false;
        this.gamePaused = false;
        this.gameLoop = null;
        
        // Difficulty settings
        this.difficulties = {
            easy: { speed: 200, scoreMultiplier: 1 },
            medium: { speed: 150, scoreMultiplier: 1.5 },
            hard: { speed: 100, scoreMultiplier: 2 }
        };
        this.currentDifficulty = 'medium';
        
        // Local storage for high score
        this.highScore = localStorage.getItem('pixelSnakeHighScore') || 0;
        
        this.initializeGame();
    }
    
    initializeGame() {
        this.updateDisplay();
        this.bindEvents();
        this.showScreen('start-screen');
    }
    
    bindEvents() {
        // Button events
        document.getElementById('start-btn').addEventListener('click', () => this.startGame());
        document.getElementById('pause-btn').addEventListener('click', () => this.pauseGame());
        document.getElementById('resume-btn').addEventListener('click', () => this.resumeGame());
        document.getElementById('restart-btn').addEventListener('click', () => this.restartGame());
        document.getElementById('main-menu-btn').addEventListener('click', () => this.showMainMenu());
        document.getElementById('play-again-btn').addEventListener('click', () => this.startGame());
        document.getElementById('menu-btn').addEventListener('click', () => this.showMainMenu());
        
        // Difficulty selector
        document.getElementById('difficulty').addEventListener('change', (e) => {
            this.currentDifficulty = e.target.value;
        });
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Touch controls for mobile
        this.addTouchControls();
    }
    
    addTouchControls() {
        let touchStartX = 0;
        let touchStartY = 0;
        
        this.canvas.addEventListener('touchstart', (e) => {
            e.preventDefault();
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        });
        
        this.canvas.addEventListener('touchend', (e) => {
            e.preventDefault();
            if (!this.gameRunning || this.gamePaused) return;
            
            const touchEndX = e.changedTouches[0].clientX;
            const touchEndY = e.changedTouches[0].clientY;
            
            const deltaX = touchEndX - touchStartX;
            const deltaY = touchEndY - touchStartY;
            
            if (Math.abs(deltaX) > Math.abs(deltaY)) {
                // Horizontal swipe
                if (deltaX > 30 && this.direction.x === 0) {
                    this.direction = { x: 1, y: 0 }; // Right
                } else if (deltaX < -30 && this.direction.x === 0) {
                    this.direction = { x: -1, y: 0 }; // Left
                }
            } else {
                // Vertical swipe
                if (deltaY > 30 && this.direction.y === 0) {
                    this.direction = { x: 0, y: 1 }; // Down
                } else if (deltaY < -30 && this.direction.y === 0) {
                    this.direction = { x: 0, y: -1 }; // Up
                }
            }
        });
    }
    
    handleKeyPress(e) {
        if (!this.gameRunning) return;
        
        // Pause/resume
        if (e.code === 'Space') {
            e.preventDefault();
            if (this.gamePaused) {
                this.resumeGame();
            } else {
                this.pauseGame();
            }
            return;
        }
        
        if (this.gamePaused) return;
        
        // Movement controls
        switch (e.code) {
            case 'ArrowUp':
            case 'KeyW':
                if (this.direction.y === 0) {
                    this.direction = { x: 0, y: -1 };
                }
                break;
            case 'ArrowDown':
            case 'KeyS':
                if (this.direction.y === 0) {
                    this.direction = { x: 0, y: 1 };
                }
                break;
            case 'ArrowLeft':
            case 'KeyA':
                if (this.direction.x === 0) {
                    this.direction = { x: -1, y: 0 };
                }
                break;
            case 'ArrowRight':
            case 'KeyD':
                if (this.direction.x === 0) {
                    this.direction = { x: 1, y: 0 };
                }
                break;
        }
    }
    
    startGame() {
        this.resetGame();
        this.gameRunning = true;
        this.gamePaused = false;
        this.showScreen('game-area');
        this.generateFood();
        this.gameLoop = setInterval(() => this.update(), this.difficulties[this.currentDifficulty].speed);
        this.draw();
    }
    
    pauseGame() {
        if (!this.gameRunning) return;
        this.gamePaused = true;
        clearInterval(this.gameLoop);
        this.showScreen('pause-screen');
    }
    
    resumeGame() {
        if (!this.gameRunning || !this.gamePaused) return;
        this.gamePaused = false;
        this.showScreen('game-area');
        this.gameLoop = setInterval(() => this.update(), this.difficulties[this.currentDifficulty].speed);
    }
    
    restartGame() {
        this.endGame();
        this.startGame();
    }
    
    showMainMenu() {
        this.endGame();
        this.showScreen('start-screen');
    }
    
    endGame() {
        this.gameRunning = false;
        this.gamePaused = false;
        clearInterval(this.gameLoop);
    }
    
    resetGame() {
        this.snake = [{ x: 10, y: 10 }];
        this.direction = { x: 0, y: 0 };
        this.score = 0;
        this.level = 1;
        this.updateDisplay();
    }
    
    update() {
        if (!this.gameRunning || this.gamePaused) return;
        
        // Move snake
        const head = { x: this.snake[0].x + this.direction.x, y: this.snake[0].y + this.direction.y };
        
        // Check wall collisions
        if (head.x < 0 || head.x >= this.tileCount || head.y < 0 || head.y >= this.tileCount) {
            this.gameOver();
            return;
        }
        
        // Check self collision
        if (this.snake.some(segment => segment.x === head.x && segment.y === head.y)) {
            this.gameOver();
            return;
        }
        
        this.snake.unshift(head);
        
        // Check food collision
        if (head.x === this.food.x && head.y === this.food.y) {
            this.eatFood();
            this.generateFood();
        } else {
            this.snake.pop();
        }
        
        this.draw();
    }
    
    eatFood() {
        const basePoints = 10;
        const points = Math.floor(basePoints * this.difficulties[this.currentDifficulty].scoreMultiplier);
        this.score += points;
        
        // Increase level every 100 points
        this.level = Math.floor(this.score / 100) + 1;
        
        this.updateDisplay();
    }
    
    generateFood() {
        do {
            this.food = {
                x: Math.floor(Math.random() * this.tileCount),
                y: Math.floor(Math.random() * this.tileCount)
            };
        } while (this.snake.some(segment => segment.x === this.food.x && segment.y === this.food.y));
    }
    
    draw() {
        // Clear canvas
        this.ctx.fillStyle = '#111';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw snake
        this.snake.forEach((segment, index) => {
            if (index === 0) {
                // Snake head
                this.ctx.fillStyle = '#4ecdc4';
                this.ctx.fillRect(segment.x * this.gridSize, segment.y * this.gridSize, this.gridSize, this.gridSize);
                
                // Add eyes to head
                this.ctx.fillStyle = '#fff';
                const eyeSize = 3;
                const eyeOffset = 5;
                this.ctx.fillRect(segment.x * this.gridSize + eyeOffset, segment.y * this.gridSize + eyeOffset, eyeSize, eyeSize);
                this.ctx.fillRect(segment.x * this.gridSize + this.gridSize - eyeOffset - eyeSize, segment.y * this.gridSize + eyeOffset, eyeSize, eyeSize);
            } else {
                // Snake body
                this.ctx.fillStyle = index % 2 === 1 ? '#45b7aa' : '#3a9d91';
                this.ctx.fillRect(segment.x * this.gridSize + 1, segment.y * this.gridSize + 1, this.gridSize - 2, this.gridSize - 2);
            }
        });
        
        // Draw food
        this.ctx.fillStyle = '#ff6b6b';
        this.ctx.fillRect(this.food.x * this.gridSize, this.food.y * this.gridSize, this.gridSize, this.gridSize);
        
        // Add food highlight
        this.ctx.fillStyle = '#ff8e8e';
        this.ctx.fillRect(this.food.x * this.gridSize + 2, this.food.y * this.gridSize + 2, this.gridSize - 4, this.gridSize - 4);
    }
    
    gameOver() {
        this.endGame();
        
        // Check for high score
        let isNewHighScore = false;
        if (this.score > this.highScore) {
            this.highScore = this.score;
            localStorage.setItem('pixelSnakeHighScore', this.highScore);
            isNewHighScore = true;
        }
        
        // Update final score display
        document.getElementById('final-score').textContent = this.score;
        const newHighScoreElement = document.getElementById('new-high-score');
        if (isNewHighScore) {
            newHighScoreElement.classList.remove('hidden');
        } else {
            newHighScoreElement.classList.add('hidden');
        }
        
        this.updateDisplay();
        this.showScreen('game-over-screen');
    }
    
    updateDisplay() {
        document.getElementById('score').textContent = this.score;
        document.getElementById('high-score').textContent = this.highScore;
        document.getElementById('level').textContent = this.level;
    }
    
    showScreen(screenId) {
        // Hide all screens
        document.querySelectorAll('.screen').forEach(screen => {
            screen.classList.add('hidden');
        });
        
        // Show selected screen
        document.getElementById(screenId).classList.remove('hidden');
    }
}

// Initialize game when page loads
document.addEventListener('DOMContentLoaded', () => {
    new PixelSnakeGame();
});