import pygame
import random
import math

class Particle:
    def __init__(self, x, y, vx, vy, color, size, life, gravity=0.2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = life
        self.max_life = life
        self.gravity = gravity

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.life -= dt

    def draw(self, surface, cam_x, cam_y):
        alpha = max(0.0, self.life / self.max_life)
        s = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        c = (self.color[0], self.color[1], self.color[2], int(alpha * 255))
        s.fill(c)
        surface.blit(s, (int(self.x - cam_x), int(self.y - cam_y)))

class FloatingText:
    def __init__(self, x, y, text, color=(255, 215, 0), font=None):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 0.8
        self.max_life = 0.8
        self.font = font

    def update(self, dt):
        self.y -= 25 * dt
        self.life -= dt

    def draw(self, surface, cam_x, cam_y):
        if not self.font:
            return
        alpha = max(0.0, self.life / self.max_life)
        txt_surf = self.font.render(self.text, False, self.color)
        txt_surf.set_alpha(int(alpha * 255))
        surface.blit(txt_surf, (int(self.x - cam_x - txt_surf.get_width() / 2), int(self.y - cam_y)))

class ParticleManager:
    def __init__(self):
        self.particles = []
        self.texts = []
        self.shake_timer = 0.0
        self.shake_magnitude = 0.0
        self.hitstop_timer = 0.0
        self.font = None

    def init_font(self):
        if not self.font:
            self.font = pygame.font.Font(None, 18)

    def trigger_screenshake(self, duration=0.2, magnitude=4.0):
        self.shake_timer = duration
        self.shake_magnitude = magnitude

    def trigger_hitstop(self, duration=0.06):
        self.hitstop_timer = duration

    def add_hit_sparks(self, x, y, color=(255, 220, 60), count=10):
        for _ in range(count):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(1.5, 4.0)
            self.particles.append(Particle(
                x, y,
                math.cos(angle) * speed,
                math.sin(angle) * speed,
                color,
                random.choice([2, 3]),
                random.uniform(0.2, 0.4),
                0.15
            ))

    def add_dust(self, x, y, count=5):
        for _ in range(count):
            vx = random.uniform(-1.0, 1.0)
            vy = random.uniform(-1.2, -0.2)
            self.particles.append(Particle(
                x + random.uniform(-4, 4), y,
                vx, vy,
                (160, 175, 140),
                2,
                random.uniform(0.25, 0.45),
                0.05
            ))

    def add_text(self, x, y, text, color=(255, 215, 0)):
        self.init_font()
        self.texts.append(FloatingText(x, y, text, color, self.font))

    def update(self, dt):
        if self.hitstop_timer > 0.0:
            self.hitstop_timer -= dt
            return True # In hitstop, world updates pause for weight

        if self.shake_timer > 0.0:
            self.shake_timer -= dt

        for p in self.particles[:]:
            p.update(dt)
            if p.life <= 0:
                self.particles.remove(p)

        for t in self.texts[:]:
            t.update(dt)
            if t.life <= 0:
                self.texts.remove(t)

        return False

    def get_shake_offset(self):
        if self.shake_timer > 0.0:
            ox = random.uniform(-self.shake_magnitude, self.shake_magnitude)
            oy = random.uniform(-self.shake_magnitude, self.shake_magnitude)
            return ox, oy
        return 0, 0

    def draw(self, surface, cam_x, cam_y):
        for p in self.particles:
            p.draw(surface, cam_x, cam_y)
        for t in self.texts:
            t.draw(surface, cam_x, cam_y)

    def clear(self):
        self.particles.clear()
        self.texts.clear()
        self.shake_timer = 0
        self.hitstop_timer = 0

particles = ParticleManager()
