import pygame
from game.settings import *
from game.sound import sound
from game.particles import particles

class Player:
    def __init__(self, x, y):
        self.spawn_x = x
        self.spawn_y = y
        self.hero_level = 1
        self.has_key = False
        self.reset()

    def reset(self):
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
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_GOLD, 20)
        particles.trigger_screenshake(0.15, 3.0)
        names = ["", "ESPADACHIM INICIANTE", "ESPADACHIM DE FERRO!", "CAVALEIRO DOURADO!"]
        particles.add_text(self.x + self.w / 2, self.y - 16, names[self.hero_level], COLOR_GOLD)

    def take_damage(self, amount, knockback_dir=0):
        if self.invulnerable_timer > 0.0 or self.is_dead:
            return
        self.hp = max(0, self.hp - amount)
        self.invulnerable_timer = 1.2
        self.is_attacking = False
        self.is_pogo = False
        self.vx = knockback_dir * 130.0
        self.vy = -140.0

        sound.play('hurt')
        particles.trigger_hitstop(0.06)
        particles.trigger_screenshake(0.2, 4.0)
        particles.add_hit_sparks(self.x + self.w / 2, self.y + self.h / 2, COLOR_RED, 12)
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

        # Pogo Downward Strike if in air and holding down!
        if not self.on_ground and holding_down:
            self.is_pogo = True
            sound.play('pogo')
        else:
            self.is_pogo = False
            sound.play('attack')

    def update(self, dt, keys, level, enemies, chests):
        if self.is_dead:
            self.death_timer += dt
            self.vy += GRAVITY * dt
            self.y += self.vy * dt
            self.check_tile_collision(level, is_vertical=True)
            self.anim_frame = min(6, int(self.death_timer / 0.11))
            return

        if self.invulnerable_timer > 0.0:
            self.invulnerable_timer -= dt

        # Coyote and jump buffer
        if self.on_ground:
            self.coyote_timer = 0.12
        else:
            self.coyote_timer -= dt

        if keys.get('jump_pressed'):
            self.jump_buffer_timer = 0.14
        else:
            self.jump_buffer_timer -= dt

        # Attack check
        holding_down = keys.get('down', False)
        if keys.get('attack_pressed') and not self.is_attacking:
            self.attack(holding_down)

        # Horizontal movement
        move_dir = (1 if keys.get('right') else 0) - (1 if keys.get('left') else 0)
        if move_dir != 0 and not self.is_attacking:
            self.facing = move_dir
            accel = PLAYER_ACCEL if self.on_ground else PLAYER_ACCEL * 0.75
            self.vx += move_dir * accel * dt
            if abs(self.vx) > PLAYER_SPEED:
                self.vx = move_dir * PLAYER_SPEED
        else:
            friction = PLAYER_FRICTION if self.on_ground else 0.92
            self.vx *= (friction ** (dt * 60))
            if abs(self.vx) < 5.0:
                self.vx = 0.0

        # Jump execution
        if self.jump_buffer_timer > 0.0 and self.coyote_timer > 0.0 and not self.is_attacking:
            self.vy = PLAYER_JUMP_FORCE
            self.jump_buffer_timer = 0.0
            self.coyote_timer = 0.0
            self.on_ground = False
            sound.play('jump')
            particles.add_dust(self.x + self.w / 2, self.y + self.h, 6)

        # Variable jump height
        if not keys.get('jump') and self.vy < -70.0:
            self.vy += 500.0 * dt

        # Gravity
        self.vy += GRAVITY * dt
        if self.vy > MAX_FALL_SPEED:
            self.vy = MAX_FALL_SPEED

        # Apply Movement & Collision
        self.move_and_collide(dt, level)

        # Update attack hitboxes
        if self.is_attacking:
            self.update_attack(dt, enemies, chests)

        # Update animation states
        self.update_animation(dt)

        # Landing dust
        if self.on_ground and not self.was_on_ground:
            particles.add_dust(self.x + self.w / 2, self.y + self.h, 5)
        self.was_on_ground = self.on_ground

        # Abyss fall check
        if self.y > level.height_in_pixels + 64:
            self.take_damage(self.hp)

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
            foot_plat = level.check_one_way_platform(self.x, self.y + self.h, self.w, self.vy * dt)
            if foot_plat:
                self.y = foot_plat.top - self.h
                self.vy = 0.0
                self.on_ground = True

    def check_tile_collision(self, level, is_vertical=False):
        c = level.check_tile_collision(self.rect)
        if c and is_vertical and self.vy > 0:
            self.y = c.top - self.h
            self.vy = 0.0

    def update_attack(self, dt, enemies, chests):
        self.attack_timer += dt
        self.attack_frame = int(self.attack_timer / 0.055)

        # Active hit frames: frames 2 to 4
        if 2 <= self.attack_frame <= 4 and not self.attack_hit_done:
            attack_dmg = self.hero_level
            reach = 22 + (self.hero_level * 4)

            if self.is_pogo:
                # Downward pogo strike box
                attack_box = pygame.Rect(int(self.x - 2), int(self.y + self.h - 4), self.w + 4, 20)
            else:
                # Normal forward strike box
                ax = int(self.x + self.w - 4 if self.facing > 0 else self.x - reach)
                attack_box = pygame.Rect(ax, int(self.y + 4), reach, 22)

            for enemy in enemies:
                if not enemy.is_dead and attack_box.colliderect(enemy.rect):
                    enemy.take_damage(attack_dmg, self.facing)
                    self.attack_hit_done = True
                    particles.trigger_hitstop(0.06)
                    particles.trigger_screenshake(0.12, 3.0)

                    # Pogo bounce if attacking downwards!
                    if self.is_pogo:
                        self.vy = POGO_BOUNCE_FORCE
                        sound.play('pogo')
                        particles.add_text(self.x + self.w / 2, self.y - 12, "POGO BOUNCE!", COLOR_GOLD)

            for chest in chests:
                if not chest.opened and attack_box.colliderect(chest.rect):
                    chest.open(self)

        if self.attack_frame >= 8:
            self.is_attacking = False
            self.is_pogo = False

    def update_animation(self, dt):
        if self.is_attacking:
            return

        if not self.on_ground:
            self.state = 'jump' if self.vy < 0 else 'fall'
            return

        if abs(self.vx) > 10.0:
            self.state = 'run'
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.09) % 8
        else:
            self.state = 'idle'
            self.anim_timer += dt
            self.anim_frame = int(self.anim_timer / 0.12) % 12

    def draw(self, surface, sprite_mgr, cam_x, cam_y):
        # Flash when invulnerable
        if self.invulnerable_timer > 0.0 and int(pygame.time.get_ticks() / 60) % 2 == 0:
            return

        prefix = f"hero{self.hero_level}_"
        row = 2 # Side-view row
        frame_idx = 0

        if self.is_dead:
            img_key = prefix + "death"
            frame_idx = self.anim_frame
        elif self.is_attacking:
            img_key = prefix + "attack"
            frame_idx = min(7, self.attack_frame)
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
            # Fallback placeholder box
            pygame.draw.rect(surface, (66, 153, 225), (int(self.x - cam_x), int(self.y - cam_y), self.w, self.h))
            return

        # 64x64 slice
        sub_rect = pygame.Rect(frame_idx * 64, row * 64, 64, 64)
        frame_surf = sheet.subsurface(sub_rect)

        if self.facing < 0:
            frame_surf = pygame.transform.flip(frame_surf, True, False)

        draw_x = int(self.x + self.w / 2 - 32 - cam_x)
        draw_y = int(self.y + self.h - 43 - cam_y)
        surface.blit(frame_surf, (draw_x, draw_y))
