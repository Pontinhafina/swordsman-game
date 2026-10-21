// Main Game Engine & Loop with 5-Stage Campaign, Hero Upgrades & Boss Fight

class Game {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');

        this.viewWidth = 480;
        this.viewHeight = 270;
        this.canvas.width = this.viewWidth;
        this.canvas.height = this.viewHeight;
        this.ctx.imageSmoothingEnabled = false;

        this.cameraX = 0;
        this.cameraY = 0;

        this.input = {
            left: false,
            right: false,
            up: false,
            down: false,
            jump: false,
            jumpPressed: false,
            attackPressed: false,
            interactPressed: false
        };

        // Campaign States
        this.currentStage = 1;
        this.totalStages = 5;
        this.state = 'loading'; // loading, title, playing, paused, stage_clear, victory, gameover

        this.score = 0;
        this.coinsCount = 0;
        this.startTime = 0;
        this.endTime = 0;
        this.savedHeroLevel = 1;

        // Entities
        this.level = null;
        this.player = null;
        this.enemies = [];
        this.coins = [];
        this.chests = [];
        this.keyItem = null;
        this.runeGate = null;
        this.goal = null;
        this.boss = null;

        this.lastTime = 0;
        this.bgmEnabled = false;

        this.stageTitles = [
            '',
            'FASE 1: A FLORESTA DOS ORCS',
            'FASE 2: AS RUÍNAS DO ENTARDECER',
            'FASE 3: O DESFILADEIRO DOS SALGUEIROS',
            'FASE 4: O PÂNTANO NOTURNO',
            'FASE 5: A FORTALEZA DO GENERAL ORC',
            'FASE PERSONALIZADA (CRIADA POR VOCÊ)'
        ];

        this.isCustomStage = false;
        this.customStageData = null;

        this.initInput();
    }

    start() {
        window.gameInstance = this;

        window.sprites.loadAll(
            (progress) => {
                this.renderLoading(progress);
            },
            () => {
                this.editor = new LevelEditor(this);
                this.state = 'title';
                requestAnimationFrame(this.loop.bind(this));
            }
        );
    }

    loadCustomCreatedStage(data) {
        this.isCustomStage = true;
        this.customStageData = data;
        this.currentStage = 6; // Custom stage title index

        this.level = new Level(1);
        this.level.loadFromCustomData(data);

        const spawn = data.entities.playerSpawn || { x: 64, y: 11 * 32 - 26 };
        this.player = new Player(spawn.x, spawn.y);
        this.player.heroLevel = this.savedHeroLevel;

        // Enemies
        this.enemies = (data.entities.orcs || []).map(o => new OrcEnemy(o.x, o.y, 60, o.type || 'orc1'));
        this.boss = this.enemies.find(e => e.isBoss) || null;

        // Coins
        this.coins = (data.entities.coins || []).map(c => new Coin(c.x, c.y));

        // Chests
        this.chests = (data.entities.chests || []).map(ch => new Chest(ch.x, ch.y, !!ch.grantsUpgrade));

        // Key & Gate
        this.keyItem = data.entities.key ? new KeyItem(data.entities.key.x, data.entities.key.y) : null;
        this.runeGate = data.entities.runeGate ? new RuneGate(data.entities.runeGate.x, data.entities.runeGate.y) : null;

        // Goal
        const goalPos = data.entities.goal || { x: 102 * 32, y: 10 * 32 - 48 };
        this.goal = new GoalFlag(goalPos.x, goalPos.y);

        this.cameraX = 0;
        this.cameraY = 0;
        this.score = 0;
        this.coinsCount = 0;
        this.startTime = Date.now();
        window.particles.clear();
        window.particles.addText(this.player.x + 8, this.player.y - 20, 'MODO TESTE DA SUA FASE!', '#4ecca3');

        this.state = 'playing';
        if (!window.sound.bgmPlaying) {
            window.sound.startBgm();
            this.bgmEnabled = true;
        }
    }

    initStage(stageNum) {
        this.isCustomStage = false;
        this.currentStage = stageNum;
        this.level = new Level(stageNum);

        // Player starting location & level carry-over
        const startY = (stageNum === 3 || stageNum === 5) ? 10 * 32 - 26 : 11 * 32 - 26;
        this.player = new Player(64, startY);
        this.player.heroLevel = this.savedHeroLevel;

        this.enemies = [];
        this.coins = [];
        this.chests = [];
        this.keyItem = null;
        this.runeGate = null;
        this.goal = null;
        this.boss = null;

        window.particles.clear();
        this.cameraX = 0;
        this.cameraY = 0;

        if (stageNum === 1) {
            // ================= FASE 1: A FLORESTA DOS ORCS =================
            this.enemies = [
                new OrcEnemy(13 * 32, 11 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(25 * 32, 9 * 32 - 28, 80, 'orc1'),
                new OrcEnemy(56 * 32, 10 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(83 * 32, 8 * 32 - 28, 70, 'orc1'),
                new OrcEnemy(90 * 32, 8 * 32 - 28, 60, 'orc1')
            ];

            this.coins = [
                new Coin(6 * 32, 10 * 32), new Coin(7 * 32, 10 * 32), new Coin(8 * 32, 10 * 32),
                new Coin(22 * 32, 8 * 32), new Coin(23 * 32, 8 * 32),
                new Coin(33 * 32, 7 * 32), new Coin(34 * 32, 7 * 32),
                new Coin(45 * 32, 5 * 32), new Coin(46 * 32, 5 * 32),
                new Coin(54 * 32, 9 * 32),
                new Coin(63 * 32, 8 * 32), new Coin(64 * 32, 7.5 * 32), new Coin(65 * 32, 7.5 * 32), new Coin(66 * 32, 8 * 32),
                new Coin(81 * 32, 7 * 32), new Coin(82 * 32, 7 * 32),
                new Coin(98 * 32, 9 * 32), new Coin(99 * 32, 9 * 32)
            ];

            this.chests = [
                new Chest(47 * 32, 6 * 32 - 24, true), // Grants Level 2 Iron Upgrade!
                new Chest(88 * 32, 8 * 32 - 24, false)
            ];

            this.goal = new GoalFlag(103 * 32, 10 * 32 - 48);

        } else if (stageNum === 2) {
            // ================= FASE 2: AS RUÍNAS DO ENTARDECER =================
            this.enemies = [
                new OrcEnemy(18 * 32, 8 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(28 * 32, 6 * 32 - 28, 50, 'orc2'),
                new OrcEnemy(47 * 32, 8 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(73 * 32, 10 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(85 * 32, 8 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(91 * 32, 8 * 32 - 28, 60, 'orc2')
            ];

            // Golden Key atop High Tower
            this.keyItem = new KeyItem(38 * 32, 3 * 32 - 16);
            // Rune Gate locks path before flag
            this.runeGate = new RuneGate(97 * 32, 9 * 32 - 24);

            this.coins = [
                new Coin(14 * 32, 8 * 32), new Coin(24 * 32, 6 * 32),
                new Coin(36 * 32, 3 * 32), new Coin(39 * 32, 3 * 32),
                new Coin(47 * 32, 7 * 32), new Coin(48 * 32, 7 * 32),
                new Coin(57 * 32, 9 * 32), new Coin(61 * 32, 8 * 32), new Coin(66 * 32, 9 * 32),
                new Coin(72 * 32, 9 * 32), new Coin(86 * 32, 7 * 32),
                new Coin(102 * 32, 8 * 32), new Coin(103 * 32, 8 * 32)
            ];

            this.chests = [
                new Chest(30 * 32, 6 * 32 - 24, true), // Grants Level 3 Golden Knight Upgrade!
                new Chest(89 * 32, 8 * 32 - 24, false)
            ];

            this.goal = new GoalFlag(104 * 32, 9 * 32 - 48);

        } else if (stageNum === 3) {
            // ================= FASE 3: O DESFILADEIRO DOS SALGUEIROS =================
            this.enemies = [
                new OrcEnemy(10 * 32, 10 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(42 * 32, 8 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(56 * 32, 9 * 32 - 28, 80, 'orc2'),
                new OrcEnemy(79 * 32, 8 * 32 - 28, 60, 'orc1'),
                new OrcEnemy(90 * 32, 7 * 32 - 28, 60, 'orc2'),
                new OrcEnemy(101 * 32, 9 * 32 - 28, 50, 'orc2')
            ];

            this.coins = [
                new Coin(8 * 32, 9 * 32), new Coin(14 * 32, 7 * 32),
                new Coin(19 * 32, 6 * 32), new Coin(23 * 32, 5 * 32),
                new Coin(29 * 32, 4 * 32), // Coins above the ravine
                new Coin(29 * 32, 10 * 32), new Coin(31 * 32, 10 * 32), // Cavern coins
                new Coin(44 * 32, 7 * 32), new Coin(57 * 32, 8 * 32),
                new Coin(68 * 32, 7 * 32), new Coin(73 * 32, 7 * 32),
                new Coin(80 * 32, 7 * 32), new Coin(91 * 32, 6 * 32)
            ];

            this.chests = [
                new Chest(28 * 32, 11 * 32 - 24, false), // Hidden cavern chest
                new Chest(92 * 32, 7 * 32 - 24, false)   // Highland chest
            ];

            this.goal = new GoalFlag(103 * 32, 9 * 32 - 48);

        } else if (stageNum === 4) {
            // ================= FASE 4: O PÂNTANO NOTURNO =================
            this.enemies = [
                new OrcEnemy(8 * 32, 11 * 32 - 28, 50, 'orc1'),
                new OrcEnemy(28 * 32, 10 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(72 * 32, 10 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(78 * 32, 10 * 32 - 28, 60, 'orc2'),
                new OrcEnemy(88 * 32, 8 * 32 - 28, 60, 'orc2')
            ];

            // Silver Key atop the sunken tower
            this.keyItem = new KeyItem(47 * 32, 3 * 32 - 16);
            // Rune Gate guarding the sanctuary
            this.runeGate = new RuneGate(93 * 32, 8 * 32 - 24);

            this.coins = [
                new Coin(14 * 32, 9 * 32), new Coin(18 * 32, 8 * 32), new Coin(22 * 32, 9 * 32),
                new Coin(39 * 32, 6 * 32), new Coin(43 * 32, 4 * 32), new Coin(48 * 32, 3 * 32),
                new Coin(53 * 32, 8 * 32), new Coin(58 * 32, 7 * 32), new Coin(63 * 32, 8 * 32),
                new Coin(74 * 32, 9 * 32), new Coin(86 * 32, 7 * 32),
                new Coin(100 * 32, 8 * 32), new Coin(102 * 32, 8 * 32)
            ];

            this.chests = [
                new Chest(38 * 32, 7 * 32 - 24, false),
                new Chest(89 * 32, 8 * 32 - 24, false)
            ];

            this.goal = new GoalFlag(103 * 32, 9 * 32 - 48);

        } else if (stageNum === 5) {
            // ================= FASE 5: A FORTALEZA DO GENERAL ORC (CHEFE) =================
            // Elite Citadel Guards
            this.enemies = [
                new OrcEnemy(10 * 32, 10 * 32 - 28, 60, 'orc2'),
                new OrcEnemy(22 * 32, 7 * 32 - 28, 60, 'orc2'),
                new OrcEnemy(33 * 32, 9 * 32 - 28, 70, 'orc2'),
                new OrcEnemy(47 * 32, 10 * 32 - 28, 60, 'orc2')
            ];

            // THE BOSS: GENERAL ORC (ORC 3)
            this.boss = new OrcEnemy(88 * 32, 8 * 32 - 32, 120, 'orc3');
            this.enemies.push(this.boss);

            this.coins = [
                new Coin(6 * 32, 9 * 32), new Coin(19 * 32, 6 * 32),
                new Coin(24 * 32, 6 * 32), new Coin(35 * 32, 8 * 32),
                new Coin(49 * 32, 9 * 32),
                // Arena high dodge coins
                new Coin(73 * 32, 4 * 32), new Coin(75 * 32, 4 * 32),
                new Coin(87 * 32, 4 * 32), new Coin(89 * 32, 4 * 32),
                new Coin(99 * 32, 4 * 32), new Coin(101 * 32, 4 * 32)
            ];

            this.chests = [
                new Chest(20 * 32, 7 * 32 - 24, true) // Final power chest!
            ];

            this.goal = new GoalFlag(102 * 32, 8 * 32 - 48);
        }
    }

    triggerVictory() {
        this.savedHeroLevel = this.player.heroLevel;

        if (this.currentStage < this.totalStages) {
            this.state = 'stage_clear';
            window.sound.playVictory();
        } else {
            this.state = 'victory';
            this.endTime = Date.now();
            window.sound.playVictory();
        }
    }

    initInput() {
        window.addEventListener('keydown', (e) => {
            const key = e.code;
            window.sound.init();

            if (key === 'F2') {
                if (this.editor) this.editor.toggleEditor();
                e.preventDefault();
                return;
            }

            if (this.state === 'editing') {
                return;
            }

            if (this.state === 'title') {
                if (key === 'Enter' || key === 'Space' || key === 'KeyZ') {
                    this.score = 0;
                    this.coinsCount = 0;
                    this.savedHeroLevel = 1;
                    this.startTime = Date.now();
                    this.initStage(1);
                    this.state = 'playing';
                    if (!window.sound.bgmPlaying) {
                        window.sound.startBgm();
                        this.bgmEnabled = true;
                    }
                    e.preventDefault();
                    return;
                }
            }

            if (this.state === 'stage_clear') {
                if (key === 'Enter' || key === 'Space') {
                    this.initStage(this.currentStage + 1);
                    this.state = 'playing';
                    e.preventDefault();
                    return;
                }
            }

            if (this.state === 'gameover') {
                if (key === 'KeyR' || key === 'Enter' || key === 'Space') {
                    if (this.isCustomStage && this.customStageData) {
                        this.loadCustomCreatedStage(this.customStageData);
                    } else {
                        this.initStage(this.currentStage);
                    }
                    this.state = 'playing';
                    e.preventDefault();
                    return;
                }
            }

            if (this.state === 'victory') {
                if (key === 'KeyR' || key === 'Enter' || key === 'Space') {
                    this.score = 0;
                    this.coinsCount = 0;
                    this.savedHeroLevel = 1;
                    this.startTime = Date.now();
                    this.initStage(1);
                    this.state = 'playing';
                    e.preventDefault();
                    return;
                }
            }

            if (key === 'Escape' || key === 'KeyP') {
                if (this.state === 'playing') this.state = 'paused';
                else if (this.state === 'paused') this.state = 'playing';
                e.preventDefault();
                return;
            }

            if (key === 'KeyM') {
                this.bgmEnabled = window.sound.toggleBgm();
                e.preventDefault();
                return;
            }

            if (key === 'ArrowLeft' || key === 'KeyA') this.input.left = true;
            if (key === 'ArrowRight' || key === 'KeyD') this.input.right = true;
            if (key === 'ArrowUp' || key === 'KeyW' || key === 'Space') {
                if (!this.input.jump) this.input.jumpPressed = true;
                this.input.jump = true;
                e.preventDefault();
            }
            if (key === 'KeyZ' || key === 'KeyJ') {
                this.input.attackPressed = true;
                e.preventDefault();
            }
            if (key === 'KeyE') {
                this.input.interactPressed = true;
                e.preventDefault();
            }
        });

        window.addEventListener('keyup', (e) => {
            const key = e.code;
            if (key === 'ArrowLeft' || key === 'KeyA') this.input.left = false;
            if (key === 'ArrowRight' || key === 'KeyD') this.input.right = false;
            if (key === 'ArrowUp' || key === 'KeyW' || key === 'Space') this.input.jump = false;
            if (key === 'KeyE') this.input.interactPressed = false;
        });

        this.canvas.addEventListener('pointerdown', () => {
            window.sound.init();
            if (this.state === 'title') {
                this.score = 0;
                this.coinsCount = 0;
                this.savedHeroLevel = 1;
                this.startTime = Date.now();
                this.initStage(1);
                this.state = 'playing';
                if (!window.sound.bgmPlaying) {
                    window.sound.startBgm();
                    this.bgmEnabled = true;
                }
            } else if (this.state === 'stage_clear') {
                this.initStage(this.currentStage + 1);
                this.state = 'playing';
            } else if (this.state === 'gameover') {
                this.initStage(this.currentStage);
                this.state = 'playing';
            } else if (this.state === 'victory') {
                this.score = 0;
                this.coinsCount = 0;
                this.savedHeroLevel = 1;
                this.startTime = Date.now();
                this.initStage(1);
                this.state = 'playing';
            }
        });
    }

    pollGamepad() {
        const gamepads = navigator.getGamepads ? navigator.getGamepads() : [];
        const gp = gamepads[0];
        if (!gp) return;

        const stickX = gp.axes[0];
        this.input.left = this.input.left || stickX < -0.3 || gp.buttons[14]?.pressed;
        this.input.right = this.input.right || stickX > 0.3 || gp.buttons[15]?.pressed;

        if (gp.buttons[0]?.pressed) {
            if (!this.input.jump) this.input.jumpPressed = true;
            this.input.jump = true;
        }
        if (gp.buttons[2]?.pressed) {
            this.input.attackPressed = true;
        }
        if (gp.buttons[1]?.pressed || gp.buttons[3]?.pressed) {
            this.input.interactPressed = true;
        }
    }

    loop(timestamp) {
        if (!this.lastTime) this.lastTime = timestamp;
        let dt = (timestamp - this.lastTime) / 1000;
        this.lastTime = timestamp;

        if (dt > 0.1) dt = 0.1;

        this.pollGamepad();
        this.update(dt);
        this.render(dt);

        this.input.jumpPressed = false;
        this.input.attackPressed = false;
        this.input.interactPressed = false;

        requestAnimationFrame(this.loop.bind(this));
    }

    update(dt) {
        if (this.state !== 'playing') return;

        this.player.update(dt, this.input, this.level);

        this.enemies.forEach(e => e.update(dt, this.player, this.level));
        this.coins.forEach(c => c.update(dt, this.player, this.level));
        this.chests.forEach(ch => ch.update(dt, this.player));

        if (this.keyItem) this.keyItem.update(dt, this.player);
        if (this.runeGate) this.runeGate.update(dt, this.player);

        if (this.goal) {
            // In stage 5, goal requires the Boss to be dead
            const isBossBeaten = !this.boss || this.boss.isDead;
            if (this.currentStage !== 5 || isBossBeaten) {
                this.goal.update(dt, this.player, this.runeGate);
            }
        }

        window.particles.update(dt);

        // Smooth Camera Follow
        const targetCamX = this.player.x + this.player.w / 2 - this.viewWidth * 0.4;
        const targetCamY = Math.min(
            this.level.heightInPixels - this.viewHeight,
            Math.max(0, this.player.y + this.player.h / 2 - this.viewHeight * 0.55)
        );

        this.cameraX += (targetCamX - this.cameraX) * 0.08;
        this.cameraY += (targetCamY - this.cameraY) * 0.08;

        this.cameraX = Math.max(0, Math.min(this.level.widthInPixels - this.viewWidth, this.cameraX));
        this.cameraY = Math.max(0, Math.min(this.level.heightInPixels - this.viewHeight, this.cameraY));

        if (this.player.isDead && this.player.deathTimer > 1.4) {
            this.state = 'gameover';
        }
    }

    render(dt = 0.016) {
        this.ctx.clearRect(0, 0, this.viewWidth, this.viewHeight);

        if (this.state === 'loading') return;
        if (this.state === 'editing') {
            if (this.editor) this.editor.draw();
            return;
        }
        if (this.state === 'title') {
            this.renderTitle();
            return;
        }

        // Parallax Background with atmospheric tints and ambient particles
        this.level.drawParallax(this.ctx, this.cameraX, this.cameraY, this.viewWidth, this.viewHeight, dt);

        this.ctx.save();
        this.ctx.translate(-Math.round(this.cameraX), -Math.round(this.cameraY));

        // Props
        this.level.drawProps(this.ctx, this.cameraX, this.cameraY);

        // Tiles
        this.level.drawTiles(this.ctx, this.cameraX, this.cameraY, this.viewWidth, this.viewHeight);

        // Interactive Objects
        if (this.keyItem) this.keyItem.draw(this.ctx);
        if (this.runeGate) this.runeGate.draw(this.ctx, this.player);
        this.chests.forEach(ch => ch.draw(this.ctx, this.player));
        this.coins.forEach(c => c.draw(this.ctx));

        // Goal Flag (hidden in stage 5 until boss is defeated)
        if (this.goal) {
            if (this.currentStage !== 5 || (this.boss && this.boss.isDead)) {
                this.goal.draw(this.ctx);
            }
        }

        // Enemies
        this.enemies.forEach(e => e.draw(this.ctx));

        // Player
        this.player.draw(this.ctx);

        // Particles
        window.particles.draw(this.ctx);

        this.ctx.restore();

        // UI & Overlays
        this.renderHUD();

        // Boss Health Bar in Stage 5
        if (this.currentStage === 5 && this.boss && !this.boss.isDead && this.player.x > 62 * 32) {
            this.renderBossHealth();
        }

        if (this.state === 'paused') this.renderPaused();
        if (this.state === 'stage_clear') this.renderStageClear();
        if (this.state === 'gameover') this.renderGameOver();
        if (this.state === 'victory') this.renderVictory();
    }

    renderLoading(progress) {
        this.ctx.fillStyle = '#0f141d';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 16px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('CARREGANDO AVENTURA...', this.viewWidth / 2, this.viewHeight / 2 - 15);

        this.ctx.strokeStyle = '#4ecca3';
        this.ctx.lineWidth = 2;
        this.ctx.strokeRect(this.viewWidth / 2 - 100, this.viewHeight / 2, 200, 16);

        this.ctx.fillStyle = '#4ecca3';
        this.ctx.fillRect(this.viewWidth / 2 - 98, this.viewHeight / 2 + 2, 196 * progress, 12);
    }

    renderTitle() {
        this.ctx.fillStyle = '#0b0e14';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#ffd700';
        this.ctx.font = 'bold 22px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('SWORDSMAN: A SAGA DAS 5 FASES', this.viewWidth / 2, 45);

        this.ctx.fillStyle = '#a0aec0';
        this.ctx.font = '10px monospace';
        this.ctx.fillText('Fase 1: Floresta • 2: Ruínas • 3: Desfiladeiro • 4: Pântano • 5: Fortaleza', this.viewWidth / 2, 65);

        const h1 = window.sprites.get('hero1_idle');
        const h2 = window.sprites.get('hero2_idle');
        const h3 = window.sprites.get('hero3_idle');
        const boss = window.sprites.get('orc3_idle');

        if (h1) this.ctx.drawImage(h1, 0, 128, 64, 64, this.viewWidth / 2 - 130, 88, 48, 48);
        if (h2) this.ctx.drawImage(h2, 0, 128, 64, 64, this.viewWidth / 2 - 75, 88, 48, 48);
        if (h3) this.ctx.drawImage(h3, 0, 128, 64, 64, this.viewWidth / 2 - 20, 88, 48, 48);

        if (boss) {
            this.ctx.save();
            this.ctx.translate(this.viewWidth / 2 + 85, 82);
            this.ctx.scale(-1, 1);
            this.ctx.drawImage(boss, 0, 128, 64, 64, -30, 0, 60, 60);
            this.ctx.restore();
        }

        const blink = Math.floor(Date.now() / 450) % 2 === 0;
        if (blink) {
            this.ctx.fillStyle = '#4ecca3';
            this.ctx.font = 'bold 13px monospace';
            this.ctx.fillText('PRESSIONE [ENTER] OU CLIQUE PARA JOGAR', this.viewWidth / 2, 185);
        }

        this.ctx.fillStyle = '#718096';
        this.ctx.font = '10px monospace';
        this.ctx.fillText('[A/D] Andar • [ESPAÇO/W] Pular • [Z/J] Atacar • [E] Abrir Baú / Interagir', this.viewWidth / 2, 225);
    }

    renderHUD() {
        this.ctx.fillStyle = '#a0aec0';
        this.ctx.font = 'bold 10px monospace';
        this.ctx.textAlign = 'left';
        this.ctx.fillText(this.stageTitles[this.currentStage], 16, 14);

        // Hearts
        for (let i = 0; i < this.player.maxHp; i++) {
            const hx = 16 + i * 14;
            const hy = 20;
            this.ctx.fillStyle = (i < this.player.hp) ? '#e53e3e' : '#4a5568';
            this.ctx.fillRect(hx, hy + 2, 10, 8);
            this.ctx.fillRect(hx + 1, hy, 3, 2);
            this.ctx.fillRect(hx + 6, hy, 3, 2);
            this.ctx.fillRect(hx + 2, hy + 10, 6, 2);
            this.ctx.fillRect(hx + 4, hy + 12, 2, 2);
        }

        const lvlNames = ['', 'NV.1 (Padrão)', 'NV.2 (Ferro)', 'NV.3 (Ouro)'];
        this.ctx.fillStyle = '#4ecca3';
        this.ctx.font = 'bold 10px monospace';
        this.ctx.fillText(`HERÓI: ${lvlNames[this.player.heroLevel]}`, 95, 30);

        if (this.player.hasKey) {
            const keyImg = window.sprites.get('key');
            if (keyImg) {
                this.ctx.drawImage(keyImg, 0, 0, 8, 8, 205, 20, 12, 12);
            }
            this.ctx.fillStyle = '#ffeb3b';
            this.ctx.fillText('CHAVE', 222, 30);
        }

        const coinImg = window.sprites.get('coin');
        if (coinImg) {
            this.ctx.drawImage(coinImg, 0, 0, 10, 10, 275, 20, 12, 12);
        }
        this.ctx.fillStyle = '#ffd700';
        this.ctx.font = 'bold 12px monospace';
        this.ctx.fillText(`x ${this.coinsCount}`, 292, 30);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.fillText(`SCORE: ${this.score}`, 345, 30);

        this.ctx.fillStyle = this.bgmEnabled ? '#48bb78' : '#718096';
        this.ctx.font = '9px monospace';
        this.ctx.textAlign = 'right';
        this.ctx.fillText(`[M] SOM: ${this.bgmEnabled ? 'ON' : 'OFF'}`, this.viewWidth - 14, 18);
    }

    renderBossHealth() {
        const barW = 200;
        const barH = 10;
        const bx = (this.viewWidth - barW) / 2;
        const by = 42;

        this.ctx.fillStyle = 'rgba(0,0,0,0.7)';
        this.ctx.fillRect(bx - 4, by - 16, barW + 8, barH + 20);

        this.ctx.fillStyle = '#e53e3e';
        this.ctx.font = 'bold 10px monospace';
        this.ctx.textAlign = 'center';
        const bossTitle = this.boss.enraged ? '⚡ GENERAL ORC ENFURECIDO ⚡' : '⚔️ CHEFE: GENERAL ORC ⚔️';
        this.ctx.fillText(bossTitle, this.viewWidth / 2, by - 4);

        this.ctx.strokeStyle = '#ffffff';
        this.ctx.lineWidth = 1;
        this.ctx.strokeRect(bx, by, barW, barH);

        const hpPct = Math.max(0, this.boss.hp / this.boss.maxHp);
        this.ctx.fillStyle = this.boss.enraged ? '#ff1a1a' : '#e53e3e';
        this.ctx.fillRect(bx + 1, by + 1, (barW - 2) * hpPct, barH - 2);
    }

    renderStageClear() {
        this.ctx.fillStyle = 'rgba(10, 25, 20, 0.85)';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#48bb78';
        this.ctx.font = 'bold 20px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`${this.stageTitles[this.currentStage]} CONCLUÍDA!`, this.viewWidth / 2, 70);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '12px monospace';
        this.ctx.fillText(`Moedas Coletadas: ${this.coinsCount} • Pontuação: ${this.score}`, this.viewWidth / 2, 105);

        this.ctx.fillStyle = '#ffd700';
        this.ctx.font = '12px monospace';
        this.ctx.fillText(`Próxima: ${this.stageTitles[this.currentStage + 1]}`, this.viewWidth / 2, 135);

        const blink = Math.floor(Date.now() / 400) % 2 === 0;
        if (blink) {
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = 'bold 13px monospace';
            this.ctx.fillText('PRESSIONE [ENTER] OU CLIQUE PARA AVANÇAR', this.viewWidth / 2, 180);
        }
    }

    renderGameOver() {
        this.ctx.fillStyle = 'rgba(20, 0, 0, 0.8)';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#e53e3e';
        this.ctx.font = 'bold 26px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('VOCÊ FOI DERROTADO!', this.viewWidth / 2, this.viewHeight / 2 - 25);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '13px monospace';
        this.ctx.fillText(`Fase: ${this.currentStage} • Pontuação: ${this.score}`, this.viewWidth / 2, this.viewHeight / 2 + 5);

        const blink = Math.floor(Date.now() / 400) % 2 === 0;
        if (blink) {
            this.ctx.fillStyle = '#ffd700';
            this.ctx.font = 'bold 12px monospace';
            this.ctx.fillText('PRESSIONE [R] OU CLIQUE PARA RECOMEÇAR ESTA FASE', this.viewWidth / 2, this.viewHeight / 2 + 40);
        }
    }

    renderVictory() {
        this.ctx.fillStyle = 'rgba(10, 30, 20, 0.9)';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#ffd700';
        this.ctx.font = 'bold 22px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('🎉 PARABÉNS! VOCÊ SALVOU O REINO! 🎉', this.viewWidth / 2, 50);

        this.ctx.fillStyle = '#4ecca3';
        this.ctx.font = '12px monospace';
        this.ctx.fillText('O temível General Orc foi derrotado e as 5 terras foram libertadas!', this.viewWidth / 2, 80);

        const elapsedSecs = Math.floor((this.endTime - this.startTime) / 1000);
        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = '12px monospace';
        this.ctx.fillText(`Tempo Total: ${elapsedSecs}s • Moedas Coletadas: ${this.coinsCount}`, this.viewWidth / 2, 110);
        this.ctx.fillStyle = '#ffd700';
        this.ctx.font = 'bold 15px monospace';
        this.ctx.fillText(`PONTUAÇÃO FINAL: ${this.score + (this.coinsCount * 30)}`, this.viewWidth / 2, 140);

        const blink = Math.floor(Date.now() / 400) % 2 === 0;
        if (blink) {
            this.ctx.fillStyle = '#ffffff';
            this.ctx.font = 'bold 12px monospace';
            this.ctx.fillText('PRESSIONE [R] OU CLIQUE PARA JOGAR NOVAMENTE', this.viewWidth / 2, 195);
        }
    }

    renderPaused() {
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.65)';
        this.ctx.fillRect(0, 0, this.viewWidth, this.viewHeight);

        this.ctx.fillStyle = '#ffffff';
        this.ctx.font = 'bold 20px monospace';
        this.ctx.textAlign = 'center';
        this.ctx.fillText('JOGO PAUSADO', this.viewWidth / 2, this.viewHeight / 2 - 10);

        this.ctx.font = '12px monospace';
        this.ctx.fillStyle = '#cbd5e0';
        this.ctx.fillText('Pressione [ESC] ou [P] para continuar', this.viewWidth / 2, this.viewHeight / 2 + 18);
    }
}

window.addEventListener('load', () => {
    const game = new Game();
    game.start();
});
