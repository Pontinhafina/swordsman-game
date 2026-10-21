// Asset Loader & Sprite Sheet Manager
class SpriteManager {
    constructor() {
        this.images = {};
        this.loadedCount = 0;
        this.totalCount = 0;
        this.isLoaded = false;
    }

    loadAll(onProgress, onComplete) {
        const manifest = {
            // Background Layers (5 layers for parallax)
            'bg_1': 'SPRITES/PLATAFORMA/2 Background/Layers/1.png',
            'bg_2': 'SPRITES/PLATAFORMA/2 Background/Layers/2.png',
            'bg_3': 'SPRITES/PLATAFORMA/2 Background/Layers/3.png',
            'bg_4': 'SPRITES/PLATAFORMA/2 Background/Layers/4.png',
            'bg_5': 'SPRITES/PLATAFORMA/2 Background/Layers/5.png',

            // Tiles
            'tileset': 'SPRITES/PLATAFORMA/1 Tiles/Tileset.png',

            // Hero Level 1
            'hero1_idle': 'SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Idle_without_shadow.png',
            'hero1_run': 'SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Run_without_shadow.png',
            'hero1_attack': 'SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_attack_without_shadow.png',
            'hero1_hurt': 'SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Hurt_without_shadow.png',
            'hero1_death': 'SPRITES/HEROI/PNG/Swordsman_lvl1/Without_shadow/Swordsman_lvl1_Death_without_shadow.png',

            // Hero Level 2 (Armor & Iron Sword)
            'hero2_idle': 'SPRITES/HEROI/PNG/Swordsman_lvl2/Without_shadow/Swordsman_lvl2_Idle_without_shadow.png',
            'hero2_run': 'SPRITES/HEROI/PNG/Swordsman_lvl2/Without_shadow/Swordsman_lvl2_Run_without_shadow.png',
            'hero2_attack': 'SPRITES/HEROI/PNG/Swordsman_lvl2/Without_shadow/Swordsman_lvl2_attack_without_shadow.png',
            'hero2_hurt': 'SPRITES/HEROI/PNG/Swordsman_lvl2/Without_shadow/Swordsman_lvl2_Hurt_without_shadow.png',
            'hero2_death': 'SPRITES/HEROI/PNG/Swordsman_lvl2/Without_shadow/Swordsman_lvl2_Death_without_shadow.png',

            // Hero Level 3 (Golden Knight)
            'hero3_idle': 'SPRITES/HEROI/PNG/Swordsman_lvl3/Without_shadow/Swordsman_lvl3_Idle_without_shadow.png',
            'hero3_run': 'SPRITES/HEROI/PNG/Swordsman_lvl3/Without_shadow/Swordsman_lvl3_Run_without_shadow.png',
            'hero3_attack': 'SPRITES/HEROI/PNG/Swordsman_lvl3/Without_shadow/Swordsman_lvl3_attack_without_shadow.png',
            'hero3_hurt': 'SPRITES/HEROI/PNG/Swordsman_lvl3/Without_shadow/Swordsman_lvl3_Hurt_without_shadow.png',
            'hero3_death': 'SPRITES/HEROI/PNG/Swordsman_lvl3/Without_shadow/Swordsman_lvl3_Death_without_shadow.png',

            // Enemy 1: Orc Scout (Green / Club)
            'orc1_idle': 'SPRITES/ORC/PNG/Orc1/Without_shadow/orc1_idle_without_shadow.png',
            'orc1_run': 'SPRITES/ORC/PNG/Orc1/Without_shadow/orc1_run_without_shadow.png',
            'orc1_attack': 'SPRITES/ORC/PNG/Orc1/Without_shadow/orc1_attack_without_shadow.png',
            'orc1_hurt': 'SPRITES/ORC/PNG/Orc1/Without_shadow/orc1_hurt_without_shadow.png',
            'orc1_death': 'SPRITES/ORC/PNG/Orc1/Without_shadow/orc1_death_without_shadow.png',

            // Enemy 2: Orc Warrior (Armored / Faster)
            'orc2_idle': 'SPRITES/ORC/PNG/Orc2/Without_shadow/orc2_idle_without_shadow.png',
            'orc2_run': 'SPRITES/ORC/PNG/Orc2/Without_shadow/orc2_run_without_shadow.png',
            'orc2_attack': 'SPRITES/ORC/PNG/Orc2/Without_shadow/orc2_attack_without_shadow.png',
            'orc2_hurt': 'SPRITES/ORC/PNG/Orc2/Without_shadow/orc2_hurt_without_shadow.png',
            'orc2_death': 'SPRITES/ORC/PNG/Orc2/Without_shadow/orc2_death_without_shadow.png',

            // Enemy 3: Orc Boss / General (Heavy Armored War Chief)
            'orc3_idle': 'SPRITES/ORC/PNG/Orc3/Without_shadow/orc3_idle_without_shadow.png',
            'orc3_run': 'SPRITES/ORC/PNG/Orc3/Without_shadow/orc3_run_without_shadow.png',
            'orc3_attack': 'SPRITES/ORC/PNG/Orc3/Without_shadow/orc3_attack_without_shadow.png',
            'orc3_hurt': 'SPRITES/ORC/PNG/Orc3/Without_shadow/orc3_hurt_without_shadow.png',
            'orc3_death': 'SPRITES/ORC/PNG/Orc3/Without_shadow/orc3_death_without_shadow.png',

            // Interactive Objects
            'coin': 'SPRITES/PLATAFORMA/4 Animated objects/Coin.png',
            'chest': 'SPRITES/PLATAFORMA/4 Animated objects/Chest.png',
            'flag': 'SPRITES/PLATAFORMA/4 Animated objects/Flag.png',
            'key': 'SPRITES/PLATAFORMA/4 Animated objects/Key.png',
            'rune': 'SPRITES/PLATAFORMA/4 Animated objects/Rune.png',

            // Props / Scenery
            'tree_1': 'SPRITES/PLATAFORMA/3 Objects/Trees/1.png',
            'tree_2': 'SPRITES/PLATAFORMA/3 Objects/Trees/2.png',
            'stone_1': 'SPRITES/PLATAFORMA/3 Objects/Stones/1.png',
            'stone_2': 'SPRITES/PLATAFORMA/3 Objects/Stones/2.png',
            'willow_1': 'SPRITES/PLATAFORMA/3 Objects/Willows/1.png'
        };

        const keys = Object.keys(manifest);
        this.totalCount = keys.length;

        keys.forEach(key => {
            const img = new Image();
            img.onload = () => {
                this.loadedCount++;
                if (onProgress) onProgress(this.loadedCount / this.totalCount);
                if (this.loadedCount === this.totalCount) {
                    this.isLoaded = true;
                    if (onComplete) onComplete();
                }
            };
            img.onerror = () => {
                console.warn(`Could not load image: ${manifest[key]}`);
                this.loadedCount++;
                if (this.loadedCount === this.totalCount) {
                    this.isLoaded = true;
                    if (onComplete) onComplete();
                }
            };
            img.src = manifest[key];
            this.images[key] = img;
        });
    }

    get(key) {
        return this.images[key];
    }
}

window.sprites = new SpriteManager();
