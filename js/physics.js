// Physics, Collision Detection & Particle System

class Particle {
    constructor(x, y, vx, vy, color, size, life, gravity = 0.2) {
        this.x = x;
        this.y = y;
        this.vx = vx;
        this.vy = vy;
        this.color = color;
        this.size = size;
        this.life = life;
        this.maxLife = life;
        this.gravity = gravity;
    }

    update(dt) {
        this.x += this.vx;
        this.y += this.vy;
        this.vy += this.gravity;
        this.life -= dt;
    }

    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = this.color;
        ctx.fillRect(Math.round(this.x), Math.round(this.y), this.size, this.size);
        ctx.restore();
    }
}

class FloatingText {
    constructor(x, y, text, color = '#ffd700', life = 0.8) {
        this.x = x;
        this.y = y;
        this.text = text;
        this.color = color;
        this.life = life;
        this.maxLife = life;
    }

    update(dt) {
        this.y -= 30 * dt;
        this.life -= dt;
    }

    draw(ctx) {
        const alpha = Math.max(0, this.life / this.maxLife);
        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.fillStyle = this.color;
        ctx.font = 'bold 12px "Courier New", monospace';
        ctx.textAlign = 'center';
        ctx.fillText(this.text, Math.round(this.x), Math.round(this.y));
        ctx.restore();
    }
}

class ParticleSystem {
    constructor() {
        this.particles = [];
        this.floatingTexts = [];
    }

    update(dt) {
        for (let i = this.particles.length - 1; i >= 0; i--) {
            this.particles[i].update(dt);
            if (this.particles[i].life <= 0) {
                this.particles.splice(i, 1);
            }
        }
        for (let i = this.floatingTexts.length - 1; i >= 0; i--) {
            this.floatingTexts[i].update(dt);
            if (this.floatingTexts[i].life <= 0) {
                this.floatingTexts.splice(i, 1);
            }
        }
    }

    draw(ctx) {
        this.particles.forEach(p => p.draw(ctx));
        this.floatingTexts.forEach(t => t.draw(ctx));
    }

    addHitSparks(x, y, color = '#ffe066', count = 8) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 1.5 + Math.random() * 3.5;
            this.particles.push(new Particle(
                x, y,
                Math.cos(angle) * speed,
                Math.sin(angle) * speed,
                color,
                Math.random() < 0.5 ? 2 : 3,
                0.25 + Math.random() * 0.25,
                0.15
            ));
        }
    }

    addDust(x, y, count = 4) {
        for (let i = 0; i < count; i++) {
            const vx = (Math.random() - 0.5) * 1.5;
            const vy = -Math.random() * 1.2;
            this.particles.push(new Particle(
                x + (Math.random() - 0.5) * 8, y,
                vx, vy,
                '#99a882',
                2,
                0.3 + Math.random() * 0.2,
                0.05
            ));
        }
    }

    addCoinSparkle(x, y, count = 6) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 1.0 + Math.random() * 2.0;
            this.particles.push(new Particle(
                x, y,
                Math.cos(angle) * speed,
                Math.sin(angle) * speed - 1.0,
                '#ffeb3b',
                2,
                0.4 + Math.random() * 0.2,
                0.1
            ));
        }
    }

    addText(x, y, text, color = '#ffd700') {
        this.floatingTexts.push(new FloatingText(x, y, text, color));
    }

    clear() {
        this.particles = [];
        this.floatingTexts = [];
    }
}

window.particles = new ParticleSystem();

// Box overlap helper
function checkAABB(a, b) {
    return (
        a.x < b.x + b.w &&
        a.x + a.w > b.x &&
        a.y < b.y + b.h &&
        a.y + a.h > b.y
    );
}
