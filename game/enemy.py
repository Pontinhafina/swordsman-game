import pygame
import math
from game.settings import *
from game.sound import sound
from game.particles import particles

class OrcEnemy:
    def __init__(self, x, y, patrol_dist=100, orc_type='orc1'):
        self.start_x = float(x)
        self.x = float(x)
        self.y = float(y)
        self.orc_type = orc_type
        self.is_boss = (orc_type == 'orc3')

        self.w = 26 if self.is_boss else 20
        self.h = 32 if self.is_boss else 28
        self.speed = 65.0 if self.is_boss else (48.0 if orc_type == 'orc2' else 38.0)
        self.vx = self.speed
        self.vy = 0.0
        self.facing = 1 # 1 = right, -1 = left

        self.patrol_left = x - patrol_dist
        self.patrol_right = x + patrol_dist

        if self.is_boss:
            self.max_hp = 10
        elif orc_type == 'orc2':
            self.max_hp = 3
        else:
            self.max_hp = 2
        self.hp = self.max_hp

        self.is_dead = False
        self.death_timer = 0.0
        self.hurt_timer = 0.0
        self.attack_cooldown = 0.0
        self.is_attacking = False
        self.attack_hit_done = False
        self.enraged = False

        self.anim_timer = 0.0
        self.anim_frame = 0
        self.on_ground = False

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def take_damage(self, amount, knockback_dir=0):
        if self.is_dead:
            return
        self.hp -= amount
        self.hurt_timer = 0.32
        self.is_attacking = False

        kb = 35.0 if self.is_boss else 90.0
        self.vx = knockback_dir * kb
        self.vy = -70.0 if self.is_boss else -100.0

        sound.play('hit')
        spark_color = (229, 62, 62) if self.is_boss else (72, 187, 120)
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, spark_color, 16 if self.is_boss else 8)
        particles.add_text(self.x + self.w / 2, self.y - 6, f"-{amount}", (255, 80, 80))

        # Boss enrage at 50% HP
        if self.is_boss and not self.enraged and self.hp <= self.max_hp // 2:
            self.enraged = True
            self.speed = 85.0
            particles.trigger_screenshake(0.4, 6.0)
            particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, (255, 0, 50), 30)
            particles.add_text(self.x + self.w / 2, self.y - 22, "⚡ GENERAL ENFURECIDO! ⚡", (255, 50, 50))

        if self.hp <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.anim_frame = 0
        self.death_timer = 0.0
        self.vx = 0.0
        sound.play('death')

    def update(self, dt, player, level, enemies_list, coins_list):
        if self.is_dead:
            self.death_timer += dt
            self.vy += GRAVITY * dt
            self.y += self.vy * dt
            c = level.check_tile_collision(self.rect)
            if c and self.vy > 0:
                self.y = c.top - self.h
                self.vy = 0.0
            self.anim_frame = min(6, int(self.death_timer / 0.12))
            return

        if self.hurt_timer > 0.0:
            self.hurt_timer -= dt
            self.move_and_collide(dt, level)
            return

        if self.attack_cooldown > 0.0:
            self.attack_cooldown -= dt

        dx = (player.x + player.w / 2) - (self.x + self.w / 2)
        dy = (player.y + player.h / 2) - (self.y + self.h / 2)
        dist = math.hypot(dx, dy)

        # Attacking logic
        if self.is_attacking:
            self.anim_timer += dt
            frame_dur = 0.07 if self.is_boss else 0.09
            self.anim_frame = int(self.anim_timer / frame_dur)

            # Hit frames: 3 to 5
            if 3 <= self.anim_frame <= 5 and not self.attack_hit_done:
                reach = 28 if self.is_boss else 22
                ax = int(self.x + self.w - 4 if self.facing > 0 else self.x - reach)
                hit_box = pygame.Rect(ax, int(self.y + 4), reach, self.h - 4)

                if not player.is_dead and hit_box.colliderect(player.rect):
                    dmg = 2 if self.is_boss else 1
                    player.take_damage(dmg, self.facing)
                    self.attack_hit_done = True
                    if self.is_boss:
                        particles.trigger_screenshake(0.2, 5.0)

            if self.anim_frame >= 8:
                self.is_attacking = False
                self.attack_cooldown = 0.6 if (self.is_boss and self.enraged) else 1.0

            self.move_and_collide(dt, level)
            return

        # Check if in strike range
        attack_dist = 36 if self.is_boss else 28
        if dist < attack_dist and abs(dy) < 24 and self.attack_cooldown <= 0.0 and not player.is_dead:
            self.is_attacking = True
            self.attack_hit_done = False
            self.anim_timer = 0.0
            self.anim_frame = 0
            self.facing = 1 if dx > 0 else -1
            self.vx = 0.0
            return

        # Aggro / Chase
        sight_range = 180 if self.is_boss else (150 if self.orc_type == 'orc2' else 120)
        if dist < sight_range and abs(dy) < 48 and not player.is_dead:
            self.facing = 1 if dx > 0 else -1
            chase_mult = 1.3 if (self.is_boss and self.enraged) else 1.15
            self.vx = self.facing * self.speed * chase_mult
        else:
            # Patrol
            if self.facing > 0 and self.x >= self.patrol_right:
                self.facing = -1
            elif self.facing < 0 and self.x <= self.patrol_left:
                self.facing = 1
            self.vx = self.facing * self.speed

        # Ledge detection (don't walk into bottomless pits during patrol)
        if self.on_ground and dist >= sight_range:
            check_px = self.x + self.w + 4 if self.facing > 0 else self.x - 4
            if not level.is_tile_solid_at_pixel(check_px, self.y + self.h + 8):
                self.facing = -self.facing
                self.vx = self.facing * self.speed

        self.move_and_collide(dt, level)

        # Contact damage
        if not player.is_dead and self.rect.colliderect(player.rect):
            player.take_damage(1, 1 if dx > 0 else -1)

    def move_and_collide(self, dt, level):
        self.vy += GRAVITY * dt
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # Horizontal
        self.x += self.vx * dt
        c_x = level.check_tile_collision(self.rect)
        if c_x:
            if self.vx > 0:
                self.x = c_x.left - self.w - 0.01
            elif self.vx < 0:
                self.x = c_x.right + 0.01
            self.facing = -self.facing
            self.vx = self.facing * abs(self.vx)

        # Vertical
        self.y += self.vy * dt
        self.on_ground = False
        c_y = level.check_tile_collision(self.rect)
        if c_y:
            if self.vy > 0:
                self.y = c_y.top - self.h - 0.01
                self.vy = 0.0
                self.on_ground = True
            elif self.vy < 0:
                self.y = c_y.bottom + 0.01
                self.vy = 0.0

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        prefix = f"{self.orc_type}_"
        row = 2
        frame_idx = 0

        if self.is_dead:
            img_key = prefix + "death"
            frame_idx = self.anim_frame
        elif self.is_attacking:
            img_key = prefix + "attack"
            frame_idx = min(7, self.anim_frame)
        elif self.hurt_timer > 0.0:
            img_key = prefix + "hurt"
            frame_idx = min(4, int(self.anim_timer / 0.08))
        else:
            img_key = prefix + "run"
            self.anim_timer += 0.016
            frame_idx = int(self.anim_timer / 0.11) % 8

        sheet = sprite_mgr.get(img_key)
        if not sheet:
            pygame.draw.rect(surface, (72, 187, 120), (int(self.x - cam_x), int(self.y - cam_y), self.w, self.h))
            return

        sub_rect = pygame.Rect(frame_idx * 64, row * 64, 64, 64)
        frame_surf = sheet.subsurface(sub_rect)

        # Note: Raw Orc sheet naturally faces LEFT, so when facing RIGHT (> 0), flip horizontally!
        if self.facing > 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)

        if self.is_boss:
            frame_surf = pygame.transform.scale(frame_surf, (76, 76))
            draw_x = int(self.x + self.w / 2 - 38 - cam_x)
            draw_y = int(self.y + self.h - 50 - cam_y)
        else:
            draw_x = int(self.x + self.w / 2 - 31 - cam_x)
            draw_y = int(self.y + self.h - 42 - cam_y)

        surface.blit(frame_surf, (draw_x, draw_y))

        # Health bar (non-boss)
        if not self.is_dead and not self.is_boss and self.hp < self.max_hp:
            bx = int(self.x - cam_x - 2)
            by = int(self.y - cam_y - 10)
            pygame.draw.rect(surface, (0, 0, 0), (bx, by, 24, 4))
            hp_w = int((self.hp / self.max_hp) * 22)
            c = (237, 137, 54) if self.orc_type == 'orc2' else (72, 187, 120)
            pygame.draw.rect(surface, c, (bx + 1, by + 1, hp_w, 2))
