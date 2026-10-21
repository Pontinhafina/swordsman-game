import pygame
import math
from game.settings import *
from game.sound import sound
from game.particles import particles

class Player:
    def __init__(self, x, y):
        self.spawn_x = float(x)
        self.spawn_y = float(y)
        self.respawn_checkpoint = (float(x), float(y))
        self.hero_level = 1
        self.has_key = False
        self.reset()

    def reset(self, to_checkpoint=False):
        if to_checkpoint and self.respawn_checkpoint:
            self.x = float(self.respawn_checkpoint[0])
            self.y = float(self.respawn_checkpoint[1])
        else:
            self.x = float(self.spawn_x)
            self.y = float(self.spawn_y)

        self.w = 16
        self.h = 26
        self.vx = 0.0
        self.vy = 0.0
        self.facing = 1 # 1 = right, -1 = left

        self.on_ground = False
        self.was_on_ground = False
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0

        # Wall slide & wall jump
        self.is_wall_sliding = False
        self.wall_dir = 0 # -1 = wall on left, 1 = wall on right
        self.wall_jump_timer = 0.0

        # Dash
        self.is_dashing = False
        self.dash_timer = 0.0
        self.dash_cooldown = 0.0
        self.can_dash = True
        self.ghost_trails = []

        # Health & State
        self.max_hp = 5
        self.hp = self.max_hp
        self.invulnerable_timer = 0.0
        self.is_dead = False
        self.death_timer = 0.0

        # Combat
        self.is_attacking = False
        self.is_pogo = False
        self.attack_timer = 0.0
        self.attack_frame = 0
        self.attack_hit_done = False

        # Animation
        self.state = 'idle'
        self.anim_timer = 0.0
        self.anim_frame = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.w, self.h)

    def upgrade_level(self, lvl):
        self.hero_level = min(3, max(1, lvl))
        sound.play('chest')
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_GOLD, 25)
        particles.trigger_screenshake(0.18, 3.5)
        names = ["", "ESPADACHIM INICIANTE", "ESPADACHIM DE FERRO!", "CAVALEIRO DOURADO!"]
        particles.add_text(self.x + self.w / 2, self.y - 16, names[self.hero_level], COLOR_GOLD)

    def take_damage(self, amount, knockback_dir=0):
        if self.invulnerable_timer > 0.0 or self.is_dead or self.is_dashing:
            return
        self.hp = max(0, self.hp - amount)
        self.invulnerable_timer = 1.2
        self.is_attacking = False
        self.is_pogo = False
        self.is_dashing = False
        self.vx = knockback_dir * 140.0
        self.vy = -150.0

        sound.play('hurt')
        particles.trigger_hitstop(0.06)
        particles.trigger_screenshake(0.2, 4.0)
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_RED, 14)
        particles.add_text(self.x + self.w / 2, self.y - 10, f"-{amount}", COLOR_RED)

        if self.hp <= 0:
            self.die()

    def die(self):
        self.is_dead = True
        self.state = 'dead'
        self.anim_frame = 0
        self.anim_timer = 0.0
        self.vx = 0.0
        sound.play('death')
        particles.trigger_screenshake(0.3, 6.0)

    def attack(self, holding_down):
        if self.is_attacking or self.is_dead:
            return
        self.is_attacking = True
        self.attack_timer = 0.0
        self.attack_frame = 0
        self.attack_hit_done = False

        # Downward pogo strike if airborne & holding down
        if not self.on_ground and holding_down:
            self.is_pogo = True
            sound.play('pogo')
        else:
            self.is_pogo = False
            sound.play('attack')

    def dash(self):
        if not self.can_dash or self.is_dashing or self.dash_cooldown > 0.0 or self.is_dead:
            return
        self.is_dashing = True
        self.dash_timer = DASH_DURATION
        self.dash_cooldown = DASH_COOLDOWN
        self.can_dash = False
        self.is_attacking = False
        self.is_pogo = False
        self.vx = self.facing * DASH_SPEED
        self.vy = 0.0
        sound.play('dash')
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_CYAN, 12)

    def update(self, dt, keys, level, enemies, chests, cracked_walls=None):
        # Update ghost trail after-images
        for ghost in self.ghost_trails:
            ghost['alpha'] -= dt * 4.5
        self.ghost_trails = [g for g in self.ghost_trails if g['alpha'] > 0]

        if self.is_dead:
            self.death_timer += dt
            self.vy += GRAVITY * dt
            self.y += self.vy * dt
            self.check_tile_collision(level, is_vertical=True)
            self.anim_frame = min(6, int(self.death_timer / 0.11))
            return

        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt

        if self.dash_cooldown > 0.0:
            self.dash_cooldown -= dt

        # Coyote and jump buffer
        if self.on_ground:
            self.coyote_timer = 0.12
            self.can_dash = True
        else:
            self.coyote_timer -= dt

        if keys.get('jump_pressed'):
            self.jump_buffer_timer = 0.14
        else:
            self.jump_buffer_timer -= dt

        # Dash execution
        if keys.get('dash_pressed'):
            self.dash()

        if self.is_dashing:
            self.dash_timer -= dt
            self.vy = 0.0
            # Emit ghost trail
            if int(self.dash_timer * 100) % 2 == 0:
                self.ghost_trails.append({
                    'x': self.x,
                    'y': self.y,
                    'facing': self.facing,
                    'hero_lvl': self.hero_level,
                    'alpha': 0.8
                })
            self.move_and_collide(dt, level)
            if self.dash_timer <= 0:
                self.is_dashing = False
                self.vx *= 0.5
            return

        # Attack check (can attack while running!)
        holding_down = keys.get('down', False)
        if keys.get('attack_pressed') and not self.is_attacking:
            self.attack(holding_down)

        # Horizontal movement
        move_dir = (1 if keys.get('right') else 0) - (1 if keys.get('left') else 0)

        # Wall jump lock timer
        if self.wall_jump_timer > 0.0:
            self.wall_jump_timer -= dt

        if self.wall_jump_timer <= 0.0:
            if move_dir != 0:
                self.facing = move_dir
                accel = PLAYER_ACCEL if self.on_ground else PLAYER_AIR_ACCEL
                self.vx += move_dir * accel * dt
                if abs(self.vx) > PLAYER_SPEED:
                    self.vx = move_dir * PLAYER_SPEED
            else:
                decel = PLAYER_DECEL if self.on_ground else PLAYER_AIR_DECEL
                if self.vx > 0:
                    self.vx = max(0.0, self.vx - decel * dt)
                elif self.vx < 0:
                    self.vx = min(0.0, self.vx + decel * dt)

        # Wall slide detection
        self.check_wall_slide(level, move_dir)

        # Jump execution (Normal Jump or Wall Jump!)
        if self.jump_buffer_timer > 0.0:
            if self.is_wall_sliding and self.wall_dir != 0:
                # WALL JUMP!
                self.vx = -self.wall_dir * WALL_JUMP_FORCE_X
                self.vy = WALL_JUMP_FORCE_Y
                self.facing = -self.wall_dir
                self.wall_jump_timer = 0.16
                self.jump_buffer_timer = 0.0
                self.coyote_timer = 0.0
                self.is_wall_sliding = False
                sound.play('jump')
                particles.add_dust(self.x + self.w / 2, self.y + self.h / 2, 8)
                particles.add_text(self.x + self.w / 2, self.y - 12, "WALL JUMP!", COLOR_CYAN)
            elif self.coyote_timer > 0.0:
                # NORMAL GROUND JUMP!
                self.vy = PLAYER_JUMP_FORCE
                self.jump_buffer_timer = 0.0
                self.coyote_timer = 0.0
                self.on_ground = False
                sound.play('jump')
                particles.add_dust(self.x + self.w / 2, self.y + self.h, 6)

        # Variable jump height (Crisp cut when releasing jump key)
        if not keys.get('jump') and self.vy < -70.0:
            self.vy *= 0.50

        # Gravity & Apex Float
        if self.is_wall_sliding:
            self.vy = min(self.vy + GRAVITY * 0.5 * dt, WALL_SLIDE_SPEED)
            if int(pygame.time.get_ticks() / 150) % 2 == 0:
                sound.play('wall_slide')
                particles.add_dust(self.x + (0 if self.wall_dir < 0 else self.w), self.y + self.h / 2, 1)
        else:
            # Gravity calculation
            if abs(self.vy) < 45.0: # Apex of jump
                eff_gravity = GRAVITY * APEX_GRAVITY_MULT
            elif self.vy > 0: # Falling
                eff_gravity = GRAVITY * FALL_GRAVITY_MULT
            else:
                eff_gravity = GRAVITY

            self.vy += eff_gravity * dt
            if self.vy > MAX_FALL_SPEED:
                self.vy = MAX_FALL_SPEED

        # Apply Movement & Collision
        self.move_and_collide(dt, level)

        # Update attack hitboxes
        if self.is_attacking:
            self.update_attack(dt, enemies, chests, cracked_walls)

        # Update animation states
        self.update_animation(dt)

        # Landing dust
        if self.on_ground and not self.was_on_ground:
            particles.add_dust(self.x + self.w / 2, self.y + self.h, 6)
        self.was_on_ground = self.on_ground

        # Abyss fall check -> Respawn at checkpoint!
        if self.y > level.height_in_pixels + 64:
            self.take_damage(1)
            if not self.is_dead:
                self.reset(to_checkpoint=True)
                particles.add_text(self.x + self.w / 2, self.y - 12, "RESPAWN!", COLOR_GOLD)

    def check_wall_slide(self, level, move_dir):
        self.is_wall_sliding = False
        self.wall_dir = 0
        if self.on_ground or self.vy < 0:
            return

        # Check left wall
        left_box = pygame.Rect(int(self.x - 3), int(self.y + 4), 3, self.h - 8)
        c_left = level.check_tile_collision(left_box)
        if c_left and move_dir < 0:
            self.is_wall_sliding = True
            self.wall_dir = -1
            return

        # Check right wall
        right_box = pygame.Rect(int(self.x + self.w), int(self.y + 4), 3, self.h - 8)
        c_right = level.check_tile_collision(right_box)
        if c_right and move_dir > 0:
            self.is_wall_sliding = True
            self.wall_dir = 1
            return

    def move_and_collide(self, dt, level):
        # Horizontal
        self.x += self.vx * dt
        c_x = level.check_tile_collision(self.rect)
        if c_x:
            if self.vx > 0:
                self.x = c_x.left - self.w - 0.01
            elif self.vx < 0:
                self.x = c_x.right + 0.01
            self.vx = 0.0

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

        # One-way platform check
        if self.vy >= 0:
            foot_plat = level.check_one_way_platform(self.x, self.y + self.h, self.w, max(2.0, self.vy * dt))
            if foot_plat:
                self.y = foot_plat.top - self.h
                self.vy = 0.0
                self.on_ground = True

    def check_tile_collision(self, level, is_vertical=False):
        c = level.check_tile_collision(self.rect)
        if c and is_vertical and self.vy > 0:
            self.y = c.top - self.h
            self.vy = 0.0

    def update_attack(self, dt, enemies, chests, cracked_walls=None):
        self.attack_timer += dt
        self.attack_frame = int(self.attack_timer / 0.05)

        # Active hit frames: frames 1 to 4
        if 1 <= self.attack_frame <= 4 and not self.attack_hit_done:
            attack_dmg = self.hero_level
            reach = 24 + (self.hero_level * 4)

            if self.is_pogo:
                attack_box = pygame.Rect(int(self.x - 4), int(self.y + self.h - 4), self.w + 8, 22)
            else:
                ax = int(self.x + self.w - 4 if self.facing > 0 else self.x - reach)
                attack_box = pygame.Rect(ax, int(self.y + 2), reach, 24)

            # Hit enemies
            for enemy in enemies:
                if not enemy.is_dead and attack_box.colliderect(enemy.rect):
                    enemy.take_damage(attack_dmg, self.facing)
                    self.attack_hit_done = True
                    particles.trigger_hitstop(0.06)
                    particles.trigger_screenshake(0.14, 3.5)

                    if self.is_pogo:
                        self.vy = POGO_BOUNCE_FORCE
                        self.can_dash = True
                        sound.play('pogo')
                        particles.add_text(self.x + self.w / 2, self.y - 12, "POGO BOUNCE!", COLOR_GOLD)

            # Hit chests
            for chest in chests:
                if not chest.opened and attack_box.colliderect(chest.rect):
                    chest.open(self)

            # Hit cracked secret walls
            if cracked_walls:
                for wall in cracked_walls:
                    if not wall.destroyed and attack_box.colliderect(wall.rect):
                        wall.hit(attack_dmg)
                        self.attack_hit_done = True
                        if self.is_pogo:
                            self.vy = POGO_BOUNCE_FORCE
                            self.can_dash = True

        if self.attack_frame >= 7:
            self.is_attacking = False
            self.is_pogo = False

    def update_animation(self, dt):
        if not self.on_ground:
            if self.is_wall_sliding:
                self.state = 'wall_slide'
            else:
                self.state = 'jump' if self.vy < 0 else 'fall'
            return

        if abs(self.vx) > 10.0:
            self.state = 'run'
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.08) % 8
        else:
            self.state = 'idle'
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.11) % 12

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        # Draw dash ghost trail after-images
        for ghost in self.ghost_trails:
            g_sheet = sprite_mgr.get(f"hero{ghost['hero_lvl']}_run")
            if g_sheet:
                sub_rect = pygame.Rect(2 * 64, 2 * 64, 64, 64)
                g_surf = g_sheet.subsurface(sub_rect).copy()
                if ghost['facing'] < 0:
                    g_surf = pygame.transform.flip(g_surf, True, False)
                # Cyan ghost color tint
                g_surf.fill((56, 217, 235, int(ghost['alpha'] * 150)), special_flags=pygame.BLEND_RGBA_MULT)
                gx = int(ghost['x'] + self.w / 2 - 32 - cam_x)
                gy = int(ghost['y'] + self.h - 43 - cam_y)
                surface.blit(g_surf, (gx, gy))

        # Flash when invulnerable
        if self.invulnerable_timer > 0.0 and int(pygame.time.get_ticks() / 50) % 2 == 0:
            return

        prefix = f"hero{self.hero_level}_"
        row = 2 # Side-view row
        frame_idx = 0

        if self.is_dead:
            img_key = prefix + "death"
            frame_idx = self.anim_frame
        elif self.is_attacking:
            # If moving on ground: USE RUN_ATTACK!
            if self.on_ground and abs(self.vx) > 15.0:
                img_key = prefix + "run_attack"
            else:
                img_key = prefix + "attack"
            frame_idx = min(7, self.attack_frame)
        elif self.state == 'wall_slide':
            img_key = prefix + "run"
            frame_idx = 4
        elif self.state == 'jump':
            img_key = prefix + "run"
            frame_idx = 2
        elif self.state == 'fall':
            img_key = prefix + "run"
            frame_idx = 5
        elif self.state == 'run':
            img_key = prefix + "run"
            frame_idx = self.anim_frame
        else:
            img_key = prefix + "idle"
            frame_idx = self.anim_frame

        sheet = sprite_mgr.get(img_key)
        if not sheet:
            sheet = sprite_mgr.get(prefix + "idle")
            if not sheet:
                pygame.draw.rect(surface, (66, 153, 225), (int(self.x - cam_x), int(self.y - cam_y), self.w, self.h))
                return

        sub_rect = pygame.Rect(frame_idx * 64, row * 64, 64, 64)
        frame_surf = sheet.subsurface(sub_rect)

        if self.facing < 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)

        draw_x = int(self.x + self.w / 2 - 32 - cam_x)
        draw_y = int(self.y + self.h - 43 - cam_y)
        surface.blit(frame_surf, (draw_x, draw_y))

        # Draw Slash VFX arc overlay when attacking!
        if self.is_attacking and 1 <= self.attack_frame <= 4:
            vfx_sheet = sprite_mgr.get('slash_vfx')
            if vfx_sheet:
                vfx_frame = min(3, self.attack_frame - 1)
                vfx_sub = pygame.Rect(vfx_frame * 64, 0, 64, 64)
                vfx_surf = vfx_sheet.subsurface(vfx_sub)

                if self.is_pogo:
                    # Rotate downward for pogo strike
                    vfx_surf = pygame.transform.rotate(vfx_surf, -90)
                    vx_pos = int(self.x + self.w / 2 - 32 - cam_x)
                    vy_pos = int(self.y + self.h - 18 - cam_y)
                else:
                    if self.facing < 0:
                        vfx_surf = pygame.transform.flip(vfx_surf, True, False)
                        vx_pos = int(self.x - 30 - cam_x)
                    else:
                        vx_pos = int(self.x + self.w - 10 - cam_x)
                    vy_pos = int(self.y - 12 - cam_y)

                surface.blit(vfx_surf, (vx_pos, vy_pos))
