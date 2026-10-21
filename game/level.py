import pygame
import random
import math
from game.settings import *
from game.objects import (
    Coin, Chest, KeyItem, RuneGate, GoalFlag,
    Spikes, SawBlade, MovingPlatform, CrackedWall,
    CheckpointTorch, PotionItem, GemItem, OwlHelper, BossShockwave
)
from game.enemy import OrcEnemy

class Level:
    def __init__(self, stage_idx=1):
        self.stage_idx = stage_idx
        self.tile_size = TILE_SIZE
        self.width_in_tiles = 115
        self.height_in_tiles = 16
        self.width_in_pixels = self.width_in_tiles * self.tile_size
        self.height_in_pixels = self.height_in_tiles * self.tile_size

        self.tiles = []
        self.one_way_platforms = []
        self.props = []
        self.ambient_particles = []

        # Interactive Stage Entities
        self.spikes = []
        self.saw_blades = []
        self.moving_platforms = []
        self.cracked_walls = []
        self.checkpoints = []
        self.potions = []
        self.gems = []
        self.owls = []
        self.shockwaves = []
        self.enemies = []
        self.coins = []
        self.chests = []
        self.key_item = None
        self.rune_gate = None
        self.goal = None
        self.boss = None
        self.player_start = (64, 11 * 32 - 26)

        self.init_ambient()
        self.build_stage(stage_idx)

    def init_ambient(self):
        self.ambient_particles = []
        for _ in range(32):
            self.ambient_particles.append({
                'x': random.uniform(0, INTERNAL_WIDTH),
                'y': random.uniform(0, INTERNAL_HEIGHT),
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(-18, -4),
                'size': random.choice([1, 2]),
                'alpha': random.uniform(0.3, 0.75),
                'pulse': random.uniform(0, math.pi * 2)
            })

    def build_stage(self, stage_idx):
        self.tiles = [[0 for _ in range(self.width_in_tiles)] for _ in range(self.height_in_tiles)]
        self.one_way_platforms = []
        self.props = []
        self.spikes = []
        self.saw_blades = []
        self.moving_platforms = []
        self.cracked_walls = []
        self.checkpoints = []
        self.potions = []
        self.gems = []
        self.owls = []
        self.shockwaves = []
        self.enemies = []
        self.coins = []
        self.chests = []

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
                if tx >= self.width_in_tiles or y >= self.height_in_tiles:
                    continue
                tile_id = 8
                if gx == 0: tile_id = 7
                elif gx == w - 1: tile_id = 9
                self.tiles[y][tx] = tile_id
                self.one_way_platforms.append(pygame.Rect(tx * self.tile_size, y * self.tile_size, self.tile_size, 10))

        def create_wall(x, y1, y2):
            for y in range(y1, y2):
                if 0 <= x < self.width_in_tiles and 0 <= y < self.height_in_tiles:
                    self.tiles[y][x] = 12

        def add_spikes(tx1, tx2, ty):
            for tx in range(tx1, tx2 + 1):
                self.spikes.append(Spikes(tx * 32, ty * 32))

        def add_coin_arc(start_tx, ty, count=4):
            for i in range(count):
                self.coins.append(Coin((start_tx + i) * 32, (ty - math.sin(i / max(1, count - 1) * math.pi) * 1.2) * 32))

        # Left border wall
        for y in range(self.height_in_tiles):
            self.tiles[y][0] = 11

        # =========================================================================
        # FASE 1: AS FRONTEIRAS DA FLORESTA & TORRE DE VIGIA
        # =========================================================================
        if stage_idx == 1:
            self.player_start = (64, 11 * 32 - 26)

            # Coruja sábia de introdução
            self.owls.append(OwlHelper(3 * 32, 11 * 32 - 32, "Ola guerreiro!\nUse [A/D] andar, [ESPACO] pular\n[J] cortar correndo!\nSegure [SHIFT] para dar DASH!"))

            create_ground(0, 11, 16, 5)
            self.enemies.append(OrcEnemy(11 * 32, 11 * 32 - 28, 40, 'orc1'))
            add_coin_arc(5, 10, 4)

            # Spike pit
            create_ground(16, 14, 8, 2)
            add_spikes(17, 22, 13)
            create_float_plat(19, 10, 3)

            # Terrace with cracked secret wall
            create_ground(24, 10, 12, 6)
            self.enemies.append(OrcEnemy(27 * 32, 10 * 32 - 28, 60, 'orc1'))
            self.cracked_walls.append(CrackedWall(35 * 32, 9 * 32))
            create_ground(36, 11, 6, 5)
            self.potions.append(PotionItem(38 * 32, 10 * 32))
            self.gems.append(GemItem(40 * 32, 10 * 32))

            # Watchtower Ascent
            create_ground(42, 7, 4, 9)
            create_wall(48, 2, 11)
            create_float_plat(44, 4, 3)
            self.chests.append(Chest(44 * 32, 4 * 32 - 24, grants_upgrade=True)) # Iron Armor Lv2

            # Checkpoint Torch
            create_ground(49, 11, 12, 5)
            self.checkpoints.append(CheckpointTorch(51 * 32, 11 * 32 - 48))
            self.enemies.append(OrcEnemy(56 * 32, 11 * 32 - 28, 50, 'orc1'))

            # Moving platform
            create_ground(61, 14, 10, 2)
            add_spikes(62, 69, 13)
            self.moving_platforms.append(MovingPlatform(62 * 32, 10 * 32, distance_x=6 * 32, speed=55.0))
            add_coin_arc(64, 8, 4)

            # Fortress gate
            create_ground(71, 10, 14, 6)
            self.enemies.append(OrcEnemy(75 * 32, 10 * 32 - 28, 60, 'orc2'))
            create_float_plat(80, 8, 4)
            self.coins.append(Coin(81 * 32, 7 * 32))
            self.coins.append(Coin(82 * 32, 7 * 32))

            # Final bridge
            create_ground(86, 11, 26, 5)
            self.enemies.append(OrcEnemy(93 * 32, 11 * 32 - 28, 60, 'orc1'))
            self.chests.append(Chest(98 * 32, 11 * 32 - 24, grants_upgrade=False))
            self.goal = GoalFlag(106 * 32, 11 * 32 - 48)

            for y in range(11): self.tiles[y][112] = 13
            self.props = [
                {'type': 'tree_1', 'x': 2 * 32, 'y': 11 * 32 - 103},
                {'type': 'stone_1', 'x': 14 * 32, 'y': 11 * 32 - 59},
                {'type': 'willow_1', 'x': 26 * 32, 'y': 10 * 32 - 135},
                {'type': 'tree_2', 'x': 53 * 32, 'y': 11 * 32 - 132},
                {'type': 'stone_2', 'x': 72 * 32, 'y': 10 * 32 - 59},
                {'type': 'tree_1', 'x': 88 * 32, 'y': 11 * 32 - 103}
            ]

        # =========================================================================
        # FASE 2: AS RUÍNAS DO ENTARDECER & LÂMINAS DE SERRA
        # =========================================================================
        elif stage_idx == 2:
            self.player_start = (64, 11 * 32 - 26)

            # Coruja sábia alerta sobre a serra
            self.owls.append(OwlHelper(8 * 32, 11 * 32 - 32, "Cuidado com a Serra!\nUse [SHIFT] DASH para passar\ninvulneravel ou pule por cima!"))

            create_ground(0, 11, 14, 5)
            self.enemies.append(OrcEnemy(9 * 32, 11 * 32 - 28, 45, 'orc1'))

            # Fork path
            create_ground(14, 14, 12, 2)
            add_spikes(15, 24, 13)
            create_float_plat(15, 9, 3)
            create_float_plat(19, 7, 3)
            create_float_plat(23, 9, 3)
            self.gems.append(GemItem(20 * 32, 6 * 32))

            # Central Fortress with saw blade
            create_ground(26, 9, 16, 7)
            self.saw_blades.append(SawBlade(29 * 32, 8 * 32, patrol_distance=6 * 32, speed=60.0))
            self.enemies.append(OrcEnemy(38 * 32, 9 * 32 - 28, 50, 'orc2'))

            # Key Tower
            create_float_plat(32, 6, 3)
            create_ground(35, 4, 5, 12)
            self.key_item = KeyItem(37 * 32, 3 * 32 - 16)
            self.potions.append(PotionItem(36 * 32, 3 * 32))

            # Checkpoint
            create_ground(43, 10, 12, 6)
            self.checkpoints.append(CheckpointTorch(45 * 32, 10 * 32 - 48))
            self.enemies.append(OrcEnemy(50 * 32, 10 * 32 - 28, 55, 'orc2'))

            # Moving platform over spikes
            create_ground(55, 14, 14, 2)
            add_spikes(56, 67, 13)
            self.moving_platforms.append(MovingPlatform(57 * 32, 10 * 32, distance_x=7 * 32, speed=65.0))
            add_coin_arc(59, 8, 4)

            # Secret Chamber
            create_ground(69, 9, 14, 7)
            self.cracked_walls.append(CrackedWall(69 * 32, 8 * 32))
            self.chests.append(Chest(71 * 32, 9 * 32 - 24, grants_upgrade=False))
            self.enemies.append(OrcEnemy(77 * 32, 9 * 32 - 28, 60, 'orc2'))

            # Rune Gate
            create_ground(84, 9, 28, 7)
            self.rune_gate = RuneGate(94 * 32, 9 * 32 - 24)
            self.enemies.append(OrcEnemy(88 * 32, 9 * 32 - 28, 50, 'orc1'))
            self.enemies.append(OrcEnemy(99 * 32, 9 * 32 - 28, 60, 'orc2'))
            self.goal = GoalFlag(106 * 32, 9 * 32 - 48)

            for y in range(9): self.tiles[y][112] = 13
            self.props = [
                {'type': 'stone_2', 'x': 3 * 32, 'y': 11 * 32 - 59},
                {'type': 'tree_2', 'x': 27 * 32, 'y': 9 * 32 - 132},
                {'type': 'stone_1', 'x': 44 * 32, 'y': 10 * 32 - 59},
                {'type': 'willow_1', 'x': 72 * 32, 'y': 9 * 32 - 135}
            ]

        # =========================================================================
        # FASE 3: O DESFILADEIRO DOS SALGUEIROS & ESCALADA VERTICAL
        # =========================================================================
        elif stage_idx == 3:
            self.player_start = (64, 10 * 32 - 26)

            # Coruja sábia ensina Wall Jump
            self.owls.append(OwlHelper(6 * 32, 10 * 32 - 32, "Voce pode saltar na parede!\nDeslize na pedra e aperte\n[ESPACO] para subir o canyon!"))

            create_ground(0, 10, 14, 6)
            self.enemies.append(OrcEnemy(8 * 32, 10 * 32 - 28, 45, 'orc1'))

            # Vertical moving lift
            create_ground(14, 15, 14, 1)
            add_spikes(15, 26, 14)
            self.moving_platforms.append(MovingPlatform(16 * 32, 11 * 32, distance_y=-5 * 32, speed=45.0))
            create_float_plat(20, 6, 4)
            self.coins.append(Coin(21 * 32, 5 * 32))
            self.coins.append(Coin(22 * 32, 5 * 32))

            # Wall-jump canyon with vertical saw
            create_ground(26, 11, 6, 5)
            create_wall(32, 3, 11)
            self.saw_blades.append(SawBlade(29 * 32, 4 * 32, patrol_distance=5 * 32, speed=50.0, is_vertical=True))
            create_float_plat(28, 4, 3)
            self.gems.append(GemItem(29 * 32, 3 * 32))

            # Checkpoint
            create_ground(33, 9, 12, 7)
            self.checkpoints.append(CheckpointTorch(35 * 32, 9 * 32 - 48))
            self.enemies.append(OrcEnemy(40 * 32, 9 * 32 - 28, 55, 'orc2'))

            # Double moving platforms
            create_ground(45, 15, 16, 1)
            add_spikes(46, 59, 14)
            self.moving_platforms.append(MovingPlatform(46 * 32, 9 * 32, distance_x=5 * 32, speed=60.0))
            self.moving_platforms.append(MovingPlatform(54 * 32, 7 * 32, distance_x=5 * 32, speed=60.0))
            add_coin_arc(51, 6, 4)

            # High canopy bridge
            create_ground(62, 8, 14, 8)
            self.enemies.append(OrcEnemy(66 * 32, 8 * 32 - 28, 60, 'orc2'))
            self.cracked_walls.append(CrackedWall(75 * 32, 7 * 32))
            self.potions.append(PotionItem(77 * 32, 7 * 32))

            create_ground(77, 9, 12, 7)
            self.enemies.append(OrcEnemy(82 * 32, 9 * 32 - 28, 60, 'orc2'))
            create_float_plat(87, 7, 3)
            self.chests.append(Chest(88 * 32, 7 * 32 - 24, grants_upgrade=False))

            # Final gauntlet
            create_ground(90, 10, 22, 6)
            self.saw_blades.append(SawBlade(94 * 32, 9 * 32, patrol_distance=4 * 32, speed=55.0))
            self.enemies.append(OrcEnemy(101 * 32, 10 * 32 - 28, 50, 'orc1'))
            self.goal = GoalFlag(106 * 32, 10 * 32 - 48)

            for y in range(10): self.tiles[y][112] = 13
            self.props = [
                {'type': 'willow_1', 'x': 2 * 32, 'y': 10 * 32 - 135},
                {'type': 'stone_2', 'x': 27 * 32, 'y': 11 * 32 - 59},
                {'type': 'tree_2', 'x': 64 * 32, 'y': 8 * 32 - 132}
            ]

        # =========================================================================
        # FASE 4: AS CATACUMBAS SUBTERRÂNEAS ALAGADAS (NOVA FASE!)
        # =========================================================================
        elif stage_idx == 4:
            self.player_start = (64, 11 * 32 - 26)

            # Coruja das catacumbas
            self.owls.append(OwlHelper(6 * 32, 11 * 32 - 32, "As Catacumbas guardam segredos!\nGolpeie paredes rachadas para abrir\nsalas secretas com tesouros!"))

            create_ground(0, 11, 15, 5)
            self.enemies.append(OrcEnemy(10 * 32, 11 * 32 - 28, 45, 'orc1'))

            # Flooded spike water trap
            create_ground(15, 14, 12, 2)
            add_spikes(16, 25, 13)
            create_float_plat(17, 9, 3)
            create_float_plat(22, 8, 3)
            self.gems.append(GemItem(20 * 32, 6 * 32))

            # Crypt hall with cracked wall
            create_ground(27, 9, 14, 7)
            self.enemies.append(OrcEnemy(31 * 32, 9 * 32 - 28, 50, 'orc2'))
            self.cracked_walls.append(CrackedWall(37 * 32, 8 * 32))
            self.chests.append(Chest(39 * 32, 9 * 32 - 24, grants_upgrade=False))

            # Key chamber
            create_float_plat(43, 6, 3)
            create_ground(46, 5, 6, 11)
            self.key_item = KeyItem(48 * 32, 4 * 32 - 16)
            self.potions.append(PotionItem(49 * 32, 4 * 32))

            # Checkpoint
            create_ground(53, 10, 12, 6)
            self.checkpoints.append(CheckpointTorch(55 * 32, 10 * 32 - 48))
            self.enemies.append(OrcEnemy(60 * 32, 10 * 32 - 28, 50, 'orc2'))

            # Moving platform crossing
            create_ground(65, 14, 14, 2)
            add_spikes(66, 77, 13)
            self.moving_platforms.append(MovingPlatform(67 * 32, 10 * 32, distance_x=7 * 32, speed=60.0))
            add_coin_arc(70, 8, 4)

            # Rune Gate
            create_ground(80, 9, 14, 7)
            self.enemies.append(OrcEnemy(84 * 32, 9 * 32 - 28, 55, 'orc2'))
            self.rune_gate = RuneGate(91 * 32, 9 * 32 - 24)

            create_ground(95, 10, 18, 6)
            self.enemies.append(OrcEnemy(100 * 32, 10 * 32 - 28, 50, 'orc1'))
            self.goal = GoalFlag(106 * 32, 10 * 32 - 48)

            for y in range(10): self.tiles[y][112] = 13
            self.props = [
                {'type': 'stone_1', 'x': 4 * 32, 'y': 11 * 32 - 59},
                {'type': 'stone_2', 'x': 28 * 32, 'y': 9 * 32 - 59},
                {'type': 'stone_1', 'x': 82 * 32, 'y': 9 * 32 - 59}
            ]

        # =========================================================================
        # FASE 5: O PÂNTANO DA LUA DE SANGUE & CASTELO INTERIOR
        # =========================================================================
        elif stage_idx == 5:
            self.player_start = (64, 11 * 32 - 26)

            # Coruja sábia ensina Pogo Attack
            self.owls.append(OwlHelper(6 * 32, 11 * 32 - 32, "Segure [S no ar] para dar POGO!\nVoce pode quicar na cabeca dos orcs\ne saltar em cima de espinhos!"))

            create_ground(0, 11, 14, 5)
            self.enemies.append(OrcEnemy(9 * 32, 11 * 32 - 28, 45, 'orc1'))

            create_ground(14, 15, 14, 1)
            add_spikes(15, 26, 14)
            create_float_plat(16, 10, 3)
            create_float_plat(21, 9, 3)
            self.saw_blades.append(SawBlade(18 * 32, 8 * 32, patrol_distance=4 * 32, speed=50.0))

            # Secret Armory: Level 3 Golden Knight Armor!
            create_ground(27, 9, 12, 7)
            self.cracked_walls.append(CrackedWall(27 * 32, 8 * 32))
            self.chests.append(Chest(29 * 32, 9 * 32 - 24, grants_upgrade=True)) # GOLDEN ARMOR!
            self.enemies.append(OrcEnemy(34 * 32, 9 * 32 - 28, 50, 'orc2'))

            # High Fortress Ramparts
            create_ground(39, 6, 6, 10)
            self.key_item = KeyItem(41 * 32, 5 * 32 - 16)
            self.potions.append(PotionItem(42 * 32, 5 * 32))

            # Checkpoint
            create_ground(46, 10, 14, 6)
            self.checkpoints.append(CheckpointTorch(48 * 32, 10 * 32 - 48))
            self.enemies.append(OrcEnemy(53 * 32, 10 * 32 - 28, 60, 'orc2'))

            # Synchronized moving platforms
            create_ground(60, 15, 16, 1)
            add_spikes(61, 74, 14)
            self.moving_platforms.append(MovingPlatform(61 * 32, 10 * 32, distance_x=5 * 32, speed=60.0))
            self.moving_platforms.append(MovingPlatform(68 * 32, 8 * 32, distance_x=5 * 32, speed=60.0))
            add_coin_arc(66, 7, 4)

            # Grand Portcullis & Rune Gate
            create_ground(76, 9, 16, 7)
            self.enemies.append(OrcEnemy(80 * 32, 9 * 32 - 28, 55, 'orc2'))
            self.rune_gate = RuneGate(87 * 32, 9 * 32 - 24)

            create_ground(92, 10, 20, 6)
            self.enemies.append(OrcEnemy(97 * 32, 10 * 32 - 28, 60, 'orc2'))
            self.gems.append(GemItem(102 * 32, 9 * 32))
            self.goal = GoalFlag(106 * 32, 10 * 32 - 48)

            for y in range(10): self.tiles[y][112] = 13
            self.props = [
                {'type': 'stone_1', 'x': 3 * 32, 'y': 11 * 32 - 59},
                {'type': 'willow_1', 'x': 28 * 32, 'y': 9 * 32 - 135},
                {'type': 'tree_2', 'x': 49 * 32, 'y': 10 * 32 - 132}
            ]

        # =========================================================================
        # FASE 6: O PICO CONGELADO DOS VENTOS (NOVA FASE!)
        # =========================================================================
        elif stage_idx == 6:
            self.player_start = (64, 10 * 32 - 26)

            self.owls.append(OwlHelper(6 * 32, 10 * 32 - 32, "Os ventos do pico sao fortes!\nCombine Pulo + DASH no ar para\natravessar precipicios distantes!"))

            create_ground(0, 10, 14, 6)
            self.enemies.append(OrcEnemy(8 * 32, 10 * 32 - 28, 45, 'orc1'))

            # Chasm with floating icy platforms
            create_ground(14, 15, 16, 1)
            add_spikes(15, 28, 14)
            create_float_plat(16, 8, 3)
            create_float_plat(21, 6, 3)
            create_float_plat(26, 7, 3)
            self.gems.append(GemItem(22 * 32, 4 * 32))

            # Icy fortress with vertical saw
            create_ground(30, 9, 14, 7)
            self.saw_blades.append(SawBlade(35 * 32, 4 * 32, patrol_distance=4 * 32, speed=55.0, is_vertical=True))
            self.enemies.append(OrcEnemy(38 * 32, 9 * 32 - 28, 50, 'orc2'))

            # Checkpoint
            create_ground(45, 10, 12, 6)
            self.checkpoints.append(CheckpointTorch(47 * 32, 10 * 32 - 48))
            self.potions.append(PotionItem(52 * 32, 9 * 32))

            # High altitude moving lift
            create_ground(57, 15, 16, 1)
            add_spikes(58, 71, 14)
            self.moving_platforms.append(MovingPlatform(58 * 32, 8 * 32, distance_x=8 * 32, speed=65.0))
            add_coin_arc(62, 6, 4)

            # Fortified outpost
            create_ground(73, 9, 16, 7)
            self.enemies.append(OrcEnemy(77 * 32, 9 * 32 - 28, 60, 'orc2'))
            self.cracked_walls.append(CrackedWall(86 * 32, 8 * 32))
            self.chests.append(Chest(88 * 32, 9 * 32 - 24, grants_upgrade=False))

            create_ground(90, 10, 22, 6)
            self.enemies.append(OrcEnemy(96 * 32, 10 * 32 - 28, 60, 'orc2'))
            self.goal = GoalFlag(106 * 32, 10 * 32 - 48)

            for y in range(10): self.tiles[y][112] = 13
            self.props = [
                {'type': 'stone_2', 'x': 2 * 32, 'y': 10 * 32 - 59},
                {'type': 'stone_1', 'x': 32 * 32, 'y': 9 * 32 - 59},
                {'type': 'tree_1', 'x': 75 * 32, 'y': 9 * 32 - 103}
            ]

        # =========================================================================
        # FASE 7: A FUNDIÇÃO VULCÂNICA DOS ORCS (NOVA FASE!)
        # =========================================================================
        elif stage_idx == 7:
            self.player_start = (64, 11 * 32 - 26)

            self.owls.append(OwlHelper(6 * 32, 11 * 32 - 32, "A Fundicao e o ultimo teste!\nMantenha a calma, use seus golpes\ne prepare-se para o Chefao!"))

            create_ground(0, 11, 14, 5)
            self.enemies.append(OrcEnemy(9 * 32, 11 * 32 - 28, 45, 'orc2'))

            # Lava pit with dual moving platforms
            create_ground(14, 15, 18, 1)
            add_spikes(15, 30, 14)
            self.moving_platforms.append(MovingPlatform(15 * 32, 10 * 32, distance_x=6 * 32, speed=60.0))
            self.moving_platforms.append(MovingPlatform(24 * 32, 8 * 32, distance_x=6 * 32, speed=60.0))
            add_coin_arc(20, 6, 4)

            # Smelter fortress with saw blades
            create_ground(33, 9, 16, 7)
            self.saw_blades.append(SawBlade(36 * 32, 8 * 32, patrol_distance=5 * 32, speed=65.0))
            self.enemies.append(OrcEnemy(44 * 32, 9 * 32 - 28, 60, 'orc2'))

            # Key chamber
            create_float_plat(41, 6, 3)
            create_ground(44, 4, 6, 12)
            self.key_item = KeyItem(46 * 32, 3 * 32 - 16)
            self.potions.append(PotionItem(47 * 32, 3 * 32))

            # Checkpoint
            create_ground(51, 10, 12, 6)
            self.checkpoints.append(CheckpointTorch(53 * 32, 10 * 32 - 48))
            self.enemies.append(OrcEnemy(58 * 32, 10 * 32 - 28, 60, 'orc2'))

            # Lava bridge with vertical saw
            create_ground(63, 15, 14, 1)
            add_spikes(64, 75, 14)
            create_float_plat(65, 9, 3)
            create_float_plat(70, 8, 3)
            self.saw_blades.append(SawBlade(68 * 32, 5 * 32, patrol_distance=4 * 32, speed=55.0, is_vertical=True))

            # Rune Gate
            create_ground(77, 9, 14, 7)
            self.enemies.append(OrcEnemy(81 * 32, 9 * 32 - 28, 60, 'orc2'))
            self.rune_gate = RuneGate(87 * 32, 9 * 32 - 24)

            create_ground(92, 10, 20, 6)
            self.gems.append(GemItem(98 * 32, 9 * 32))
            self.goal = GoalFlag(106 * 32, 10 * 32 - 48)

            for y in range(10): self.tiles[y][112] = 13
            self.props = [
                {'type': 'stone_1', 'x': 3 * 32, 'y': 11 * 32 - 59},
                {'type': 'stone_2', 'x': 34 * 32, 'y': 9 * 32 - 59},
                {'type': 'stone_1', 'x': 78 * 32, 'y': 9 * 32 - 59}
            ]

        # =========================================================================
        # FASE 8: A GRANDE FORTALEZA DO GENERAL ORC (O CLÍMAX FINAL!)
        # =========================================================================
        elif stage_idx == 8:
            self.player_start = (64, 10 * 32 - 26)

            # Coruja sábia na entrada do trono
            self.owls.append(OwlHelper(6 * 32, 10 * 32 - 32, "CUIDADO COM O GENERAL!\nEle bate no chao criando ondas!\nPule nos andares altos para desviar\ne caia com POGO na cabeca dele!"))

            create_ground(0, 10, 14, 6)
            self.enemies.append(OrcEnemy(9 * 32, 10 * 32 - 28, 45, 'orc2'))

            # Hazard bridge
            create_ground(14, 15, 12, 1)
            add_spikes(15, 24, 14)
            create_float_plat(16, 8, 4)
            create_float_plat(21, 7, 3)
            self.saw_blades.append(SawBlade(18 * 32, 6 * 32, patrol_distance=4 * 32, speed=60.0))

            # Outer court
            create_ground(26, 9, 14, 7)
            self.enemies.append(OrcEnemy(30 * 32, 9 * 32 - 28, 60, 'orc2'))
            self.enemies.append(OrcEnemy(36 * 32, 9 * 32 - 28, 60, 'orc2'))

            # Pre-Boss Sanctuary (Full Health & Checkpoint!)
            create_ground(40, 9, 12, 7)
            self.checkpoints.append(CheckpointTorch(42 * 32, 9 * 32 - 48))
            self.potions.append(PotionItem(45 * 32, 8 * 32))
            self.chests.append(Chest(48 * 32, 9 * 32 - 24, grants_upgrade=False))

            # =====================================================================
            # THE BOSS ARENA (Throne Room of General Orc)
            # Multi-tiered 3-level ledges to evade ground shockwaves & pogo boss!
            # =====================================================================
            create_ground(53, 9, 58, 7) # Main arena floor
            create_wall(53, 2, 9) # Arena left entrance wall
            create_wall(109, 2, 9) # Arena right throne wall

            # Elevated tactical ledges (Tier 1 & Tier 2)
            create_float_plat(60, 6, 4)
            create_float_plat(72, 5, 5)
            create_float_plat(84, 5, 5)
            create_float_plat(96, 6, 4)

            # Coins & Gems in rafters
            self.coins.append(Coin(62 * 32, 4 * 32))
            self.coins.append(Coin(74 * 32, 3 * 32))
            self.coins.append(Coin(86 * 32, 3 * 32))
            self.coins.append(Coin(98 * 32, 4 * 32))
            self.gems.append(GemItem(80 * 32, 3 * 32))

            # THE BOSS: GENERAL ORC (Smart Boss AI with Shockwaves!)
            self.boss = OrcEnemy(82 * 32, 9 * 32 - 32, 120, 'orc3')
            self.enemies.append(self.boss)

            # Final Victory Flag at throne!
            self.goal = GoalFlag(105 * 32, 9 * 32 - 48)

            self.props = [
                {'type': 'stone_2', 'x': 2 * 32, 'y': 10 * 32 - 59},
                {'type': 'tree_2', 'x': 28 * 32, 'y': 9 * 32 - 132},
                {'type': 'stone_1', 'x': 56 * 32, 'y': 9 * 32 - 59},
                {'type': 'tree_1', 'x': 90 * 32, 'y': 9 * 32 - 103}
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
        left_t = max(0, rect.left // self.tile_size)
        right_t = min(self.width_in_tiles - 1, rect.right // self.tile_size)
        top_t = max(0, rect.top // self.tile_size)
        bottom_t = min(self.height_in_tiles - 1, rect.bottom // self.tile_size)

        for ty in range(top_t, bottom_t + 1):
            for tx in range(left_t, right_t + 1):
                tid = self.tiles[ty][tx]
                if self.is_tile_solid(tid):
                    tile_rect = pygame.Rect(tx * self.tile_size, ty * self.tile_size, self.tile_size, self.tile_size)
                    if rect.colliderect(tile_rect):
                        return tile_rect

        for cw in self.cracked_walls:
            if not cw.destroyed and rect.colliderect(cw.rect):
                return cw.rect

        return None

    def check_one_way_platform(self, px, py, pw, p_vy):
        player_feet = pygame.Rect(round(px), round(py - 4), pw, 8)
        for plat in self.one_way_platforms:
            if player_feet.colliderect(plat) and (py - p_vy) <= plat.top + 6:
                return plat
        return None

    def draw_background(self, surface, sprite_mgr, cam_x, cam_y, dt):
        bg_w = 480
        speeds = [0.05, 0.12, 0.22, 0.38, 0.55]
        y_offsets = [0, 10, 15, 20, 30]

        for i in range(1, 6):
            img = sprite_mgr.get(f'bg_{i}')
            if not img:
                continue
            speed = speeds[i - 1]
            y_off = y_offsets[i - 1]

            scroll_x = int(-(cam_x * speed) % bg_w)
            if scroll_x > 0:
                scroll_x -= bg_w
            x = scroll_x
            while x < INTERNAL_WIDTH + bg_w:
                surface.blit(img, (x, int(y_off - cam_y * 0.08)))
                x += bg_w

        # Stage Atmospheric Lighting & Tint (8 distinct palettes!)
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        if self.stage_idx == 1:
            overlay.fill((30, 80, 50, 15)) # Lush forest green
        elif self.stage_idx == 2:
            overlay.fill((237, 137, 54, 45)) # Sunset glow
        elif self.stage_idx == 3:
            overlay.fill((70, 160, 180, 40)) # Misty canyon teal
        elif self.stage_idx == 4:
            overlay.fill((20, 45, 60, 75)) # Deep subterranean blue
        elif self.stage_idx == 5:
            overlay.fill((45, 15, 60, 85)) # Blood moon marsh
        elif self.stage_idx == 6:
            overlay.fill((160, 210, 255, 35)) # Frozen peak frost
        elif self.stage_idx == 7:
            overlay.fill((220, 60, 20, 60)) # Volcanic magma glow
        elif self.stage_idx == 8:
            overlay.fill((90, 15, 30, 80)) # Royal throne crimson

        surface.blit(overlay, (0, 0))

        # Ambient floating dust particles
        if self.stage_idx >= 2:
            p_surf = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
            for p in self.ambient_particles:
                p['x'] += p['vx'] * dt
                p['y'] += p['vy'] * dt
                p['pulse'] += dt * 3
                if p['y'] < -10: p['y'] = INTERNAL_HEIGHT + 10
                if p['x'] < -10: p['x'] = INTERNAL_WIDTH + 10
                if p['x'] > INTERNAL_WIDTH + 10: p['x'] = -10

                a = max(0.1, p['alpha'] + math.sin(p['pulse']) * 0.3)
                if self.stage_idx in [1, 2, 3]:
                    color = (255, 215, 0, int(a * 220)) # Gold pollen
                elif self.stage_idx == 4:
                    color = (56, 217, 235, int(a * 220)) # Luminescent cave spores
                elif self.stage_idx == 6:
                    color = (240, 250, 255, int(a * 240)) # Snowflakes
                elif self.stage_idx == 7:
                    color = (255, 120, 30, int(a * 240)) # Fiery embers
                else:
                    color = (255, 50, 50, int(a * 230)) # Crimson wrath

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
