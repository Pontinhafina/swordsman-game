import pygame
import random
import math
from game.settings import *

class Level:
    def __init__(self, stage_idx=1):
        self.stage_idx = stage_idx
        self.tile_size = TILE_SIZE
        self.width_in_tiles = 110
        self.height_in_tiles = 15
        self.width_in_pixels = self.width_in_tiles * self.tile_size
        self.height_in_pixels = self.height_in_tiles * self.tile_size

        self.tiles = []
        self.one_way_platforms = []
        self.props = []
        self.ambient_particles = []

        self.init_ambient()
        self.init_stage(stage_idx)

    def init_ambient(self):
        self.ambient_particles = []
        for _ in range(25):
            self.ambient_particles.append({
                'x': random.uniform(0, INTERNAL_WIDTH),
                'y': random.uniform(0, INTERNAL_HEIGHT),
                'vx': random.uniform(-8, 8),
                'vy': random.uniform(-15, -4),
                'size': random.choice([1, 2]),
                'alpha': random.uniform(0.3, 0.7),
                'pulse': random.uniform(0, math.pi * 2)
            })

    def init_stage(self, stage_idx):
        self.tiles = [[0 for _ in range(self.width_in_tiles)] for _ in range(self.height_in_tiles)]
        self.one_way_platforms = []
        self.props = []

        def create_ground(x, y, w, h):
            for gy in range(h):
                for gx in range(w):
                    tx = x + gx
                    ty = y + gy
                    if tx >= self.width_in_tiles or ty >= self.height_in_tiles:
                        continue
                    tile_id = 12
                    is_top = (gy == 0)
                    is_bot = (gy == h - 1)
                    is_left = (gx == 0)
                    is_right = (gx == w - 1)

                    if is_top and is_left: tile_id = 1
                    elif is_top and is_right: tile_id = 3
                    elif is_top: tile_id = 2
                    elif is_bot and is_left: tile_id = 21
                    elif is_bot and is_right: tile_id = 23
                    elif is_bot: tile_id = 22
                    elif is_left: tile_id = 11
                    elif is_right: tile_id = 13
                    self.tiles[ty][tx] = tile_id

        def create_float_plat(x, y, w):
            for gx in range(w):
                tx = x + gx
                tile_id = 8
                if gx == 0: tile_id = 7
                elif gx == w - 1: tile_id = 9
                self.tiles[y][tx] = tile_id
                self.one_way_platforms.append(pygame.Rect(tx * self.tile_size, y * self.tile_size, self.tile_size, 10))

        def create_water(x, y, w, h):
            for gy in range(h):
                for gx in range(w):
                    tx = x + gx
                    ty = y + gy
                    if tx < self.width_in_tiles and ty < self.height_in_tiles:
                        self.tiles[ty][tx] = 10 if gy == 0 else 20

        # Boundary left wall
        for y in range(15):
            self.tiles[y][0] = 11

        if stage_idx == 1:
            # FASE 1: Floresta dos Orcs
            create_ground(0, 11, 19, 4)
            create_ground(17, 10, 3, 5) # 1-step stairs
            create_ground(19, 9, 13, 6) # Terrace
            create_float_plat(32, 8, 4)
            create_ground(36, 8, 8, 7)  # Plateau
            create_float_plat(42, 7, 3)
            create_ground(45, 6, 5, 9)  # Secret cliff
            create_float_plat(50, 8, 3)
            create_ground(53, 10, 8, 5) # Valley
            create_water(61, 13, 9, 2)
            create_float_plat(61, 9, 4)
            create_float_plat(66, 9, 4)
            create_ground(70, 10, 7, 5)
            create_ground(77, 9, 3, 6)
            create_ground(80, 8, 14, 7) # Fortress
            create_float_plat(94, 9, 3)
            create_ground(97, 10, 12, 5) # Goal altar

            for y in range(10): self.tiles[y][108] = 13
            self.props = [
                {'type': 'tree_1', 'x': 3 * 32, 'y': 11 * 32 - 103},
                {'type': 'stone_1', 'x': 10 * 32, 'y': 11 * 32 - 59},
                {'type': 'willow_1', 'x': 21 * 32, 'y': 9 * 32 - 135},
                {'type': 'stone_2', 'x': 29 * 32, 'y': 9 * 32 - 59},
                {'type': 'tree_2', 'x': 37 * 32, 'y': 8 * 32 - 132},
                {'type': 'tree_1', 'x': 55 * 32, 'y': 10 * 32 - 103},
                {'type': 'stone_1', 'x': 72 * 32, 'y': 10 * 32 - 59},
                {'type': 'tree_2', 'x': 82 * 32, 'y': 8 * 32 - 132},
                {'type': 'willow_1', 'x': 104 * 32, 'y': 10 * 32 - 135}
            ]

        elif stage_idx == 2:
            # FASE 2: Ruínas do Entardecer
            create_ground(0, 11, 14, 4)
            create_float_plat(12, 9, 4)
            create_ground(15, 8, 10, 7)
            create_float_plat(23, 7, 3)
            create_ground(26, 6, 8, 9)
            create_float_plat(32, 5, 3)
            create_ground(35, 4, 7, 11) # High Tower
            create_float_plat(42, 6, 3)
            create_ground(45, 8, 8, 7)
            create_float_plat(52, 9, 4)
            create_water(55, 13, 14, 2)
            create_float_plat(56, 10, 3)
            create_float_plat(60, 9, 4)
            create_float_plat(65, 10, 3)
            create_ground(69, 10, 11, 5)
            create_ground(79, 9, 3, 6)
            create_ground(82, 8, 14, 7)
            create_float_plat(96, 8, 3)
            create_ground(99, 9, 10, 6)

            for y in range(9): self.tiles[y][108] = 13
            self.props = [
                {'type': 'stone_2', 'x': 2 * 32, 'y': 11 * 32 - 59},
                {'type': 'tree_2', 'x': 17 * 32, 'y': 8 * 32 - 132},
                {'type': 'stone_1', 'x': 36 * 32, 'y': 4 * 32 - 59},
                {'type': 'willow_1', 'x': 46 * 32, 'y': 8 * 32 - 135},
                {'type': 'tree_1', 'x': 84 * 32, 'y': 8 * 32 - 103}
            ]

        elif stage_idx == 3:
            # FASE 3: Desfiladeiro dos Salgueiros
            create_ground(0, 10, 15, 5)
            create_float_plat(13, 8, 4)
            create_float_plat(18, 7, 3)
            create_float_plat(22, 6, 3)
            create_ground(26, 11, 8, 4) # Cavern
            create_float_plat(28, 5, 4)
            create_float_plat(34, 6, 3)
            create_ground(38, 8, 12, 7)
            create_float_plat(48, 7, 3)
            create_ground(52, 9, 14, 6)
            create_water(66, 13, 10, 2)
            create_float_plat(66, 9, 4)
            create_float_plat(71, 8, 4)
            create_ground(76, 8, 10, 7)
            create_float_plat(85, 7, 3)
            create_ground(88, 7, 8, 8)
            create_float_plat(95, 8, 3)
            create_ground(98, 9, 10, 6)

            for y in range(9): self.tiles[y][107] = 13
            self.props = [
                {'type': 'willow_1', 'x': 3 * 32, 'y': 10 * 32 - 135},
                {'type': 'stone_2', 'x': 27 * 32, 'y': 11 * 32 - 59},
                {'type': 'willow_1', 'x': 54 * 32, 'y': 9 * 32 - 135},
                {'type': 'stone_1', 'x': 78 * 32, 'y': 8 * 32 - 59}
            ]

        elif stage_idx == 4:
            # FASE 4: Pântano Noturno
            create_ground(0, 11, 12, 4)
            create_water(12, 13, 12, 2)
            create_float_plat(13, 10, 3)
            create_float_plat(17, 9, 3)
            create_float_plat(21, 10, 3)
            create_ground(24, 10, 12, 5)
            create_float_plat(34, 8, 3)
            create_ground(37, 7, 7, 8)
            create_float_plat(42, 5, 3)
            create_ground(45, 4, 6, 11) # Tower
            create_water(51, 13, 16, 2)
            create_float_plat(52, 9, 3)
            create_float_plat(56, 8, 4)
            create_float_plat(61, 9, 3)
            create_float_plat(65, 10, 3)
            create_ground(68, 10, 14, 5)
            create_float_plat(81, 8, 3)
            create_ground(84, 8, 12, 7)
            create_float_plat(95, 8, 3)
            create_ground(98, 9, 10, 6)

            for y in range(9): self.tiles[y][107] = 13
            self.props = [
                {'type': 'willow_1', 'x': 2 * 32, 'y': 11 * 32 - 135},
                {'type': 'stone_1', 'x': 26 * 32, 'y': 10 * 32 - 59},
                {'type': 'willow_1', 'x': 70 * 32, 'y': 10 * 32 - 135}
            ]

        elif stage_idx == 5:
            # FASE 5: Fortaleza do Chefe
            create_ground(0, 10, 16, 5)
            create_float_plat(14, 8, 4)
            create_ground(17, 7, 10, 8)
            create_float_plat(26, 8, 3)
            create_ground(28, 9, 12, 6)
            create_float_plat(39, 9, 3)
            create_ground(42, 10, 14, 5)
            create_ground(55, 9, 4, 6)
            create_ground(58, 8, 4, 7)
            create_ground(62, 8, 44, 7) # Throne Room Arena
            create_float_plat(72, 5, 4)
            create_float_plat(86, 5, 4)
            create_float_plat(98, 5, 4)

            for y in range(8): self.tiles[y][105] = 13
            self.props = [
                {'type': 'stone_2', 'x': 2 * 32, 'y': 10 * 32 - 59},
                {'type': 'tree_2', 'x': 18 * 32, 'y': 7 * 32 - 132},
                {'type': 'stone_2', 'x': 64 * 32, 'y': 8 * 32 - 59},
                {'type': 'tree_1', 'x': 80 * 32, 'y': 8 * 32 - 103}
            ]

    def is_tile_solid(self, tile_id):
        return tile_id in [1, 2, 3, 11, 12, 13, 21, 22, 23]

    def is_tile_solid_at_pixel(self, px, py):
        tx = int(px // self.tile_size)
        ty = int(py // self.tile_size)
        if 0 <= tx < self.width_in_tiles and 0 <= ty < self.height_in_tiles:
            return self.is_tile_solid(self.tiles[ty][tx])
        return False

    def check_tile_collision(self, rect):
        start_x = max(0, rect.left // self.tile_size)
        end_x = min(self.width_in_tiles - 1, rect.right // self.tile_size)
        start_y = max(0, rect.top // self.tile_size)
        end_y = min(self.height_in_tiles - 1, rect.bottom // self.tile_size)

        for ty in range(start_y, end_y + 1):
            for tx in range(start_x, end_x + 1):
                tid = self.tiles[ty][tx]
                if self.is_tile_solid(tid):
                    t_rect = pygame.Rect(tx * self.tile_size, ty * self.tile_size, self.tile_size, self.tile_size)
                    if rect.colliderect(t_rect):
                        return t_rect
        return None

    def check_one_way_platform(self, foot_x, foot_y, foot_w, vy_dt):
        f_rect = pygame.Rect(int(foot_x), int(foot_y - 2), int(foot_w), 6)
        for p in self.one_way_platforms:
            if f_rect.colliderect(p):
                prev_y = foot_y - max(1.0, vy_dt)
                if prev_y <= p.top + 4:
                    return p
        return None

    def draw_parallax(self, surface, sprite_mgr, cam_x, cam_y, dt=0.016):
        bg_w = 576
        bg_h = 324
        layers = [
            ('bg_1', 0.05, 0),
            ('bg_2', 0.15, 20),
            ('bg_3', 0.32, 40),
            ('bg_4', 0.55, 60),
            ('bg_5', 0.80, 80)
        ]
        for key, speed, y_off in layers:
            img = sprite_mgr.get(key)
            if not img:
                continue
            scroll_x = int(-(cam_x * speed) % bg_w)
            if scroll_x > 0:
                scroll_x -= bg_w
            x = scroll_x
            while x < INTERNAL_WIDTH + bg_w:
                surface.blit(img, (x, int(y_off - cam_y * 0.1)))
                x += bg_w

        # Tint overlay
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        if self.stage_idx == 2:
            overlay.fill((237, 137, 54, 55)) # Sunset
            surface.blit(overlay, (0, 0))
        elif self.stage_idx == 3:
            overlay.fill((215, 60, 45, 55)) # Crimson dusk
            surface.blit(overlay, (0, 0))
        elif self.stage_idx == 4:
            overlay.fill((15, 23, 60, 95)) # Moonlight
            surface.blit(overlay, (0, 0))
        elif self.stage_idx == 5:
            overlay.fill((80, 15, 30, 80)) # Blood moon
            surface.blit(overlay, (0, 0))

        # Ambient floating particles in stages 3, 4, 5
        if self.stage_idx >= 3:
            p_surf = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
            for p in self.ambient_particles:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['pulse'] += dt * 3
                if p['y'] < -10: p['y'] = INTERNAL_HEIGHT + 10
                if p['x'] < -10: p['x'] = INTERNAL_WIDTH + 10
                if p['x'] > INTERNAL_WIDTH + 10: p['x'] = -10

                a = max(0.1, p['alpha'] + math.sin(p['pulse']) * 0.3)
                color = (78, 204, 163, int(a * 255)) if self.stage_idx == 4 else ((255, 77, 77, int(a * 255)) if self.stage_idx == 5 else (255, 215, 0, int(a * 255)))
                pygame.draw.rect(p_surf, color, (int(p['x']), int(p['y']), p['size'], p['size']))
            surface.blit(p_surf, (0, 0))

    def draw_props(self, surface, sprite_mgr, cam_x, cam_y):
        for prop in self.props:
            img = sprite_mgr.get(prop['type'])
            if img:
                px = prop['x'] - cam_x
                py = prop['y'] - cam_y
                if -150 < px < INTERNAL_WIDTH + 50:
                    surface.blit(img, (int(px), int(py)))

    def draw_tiles(self, surface, sprite_mgr, cam_x, cam_y):
        tileset = sprite_mgr.get('tileset')
        if not tileset:
            return
        start_col = max(0, int(cam_x // self.tile_size))
        end_col = min(self.width_in_tiles - 1, int((cam_x + INTERNAL_WIDTH) // self.tile_size) + 1)
        start_row = max(0, int(cam_y // self.tile_size))
        end_row = min(self.height_in_tiles - 1, int((cam_y + INTERNAL_HEIGHT) // self.tile_size) + 1)

        for ty in range(start_row, end_row + 1):
            for tx in range(start_col, end_col + 1):
                tid = self.tiles[ty][tx]
                if tid <= 0:
                    continue
                t_idx = tid - 1
                sx = (t_idx % 10) * 32
                sy = (t_idx // 10) * 32
                sub_rect = pygame.Rect(sx, sy, 32, 32)
                surface.blit(tileset, (int(tx * 32 - cam_x), int(ty * 32 - cam_y)), sub_rect)
