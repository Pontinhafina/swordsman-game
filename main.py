import pygame
import sys
import os

from game.settings import *
from game.sound import sound
from game.sprites import init_sprites
from game.particles import particles
from game.player import Player
from game.enemy import OrcEnemy
from game.objects import (
    Coin, Chest, KeyItem, RuneGate, GoalFlag,
    Spikes, SawBlade, MovingPlatform, CrackedWall,
    CheckpointTorch, PotionItem, GemItem, OwlHelper, BossShockwave,
    FallingIcicle, IceSpikeHazard
)
from game.level import Level

class PlatformerGame:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Swordsman: A Saga das 10 Fases")

        self.fullscreen = False
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        self.canvas = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.Font(None, 16)
        self.font_large = pygame.font.Font(None, 24)
        self.font_title = pygame.font.Font(None, 32)

        self.sprite_mgr = init_sprites()

        self.current_stage = 1
        self.total_stages = 10
        self.state = 'title' # 'title', 'playing', 'paused', 'stage_clear', 'gameover', 'victory'

        self.stats = {'score': 0, 'coins': 0}
        self.saved_hero_level = 1
        self.start_ticks = 0

        self.cam_x = 0.0
        self.cam_y = 0.0

        self.stage_titles = [
            "",
            "FASE 1: AS FRONTEIRAS DA FLORESTA & TORRE DE VIGIA",
            "FASE 2: AS RUÍNAS DO ENTARDECER & LÂMINAS DE SERRA",
            "FASE 3: O DESFILADEIRO DOS SALGUEIROS & ESCALADA",
            "FASE 4: AS DUNAS ESCALDANTES & TEMPLO DO DESERTO",
            "FASE 5: O OÁSIS SECRETO & CATACUMBA ENTERRADA",
            "FASE 6: AS CATACUMBAS SUBTERRÂNEAS ALAGADAS",
            "FASE 7: AS CAVERNAS DE CRISTAL E ESTALACTITES",
            "FASE 8: O TRONO GLACIAL DO TITÃ DE GELO (BOSS)",
            "FASE 9: A FUNDIÇÃO VULCÂNICA DOS ORCS",
            "FASE 10: A GRANDE FORTALEZA DO GENERAL ORC (CLÍMAX FINAL)"
        ]

        self.level = None
        self.player = None
        self.enemies = []
        self.coins = []
        self.chests = []
        self.spikes = []
        self.saw_blades = []
        self.moving_platforms = []
        self.cracked_walls = []
        self.checkpoints = []
        self.potions = []
        self.gems = []
        self.owls = []
        self.shockwaves = []
        self.icicles = []
        self.ice_spikes = []
        self.key_item = None
        self.rune_gate = None
        self.goal = None
        self.boss = None

        self.init_gamepad()

    def init_gamepad(self):
        self.joystick = None
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

    def load_stage(self, stage_num):
        self.current_stage = stage_num
        self.level = Level(stage_num)

        start_x, start_y = self.level.player_start
        self.player = Player(start_x, start_y)
        self.player.hero_level = self.saved_hero_level

        self.enemies = self.level.enemies
        self.coins = self.level.coins
        self.chests = self.level.chests
        self.spikes = self.level.spikes
        self.saw_blades = self.level.saw_blades
        self.moving_platforms = self.level.moving_platforms
        self.cracked_walls = self.level.cracked_walls
        self.checkpoints = self.level.checkpoints
        self.potions = self.level.potions
        self.gems = self.level.gems
        self.owls = self.level.owls
        self.shockwaves = self.level.shockwaves
        self.icicles = self.level.icicles
        self.ice_spikes = self.level.ice_spikes
        self.key_item = self.level.key_item
        self.rune_gate = self.level.rune_gate
        self.goal = self.level.goal
        self.boss = self.level.boss

        particles.clear()
        self.cam_x = 0.0
        self.cam_y = 0.0

        if stage_num in [8, 10]:
            sound.play_bgm('boss')
        else:
            sound.play_bgm('stage')

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            if dt > 0.08: dt = 0.08

            keys_pressed = {
                'left': False, 'right': False, 'up': False, 'down': False,
                'jump': False, 'jump_pressed': False,
                'attack_pressed': False, 'dash_pressed': False, 'interact_pressed': False
            }

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                        if self.state == 'playing': self.state = 'paused'
                        elif self.state == 'paused': self.state = 'playing'

                    if event.key == pygame.K_f:
                        self.toggle_fullscreen()

                    if event.key == pygame.K_m:
                        sound.toggle_music()

                    if self.state == 'title':
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_z, pygame.K_j]:
                            self.stats = {'score': 0, 'coins': 0}
                            self.saved_hero_level = 1
                            self.start_ticks = pygame.time.get_ticks()
                            self.load_stage(1)
                            self.state = 'playing'

                    elif self.state == 'stage_clear':
                        if event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                            self.load_stage(self.current_stage + 1)
                            self.state = 'playing'

                    elif self.state in ['gameover', 'victory']:
                        if event.key in [pygame.K_r, pygame.K_RETURN, pygame.K_SPACE]:
                            if self.state == 'victory':
                                self.stats = {'score': 0, 'coins': 0}
                                self.saved_hero_level = 1
                                self.start_ticks = pygame.time.get_ticks()
                                self.load_stage(1)
                            else:
                                self.load_stage(self.current_stage)
                            self.state = 'playing'

                    if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                        keys_pressed['jump_pressed'] = True
                    if event.key in [pygame.K_z, pygame.K_j]:
                        keys_pressed['attack_pressed'] = True
                    if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT, pygame.K_k, pygame.K_c]:
                        keys_pressed['dash_pressed'] = True
                    if event.key == pygame.K_e:
                        keys_pressed['interact_pressed'] = True

            # Polling continuous keyboard
            py_keys = pygame.key.get_pressed()
            keys_pressed['left'] = py_keys[pygame.K_LEFT] or py_keys[pygame.K_a]
            keys_pressed['right'] = py_keys[pygame.K_RIGHT] or py_keys[pygame.K_d]
            keys_pressed['up'] = py_keys[pygame.K_UP] or py_keys[pygame.K_w]
            keys_pressed['down'] = py_keys[pygame.K_DOWN] or py_keys[pygame.K_s]
            keys_pressed['jump'] = py_keys[pygame.K_SPACE] or py_keys[pygame.K_UP] or py_keys[pygame.K_w]

            # Polling Gamepad if connected
            if self.joystick:
                axis_x = self.joystick.get_axis(0)
                axis_y = self.joystick.get_axis(1)
                if axis_x < -0.3: keys_pressed['left'] = True
                elif axis_x > 0.3: keys_pressed['right'] = True
                if axis_y > 0.4: keys_pressed['down'] = True
                elif axis_y < -0.4: keys_pressed['up'] = True

                if self.joystick.get_button(0): keys_pressed['jump'] = True
                if self.joystick.get_button(2): keys_pressed['attack_pressed'] = True
                if self.joystick.get_button(1) or self.joystick.get_button(5): keys_pressed['dash_pressed'] = True
                if self.joystick.get_button(3): keys_pressed['interact_pressed'] = True

            # Update & Render
            self.update(dt, keys_pressed)
            self.render(dt)

            # Blit canvas to window
            w_w, w_h = self.window.get_size()
            scaled_surf = pygame.transform.scale(self.canvas, (w_w, w_h))
            self.window.blit(scaled_surf, (0, 0))
            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def update(self, dt, keys):
        if self.state != 'playing':
            return

        in_hitstop = particles.update(dt)
        if in_hitstop:
            return

        # Player
        self.player.update(dt, keys, self.level, self.enemies, self.chests, self.cracked_walls)

        # Helper Owls
        for owl in self.owls:
            owl.update(dt, self.player, self.potions)

        # Boss Shockwaves
        for sw in self.shockwaves:
            sw.update(dt, self.player)
        self.shockwaves = [sw for sw in self.shockwaves if sw.lifetime > 0]
        self.level.shockwaves = self.shockwaves

        # Falling Icicles
        for ic in self.icicles:
            ic.update(dt, self.player, self.level)

        # Ice Spike Hazards
        for isp in self.ice_spikes:
            isp.update(dt, self.player)
        self.ice_spikes = [isp for isp in self.ice_spikes if isp.lifetime > 0]
        self.level.ice_spikes = self.ice_spikes

        # Moving Platforms
        for mp in self.moving_platforms:
            mp.update(dt, self.player)

        # Hazards: Spikes & Saw Blades
        for sp in self.spikes:
            sp.update(dt, self.player)

        for sb in self.saw_blades:
            sb.update(dt, self.player)

        # Checkpoints
        for cp in self.checkpoints:
            cp.update(dt, self.player)

        # Items: Potions & Gems
        for pot in self.potions:
            pot.update(dt, self.player)

        for gem in self.gems:
            gem.update(dt, self.player, self.stats)

        # Enemies
        for e in self.enemies:
            e.update(dt, self.player, self.level, self.enemies, self.coins)

        # Coins & Chests
        for c in self.coins:
            c.update(dt, self.player, self.level, self.stats)

        for ch in self.chests:
            ch.update(dt, self.player, keys)

        # Key & Rune Gate
        if self.key_item:
            self.key_item.update(dt, self.player, self.stats)

        if self.rune_gate:
            self.rune_gate.update(dt, self.player)

        # Goal Flag / Stage Complete
        if self.goal:
            is_boss_beaten = not self.boss or self.boss.is_dead
            if self.current_stage not in [8, 10] or is_boss_beaten:
                won = self.goal.update(dt, self.player, self.rune_gate)
                if won:
                    self.saved_hero_level = self.player.hero_level
                    if self.current_stage < self.total_stages:
                        self.state = 'stage_clear'
                    else:
                        self.state = 'victory'

        # Smooth Camera with deadzone and platform lookahead
        target_cam_x = self.player.x + self.player.w / 2 - INTERNAL_WIDTH * 0.4
        target_cam_y = min(self.level.height_in_pixels - INTERNAL_HEIGHT, max(0, self.player.y + self.player.h / 2 - INTERNAL_HEIGHT * 0.55))

        self.cam_x += (target_cam_x - self.cam_x) * 0.10
        self.cam_y += (target_cam_y - self.cam_y) * 0.10
        self.cam_x = max(0, min(self.level.width_in_pixels - INTERNAL_WIDTH, self.cam_x))
        self.cam_y = max(0, min(self.level.height_in_pixels - INTERNAL_HEIGHT, self.cam_y))

        if self.player.is_dead and self.player.death_timer > 1.4:
            self.state = 'gameover'

    def render(self, dt):
        self.canvas.fill(COLOR_BG)

        if self.state == 'title':
            self.render_title()
            return

        sh_x, sh_y = particles.get_shake_offset()
        final_cam_x = self.cam_x + sh_x
        final_cam_y = self.cam_y + sh_y

        # Parallax Background
        self.level.draw_background(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y, dt)

        # Props
        self.level.draw_props(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Tiles
        self.level.draw_tiles(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Cracked Walls
        for cw in self.cracked_walls:
            cw.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Spikes
        for sp in self.spikes:
            sp.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Moving Platforms
        for mp in self.moving_platforms:
            mp.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Checkpoints
        for cp in self.checkpoints:
            cp.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Potions & Gems
        for pot in self.potions:
            pot.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        for gem in self.gems:
            gem.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Saw Blades
        for sb in self.saw_blades:
            sb.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Falling Icicles
        for ic in self.icicles:
            ic.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Ice Spike Hazards
        for isp in self.ice_spikes:
            isp.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Boss Shockwaves
        for sw in self.shockwaves:
            sw.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Helper Owls
        for owl in self.owls:
            owl.draw(self.canvas, self.sprite_mgr, self.font, self.player, final_cam_x, final_cam_y)

        # Objects: Key, Rune Gate, Chests, Coins
        if self.key_item:
            self.key_item.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)
        if self.rune_gate:
            self.rune_gate.draw(self.canvas, self.sprite_mgr, self.font, self.player, final_cam_x, final_cam_y)
        for ch in self.chests:
            ch.draw(self.canvas, self.sprite_mgr, self.font, self.player, final_cam_x, final_cam_y)
        for c in self.coins:
            c.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Goal Flag
        if self.goal:
            if self.current_stage not in [8, 10] or (self.boss and self.boss.is_dead):
                self.goal.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Enemies
        for e in self.enemies:
            e.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Player
        self.player.draw(self.canvas, self.sprite_mgr, final_cam_x, final_cam_y)

        # Particles & Damage Floating Text
        particles.draw(self.canvas, final_cam_x, final_cam_y)

        # HUD
        self.render_hud()

        # State Overlays
        if self.state == 'paused': self.render_paused()
        elif self.state == 'stage_clear': self.render_stage_clear()
        elif self.state == 'gameover': self.render_gameover()
        elif self.state == 'victory': self.render_victory()

    def render_hud(self):
        # Stage title banner
        txt = self.font.render(self.stage_titles[self.current_stage], False, (185, 200, 220))
        self.canvas.blit(txt, (14, 10))

        # Hearts
        for i in range(self.player.max_hp):
            hx = 14 + i * 14
            hy = 24
            c = COLOR_RED if i < self.player.hp else (65, 75, 95)
            pygame.draw.rect(self.canvas, c, (hx, hy + 2, 10, 8))
            pygame.draw.rect(self.canvas, c, (hx + 1, hy, 3, 2))
            pygame.draw.rect(self.canvas, c, (hx + 6, hy, 3, 2))
            pygame.draw.rect(self.canvas, c, (hx + 2, hy + 10, 6, 2))
            pygame.draw.rect(self.canvas, c, (hx + 4, hy + 12, 2, 2))

        # Hero armor badge
        lvl_names = ["", "NV.1 (Padrão)", "NV.2 (Ferro)", "NV.3 (Ouro)"]
        t_lvl = self.font.render(f"HERÓI: {lvl_names[self.player.hero_level]}", False, COLOR_GREEN)
        self.canvas.blit(t_lvl, (90, 24))

        # Dash Badge / Status
        if self.player.dash_cooldown <= 0.0:
            t_dash = self.font.render("DASH [PRONTO]", False, COLOR_CYAN)
        else:
            t_dash = self.font.render("DASH [...]", False, (120, 130, 145))
        self.canvas.blit(t_dash, (200, 24))

        # Music badge
        m_txt = "♫ ON" if sound.music_enabled else "♫ OFF"
        m_col = (140, 220, 140) if sound.music_enabled else (140, 140, 150)
        t_mus = self.font.render(f"[M] {m_txt}", False, m_col)
        self.canvas.blit(t_mus, (285, 24))

        # Coins & Score
        t_coins = self.font.render(f"💰 x {self.stats['coins']}", False, COLOR_GOLD)
        self.canvas.blit(t_coins, (345, 24))

        t_score = self.font.render(f"PTS: {self.stats['score']}", False, COLOR_WHITE)
        self.canvas.blit(t_score, (410, 24))

        # Boss health bar in stage 8 (Frost Boss) & stage 10 (General Orc)
        if self.boss and not self.boss.is_dead and self.player.x > 45 * 32:
            bx = 140
            by = 45
            bw = 200
            bh = 10
            pygame.draw.rect(self.canvas, (0, 0, 0), (bx - 2, by - 14, bw + 4, bh + 16))

            if getattr(self.boss, 'is_frost_boss', False):
                title = "⚡ TITÃ GLACIAL ENFURECIDO ⚡" if self.boss.enraged else "❄️ CHEFE: TITÃ GLACIAL DO NORTE ❄️"
                bar_color = COLOR_CYAN if not self.boss.enraged else (160, 240, 255)
            else:
                title = "⚡ GENERAL ORC ENFURECIDO ⚡" if self.boss.enraged else "⚔️ CHEFE: GENERAL ORC SUPREMO ⚔️"
                bar_color = COLOR_RED if not self.boss.enraged else (255, 40, 40)

            t_boss = self.font.render(title, False, bar_color)
            self.canvas.blit(t_boss, (bx + bw / 2 - t_boss.get_width() / 2, by - 12))

            pygame.draw.rect(self.canvas, (255, 255, 255), (bx, by, bw, bh), 1)
            pct = max(0.0, self.boss.hp / self.boss.max_hp)
            pygame.draw.rect(self.canvas, bar_color, (bx + 1, by + 1, int((bw - 2) * pct), bh - 2))

    def render_title(self):
        title_bg = self.sprite_mgr.get('title_bg')
        if title_bg:
            self.canvas.blit(title_bg, (0, 0))
            # Elegant dark vignette to make title & menu readable
            overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
            overlay.fill((10, 15, 25, 65))
            # Dark gradient at top for title
            pygame.draw.rect(overlay, (5, 8, 15, 160), (0, 0, INTERNAL_WIDTH, 70))
            # Dark gradient at bottom for menu & controls
            pygame.draw.rect(overlay, (5, 8, 15, 190), (0, 165, INTERNAL_WIDTH, 105))
            self.canvas.blit(overlay, (0, 0))
        else:
            self.canvas.fill(COLOR_BG)

        # Title shadow & gold text
        t1_shadow = self.font_title.render("SWORDSMAN: A SAGA DAS 10 FASES", False, (10, 10, 15))
        t1 = self.font_title.render("SWORDSMAN: A SAGA DAS 10 FASES", False, COLOR_GOLD)
        self.canvas.blit(t1_shadow, (INTERNAL_WIDTH / 2 - t1.get_width() / 2 + 2, 22))
        self.canvas.blit(t1, (INTERNAL_WIDTH / 2 - t1.get_width() / 2, 20))

        t2_shadow = self.font.render("Campanha Completa de 10 Fases • Deserto, Gelo & 2 Chefões Épicos", False, (0, 0, 0))
        t2 = self.font.render("Campanha Completa de 10 Fases • Deserto, Gelo & 2 Chefões Épicos", False, (220, 235, 255))
        self.canvas.blit(t2_shadow, (INTERNAL_WIDTH / 2 - t2.get_width() / 2 + 1, 51))
        self.canvas.blit(t2, (INTERNAL_WIDTH / 2 - t2.get_width() / 2, 50))

        # Start prompt with pulsing green/gold
        if int(pygame.time.get_ticks() / 450) % 2 == 0:
            prompt_sh = self.font_large.render("PRESSIONE [ENTER] OU [ESPAÇO] PARA JOGAR", False, (0, 0, 0))
            prompt = self.font_large.render("PRESSIONE [ENTER] OU [ESPAÇO] PARA JOGAR", False, (80, 255, 120))
            self.canvas.blit(prompt_sh, (INTERNAL_WIDTH / 2 - prompt.get_width() / 2 + 1, 181))
            self.canvas.blit(prompt, (INTERNAL_WIDTH / 2 - prompt.get_width() / 2, 180))

        # Controls & Tips
        h1 = self.font.render("[A/D] Mover  •  [ESPAÇO] Pular  •  [SHIFT/K] Dash  •  [J/Z] Cortar", False, COLOR_WHITE)
        h2 = self.font.render("[S no ar] Pogo Strike  •  [M] Música Chiptune  •  [F] Tela Cheia", False, (160, 200, 240))
        self.canvas.blit(h1, (INTERNAL_WIDTH / 2 - h1.get_width() / 2, 218))
        self.canvas.blit(h2, (INTERNAL_WIDTH / 2 - h2.get_width() / 2, 238))

    def render_stage_clear(self):
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 25, 20, 220))
        self.canvas.blit(overlay, (0, 0))

        t1 = self.font_large.render(f"FASE {self.current_stage} CONCLUÍDA!", False, COLOR_GREEN)
        self.canvas.blit(t1, (INTERNAL_WIDTH / 2 - t1.get_width() / 2, 70))

        t2 = self.font.render(f"Moedas: {self.stats['coins']}  •  Pontuação: {self.stats['score']}", False, COLOR_WHITE)
        self.canvas.blit(t2, (INTERNAL_WIDTH / 2 - t2.get_width() / 2, 105))

        t3 = self.font.render(f"Próxima: {self.stage_titles[self.current_stage + 1]}", False, COLOR_GOLD)
        self.canvas.blit(t3, (INTERNAL_WIDTH / 2 - t3.get_width() / 2, 135))

        if int(pygame.time.get_ticks() / 400) % 2 == 0:
            p = self.font.render("PRESSIONE [ENTER] PARA AVANÇAR", False, COLOR_WHITE)
            self.canvas.blit(p, (INTERNAL_WIDTH / 2 - p.get_width() / 2, 180))

    def render_gameover(self):
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((25, 0, 0, 210))
        self.canvas.blit(overlay, (0, 0))

        t = self.font_title.render("VOCÊ FOI DERROTADO!", False, COLOR_RED)
        self.canvas.blit(t, (INTERNAL_WIDTH / 2 - t.get_width() / 2, 75))

        sub = self.font.render(f"Fase: {self.current_stage}  •  Pontos: {self.stats['score']}", False, COLOR_WHITE)
        self.canvas.blit(sub, (INTERNAL_WIDTH / 2 - sub.get_width() / 2, 115))

        if int(pygame.time.get_ticks() / 400) % 2 == 0:
            p = self.font.render("PRESSIONE [R] PARA RECOMEÇAR ESTA FASE", False, COLOR_GOLD)
            self.canvas.blit(p, (INTERNAL_WIDTH / 2 - p.get_width() / 2, 170))

    def render_victory(self):
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((10, 30, 20, 230))
        self.canvas.blit(overlay, (0, 0))

        t = self.font_title.render("🎉 PARABÉNS! VOCÊ LIBERTOU TODAS AS 10 TERRAS! 🎉", False, COLOR_GOLD)
        self.canvas.blit(t, (INTERNAL_WIDTH / 2 - t.get_width() / 2, 50))

        sub = self.font.render("O Titã Glacial e o General Orc Supremo foram derrotados!", False, COLOR_GREEN)
        self.canvas.blit(sub, (INTERNAL_WIDTH / 2 - sub.get_width() / 2, 85))

        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        t_time = self.font.render(f"Tempo Total: {elapsed}s  •  Moedas Coletadas: {self.stats['coins']}", False, COLOR_WHITE)
        self.canvas.blit(t_time, (INTERNAL_WIDTH / 2 - t_time.get_width() / 2, 115))

        final_score = self.stats['score'] + self.stats['coins'] * 35
        t_sc = self.font_large.render(f"PONTUAÇÃO FINAL: {final_score}", False, COLOR_GOLD)
        self.canvas.blit(t_sc, (INTERNAL_WIDTH / 2 - t_sc.get_width() / 2, 145))

        if int(pygame.time.get_ticks() / 400) % 2 == 0:
            p = self.font.render("PRESSIONE [R] PARA JOGAR NOVAMENTE", False, COLOR_WHITE)
            self.canvas.blit(p, (INTERNAL_WIDTH / 2 - p.get_width() / 2, 195))

    def render_paused(self):
        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.canvas.blit(overlay, (0, 0))

        t = self.font_large.render("JOGO PAUSADO", False, COLOR_WHITE)
        self.canvas.blit(t, (INTERNAL_WIDTH / 2 - t.get_width() / 2, 110))

        sub = self.font.render("Pressione [ESC] ou [P] para continuar  •  [M] Música", False, (200, 210, 225))
        self.canvas.blit(sub, (INTERNAL_WIDTH / 2 - sub.get_width() / 2, 140))

if __name__ == '__main__':
    game = PlatformerGame()
    game.run()
