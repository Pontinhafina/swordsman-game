// Player (Swordsman) Controller & State Machine

class Player {
    constructor(x, y) {
        this.spawnX = x;
        this.spawnY = y;
        this.heroLevel = 1; // 1, 2, 3
        this.hasKey = false;
        this.reset();
    }

    reset() {
        this.x = this.spawnX;
        this.y = this.spawnY;
        this.w = 16;
        this.h = 26;
        this.vx = 0;
        this.vy = 0;
        this.facing = 1; // 1 = right, -1 = left

        this.onGround = false;
        this.wasOnGround = false;

        // Platformer feel assists
        this.coyoteTimer = 0;
        this.jumpBufferTimer = 0;

        // Health & combat
        this.maxHp = 5;
        this.hp = this.maxHp;
        this.invulnerableTimer = 0;
        this.isAttacking = false;
        this.attackFrame = 0;
        this.attackTimer = 0;
        this.attackHitDone = false;

        // Animation
        this.state = 'idle'; // idle, run, jump, fall, attack, hurt, dead
        this.animTimer = 0;
        this.animFrame = 0;

        this.isDead = false;
        this.deathTimer = 0;
    }

    upgradeLevel(lvl) {
        this.heroLevel = Math.min(3, Math.max(1, lvl));
        window.sound.playChest();
        const titles = ['', 'ESPADACHIM INICIANTE', 'ESPADACHIM DE FERRO!', 'CAVALEIRO DOURADO!'];
        window.particles.addHitSparks(this.x + this.w / 2, this.y + this.h / 2, '#ffd700', 18);
        window.particles.addText(this.x + this.w / 2, this.y - 16, titles[this.heroLevel], '#ffd700');
    }

    takeDamage(amount, knockbackDir = 0) {
        if (this.invulnerableTimer > 0 || this.isDead) return;

        this.hp = Math.max(0, this.hp - amount);
        this.invulnerableTimer = 1.2;
        this.state = 'hurt';
        this.animFrame = 0;
        this.animTimer = 0;
        this.isAttacking = false;

        this.vx = knockbackDir * 120;
        this.vy = -140;

        window.sound.playHurt();
        window.particles.addHitSparks(this.x + this.w / 2, this.y + this.h / 2, '#ff3333', 10);

        if (this.hp <= 0) {
            this.die();
        }
    }

    die() {
        this.isDead = true;
        this.state = 'dead';
        this.animFrame = 0;
        this.animTimer = 0;
        this.vx = 0;
        window.sound.playPlayerDeath();
    }

    attack() {
        if (this.isAttacking || this.state === 'hurt' || this.isDead) return;
        this.isAttacking = true;
        this.state = 'attack';
        this.attackFrame = 0;
        this.attackTimer = 0;
        this.attackHitDone = false;
        window.sound.playAttack();
    }

    update(dt, input, level) {
        if (this.isDead) {
            this.updateDead(dt, level);
            return;
        }

        if (this.invulnerableTimer > 0) {
            this.invulnerableTimer -= dt;
        }

        // Coyote & Jump buffer timers
        if (this.onGround) {
            this.coyoteTimer = 0.12;
        } else {
            this.coyoteTimer -= dt;
        }

        if (input.jumpPressed) {
            this.jumpBufferTimer = 0.14;
        } else {
            this.jumpBufferTimer -= dt;
        }

        // Attack input
        if (input.attackPressed && !this.isAttacking && this.state !== 'hurt') {
            this.attack();
        }

        // Handle Horizontal Input
        const moveDir = (input.right ? 1 : 0) - (input.left ? 1 : 0);
        if (moveDir !== 0 && !this.isAttacking) {
            this.facing = moveDir;
            const accel = this.onGround ? 700 : 500;
            this.vx += moveDir * accel * dt;
            const maxSpeed = 145;
            if (Math.abs(this.vx) > maxSpeed) {
                this.vx = moveDir * maxSpeed;
            }
        } else {
            const friction = this.onGround ? 0.75 : 0.90;
            this.vx *= Math.pow(friction, dt * 60);
            if (Math.abs(this.vx) < 5) this.vx = 0;
        }

        // Jump Execution
        if (this.jumpBufferTimer > 0 && this.coyoteTimer > 0 && !this.isAttacking) {
            this.vy = -315;
            this.jumpBufferTimer = 0;
            this.coyoteTimer = 0;
            this.onGround = false;
            window.sound.playJump();
            window.particles.addDust(this.x + this.w / 2, this.y + this.h, 6);
        }

        // Variable jump height: release early cuts jump
        if (!input.jump && this.vy < -70) {
            this.vy += 500 * dt;
        }

        // Gravity
        this.vy += 620 * dt;
        if (this.vy > 420) this.vy = 420; // Terminal velocity

        // Apply movement & Collide with Level
        this.moveAndCollide(dt, level);

        // Update Animation State
        this.updateAnimation(dt);

        // Check if landed this frame (dust effect)
        if (this.onGround && !this.wasOnGround) {
            window.particles.addDust(this.x + this.w / 2, this.y + this.h, 5);
        }
        this.wasOnGround = this.onGround;

        // Fall into abyss check
        if (this.y > level.heightInPixels + 64) {
            this.takeDamage(this.hp);
        }
    }

    moveAndCollide(dt, level) {
        // Horizontal step
        this.x += this.vx * dt;
        let collideX = level.checkTileCollision(this);
        if (collideX) {
            if (this.vx > 0) {
                this.x = collideX.tileX * level.tileSize - this.w - 0.01;
            } else if (this.vx < 0) {
                this.x = (collideX.tileX + 1) * level.tileSize + 0.01;
            }
            this.vx = 0;
        }

        // Vertical step
        this.y += this.vy * dt;
        this.onGround = false;
        let collideY = level.checkTileCollision(this);
        if (collideY) {
            if (this.vy > 0) {
                this.y = collideY.tileY * level.tileSize - this.h - 0.01;
                this.vy = 0;
                this.onGround = true;
            } else if (this.vy < 0) {
                this.y = (collideY.tileY + 1) * level.tileSize + 0.01;
                this.vy = 0;
            }
        }

        // One-way platform check
        if (this.vy >= 0) {
            const feetPlatform = level.checkOneWayPlatform(this.x, this.y + this.h, this.w, this.vy * dt);
            if (feetPlatform) {
                this.y = feetPlatform.y - this.h;
                this.vy = 0;
                this.onGround = true;
            }
        }
    }

    updateAnimation(dt) {
        if (this.isAttacking) {
            this.attackTimer += dt;
            const attackFrameDur = 0.055;
            this.attackFrame = Math.floor(this.attackTimer / attackFrameDur);

            // Active hit frame (frames 2 to 4)
            if (this.attackFrame >= 2 && this.attackFrame <= 4 && !this.attackHitDone) {
                this.checkAttackHit();
            }

            if (this.attackFrame >= 8) {
                this.isAttacking = false;
                this.attackFrame = 0;
            }
            return;
        }

        if (this.state === 'hurt') {
            this.animTimer += dt;
            this.animFrame = Math.floor(this.animTimer / 0.08);
            if (this.animFrame >= 5) {
                this.state = 'idle';
                this.animFrame = 0;
            }
            return;
        }

        if (!this.onGround) {
            if (this.vy < 0) {
                this.state = 'jump';
            } else {
                this.state = 'fall';
            }
            return;
        }

        if (Math.abs(this.vx) > 10) {
            this.state = 'run';
            this.animTimer += dt;
            const runFrameDur = 0.09;
            this.animFrame = Math.floor(this.animTimer / runFrameDur) % 8;
        } else {
            this.state = 'idle';
            this.animTimer += dt;
            const idleFrameDur = 0.12;
            this.animFrame = Math.floor(this.animTimer / idleFrameDur) % 12;
        }
    }

    checkAttackHit() {
        const attackReach = 20 + (this.heroLevel * 4); // lvl1=24, lvl2=28, lvl3=32
        const attackDamage = this.heroLevel; // lvl1=1, lvl2=2, lvl3=3

        const attackBox = {
            x: this.facing > 0 ? this.x + this.w - 4 : this.x - attackReach,
            y: this.y + 4,
            w: attackReach,
            h: 22
        };

        if (window.gameInstance && window.gameInstance.enemies) {
            window.gameInstance.enemies.forEach(enemy => {
                if (!enemy.isDead && checkAABB(attackBox, enemy)) {
                    enemy.takeDamage(attackDamage, this.facing);
                    this.attackHitDone = true;
                }
            });
        }

        // Also check if hitting chest
        if (window.gameInstance && window.gameInstance.chests) {
            window.gameInstance.chests.forEach(chest => {
                if (!chest.opened && checkAABB(attackBox, chest)) {
                    chest.open();
                }
            });
        }
    }

    updateDead(dt, level) {
        this.deathTimer += dt;
        this.vy += 680 * dt;
        this.y += this.vy * dt;
        let collideY = level.checkTileCollision(this);
        if (collideY && this.vy > 0) {
            this.y = collideY.tileY * level.tileSize - this.h;
            this.vy = 0;
        }

        const deathFrameDur = 0.11;
        this.animFrame = Math.min(6, Math.floor(this.deathTimer / deathFrameDur));
    }

    draw(ctx) {
        // Flash when invulnerable
        if (this.invulnerableTimer > 0 && Math.floor(Date.now() / 60) % 2 === 0) {
            return;
        }

        const prefix = `hero${this.heroLevel}_`;
        let imgKey = prefix + 'idle';
        let frameIdx = 0;
        const row = 2; // Side-view row

        if (this.isDead) {
            imgKey = prefix + 'death';
            frameIdx = this.animFrame;
        } else if (this.isAttacking) {
            imgKey = prefix + 'attack';
            frameIdx = Math.min(7, this.attackFrame);
        } else if (this.state === 'hurt') {
            imgKey = prefix + 'hurt';
            frameIdx = Math.min(4, this.animFrame);
        } else if (this.state === 'jump') {
            imgKey = prefix + 'run';
            frameIdx = 2; // Dynamic mid-air jump pose
        } else if (this.state === 'fall') {
            imgKey = prefix + 'run';
            frameIdx = 5; // Mid-air fall pose
        } else if (this.state === 'run') {
            imgKey = prefix + 'run';
            frameIdx = this.animFrame;
        } else {
            imgKey = prefix + 'idle';
            frameIdx = this.animFrame;
        }

        const img = window.sprites.get(imgKey);
        if (!img) return;

        ctx.save();
        const drawX = Math.round(this.x + this.w / 2);
        const drawY = Math.round(this.y + this.h);

        ctx.translate(drawX, drawY);
        ctx.scale(this.facing, 1);

        const sx = frameIdx * 64;
        const sy = row * 64;
        ctx.drawImage(img, sx, sy, 64, 64, -32, -43, 64, 64);

        ctx.restore();
    }
}
