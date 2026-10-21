// Orc Enemy Class supporting Orc1, Orc2 (Warrior) and Orc3 (Boss General)

class OrcEnemy {
    constructor(x, y, patrolDist = 120, type = 'orc1') {
        this.startX = x;
        this.x = x;
        this.y = y;
        this.type = type; // 'orc1', 'orc2', 'orc3'
        this.isBoss = (type === 'orc3');

        this.w = this.isBoss ? 26 : 20;
        this.h = this.isBoss ? 32 : 28;
        this.vx = (type === 'orc2' ? 50 : 38);
        this.vy = 0;
        this.facing = 1; // 1 = right, -1 = left

        this.patrolLeft = x - patrolDist;
        this.patrolRight = x + patrolDist;

        // Health tuning
        if (this.isBoss) {
            this.maxHp = 10;
        } else if (type === 'orc2') {
            this.maxHp = 3;
        } else {
            this.maxHp = 2;
        }
        this.hp = this.maxHp;

        this.isDead = false;
        this.deathTimer = 0;
        this.enraged = false;

        this.state = 'run'; // idle, run, attack, hurt, dead
        this.animTimer = 0;
        this.animFrame = 0;

        this.attackCooldown = 0;
        this.attackHitDone = false;
        this.hurtTimer = 0;
        this.onGround = false;
    }

    takeDamage(amount, knockbackDir = 0) {
        if (this.isDead) return;

        this.hp -= amount;
        this.hurtTimer = 0.32;
        this.state = 'hurt';
        this.animFrame = 0;
        this.animTimer = 0;

        // Boss resists knockback more
        const kb = this.isBoss ? 35 : 90;
        this.vx = knockbackDir * kb;
        this.vy = this.isBoss ? -60 : -100;

        window.sound.playHit();
        const sparkColor = this.isBoss ? '#e53e3e' : '#48bb78';
        window.particles.addHitSparks(this.x + this.w / 2, this.y + this.h / 2, sparkColor, this.isBoss ? 16 : 8);
        window.particles.addText(this.x + this.w / 2, this.y - 4, `-${amount}`, '#ff5555');

        // Boss Enrage at 50% HP
        if (this.isBoss && !this.enraged && this.hp <= this.maxHp / 2) {
            this.enraged = true;
            window.particles.addHitSparks(this.x + this.w / 2, this.y + this.h / 2, '#ff0033', 25);
            window.particles.addText(this.x + this.w / 2, this.y - 20, '⚔️ GENERAL ENFURECIDO! ⚔️', '#ff3333');
            // Summon an orc scout minion to flank the player!
            if (window.gameInstance && window.gameInstance.enemies) {
                const minion = new OrcEnemy(this.x - 70, this.y, 40, 'orc1');
                window.gameInstance.enemies.push(minion);
            }
        }

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

        window.sound.playEnemyDeath();

        const points = this.isBoss ? 500 : (this.type === 'orc2' ? 200 : 100);
        window.particles.addText(this.x + this.w / 2, this.y - 14, `+${points}`, '#ffd700');

        if (window.gameInstance) {
            window.gameInstance.score += points;
            // Boss drops a fountain of coins!
            const coinDrops = this.isBoss ? 6 : (this.type === 'orc2' ? 2 : 1);
            for (let i = 0; i < coinDrops; i++) {
                const c = new Coin(this.x + (Math.random() - 0.5) * 20, this.y + (Math.random() - 0.5) * 10, true);
                c.vy = -100 - Math.random() * 80;
                c.vx = (Math.random() - 0.5) * 80;
                window.gameInstance.coins.push(c);
            }
        }
    }

    update(dt, player, level) {
        if (this.isDead) {
            this.deathTimer += dt;
            const deathDur = 0.12;
            this.animFrame = Math.min(6, Math.floor(this.deathTimer / deathDur));
            this.vy += 650 * dt;
            this.y += this.vy * dt;
            let collide = level.checkTileCollision(this);
            if (collide && this.vy > 0) {
                this.y = collide.tileY * level.tileSize - this.h;
                this.vy = 0;
            }
            return;
        }

        if (this.hurtTimer > 0) {
            this.hurtTimer -= dt;
            this.animTimer += dt;
            this.animFrame = Math.floor(this.animTimer / 0.08) % 5;
            this.moveAndCollide(dt, level);
            if (this.hurtTimer <= 0) {
                this.state = 'run';
            }
            return;
        }

        if (this.attackCooldown > 0) {
            this.attackCooldown -= dt;
        }

        const dx = (player.x + player.w / 2) - (this.x + this.w / 2);
        const dy = (player.y + player.h / 2) - (this.y + this.h / 2);
        const dist = Math.sqrt(dx * dx + dy * dy);

        // State behavior
        if (this.state === 'attack') {
            this.animTimer += dt;
            const frameDur = this.isBoss ? 0.08 : 0.09;
            this.animFrame = Math.floor(this.animTimer / frameDur);

            // Active attack hit window (frames 3 to 5)
            if (this.animFrame >= 3 && this.animFrame <= 5 && !this.attackHitDone) {
                const reach = this.isBoss ? 28 : 22;
                const attackBox = {
                    x: this.facing > 0 ? this.x + this.w - 4 : this.x - reach,
                    y: this.y + 4,
                    w: reach,
                    h: this.h - 4
                };
                if (!player.isDead && checkAABB(attackBox, player)) {
                    player.takeDamage(this.isBoss ? 2 : 1, this.facing);
                    this.attackHitDone = true;
                }
            }

            if (this.animFrame >= 8) {
                this.state = 'run';
                this.attackCooldown = this.isBoss ? 0.7 : 1.0;
            }
            this.moveAndCollide(dt, level);
            return;
        }

        // Check if player in attack range
        const attackDist = this.isBoss ? 38 : 30;
        if (dist < attackDist && Math.abs(dy) < 28 && this.attackCooldown <= 0 && !player.isDead) {
            this.state = 'attack';
            this.animFrame = 0;
            this.animTimer = 0;
            this.attackHitDone = false;
            this.facing = dx > 0 ? 1 : -1;
            this.vx = 0;
            return;
        }

        // Aggro / Chase player if within range
        const sightRange = this.isBoss ? 180 : (this.type === 'orc2' ? 150 : 130);
        if (dist < sightRange && Math.abs(dy) < 56 && !player.isDead) {
            this.facing = dx > 0 ? 1 : -1;
            const chaseSpeed = this.isBoss ? 75 : (this.type === 'orc2' ? 70 : 60);
            this.vx = this.facing * chaseSpeed;
            this.state = 'run';
        } else {
            // Normal patrol
            if (this.facing > 0 && this.x >= this.patrolRight) {
                this.facing = -1;
            } else if (this.facing < 0 && this.x <= this.patrolLeft) {
                this.facing = 1;
            }
            const patrolSpeed = this.type === 'orc2' ? 44 : 36;
            this.vx = this.facing * patrolSpeed;
            this.state = 'run';
        }

        // Ledge checking: don't walk into bottomless pits during patrol
        if (this.onGround && dist >= sightRange) {
            const checkX = this.facing > 0 ? this.x + this.w + 4 : this.x - 4;
            const tileBelow = level.isTileSolidAtPixel(checkX, this.y + this.h + 8);
            if (!tileBelow) {
                this.facing = -this.facing;
                this.vx = this.facing * 36;
            }
        }

        // Update run animation
        this.animTimer += dt;
        const runFrameDur = 0.11;
        this.animFrame = Math.floor(this.animTimer / runFrameDur) % 8;

        this.moveAndCollide(dt, level);

        // Contact damage
        if (!player.isDead && checkAABB(this, player)) {
            player.takeDamage(1, dx > 0 ? 1 : -1);
        }
    }

    moveAndCollide(dt, level) {
        this.vy += 650 * dt;
        if (this.vy > 400) this.vy = 400;

        this.x += this.vx * dt;
        let collideX = level.checkTileCollision(this);
        if (collideX) {
            if (this.vx > 0) {
                this.x = collideX.tileX * level.tileSize - this.w - 0.01;
            } else if (this.vx < 0) {
                this.x = (collideX.tileX + 1) * level.tileSize + 0.01;
            }
            this.facing = -this.facing;
            this.vx = this.facing * Math.abs(this.vx);
        }

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
    }

    draw(ctx) {
        const prefix = `${this.type}_`;
        let imgKey = prefix + 'run';
        let frameIdx = 0;
        const row = 2; // Side-view row

        if (this.isDead) {
            imgKey = prefix + 'death';
            frameIdx = this.animFrame;
        } else if (this.state === 'attack') {
            imgKey = prefix + 'attack';
            frameIdx = Math.min(7, this.animFrame);
        } else if (this.state === 'hurt') {
            imgKey = prefix + 'hurt';
            frameIdx = Math.min(4, this.animFrame);
        } else if (this.state === 'run') {
            imgKey = prefix + 'run';
            frameIdx = this.animFrame;
        } else {
            imgKey = prefix + 'idle';
            frameIdx = this.animFrame % 4;
        }

        const img = window.sprites.get(imgKey);
        if (!img) return;

        ctx.save();
        const drawX = Math.round(this.x + this.w / 2);
        const drawY = Math.round(this.y + this.h);

        ctx.translate(drawX, drawY);
        // All Orc raw sprite sheets naturally face LEFT, so flip with -this.facing
        ctx.scale(-this.facing, 1);

        const sx = frameIdx * 64;
        const sy = row * 64;

        // Boss scales slightly larger for intimidating presence
        const scale = this.isBoss ? 1.2 : 1.0;
        ctx.scale(scale, scale);
        ctx.drawImage(img, sx, sy, 64, 64, -31, -42, 64, 64);

        ctx.restore();

        // Draw Health bar on top if damaged (non-boss)
        if (!this.isDead && !this.isBoss && this.hp < this.maxHp) {
            ctx.save();
            ctx.fillStyle = 'rgba(0,0,0,0.6)';
            ctx.fillRect(this.x - 2, this.y - 12, 24, 4);
            ctx.fillStyle = this.type === 'orc2' ? '#ed8936' : '#48bb78';
            ctx.fillRect(this.x - 1, this.y - 11, (this.hp / this.maxHp) * 22, 2);
            ctx.restore();
        }
    }
}
