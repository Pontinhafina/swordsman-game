// Level Map Generator supporting 5 Distinct Stages with Unique Environments and Mechanics

class Level {
    constructor(stageIndex = 1) {
        this.stageIndex = stageIndex;
        this.tileSize = 32;
        this.widthInTiles = 110;
        this.heightInTiles = 15;
        this.widthInPixels = this.widthInTiles * this.tileSize;
        this.heightInPixels = this.heightInTiles * this.tileSize;

        this.tiles = [];
        this.oneWayPlatforms = [];
        this.props = [];

        this.ambientParticles = [];
        this.initAmbientParticles();

        this.initStage(stageIndex);
    }

    initAmbientParticles() {
        this.ambientParticles = [];
        // Ambient floating particles (fireflies, leaves, embers)
        const count = 25;
        for (let i = 0; i < count; i++) {
            this.ambientParticles.push({
                x: Math.random() * 480,
                y: Math.random() * 270,
                vx: (Math.random() - 0.5) * 15,
                vy: -5 - Math.random() * 15,
                size: Math.random() < 0.6 ? 1.5 : 2.5,
                alpha: 0.2 + Math.random() * 0.6,
                pulse: Math.random() * Math.PI * 2
            });
        }
    }

    initStage(stageIndex) {
        this.tiles = [];
        for (let y = 0; y < this.heightInTiles; y++) {
            this.tiles[y] = new Array(this.widthInTiles).fill(0);
        }
        this.oneWayPlatforms = [];
        this.props = [];

        const createGroundBlock = (startX, startY, width, height) => {
            for (let y = 0; y < height; y++) {
                for (let x = 0; x < width; x++) {
                    const gx = startX + x;
                    const gy = startY + y;
                    if (gx >= this.widthInTiles || gy >= this.heightInTiles) continue;

                    let tileId = 12; // default center fill

                    const isTop = (y === 0);
                    const isBot = (y === height - 1);
                    const isLeft = (x === 0);
                    const isRight = (x === width - 1);

                    if (isTop && isLeft) tileId = 1;
                    else if (isTop && isRight) tileId = 3;
                    else if (isTop) tileId = 2;
                    else if (isBot && isLeft) tileId = 21;
                    else if (isBot && isRight) tileId = 23;
                    else if (isBot) tileId = 22;
                    else if (isLeft) tileId = 11;
                    else if (isRight) tileId = 13;

                    this.tiles[gy][gx] = tileId;
                }
            }
        };

        const createFloatingPlatform = (startX, y, width) => {
            for (let x = 0; x < width; x++) {
                const gx = startX + x;
                let tileId = 8;
                if (x === 0) tileId = 7;
                if (x === width - 1) tileId = 9;
                this.tiles[y][gx] = tileId;
                this.oneWayPlatforms.push({
                    x: gx * this.tileSize,
                    y: y * this.tileSize,
                    w: this.tileSize,
                    h: 12
                });
            }
        };

        const createWater = (startX, startY, width, height) => {
            for (let y = 0; y < height; y++) {
                for (let x = 0; x < width; x++) {
                    const gx = startX + x;
                    const gy = startY + y;
                    if (gx >= this.widthInTiles || gy >= this.heightInTiles) continue;
                    this.tiles[gy][gx] = (y === 0) ? 10 : 20;
                }
            }
        };

        // Left Boundary Wall
        for (let y = 0; y < 15; y++) {
            this.tiles[y][0] = 11;
        }

        if (stageIndex === 1) {
            // ==========================================
            // FASE 1: A FLORESTA DOS ORCS (DIA)
            // ==========================================
            createGroundBlock(0, 11, 19, 4);
            createGroundBlock(17, 10, 3, 5); // Step 1
            createGroundBlock(19, 9, 13, 6);  // Terrace
            createFloatingPlatform(32, 8, 4); // Chasm step
            createGroundBlock(36, 8, 8, 7);   // Plateau
            createFloatingPlatform(42, 7, 3); // High step
            createGroundBlock(45, 6, 5, 9);   // Secret cliff (Chest 1)
            createFloatingPlatform(50, 8, 3); // Down step
            createGroundBlock(53, 10, 8, 5);  // Valley floor
            createWater(61, 13, 9, 2);        // River
            createFloatingPlatform(61, 9, 4); // River bridge 1
            createFloatingPlatform(66, 9, 4); // River bridge 2
            createGroundBlock(70, 10, 7, 5);  // Right bank
            createGroundBlock(77, 9, 3, 6);   // Stair
            createGroundBlock(80, 8, 14, 7);  // Fortress
            createFloatingPlatform(94, 9, 3); // Step down
            createGroundBlock(97, 10, 12, 5); // Sanctuary

            for (let y = 0; y < 10; y++) this.tiles[y][108] = 13;

            this.props = [
                { type: 'tree_1', x: 3 * 32, y: 11 * 32 - 103 },
                { type: 'stone_1', x: 10 * 32, y: 11 * 32 - 59 },
                { type: 'willow_1', x: 21 * 32, y: 9 * 32 - 135 },
                { type: 'stone_2', x: 29 * 32, y: 9 * 32 - 59 },
                { type: 'tree_2', x: 37 * 32, y: 8 * 32 - 132 },
                { type: 'tree_1', x: 55 * 32, y: 10 * 32 - 103 },
                { type: 'stone_1', x: 72 * 32, y: 10 * 32 - 59 },
                { type: 'tree_2', x: 82 * 32, y: 8 * 32 - 132 },
                { type: 'willow_1', x: 104 * 32, y: 10 * 32 - 135 }
            ];

        } else if (stageIndex === 2) {
            // ==========================================
            // FASE 2: AS RUÍNAS DO ENTARDECER (PÔR DO SOL)
            // ==========================================
            createGroundBlock(0, 11, 14, 4);
            createFloatingPlatform(12, 9, 4);
            createGroundBlock(15, 8, 10, 7); // First ruins column

            // Tower ascent for Key
            createFloatingPlatform(23, 7, 3);
            createGroundBlock(26, 6, 8, 9);  // Mid tower
            createFloatingPlatform(32, 5, 3);
            createGroundBlock(35, 4, 7, 11); // High Tower with Key!

            // Descending pillars
            createFloatingPlatform(42, 6, 3);
            createGroundBlock(45, 8, 8, 7);
            createFloatingPlatform(52, 9, 4);

            // Broken bridge valley with water
            createWater(55, 13, 14, 2);
            createFloatingPlatform(56, 10, 3);
            createFloatingPlatform(60, 9, 4);
            createFloatingPlatform(65, 10, 3);

            // Second Temple & Rune Gate
            createGroundBlock(69, 10, 11, 5);
            createGroundBlock(79, 9, 3, 6);
            createGroundBlock(82, 8, 14, 7); // Grand Hall (Chest 2 here)

            // Sanctuary with locked Rune Gate before flag
            createFloatingPlatform(96, 8, 3);
            createGroundBlock(99, 9, 10, 6);

            for (let y = 0; y < 9; y++) this.tiles[y][108] = 13;

            this.props = [
                { type: 'stone_2', x: 2 * 32, y: 11 * 32 - 59 },
                { type: 'tree_2', x: 17 * 32, y: 8 * 32 - 132 },
                { type: 'stone_1', x: 36 * 32, y: 4 * 32 - 59 },
                { type: 'willow_1', x: 46 * 32, y: 8 * 32 - 135 },
                { type: 'stone_1', x: 71 * 32, y: 10 * 32 - 59 },
                { type: 'tree_1', x: 84 * 32, y: 8 * 32 - 103 },
                { type: 'stone_2', x: 100 * 32, y: 9 * 32 - 59 }
            ];

        } else if (stageIndex === 3) {
            // ==========================================
            // FASE 3: O DESFILADEIRO DOS SALGUEIROS (CREPÚSCULO)
            // ==========================================
            // High cliff start
            createGroundBlock(0, 10, 15, 5);
            createFloatingPlatform(13, 8, 4);

            // Canyon suspended platforms spanning large gap
            createFloatingPlatform(18, 7, 3);
            createFloatingPlatform(22, 6, 3);
            // Secret lower cavern with chest
            createGroundBlock(26, 11, 8, 4); // Cavern floor
            createFloatingPlatform(28, 5, 4); // High path over cavern
            createFloatingPlatform(34, 6, 3);

            // Mid-canyon rocky plateau
            createGroundBlock(38, 8, 12, 7);
            createFloatingPlatform(48, 7, 3);

            // Giant Willow Grove
            createGroundBlock(52, 9, 14, 6);
            createWater(66, 13, 10, 2);
            createFloatingPlatform(66, 9, 4);
            createFloatingPlatform(71, 8, 4);

            // Highland Altar
            createGroundBlock(76, 8, 10, 7);
            createFloatingPlatform(85, 7, 3);
            createGroundBlock(88, 7, 8, 8);
            createFloatingPlatform(95, 8, 3);
            createGroundBlock(98, 9, 10, 6);

            for (let y = 0; y < 9; y++) this.tiles[y][107] = 13;

            this.props = [
                { type: 'willow_1', x: 3 * 32, y: 10 * 32 - 135 },
                { type: 'stone_1', x: 10 * 32, y: 10 * 32 - 59 },
                { type: 'stone_2', x: 27 * 32, y: 11 * 32 - 59 },
                { type: 'tree_2', x: 40 * 32, y: 8 * 32 - 132 },
                { type: 'willow_1', x: 54 * 32, y: 9 * 32 - 135 },
                { type: 'willow_1', x: 62 * 32, y: 9 * 32 - 135 },
                { type: 'stone_1', x: 78 * 32, y: 8 * 32 - 59 },
                { type: 'tree_1', x: 90 * 32, y: 7 * 32 - 103 },
                { type: 'willow_1', x: 101 * 32, y: 9 * 32 - 135 }
            ];

        } else if (stageIndex === 4) {
            // ==========================================
            // FASE 4: O PÂNTANO NOTURNO (LUAR & BRUMAS)
            // ==========================================
            // Sinking swamp islands
            createGroundBlock(0, 11, 12, 4);
            createWater(12, 13, 12, 2);
            createFloatingPlatform(13, 10, 3);
            createFloatingPlatform(17, 9, 3);
            createFloatingPlatform(21, 10, 3);

            // Sunken temple
            createGroundBlock(24, 10, 12, 5);
            // High Tower with Silver Key
            createFloatingPlatform(34, 8, 3);
            createGroundBlock(37, 7, 7, 8);
            createFloatingPlatform(42, 5, 3);
            createGroundBlock(45, 4, 6, 11); // High tower for Key!

            // Deep swamp crossing
            createWater(51, 13, 16, 2);
            createFloatingPlatform(52, 9, 3);
            createFloatingPlatform(56, 8, 4);
            createFloatingPlatform(61, 9, 3);
            createFloatingPlatform(65, 10, 3);

            // Citadel outpost guarded by Orc2 warriors
            createGroundBlock(68, 10, 14, 5);
            createFloatingPlatform(81, 8, 3);
            createGroundBlock(84, 8, 12, 7); // Shrine plateau with Rune Gate!

            // Final passage
            createFloatingPlatform(95, 8, 3);
            createGroundBlock(98, 9, 10, 6);

            for (let y = 0; y < 9; y++) this.tiles[y][107] = 13;

            this.props = [
                { type: 'willow_1', x: 2 * 32, y: 11 * 32 - 135 },
                { type: 'stone_1', x: 26 * 32, y: 10 * 32 - 59 },
                { type: 'tree_1', x: 38 * 32, y: 7 * 32 - 103 },
                { type: 'stone_2', x: 46 * 32, y: 4 * 32 - 59 },
                { type: 'willow_1', x: 70 * 32, y: 10 * 32 - 135 },
                { type: 'stone_1', x: 86 * 32, y: 8 * 32 - 59 },
                { type: 'tree_2', x: 100 * 32, y: 9 * 32 - 132 }
            ];

        } else if (stageIndex === 5) {
            // ==========================================
            // FASE 5: A FORTALEZA DO GENERAL ORC (CHEFE FINAL)
            // ==========================================
            // Entrance bridge & battlements
            createGroundBlock(0, 10, 16, 5);
            createFloatingPlatform(14, 8, 4);
            createGroundBlock(17, 7, 10, 8); // High fortress wall
            createFloatingPlatform(26, 8, 3);

            // Inner courtyard descent
            createGroundBlock(28, 9, 12, 6);
            createFloatingPlatform(39, 9, 3);
            createGroundBlock(42, 10, 14, 5);

            // Grand ascension stairs into the Throne Room
            createGroundBlock(55, 9, 4, 6);
            createGroundBlock(58, 8, 4, 7);

            // ========================================
            // THE THRONE ROOM ARENA (x: 62 to 106)
            // ========================================
            createGroundBlock(62, 8, 44, 7); // Epic battlefield!
            // Upper dodge platforms to leap over boss sweeps!
            createFloatingPlatform(72, 5, 4);
            createFloatingPlatform(86, 5, 4);
            createFloatingPlatform(98, 5, 4);

            for (let y = 0; y < 8; y++) this.tiles[y][105] = 13;

            this.props = [
                { type: 'stone_2', x: 2 * 32, y: 10 * 32 - 59 },
                { type: 'tree_2', x: 18 * 32, y: 7 * 32 - 132 },
                { type: 'stone_1', x: 30 * 32, y: 9 * 32 - 59 },
                { type: 'willow_1', x: 44 * 32, y: 10 * 32 - 135 },
                { type: 'stone_2', x: 64 * 32, y: 8 * 32 - 59 },
                { type: 'tree_1', x: 80 * 32, y: 8 * 32 - 103 },
                { type: 'stone_1', x: 102 * 32, y: 8 * 32 - 59 }
            ];
        }
    }

    loadFromCustomData(data) {
        this.tiles = JSON.parse(JSON.stringify(data.tiles));
        this.oneWayPlatforms = [];
        this.props = JSON.parse(JSON.stringify(data.entities.props || []));

        // Recompute one-way platforms (tiles 7, 8, 9)
        for (let y = 0; y < this.heightInTiles; y++) {
            for (let x = 0; x < this.widthInTiles; x++) {
                const t = this.tiles[y][x];
                if (t === 7 || t === 8 || t === 9) {
                    this.oneWayPlatforms.push({
                        x: x * this.tileSize,
                        y: y * this.tileSize,
                        w: this.tileSize,
                        h: 12
                    });
                }
            }
        }
    }

    isTileSolid(tileId) {
        const solidIds = [1, 2, 3, 11, 12, 13, 21, 22, 23];
        return solidIds.includes(tileId);
    }

    isTileSolidAtPixel(px, py) {
        const tx = Math.floor(px / this.tileSize);
        const ty = Math.floor(py / this.tileSize);
        if (tx < 0 || tx >= this.widthInTiles || ty < 0 || ty >= this.heightInTiles) {
            return false;
        }
        return this.isTileSolid(this.tiles[ty][tx]);
    }

    checkTileCollision(box) {
        const startX = Math.floor(box.x / this.tileSize);
        const endX = Math.floor((box.x + box.w) / this.tileSize);
        const startY = Math.floor(box.y / this.tileSize);
        const endY = Math.floor((box.y + box.h) / this.tileSize);

        for (let ty = startY; ty <= endY; ty++) {
            for (let tx = startX; tx <= endX; tx++) {
                if (tx < 0 || tx >= this.widthInTiles || ty < 0 || ty >= this.heightInTiles) {
                    continue;
                }
                const tileId = this.tiles[ty][tx];
                if (this.isTileSolid(tileId)) {
                    const tileBox = {
                        x: tx * this.tileSize,
                        y: ty * this.tileSize,
                        w: this.tileSize,
                        h: this.tileSize
                    };
                    if (checkAABB(box, tileBox)) {
                        return { tileX: tx, tileY: ty, tileId };
                    }
                }
            }
        }
        return null;
    }

    checkOneWayPlatform(footX, footY, footW, vyDt) {
        for (const p of this.oneWayPlatforms) {
            if (footX + footW > p.x && footX < p.x + p.w) {
                const prevY = footY - Math.max(1, vyDt);
                if (prevY <= p.y + 4 && footY >= p.y - 3) {
                    return p;
                }
            }
        }
        return null;
    }

    drawParallax(ctx, cameraX, cameraY, viewWidth, viewHeight, dt = 0.016) {
        const bgWidth = 576;
        const bgHeight = 324;

        const layers = [
            { key: 'bg_1', speed: 0.05, yOffset: 0 },
            { key: 'bg_2', speed: 0.15, yOffset: 20 },
            { key: 'bg_3', speed: 0.32, yOffset: 40 },
            { key: 'bg_4', speed: 0.55, yOffset: 60 },
            { key: 'bg_5', speed: 0.80, yOffset: 80 }
        ];

        layers.forEach(layer => {
            const img = window.sprites.get(layer.key);
            if (!img) return;

            const scrollX = -(cameraX * layer.speed) % bgWidth;
            let startDrawX = scrollX;
            if (startDrawX > 0) startDrawX -= bgWidth;

            for (let x = startDrawX; x < viewWidth + bgWidth; x += bgWidth) {
                ctx.drawImage(img, Math.round(x), Math.round(layer.yOffset - cameraY * 0.1), bgWidth, bgHeight);
            }
        });

        // Stage atmospheric lighting overlays
        if (this.stageIndex === 2) {
            // Sunset / Twilight golden glow
            ctx.fillStyle = 'rgba(237, 137, 54, 0.22)';
            ctx.fillRect(0, 0, viewWidth, viewHeight);
        } else if (this.stageIndex === 3) {
            // Crimson dusk ravine
            ctx.fillStyle = 'rgba(215, 60, 45, 0.22)';
            ctx.fillRect(0, 0, viewWidth, viewHeight);
        } else if (this.stageIndex === 4) {
            // Midnight blue moonlight & mist
            ctx.fillStyle = 'rgba(15, 23, 60, 0.38)';
            ctx.fillRect(0, 0, viewWidth, viewHeight);
        } else if (this.stageIndex === 5) {
            // Blood Moon Citadel ominous red
            ctx.fillStyle = 'rgba(80, 15, 30, 0.32)';
            ctx.fillRect(0, 0, viewWidth, viewHeight);
        }

        // Draw ambient floating particles (fireflies, glowing spores, wind embers)
        if (this.stageIndex >= 3) {
            ctx.save();
            this.ambientParticles.forEach(p => {
                p.x += p.vx * dt;
                p.y += p.vy * dt;
                p.pulse += dt * 3;
                if (p.y < -10) p.y = viewHeight + 10;
                if (p.x < -10) p.x = viewWidth + 10;
                if (p.x > viewWidth + 10) p.x = -10;

                const currentAlpha = Math.max(0.1, p.alpha + Math.sin(p.pulse) * 0.3);
                ctx.globalAlpha = currentAlpha;
                ctx.fillStyle = this.stageIndex === 4 ? '#4ecca3' : (this.stageIndex === 5 ? '#ff4d4d' : '#ffd700');
                ctx.fillRect(Math.round(p.x), Math.round(p.y), p.size, p.size);
            });
            ctx.restore();
        }
    }

    drawProps(ctx, cameraX, cameraY) {
        this.props.forEach(prop => {
            const img = window.sprites.get(prop.type);
            if (!img) return;
            if (prop.x + img.width > cameraX && prop.x < cameraX + 640) {
                ctx.drawImage(img, Math.round(prop.x), Math.round(prop.y));
            }
        });
    }

    drawTiles(ctx, cameraX, cameraY, viewWidth, viewHeight) {
        const img = window.sprites.get('tileset');
        if (!img) return;

        const startCol = Math.max(0, Math.floor(cameraX / this.tileSize));
        const endCol = Math.min(this.widthInTiles - 1, Math.ceil((cameraX + viewWidth) / this.tileSize));
        const startRow = Math.max(0, Math.floor(cameraY / this.tileSize));
        const endRow = Math.min(this.heightInTiles - 1, Math.ceil((cameraY + viewHeight) / this.tileSize));

        for (let ty = startRow; ty <= endRow; ty++) {
            for (let tx = startCol; tx <= endCol; tx++) {
                const tileId = this.tiles[ty][tx];
                if (tileId <= 0) continue;

                const tileIndex = tileId - 1;
                const sx = (tileIndex % 10) * 32;
                const sy = Math.floor(tileIndex / 10) * 32;

                ctx.drawImage(
                    img,
                    sx, sy, 32, 32,
                    Math.round(tx * this.tileSize),
                    Math.round(ty * this.tileSize),
                    32, 32
                );
            }
        }
    }
}
