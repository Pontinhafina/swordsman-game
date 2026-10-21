// Interactive World Objects: Coins, Chests, Keys, Runes, Goal Flag

class Coin {
    constructor(x, y, isDrop = false) {
        this.x = x;
        this.y = y;
        this.baseY = y;
        this.w = 12;
        this.h = 12;
        this.isDrop = isDrop;
        this.vy = isDrop ? -120 : 0;
        this.vx = isDrop ? (Math.random() - 0.5) * 60 : 0;
        this.collected = false;

        this.animTimer = Math.random() * 0.5;
        this.animFrame = 0;
        this.hoverTime = Math.random() * Math.PI;
    }

    update(dt, player, level) {
        if (this.collected) return;

        this.animTimer += dt;
        this.animFrame = Math.floor(this.animTimer / 0.12) % 4;

        if (this.isDrop) {
            this.vy += 500 * dt;
            this.x += this.vx * dt;
            this.y += this.vy * dt;
            const collide = level.checkTileCollision(this);
            if (collide && this.vy > 0) {
                this.y = collide.tileY * level.tileSize - this.h;
                this.vy = 0;
                this.vx = 0;
                this.baseY = this.y;
                this.isDrop = false;
            }
        } else {
            this.hoverTime += dt * 3;
            this.y = this.baseY + Math.sin(this.hoverTime) * 3;
        }

        if (!player.isDead && checkAABB(this, player)) {
            this.collect();
        }
    }

    collect() {
        this.collected = true;
        window.sound.playCoin();
        window.particles.addCoinSparkle(this.x + this.w / 2, this.y + this.h / 2, 8);
        window.particles.addText(this.x + this.w / 2, this.y - 6, '+10', '#ffd700');
        if (window.gameInstance) {
            window.gameInstance.coinsCount++;
            window.gameInstance.score += 10;
        }
    }

    draw(ctx) {
        if (this.collected) return;
        const img = window.sprites.get('coin');
        if (!img) return;

        const sx = this.animFrame * 10;
        ctx.drawImage(img, sx, 0, 10, 10, Math.round(this.x), Math.round(this.y), 12, 12);
    }
}

class KeyItem {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.baseY = y;
        this.w = 16;
        this.h = 16;
        this.collected = false;
        this.animTimer = 0;
        this.animFrame = 0;
        this.hoverTime = 0;
    }

    update(dt, player) {
        if (this.collected) return;

        this.animTimer += dt;
        this.animFrame = Math.floor(this.animTimer / 0.1) % 6;

        this.hoverTime += dt * 3;
        this.y = this.baseY + Math.sin(this.hoverTime) * 4;

        if (!player.isDead && checkAABB(this, player)) {
            this.collected = true;
            player.hasKey = true;
            window.sound.playChest();
            window.particles.addHitSparks(this.x + 8, this.y + 8, '#ffd700', 16);
            window.particles.addText(this.x + 8, this.y - 12, 'CHAVE ENCONTRADA!', '#ffeb3b');
            if (window.gameInstance) {
                window.gameInstance.score += 150;
            }
        }
    }

    draw(ctx) {
        if (this.collected) return;
        const img = window.sprites.get('key');
        if (!img) return;

        const sx = this.animFrame * 8;
        ctx.drawImage(img, sx, 0, 8, 8, Math.round(this.x), Math.round(this.y), 16, 16);
    }
}

class RuneGate {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 24;
        this.h = 32;
        this.unlocked = false;
        this.animTimer = 0;
        this.animFrame = 0;
    }

    update(dt, player) {
        this.animTimer += dt;
        this.animFrame = Math.floor(this.animTimer / 0.15) % 4;

        if (!this.unlocked && !player.isDead) {
            const dist = Math.abs((player.x + player.w / 2) - (this.x + this.w / 2));
            if (dist < 32 && Math.abs(player.y - this.y) < 28) {
                if (player.hasKey) {
                    this.unlocked = true;
                    player.hasKey = false;
                    window.sound.playChest();
                    window.particles.addHitSparks(this.x + 12, this.y + 16, '#4ecca3', 20);
                    window.particles.addText(this.x + 12, this.y - 12, 'PORTÃO DESBLOQUEADO!', '#4ecca3');
                }
            }
        }
    }

    draw(ctx, player) {
        if (this.unlocked) return; // Disappears when unlocked
        const img = window.sprites.get('rune');
        if (!img) return;

        const sx = this.animFrame * 16;
        ctx.drawImage(img, sx, 0, 16, 16, Math.round(this.x), Math.round(this.y), 24, 24);

        if (player && !player.isDead) {
            const dist = Math.abs((player.x + player.w / 2) - (this.x + this.w / 2));
            if (dist < 40 && Math.abs(player.y - this.y) < 28) {
                ctx.save();
                ctx.fillStyle = '#ff5555';
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.font = 'bold 9px monospace';
                ctx.textAlign = 'center';
                const msg = player.hasKey ? '[TEM A CHAVE!]' : '[PRECISA DA CHAVE]';
                ctx.strokeText(msg, Math.round(this.x + 12), Math.round(this.y - 8));
                ctx.fillText(msg, Math.round(this.x + 12), Math.round(this.y - 8));
                ctx.restore();
            }
        }
    }
}

class Chest {
    constructor(x, y, grantsUpgrade = false) {
        this.x = x;
        this.y = y;
        this.w = 32;
        this.h = 24;
        this.opened = false;
        this.grantsUpgrade = grantsUpgrade;
        this.animFrame = 0;
        this.animTimer = 0;
    }

    open() {
        if (this.opened) return;
        this.opened = true;
        window.sound.playChest();

        window.particles.addHitSparks(this.x + 16, this.y + 12, '#ffd700', 16);

        if (this.grantsUpgrade && window.gameInstance && window.gameInstance.player) {
            const nextLvl = window.gameInstance.player.heroLevel + 1;
            window.gameInstance.player.upgradeLevel(nextLvl);
        } else {
            window.particles.addText(this.x + 16, this.y - 12, '+50 BÔNUS!', '#ffeb3b');
        }

        if (window.gameInstance) {
            window.gameInstance.score += 50;
            window.gameInstance.coinsCount += 5;
            for (let i = 0; i < 4; i++) {
                const drop = new Coin(this.x + 8 + (Math.random() - 0.5) * 16, this.y - 8, true);
                drop.vy = -120 - Math.random() * 80;
                drop.vx = (Math.random() - 0.5) * 80;
                window.gameInstance.coins.push(drop);
            }
        }
    }

    update(dt, player) {
        if (this.opened && this.animFrame < 3) {
            this.animTimer += dt;
            this.animFrame = Math.min(3, Math.floor(this.animTimer / 0.1));
        }

        if (!this.opened && !player.isDead) {
            const dist = Math.abs((player.x + player.w / 2) - (this.x + this.w / 2));
            if (dist < 28 && Math.abs(player.y - this.y) < 24) {
                if (window.gameInstance && window.gameInstance.input.interactPressed) {
                    this.open();
                }
            }
        }
    }

    draw(ctx, player) {
        const img = window.sprites.get('chest');
        if (!img) return;

        const sx = this.animFrame * 32;
        ctx.drawImage(img, sx, 0, 32, 32, Math.round(this.x), Math.round(this.y - 8), 32, 32);

        if (!this.opened && player && !player.isDead) {
            const dist = Math.abs((player.x + player.w / 2) - (this.x + this.w / 2));
            if (dist < 32 && Math.abs(player.y - this.y) < 24) {
                ctx.save();
                ctx.fillStyle = '#ffffff';
                ctx.strokeStyle = '#000000';
                ctx.lineWidth = 2;
                ctx.font = 'bold 10px monospace';
                ctx.textAlign = 'center';
                const promptText = '[E] ABRIR';
                ctx.strokeText(promptText, Math.round(this.x + 16), Math.round(this.y - 14));
                ctx.fillText(promptText, Math.round(this.x + 16), Math.round(this.y - 14));
                ctx.restore();
            }
        }
    }
}

class GoalFlag {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 32;
        this.h = 48;
        this.animTimer = 0;
        this.animFrame = 0;
        this.triggered = false;
    }

    update(dt, player, runeGate = null) {
        this.animTimer += dt;
        this.animFrame = Math.floor(this.animTimer / 0.15) % 4;

        // If rune gate exists and is still locked, cannot trigger victory yet!
        if (runeGate && !runeGate.unlocked) return;

        if (!this.triggered && !player.isDead && checkAABB(this, player)) {
            this.triggered = true;
            if (window.gameInstance) {
                window.gameInstance.triggerVictory();
            }
        }
    }

    draw(ctx) {
        const img = window.sprites.get('flag');
        if (!img) return;

        const sx = this.animFrame * 48;
        ctx.drawImage(img, sx, 0, 48, 48, Math.round(this.x - 8), Math.round(this.y), 48, 48);
    }
}
