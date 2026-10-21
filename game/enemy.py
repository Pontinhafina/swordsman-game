import pygame
import math
import random
from game.settings import *
from game.sound import sound
from game.particles import particles
from game.objects import BossShockwave

class OrcEnemy:
    def __init__(self, x, y, patrol_dist=100, orc_type='orc1'):
        self.start_x = float(x)
        self.x = float(x)
        self.y = float(y)
        self.orc_type = orc_type
        self.is_boss = (orc_type == 'orc3')

        self.w = 26 if self.is_boss else 20
        self.h = 32 if self.is_boss else 28
        self.speed = 68.0 if self.is_boss else (48.0 if orc_type == 'orc2' else 38.0)
        self.vx = self.speed
        self.vy = 0.0
        self.facing = 1 # 1 = right, -1 = left

        self.patrol_left = x - patrol_dist
        self.patrol_right = x + patrol_dist

        if self.is_boss:
            self.max_hp = 14
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

        # Boss Intelligent AI States
        self.boss_state = 'chase' # 'chase', 'melee', 'slam_windup', 'slam_air', 'charge', 'retreat'
        self.boss_timer = 0.0
        self.charge_vx = 0.0
        self.hits_in_streak = 0
        self.minions_summoned = False

        self.anim_timer = 0.0
        self.anim_frame = 0
        self.on_ground = False

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.w, self.h)

    def take_damage(self, amount, knockback_dir=0):
        if self.is_dead:
            return
        self.hp -= amount
        self.hurt_timer = 0.28
        self.is_attacking = False
        self.hits_in_streak += 1

        kb = 30.0 if self.is_boss else 95.0
        self.vx = knockback_dir * kb
        self.vy = -60.0 if self.is_boss else -100.0

        sound.play('hit')
        spark_color = (255, 60, 60) if self.is_boss else (72, 187, 120)
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, spark_color, 18 if self.is_boss else 8)
        particles.add_text(self.x + self.w / 2, self.y - 6, f"-{amount}", (255, 80, 80))

        # Boss Smart Reaction: Leaps back after taking 2 hits to create tactical distance!
        if self.is_boss and self.hits_in_streak >= 2 and not self.is_dead:
            self.hits_in_streak = 0
            self.boss_state = 'retreat'
            self.boss_timer = 0.4
            self.vx = -self.facing * 140.0
            self.vy = -180.0
            particles.add_text(self.x + self.w / 2, self.y - 18, "RECUO TÁTICO!", COLOR_GOLD)

        # Boss enrage at 50% HP
        if self.is_boss and not self.enraged and self.hp <= self.max_hp // 2:
            self.enraged = True
            self.speed = 92.0
            sound.play('boss_roar')
            particles.trigger_screenshake(0.45, 7.0)
            particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, (255, 0, 50), 35)
            particles.add_text(self.x + self.w / 2, self.y - 22, "⚡ GENERAL ENFURECIDO! ⚡", (255, 50, 50))

        if self.hp <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.anim_frame = 0
        self.death_timer = 0.0
        self.vx = 0.0
        sound.play('death')
        if self.is_boss:
            sound.play('victory')
            particles.trigger_screenshake(0.5, 8.0)
            particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_GOLD, 50)
            particles.add_text(self.x + self.w / 2, self.y - 20, "GENERAL DERROTADO!", COLOR_GOLD)

    def update(self, dt, player, level, enemies_list, coins_list):
        if self.is_dead:
            self.death_timer += dt
            self.vy += GRAVITY * dt
            self.y += self.vy * dt
            c = level.check_tile_collision(self.rect)
            if c and self.vy > 0:
                self.y = float(c.top - self.h)
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

        # =====================================================================
        # INTELLIGENT BOSS AI (Orc 3 General)
        # =====================================================================
        if self.is_boss:
            self.update_boss_ai(dt, player, level, enemies_list, dx, dy, dist)
            return

        # =====================================================================
        # STANDARD ORC AI (Orc 1 & Orc 2)
        # =====================================================================
        if self.is_attacking:
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.08)

            # Hit frames: 3 to 5
            if 3 <= self.anim_frame <= 5 and not self.attack_hit_done:
                reach = 22
                ax = int(self.x + self.w - 4 if self.facing > 0 else self.x - reach)
                hit_box = pygame.Rect(ax, int(self.y + 4), reach, self.h - 4)

                if not player.is_dead and hit_box.colliderect(player.rect):
                    player.take_damage(1, self.facing)
                    self.attack_hit_done = True

            if self.anim_frame >= 8:
                self.is_attacking = False
                self.attack_cooldown = 1.0

            self.move_and_collide(dt, level)
            return

        # Check if in strike range
        if dist < 28 and abs(dy) < 24 and self.attack_cooldown <= 0.0 and not player.is_dead:
            self.is_attacking = True
            self.attack_hit_done = False
            self.anim_timer = 0.0
            self.anim_frame = 0
            self.facing = 1 if dx > 0 else -1
            self.vx = 0.0
            return

        # Aggro / Chase
        sight_range = 150 if self.orc_type == 'orc2' else 120
        if dist < sight_range and abs(dy) < 48 and not player.is_dead:
            self.facing = 1 if dx > 0 else -1
            self.vx = self.facing * self.speed * 1.15
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

    def update_boss_ai(self, dt, player, level, enemies_list, dx, dy, dist):
        self.boss_timer -= dt

        # Spawn minion scouts once upon entering Phase 2
        if self.enraged and not self.minions_summoned:
            self.minions_summoned = True
            enemies_list.append(OrcEnemy(self.x - 40, self.y, 40, 'orc1'))
            enemies_list.append(OrcEnemy(self.x + 60, self.y, 40, 'orc1'))
            particles.add_text(self.x + self.w / 2, self.y - 26, "INVOCAÇÃO DE BATEDORES!", COLOR_RED)

        # State 1: Retreat
        if self.boss_state == 'retreat':
            if self.boss_timer <= 0 or self.on_ground:
                # Decide next move: Ground slam or Charge!
                self.boss_state = 'slam_windup' if random.random() < 0.55 else 'charge'
                self.boss_timer = 0.45
            self.move_and_collide(dt, level)
            return

        # State 2: Ground Slam Windup
        if self.boss_state == 'slam_windup':
            self.vx = 0.0
            self.facing = 1 if dx > 0 else -1
            if self.boss_timer <= 0:
                # Leap into air!
                self.boss_state = 'slam_air'
                self.vy = -260.0
                self.vx = self.facing * 80.0
                particles.add_text(self.x + self.w / 2, self.y - 18, "⚡ IMPACTO DE CHÃO! ⚡", COLOR_GOLD)
            self.move_and_collide(dt, level)
            return

        # State 3: Ground Slam in Air
        if self.boss_state == 'slam_air':
            self.move_and_collide(dt, level)
            if self.on_ground and self.vy >= 0:
                # SLAM DOWN!
                sound.play('boss_slam')
                particles.trigger_screenshake(0.35, 6.5)
                particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h, (255, 140, 20), 30)

                # Emit shockwaves left and right!
                sw_speed = 180.0 if self.enraged else 140.0
                level.shockwaves.append(BossShockwave(self.x - 12, self.y + self.h - 22, direction=-1, speed=sw_speed))
                level.shockwaves.append(BossShockwave(self.x + self.w, self.y + self.h - 22, direction=1, speed=sw_speed))

                self.boss_state = 'chase'
                self.attack_cooldown = 1.0 if self.enraged else 1.6
            return

        # State 4: Shield Charge
        if self.boss_state == 'charge':
            if self.boss_timer > 0.35: # Telegraph windup
                self.vx = 0.0
                self.facing = 1 if dx > 0 else -1
                particles.add_text(self.x + self.w / 2, self.y - 16, "⚡ CARGA FURADA! ⚡", COLOR_RED)
            else: # Actual charge
                charge_speed = 190.0 if self.enraged else 160.0
                self.vx = self.facing * charge_speed
                if self.boss_timer <= 0:
                    self.boss_state = 'chase'
                    self.attack_cooldown = 1.2
            self.move_and_collide(dt, level)

            # High contact damage during charge
            if not player.is_dead and self.rect.colliderect(player.rect):
                player.take_damage(2, self.facing)
            return

        # State 5: Melee Attack
        if self.is_attacking:
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.065)

            if 2 <= self.anim_frame <= 5 and not self.attack_hit_done:
                reach = 32
                ax = int(self.x + self.w - 4 if self.facing > 0 else self.x - reach)
                hit_box = pygame.Rect(ax, int(self.y + 2), reach, self.h)

                if not player.is_dead and hit_box.colliderect(player.rect):
                    player.take_damage(2, self.facing)
                    self.attack_hit_done = True
                    particles.trigger_screenshake(0.2, 5.0)

            if self.anim_frame >= 8:
                self.is_attacking = False
                self.boss_state = 'chase'
                self.attack_cooldown = 0.5 if self.enraged else 0.9

            self.move_and_collide(dt, level)
            return

        # Default: Chase & Tactical Selection
        self.facing = 1 if dx > 0 else -1

        # In melee range: Slash!
        if dist < 38 and abs(dy) < 28 and self.attack_cooldown <= 0.0:
            self.is_attacking = True
            self.attack_hit_done = False
            self.anim_timer = 0.0
            self.anim_frame = 0
            self.vx = 0.0
            return

        # Medium distance: Randomly choose between Slam or Charge when cooldown expires!
        if dist > 60 and self.attack_cooldown <= 0.0 and random.random() < 0.03:
            choice = random.choice(['slam', 'charge'])
            if choice == 'slam':
                self.boss_state = 'slam_windup'
                self.boss_timer = 0.4
            else:
                self.boss_state = 'charge'
                self.boss_timer = 0.8
            return

        # If player is high above on platforms: Leap up to challenge!
        if dy < -45 and abs(dx) < 70 and self.on_ground and random.random() < 0.04:
            self.vy = -270.0
            self.vx = self.facing * 75.0
            particles.add_text(self.x + self.w / 2, self.y - 14, "SALTO DE GUERRA!", COLOR_GOLD)

        chase_mult = 1.35 if self.enraged else 1.10
        self.vx = self.facing * self.speed * chase_mult
        self.move_and_collide(dt, level)

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
                self.x = float(c_x.left - self.w)
            elif self.vx < 0:
                self.x = float(c_x.right)
            self.facing = -self.facing
            self.vx = self.facing * abs(self.vx)

        # Vertical
        self.y += self.vy * dt
        c_y = level.check_tile_collision(self.rect)
        if c_y:
            if self.vy > 0:
                self.y = float(c_y.top - self.h)
                self.vy = 0.0
                self.on_ground = True
            elif self.vy < 0:
                self.y = float(c_y.bottom)
                self.vy = 0.0
        else:
            if self.vy >= 0:
                probe = pygame.Rect(round(self.x) + 2, round(self.y) + self.h, self.w - 4, 3)
                ground_tile = level.check_tile_collision(probe)
                if ground_tile:
                    self.y = float(ground_tile.top - self.h)
                    self.vy = 0.0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = False

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

        # Orc sheets face LEFT by default, so invert flip
        if self.facing > 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)

        if self.is_boss:
            frame_surf = pygame.transform.scale(frame_surf, (80, 80))
            if self.enraged and int(pygame.time.get_ticks() / 100) % 2 == 0:
                # Red rage glow
                frame_surf.fill((255, 60, 60, 100), special_flags=pygame.BLEND_RGB_ADD)
            draw_x = int(self.x + self.w / 2 - 40 - cam_x)
            draw_y = int(self.y + self.h - 52 - cam_y)
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

class BatEnemy:
    def __init__(self, x, y, patrol_dist=80):
        self.start_x = float(x)
        self.start_y = float(y)
        self.x = float(x)
        self.y = float(y)
        self.w = 20
        self.h = 16
        self.speed = 55.0
        self.patrol_dist = patrol_dist
        self.facing = 1
        self.hp = 1
        self.max_hp = 1
        self.is_dead = False
        self.death_timer = 0.0
        self.anim_timer = random.uniform(0, math.pi * 2)
        self.is_boss = False
        self.orc_type = 'bat'

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.w, self.h)

    def take_damage(self, amount, knockback_dir=0):
        if self.is_dead:
            return
        self.hp = 0
        self.is_dead = True
        sound.play('hit')
        particles.add_hit_sparks(self.x + 10, self.y + 8, (160, 100, 200), 12)
        particles.add_text(self.x + 10, self.y - 8, "-1", COLOR_GOLD)

    def update(self, dt, player, level, enemies_list, coins_list):
        if self.is_dead:
            self.death_timer += dt
            self.y += 180.0 * dt
            return

        self.anim_timer += dt * 8.0

        dx = (player.x + player.w / 2) - (self.x + self.w / 2)
        dy = (player.y + player.h / 2) - (self.y + self.h / 2)
        dist = math.hypot(dx, dy)

        # Swoop towards player if close!
        if dist < 150.0 and not player.is_dead:
            self.facing = 1 if dx > 0 else -1
            self.x += self.facing * self.speed * 1.3 * dt
            # Wave dive
            self.y += math.sin(self.anim_timer * 0.8) * 40.0 * dt + (15.0 if dy > 0 else -10.0) * dt
        else:
            # Patrol horizontally with sine float
            self.x += self.facing * self.speed * dt
            if self.facing > 0 and self.x > self.start_x + self.patrol_dist:
                self.facing = -1
            elif self.facing < 0 and self.x < self.start_x - self.patrol_dist:
                self.facing = 1
            self.y = self.start_y + math.sin(self.anim_timer * 0.5) * 12.0

        # Contact damage
        if not player.is_dead and self.rect.colliderect(player.rect):
            player.take_damage(1, self.facing)

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.is_dead and self.death_timer > 0.4:
            return
        img = sprite_mgr.get('bat')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 4
        sub_rect = pygame.Rect(frame_idx * 28, 0, 28, 20)
        frame_surf = img.subsurface(sub_rect)
        if self.facing < 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)
        surface.blit(frame_surf, (int(self.x - cam_x - 4), int(self.y - cam_y - 2)))

class ScorpionEnemy:
    def __init__(self, x, y, patrol_dist=90):
        self.start_x = float(x)
        self.x = float(x)
        self.y = float(y)
        self.w = 26
        self.h = 18
        self.speed = 42.0
        self.patrol_dist = patrol_dist
        self.facing = 1
        self.hp = 2
        self.max_hp = 2
        self.is_dead = False
        self.death_timer = 0.0
        self.hurt_timer = 0.0
        self.anim_timer = 0.0
        self.is_boss = False
        self.orc_type = 'scorpion'

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.w, self.h)

    def take_damage(self, amount, knockback_dir=0):
        if self.is_dead:
            return
        self.hp -= amount
        self.hurt_timer = 0.25
        sound.play('hit')
        particles.add_hit_sparks(self.x + 13, self.y + 9, (240, 180, 50), 10)
        particles.add_text(self.x + 13, self.y - 8, f"-{amount}", COLOR_RED)
        if self.hp <= 0:
            self.is_dead = True
            sound.play('death')

    def update(self, dt, player, level, enemies_list, coins_list):
        if self.is_dead:
            self.death_timer += dt
            return

        if self.hurt_timer > 0.0:
            self.hurt_timer -= dt
            return

        self.anim_timer += dt * 7.0

        dx = (player.x + player.w / 2) - (self.x + self.w / 2)
        dist = abs(dx)

        # Chase on ground
        if dist < 120.0 and abs(player.y - self.y) < 32 and not player.is_dead:
            self.facing = 1 if dx > 0 else -1
            self.x += self.facing * self.speed * 1.35 * dt
        else:
            self.x += self.facing * self.speed * dt
            if self.facing > 0 and self.x > self.start_x + self.patrol_dist:
                self.facing = -1
            elif self.facing < 0 and self.x < self.start_x - self.patrol_dist:
                self.facing = 1

        # Ledge check
        check_px = self.x + self.w + 4 if self.facing > 0 else self.x - 4
        if not level.is_tile_solid_at_pixel(check_px, self.y + self.h + 6):
            self.facing = -self.facing

        # Contact damage
        if not player.is_dead and self.rect.colliderect(player.rect):
            player.take_damage(1, self.facing)

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        if self.is_dead and self.death_timer > 0.4:
            return
        img = sprite_mgr.get('scorpion')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 4
        sub_rect = pygame.Rect(frame_idx * 32, 0, 32, 24)
        frame_surf = img.subsurface(sub_rect)
        if self.facing > 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)
        surface.blit(frame_surf, (int(self.x - cam_x - 3), int(self.y - cam_y - 6)))

class FrostBoss:
    def __init__(self, x, y):
        self.start_x = float(x)
        self.x = float(x)
        self.y = float(y)
        self.w = 34
        self.h = 48
        self.speed = 64.0
        self.vx = 0.0
        self.vy = 0.0
        self.facing = -1
        self.max_hp = 16
        self.hp = self.max_hp
        self.is_boss = True
        self.is_frost_boss = True
        self.is_dead = False
        self.death_timer = 0.0
        self.hurt_timer = 0.0
        self.enraged = False
        self.anim_timer = 0.0
        self.boss_state = 'chase' # 'chase', 'slam_windup', 'slam_air', 'charge', 'blizzard'
        self.boss_timer = 0.0
        self.attack_cooldown = 0.0
        self.hits_streak = 0
        self.on_ground = True
        self.orc_type = 'frost_boss'

    @property
    def rect(self):
        return pygame.Rect(round(self.x), round(self.y), self.w, self.h)

    def take_damage(self, amount, knockback_dir=0):
        if self.is_dead:
            return
        self.hp -= amount
        self.hurt_timer = 0.28
        self.hits_streak += 1
        sound.play('hit')
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, (120, 220, 255), 24)
        particles.add_text(self.x + self.w / 2, self.y - 10, f"-{amount}", COLOR_CYAN)

        # Tactical Leap Back
        if self.hits_streak >= 2:
            self.hits_streak = 0
            self.boss_state = 'slam_windup'
            self.boss_timer = 0.35
            self.vy = -200.0
            self.vx = -self.facing * 90.0

        # Phase 2 Enrage
        if not self.enraged and self.hp <= self.max_hp // 2:
            self.enraged = True
            self.speed = 88.0
            sound.play('boss_roar')
            particles.trigger_screenshake(0.45, 8.0)
            particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, (100, 240, 255), 40)
            particles.add_text(self.x + self.w / 2, self.y - 24, "⚡ TITÃ GLACIAL ENFURECIDO! ⚡", COLOR_CYAN)

        if self.hp <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        sound.play('victory')
        particles.trigger_screenshake(0.6, 9.0)
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, (180, 240, 255), 60)
        particles.add_text(self.x + self.w / 2, self.y - 24, "TITÃ DE GELO DERROTADO!", COLOR_CYAN)

    def update(self, dt, player, level, enemies_list, coins_list):
        if self.is_dead:
            self.death_timer += dt
            return

        if self.hurt_timer > 0.0:
            self.hurt_timer -= dt

        self.anim_timer += dt * 6.0
        self.boss_timer -= dt
        if self.attack_cooldown > 0.0:
            self.attack_cooldown -= dt

        dx = (player.x + player.w / 2) - (self.x + self.w / 2)
        dy = (player.y + player.h / 2) - (self.y + self.h / 2)
        dist = math.hypot(dx, dy)

        # State: Slam Windup
        if self.boss_state == 'slam_windup':
            self.vx = 0.0
            self.facing = 1 if dx > 0 else -1
            if self.boss_timer <= 0:
                self.boss_state = 'slam_air'
                self.vy = -280.0
                self.vx = self.facing * 75.0
                particles.add_text(self.x + self.w / 2, self.y - 16, "⚡ MARTELO DE GELO! ⚡", COLOR_CYAN)
            self.move_and_collide(dt, level)
            return

        # State: Slam in Air
        if self.boss_state == 'slam_air':
            self.move_and_collide(dt, level)
            if self.on_ground and self.vy >= 0:
                # Land with ice spikes!
                sound.play('boss_slam')
                particles.trigger_screenshake(0.4, 7.0)
                particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h, (180, 240, 255), 35)

                from game.objects import IceSpikeHazard
                level.ice_spikes.append(IceSpikeHazard(self.x - 14, self.y + self.h - 32, direction=-1, speed=160.0))
                level.ice_spikes.append(IceSpikeHazard(self.x + self.w, self.y + self.h - 32, direction=1, speed=160.0))

                self.boss_state = 'chase'
                self.attack_cooldown = 1.2 if self.enraged else 1.8
            return

        # State: Frost Charge
        if self.boss_state == 'charge':
            charge_speed = 180.0 if self.enraged else 150.0
            self.vx = self.facing * charge_speed
            if self.boss_timer <= 0:
                self.boss_state = 'chase'
                self.attack_cooldown = 1.3
            self.move_and_collide(dt, level)

            if not player.is_dead and self.rect.colliderect(player.rect):
                player.take_damage(2, self.facing)
            return

        # Default Chase
        self.facing = 1 if dx > 0 else -1

        # Slam attack trigger
        if dist > 60 and self.attack_cooldown <= 0.0 and random.random() < 0.035:
            self.boss_state = 'slam_windup'
            self.boss_timer = 0.4
            return

        # Charge attack trigger
        if dist > 80 and self.attack_cooldown <= 0.0 and random.random() < 0.03:
            self.boss_state = 'charge'
            self.boss_timer = 0.75
            particles.add_text(self.x + self.w / 2, self.y - 16, "⚡ CARGA GLACIAL! ⚡", COLOR_CYAN)
            return

        chase_mult = 1.3 if self.enraged else 1.05
        self.vx = self.facing * self.speed * chase_mult
        self.move_and_collide(dt, level)

        if not player.is_dead and self.rect.colliderect(player.rect):
            player.take_damage(1, self.facing)

    def move_and_collide(self, dt, level):
        self.vy += GRAVITY * dt
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        self.x += self.vx * dt
        c_x = level.check_tile_collision(self.rect)
        if c_x:
            if self.vx > 0:
                self.x = float(c_x.left - self.w)
            elif self.vx < 0:
                self.x = float(c_x.right)
            self.facing = -self.facing
            self.vx = self.facing * abs(self.vx)

        self.y += self.vy * dt
        c_y = level.check_tile_collision(self.rect)
        if c_y:
            if self.vy > 0:
                self.y = float(c_y.top - self.h)
                self.vy = 0.0
                self.on_ground = True
            elif self.vy < 0:
                self.y = float(c_y.bottom)
                self.vy = 0.0
        else:
            if self.vy >= 0:
                probe = pygame.Rect(round(self.x) + 2, round(self.y) + self.h, self.w - 4, 3)
                gt = level.check_tile_collision(probe)
                if gt:
                    self.y = float(gt.top - self.h)
                    self.vy = 0.0
                    self.on_ground = True
                else:
                    self.on_ground = False
            else:
                self.on_ground = False

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        img = sprite_mgr.get('frost_boss')
        if not img:
            return
        frame_idx = int(self.anim_timer) % 6
        sub_rect = pygame.Rect(frame_idx * 64, 0, 64, 64)
        frame_surf = img.subsurface(sub_rect)

        # Scale to 84x84
        frame_surf = pygame.transform.scale(frame_surf, (84, 84))
        if self.facing < 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)

        if self.enraged and int(pygame.time.get_ticks() / 100) % 2 == 0:
            frame_surf.fill((60, 220, 255, 120), special_flags=pygame.BLEND_RGB_ADD)

        surface.blit(frame_surf, (int(self.x + self.w / 2 - 42 - cam_x), int(self.y + self.h - 70 - cam_y)))
