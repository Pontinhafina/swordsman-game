import pygame
import math
import random
from game.sound import sound
from game.particles import particles
from game.settings import *

class Coin:
    def __init__(self, x, y, is_drop=False):
        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)
        self.w = 12
        self.h = 12
        self.is_drop = is_drop
        self.vy = -120.0 if is_drop else 0.0
        self.vx = random.uniform(-40, 40) if is_drop else 0.0
        self.collected = False
        self.hover_time = random.uniform(0, math.pi * 2)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player, level, game_stats):
        if self.collected:
            return

        if self.is_drop:
            self.vy += GRAVITY * dt
            self.x += self.vx * dt
            self.y += self.vy * dt
            c = level.check_tile_collision(self.rect)
            if c and self.vy > 0:
                self.y = c.top - self.h
                self.vy = 0
                self.vx = 0
                self.base_y = self.y
                self.is_drop = False
        else:
            self.hover_time += dt * 3.5
            self.y = self.base_y + math.sin(self.hover_time) * 3.0

        if not player.is_dead and self.rect.colliderect(player.rect):
            self.collect(game_stats)

    def collect(self, game_stats):
        self.collected = True
        sound.play('coin')
        particles.add_hit_sparks(self.x + 6, self.y + 6, COLOR_GOLD, 8)
        particles.add_text(self.x + 6, self.y - 6, "+10", COLOR_GOLD)
        game_stats['score'] += 10
        game_stats['coins'] += 1

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.collected:
            return
        img = sprite_mgr.get('coin')
        if not img:
            return
        frame_idx = int(self.hover_time * 2.0) % 4
        sub_rect = pygame.Rect(frame_idx * 10, 0, 10, 10)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y)))

class PotionItem:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)
        self.w = 16
        self.h = 20
        self.collected = False
        self.anim_timer = random.uniform(0, math.pi * 2)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player):
        if self.collected:
            return
        self.anim_timer += dt * 3.0
        self.y = self.base_y + math.sin(self.anim_timer) * 3.0

        if not player.is_dead and self.rect.colliderect(player.rect):
            if player.hp < player.max_hp:
                self.collected = True
                heal = min(player.max_hp - player.hp, 2)
                player.hp += heal
                sound.play('potion')
                particles.add_hit_sparks(self.x + 8, self.y + 10, COLOR_GREEN, 16)
                particles.add_text(self.x + 8, self.y - 10, f"+{heal} VIDA!", COLOR_GREEN)

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.collected:
            return
        img = sprite_mgr.get('potion')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 4
        sub_rect = pygame.Rect(frame_idx * 24, 0, 24, 24)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x - 4), int(self.y - cam_y - 2)))

class GemItem:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)
        self.w = 16
        self.h = 16
        self.collected = False
        self.anim_timer = random.uniform(0, math.pi * 2)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player, game_stats):
        if self.collected:
            return
        self.anim_timer += dt * 3.2
        self.y = self.base_y + math.sin(self.anim_timer) * 3.0

        if not player.is_dead and self.rect.colliderect(player.rect):
            self.collected = True
            sound.play('coin')
            particles.add_hit_sparks(self.x + 8, self.y + 8, COLOR_CYAN, 20)
            particles.add_text(self.x + 8, self.y - 12, "+100 RELÍQUIA!", COLOR_CYAN)
            game_stats['score'] += 100

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.collected:
            return
        img = sprite_mgr.get('gem')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 4
        sub_rect = pygame.Rect(frame_idx * 24, 0, 24, 24)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x - 4), int(self.y - cam_y - 4)))

class CheckpointTorch:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 24
        self.h = 44
        self.lit = False
        self.anim_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x + 4), int(self.y + 4), self.w, self.h)

    def update(self, dt, player):
        if self.lit:
            self.anim_timer += dt * 8.0

        if not self.lit and not player.is_dead and self.rect.colliderect(player.rect):
            self.lit = True
            player.respawn_checkpoint = (self.x, self.y - 4)
            player.hp = player.max_hp
            sound.play('checkpoint')
            particles.add_hit_sparks(self.x + 16, self.y + 14, COLOR_GOLD, 25)
            particles.add_text(self.x + 16, self.y - 14, "CHECKPOINT ATIVADO!", COLOR_GOLD)

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('checkpoint_torch')
        if not img:
            return
        frame_idx = (1 + int(self.anim_timer) % 4) if self.lit else 0
        sub_rect = pygame.Rect(frame_idx * 32, 0, 32, 48)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y)))

class Spikes:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 24

    @property
    def rect(self):
        # Precise collision box (top spikes hurt, not base air)
        return pygame.Rect(int(self.x + 3), int(self.y + 10), self.w - 6, self.h - 10)

    @property
    def pogo_box(self):
        # Generous top box to bounce on with downthrust!
        return pygame.Rect(int(self.x), int(self.y + 4), self.w, 14)

    def update(self, dt, player):
        if player.is_dead or player.invulnerable_timer > 0.0:
            return

        if self.rect.colliderect(player.rect):
            # Check if player is performing pogo downwards!
            if player.is_pogo and player.vy > 0:
                player.vy = POGO_BOUNCE_FORCE
                player.is_attacking = False
                player.is_pogo = False
                sound.play('pogo')
                particles.add_hit_sparks(player.x + player.w / 2, self.y + 6, COLOR_GOLD, 16)
                particles.add_text(player.x + player.w / 2, player.y - 14, "SPIKE POGO!", COLOR_GOLD)
            else:
                player.take_damage(1, knockback_dir=(-1 if player.x < self.x + 16 else 1))

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('spikes')
        if not img:
            return
        surface.blit(img, (int(self.x - cam_x), int(self.y - cam_y)))

class SawBlade:
    def __init__(self, x, y, patrol_distance=0, speed=60.0, is_vertical=False):
        self.base_x = float(x)
        self.base_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.patrol_distance = float(patrol_distance)
        self.speed = float(speed)
        self.is_vertical = is_vertical
        self.direction = 1
        self.anim_timer = 0.0
        self.w = 26
        self.h = 26

    @property
    def rect(self):
        return pygame.Rect(int(self.x + 3), int(self.y + 3), self.w, self.h)

    def update(self, dt, player):
        self.anim_timer += dt * 14.0

        if self.patrol_distance > 0:
            if self.is_vertical:
                self.y += self.direction * self.speed * dt
                if self.y > self.base_y + self.patrol_distance:
                    self.direction = -1
                elif self.y < self.base_y:
                    self.direction = 1
            else:
                self.x += self.direction * self.speed * dt
                if self.x > self.base_x + self.patrol_distance:
                    self.direction = -1
                elif self.x < self.base_x:
                    self.direction = 1

        if not player.is_dead and player.invulnerable_timer <= 0.0:
            if self.rect.colliderect(player.rect):
                if player.is_pogo and player.vy > 0:
                    player.vy = POGO_BOUNCE_FORCE
                    player.is_attacking = False
                    player.is_pogo = False
                    sound.play('pogo')
                    particles.add_hit_sparks(self.x + 16, self.y + 16, COLOR_GOLD, 16)
                    particles.add_text(player.x + player.w / 2, player.y - 14, "SAW POGO!", COLOR_GOLD)
                else:
                    player.take_damage(1, knockback_dir=(-1 if player.x < self.x + 16 else 1))

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('saw_blade')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 4
        sub_rect = pygame.Rect(frame_idx * 32, 0, 32, 32)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y)))

class MovingPlatform:
    def __init__(self, x, y, distance_x=0, distance_y=0, speed=50.0):
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.target_x = float(x + distance_x)
        self.target_y = float(y + distance_y)
        self.speed = float(speed)
        self.w = 64
        self.h = 16
        self.progress = 0.0
        self.forward = True

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player):
        total_dist = math.hypot(self.target_x - self.start_x, self.target_y - self.start_y)
        if total_dist <= 0:
            return

        step = (self.speed * dt) / total_dist
        if self.forward:
            self.progress += step
            if self.progress >= 1.0:
                self.progress = 1.0
                self.forward = False
        else:
            self.progress -= step
            if self.progress <= 0.0:
                self.progress = 0.0
                self.forward = True

        prev_x = self.x
        prev_y = self.y
        self.x = self.start_x + (self.target_x - self.start_x) * self.progress
        self.y = self.start_y + (self.target_y - self.start_y) * self.progress

        dx = self.x - prev_x
        dy = self.y - prev_y

        # If player is standing on this platform, carry them!
        if not player.is_dead:
            foot_box = pygame.Rect(int(player.x), int(player.y + player.h - 2), player.w, 4)
            if foot_box.colliderect(self.rect) and player.vy >= 0:
                player.x += dx
                player.y = self.y - player.h
                player.vy = 0.0
                player.on_ground = True

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('moving_plat')
        if not img:
            return
        surface.blit(img, (int(self.x - cam_x), int(self.y - cam_y)))

class CrackedWall:
    def __init__(self, x, y, drops_chest=False):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 32
        self.destroyed = False
        self.hp = 2
        self.drops_chest = drops_chest

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def hit(self, dmg=1):
        if self.destroyed:
            return
        self.hp -= dmg
        sound.play('break')
        particles.add_hit_sparks(self.x + 16, self.y + 16, (140, 150, 165), 14)
        particles.trigger_screenshake(0.12, 3.5)
        if self.hp <= 0:
            self.destroyed = True
            sound.play('break')
            particles.add_hit_sparks(self.x + 16, self.y + 16, COLOR_GOLD, 25)
            particles.add_text(self.x + 16, self.y - 10, "PAREDE QUEBRADA!", COLOR_GOLD)

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.destroyed:
            return
        img = sprite_mgr.get('cracked_wall')
        if not img:
            return
        surface.blit(img, (int(self.x - cam_x), int(self.y - cam_y)))

class KeyItem:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.base_y = float(y)
        self.w = 16
        self.h = 16
        self.collected = False
        self.anim_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player, game_stats):
        if self.collected:
            return
        self.anim_timer += dt
        self.y = self.base_y + math.sin(self.anim_timer * 3.0) * 4.0

        if not player.is_dead and self.rect.colliderect(player.rect):
            self.collected = True
            player.has_key = True
            sound.play('chest')
            particles.add_hit_sparks(self.x + 8, self.y + 8, COLOR_GOLD, 16)
            particles.add_text(self.x + 8, self.y - 14, "CHAVE DOURADA!", (255, 235, 60))
            game_stats['score'] += 150

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.collected:
            return
        img = sprite_mgr.get('key')
        if not img:
            return
        frame_idx = int(self.anim_timer / 0.1) % 6
        sub_rect = pygame.Rect(frame_idx * 8, 0, 8, 8)
        frame_surf = pygame.transform.scale(img.subsurface(sub_rect), (16, 16))
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y)))

class RuneGate:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 24
        self.h = 32
        self.unlocked = False
        self.anim_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player):
        if self.unlocked:
            return
        self.anim_timer += dt

        if not player.is_dead and self.rect.colliderect(player.rect):
            if player.has_key:
                self.unlocked = True
                player.has_key = False
                sound.play('chest')
                particles.add_hit_sparks(self.x + 12, self.y + 16, COLOR_GREEN, 24)
                particles.add_text(self.x + 12, self.y - 14, "PORTÃO DESBLOQUEADO!", COLOR_GREEN)

    def draw(self, surface, sprite_mgr, font, player, cam_x, cam_y):
        if self.unlocked:
            return
        img = sprite_mgr.get('rune')
        if not img:
            return
        frame_idx = int(self.anim_timer / 0.15) % 4
        sub_rect = pygame.Rect(frame_idx * 16, 0, 16, 16)
        frame_surf = pygame.transform.scale(img.subsurface(sub_rect), (24, 24))
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y)))

        if player and not player.is_dead and abs(player.x - self.x) < 40 and abs(player.y - self.y) < 28:
            msg = "[TEM A CHAVE!]" if player.has_key else "[PRECISA DA CHAVE]"
            color = (100, 255, 100) if player.has_key else (255, 80, 80)
            txt = font.render(msg, False, color)
            surface.blit(txt, (int(self.x - cam_x + 12 - txt.get_width() / 2), int(self.y - cam_y - 12)))

class Chest:
    def __init__(self, x, y, grants_upgrade=False):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 24
        self.opened = False
        self.grants_upgrade = grants_upgrade
        self.anim_frame = 0
        self.anim_timer = 0.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def open(self, player):
        if self.opened:
            return
        self.opened = True
        sound.play('chest')
        particles.add_hit_sparks(self.x + 16, self.y + 12, COLOR_GOLD, 20)

        if self.grants_upgrade:
            player.upgrade_level(player.hero_level + 1)
        else:
            particles.add_text(self.x + 16, self.y - 12, "+50 BÔNUS!", (255, 235, 60))

    def update(self, dt, player, keys):
        if self.opened and self.anim_frame < 3:
            self.anim_timer += dt
            self.anim_frame = min(3, int(self.anim_timer / 0.08))

        if not self.opened and not player.is_dead:
            if abs(player.x - self.x) < 32 and abs(player.y - self.y) < 24:
                if keys.get('interact_pressed'):
                    self.open(player)

    def draw(self, surface, sprite_mgr, font, player, cam_x, cam_y):
        img = sprite_mgr.get('chest')
        if not img:
            return
        sub_rect = pygame.Rect(self.anim_frame * 32, 0, 32, 32)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x), int(self.y - cam_y - 8)))

        if not self.opened and player and not player.is_dead:
            if abs(player.x - self.x) < 32 and abs(player.y - self.y) < 24:
                txt = font.render("[E] ABRIR", False, (255, 255, 255))
                surface.blit(txt, (int(self.x - cam_x + 16 - txt.get_width() / 2), int(self.y - cam_y - 18)))

class GoalFlag:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.w = 32
        self.h = 48
        self.anim_timer = 0.0
        self.triggered = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def update(self, dt, player, rune_gate=None):
        self.anim_timer += dt
        if rune_gate and not rune_gate.unlocked:
            return False

        if not self.triggered and not player.is_dead and self.rect.colliderect(player.rect):
            self.triggered = True
            sound.play('victory')
            return True
        return False

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('flag')
        if not img:
            return
        frame_idx = int(self.anim_timer / 0.15) % 4
        sub_rect = pygame.Rect(frame_idx * 48, 0, 48, 48)
        frame_surf = img.subsurface(sub_rect)
        surface.blit(frame_surf, (int(self.x - cam_x - 8), int(self.y - cam_y)))
