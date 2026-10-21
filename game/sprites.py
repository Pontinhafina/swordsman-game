import pygame
import os

class SpriteManager:
    def __init__(self):
        self.images = {}
        self.load_assets()

    def load_image(self, rel_path):
        if not os.path.exists(rel_path):
            print("Warning: Missing image:", rel_path)
            surf = pygame.Surface((32, 32), pygame.SRCALPHA)
            surf.fill((255, 0, 255))
            return surf
        return pygame.image.load(rel_path).convert_alpha()

    def load_assets(self):
        # Backgrounds
        for i in range(1, 6):
            self.images[f'bg_{i}'] = self.load_image(f'SPRITES/PLATAFORMA/2 Background/Layers/{i}.png')

        # Tiles
        self.images['tileset'] = self.load_image('SPRITES/PLATAFORMA/1 Tiles/Tileset.png')

        # Hero 1, 2, 3
        for lvl in range(1, 4):
            path_lvl = f'SPRITES/HEROI/PNG/Swordsman_lvl{lvl}/Without_shadow/'
            self.images[f'hero{lvl}_idle'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_Idle_without_shadow.png')
            self.images[f'hero{lvl}_run'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_Run_without_shadow.png')
            self.images[f'hero{lvl}_run_attack'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_Run_Attack_without_shadow.png')
            self.images[f'hero{lvl}_attack'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_attack_without_shadow.png')
            self.images[f'hero{lvl}_hurt'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_Hurt_without_shadow.png')
            self.images[f'hero{lvl}_death'] = self.load_image(path_lvl + f'Swordsman_lvl{lvl}_Death_without_shadow.png')

        # Orc 1, 2, 3
        for idx in range(1, 4):
            path_orc = f'SPRITES/ORC/PNG/Orc{idx}/Without_shadow/'
            self.images[f'orc{idx}_idle'] = self.load_image(path_orc + f'orc{idx}_idle_without_shadow.png')
            self.images[f'orc{idx}_run'] = self.load_image(path_orc + f'orc{idx}_run_without_shadow.png')
            self.images[f'orc{idx}_attack'] = self.load_image(path_orc + f'orc{idx}_attack_without_shadow.png')
            self.images[f'orc{idx}_hurt'] = self.load_image(path_orc + f'orc{idx}_hurt_without_shadow.png')
            self.images[f'orc{idx}_death'] = self.load_image(path_orc + f'orc{idx}_death_without_shadow.png')

        # Objects
        self.images['coin'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/Coin.png')
        self.images['chest'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/Chest.png')
        self.images['flag'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/Flag.png')
        self.images['key'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/Key.png')
        self.images['rune'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/Rune.png')
        self.images['spikes'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Hazards/spikes.png')
        self.images['saw_blade'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/saw_blade.png')
        self.images['moving_plat'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Hazards/moving_plat.png')
        self.images['cracked_wall'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Hazards/cracked_wall.png')
        self.images['checkpoint_torch'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/checkpoint_torch.png')
        self.images['potion'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/potion.png')
        self.images['gem'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/gem.png')
        self.images['slash_vfx'] = self.load_image('SPRITES/PLATAFORMA/4 Animated objects/slash_vfx.png')

        # Props
        self.images['tree_1'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Trees/1.png')
        self.images['tree_2'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Trees/2.png')
        self.images['stone_1'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Stones/1.png')
        self.images['stone_2'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Stones/2.png')
        self.images['willow_1'] = self.load_image('SPRITES/PLATAFORMA/3 Objects/Willows/1.png')

    def get(self, key):
        return self.images.get(key)

sprites = None

def init_sprites():
    global sprites
    if sprites is None:
        sprites = SpriteManager()
    return sprites
