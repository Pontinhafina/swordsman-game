// In-Browser Visual Level Editor (Mario Maker style) for Swordsman Platformer

class LevelEditor {
    constructor(game) {
        this.game = game;
        this.canvas = game.canvas;
        this.ctx = game.ctx;

        this.active = false;
        this.camX = 0;
        this.camY = 0;

        this.tileSize = 32;
        this.widthInTiles = 110;
        this.heightInTiles = 15;

        // Level Data
        this.tiles = [];
        this.entities = {
            playerSpawn: { x: 64, y: 11 * 32 - 26 },
            orcs: [], // { x, y, type }
            coins: [], // { x, y }
            chests: [], // { x, y, grantsUpgrade }
            key: null, // { x, y }
            runeGate: null, // { x, y }
            goal: { x: 102 * 32, y: 10 * 32 - 48 },
            props: [] // { x, y, type }
        };

        // Tools
        this.currentCategory = 'tiles'; // 'tiles', 'entities', 'props'
        this.selectedTileId = 2; // Default: grass top
        this.selectedEntity = 'orc1';
        this.selectedProp = 'tree_1';
        this.isErasing = false;
        this.showGrid = true;

        // Mouse drag / pan state
        this.isMouseDown = false;
        this.mouseButton = 0;
        this.mouseX = 0;
        this.mouseY = 0;
        this.hoverTileX = 0;
        this.hoverTileY = 0;

        this.isPanning = false;
        this.panStartX = 0;
        this.panStartCamX = 0;

        this.initEmptyLevel();
        this.initDOM();
        this.initEvents();
    }

    initEmptyLevel() {
        this.tiles = [];
        for (let y = 0; y < this.heightInTiles; y++) {
            this.tiles[y] = new Array(this.widthInTiles).fill(0);
        }
        // Base ground to start with
        for (let x = 0; x < this.widthInTiles; x++) {
            this.tiles[11][x] = 2; // grass top
            for (let y = 12; y < this.heightInTiles; y++) {
                this.tiles[y][x] = 12; // dirt fill
            }
        }
        // Left wall
        for (let y = 0; y < 15; y++) {
            this.tiles[y][0] = 11;
        }

        this.entities = {
            playerSpawn: { x: 64, y: 11 * 32 - 26 },
            orcs: [
                { x: 14 * 32, y: 11 * 32 - 28, type: 'orc1' },
                { x: 26 * 32, y: 11 * 32 - 28, type: 'orc2' }
            ],
            coins: [
                { x: 8 * 32, y: 10 * 32 },
                { x: 9 * 32, y: 10 * 32 },
                { x: 10 * 32, y: 10 * 32 }
            ],
            chests: [
                { x: 20 * 32, y: 11 * 32 - 24, grantsUpgrade: true }
            ],
            key: null,
            runeGate: null,
            goal: { x: 45 * 32, y: 11 * 32 - 48 },
            props: [
                { x: 3 * 32, y: 11 * 32 - 103, type: 'tree_1' },
                { x: 18 * 32, y: 11 * 32 - 59, type: 'stone_1' }
            ]
        };
    }

    initDOM() {
        // Toolbar UI wrapper
        const panel = document.createElement('div');
        panel.id = 'editorToolbar';
        panel.className = 'editor-toolbar';
        panel.style.display = 'none';

        panel.innerHTML = `
            <div class="editor-header">
                <span class="editor-title">🛠️ CRIADOR DE FASES (EDITOR)</span>
                <div class="editor-main-btns">
                    <button id="btnPlayTest" class="btn btn-primary">▶️ Testar Fase</button>
                    <button id="btnSaveLocal" class="btn">💾 Salvar</button>
                    <button id="btnLoadLocal" class="btn">📂 Carregar</button>
                    <button id="btnExportJSON" class="btn">📋 JSON</button>
                    <button id="btnClearMap" class="btn btn-danger">🧹 Limpar</button>
                    <button id="btnCloseEditor" class="btn">✖ Sair</button>
                </div>
            </div>

            <!-- Category Switcher -->
            <div class="editor-tabs">
                <button class="tab-btn active" data-tab="tiles">🧱 Plataformas & Blocos</button>
                <button class="tab-btn" data-tab="entities">👾 Inimigos & Itens</button>
                <button class="tab-btn" data-tab="props">🌳 Árvores & Decorações</button>
                <button class="tab-btn" data-tool="eraser">❌ Borracha</button>
            </div>

            <!-- Tiles Palette -->
            <div id="paletteTiles" class="palette-group">
                <button class="item-btn active" data-tile="2" title="Chão com Grama">🟩 Grama Topo</button>
                <button class="item-btn" data-tile="1" title="Canto Esquerdo">◤ Canto Esq.</button>
                <button class="item-btn" data-tile="3" title="Canto Direito">◥ Canto Dir.</button>
                <button class="item-btn" data-tile="12" title="Terra / Centro">🟫 Terra Centro</button>
                <button class="item-btn" data-tile="11" title="Parede Esquerda">▎ Parede Esq.</button>
                <button class="item-btn" data-tile="13" title="Parede Direita">🮇 Parede Dir.</button>
                <button class="item-btn" data-tile="8" title="Plataforma Flutuante Meio">🪵 Ponte Meio</button>
                <button class="item-btn" data-tile="7" title="Plataforma Flutuante Esquerda">🪵 Ponte Esq.</button>
                <button class="item-btn" data-tile="9" title="Plataforma Flutuante Direita">🪵 Ponte Dir.</button>
                <button class="item-btn" data-tile="10" title="Água Superfície">🌊 Água Topo</button>
                <button class="item-btn" data-tile="20" title="Água Fundo">💧 Água Fundo</button>
            </div>

            <!-- Entities Palette -->
            <div id="paletteEntities" class="palette-group" style="display: none;">
                <button class="item-btn" data-entity="player" title="Local de Início do Jogador">🗡️ Herói (Início)</button>
                <button class="item-btn active" data-entity="orc1" title="Orc Batedor (Verde)">🧌 Orc 1 (Batedor)</button>
                <button class="item-btn" data-entity="orc2" title="Orc Guerreiro (Armadura)">🛡️ Orc 2 (Guerreiro)</button>
                <button class="item-btn" data-entity="orc3" title="General Chefe">👑 Chefe (General)</button>
                <button class="item-btn" data-entity="coin" title="Moeda de Ouro">💰 Moeda</button>
                <button class="item-btn" data-entity="chest" title="Baú de Tesouro">📦 Baú Bônus</button>
                <button class="item-btn" data-entity="chest_upgrade" title="Baú com Armadura">⭐ Baú Upgrade</button>
                <button class="item-btn" data-entity="key" title="Chave Dourada">🔑 Chave</button>
                <button class="item-btn" data-entity="runeGate" title="Portão que precisa de Chave">🔮 Portão Runas</button>
                <button class="item-btn" data-entity="goal" title="Bandeira de Final de Fase">🚩 Bandeira (Fim)</button>
            </div>

            <!-- Props Palette -->
            <div id="paletteProps" class="palette-group" style="display: none;">
                <button class="item-btn active" data-prop="tree_1" title="Árvore Antiga">🌳 Árvore 1</button>
                <button class="item-btn" data-prop="tree_2" title="Árvore Alta">🌲 Árvore 2</button>
                <button class="item-btn" data-prop="willow_1" title="Salgueiro Gigante">🌿 Salgueiro</button>
                <button class="item-btn" data-prop="stone_1" title="Pedra Coberta de Musgo">🪨 Pedra 1</button>
                <button class="item-btn" data-prop="stone_2" title="Rochedo">⛰️ Pedra 2</button>
            </div>

            <!-- Pan & Position bar -->
            <div class="editor-footer">
                <span id="editorCoords">Posição: X: 0, Y: 0</span>
                <div class="editor-controls-hint">
                    [Botão Esquerdo] Desenhar • [Botão Direito] Apagar • [Botão do Meio / Shift + Arrastar] Mover Câmera
                </div>
            </div>
        `;

        document.querySelector('.game-wrapper').appendChild(panel);

        // Add "🛠️ Criar Fase" button to top bar
        const topBarBtns = document.querySelector('.top-buttons');
        const btnToggleEditor = document.createElement('button');
        btnToggleEditor.id = 'btnToggleEditor';
        btnToggleEditor.className = 'btn';
        btnToggleEditor.innerHTML = '🛠️ Criar Fase';
        topBarBtns.insertBefore(btnToggleEditor, topBarBtns.firstChild);

        // Modal for JSON Import/Export
        const modal = document.createElement('div');
        modal.id = 'jsonModal';
        modal.className = 'editor-modal';
        modal.style.display = 'none';
        modal.innerHTML = `
            <div class="modal-content">
                <h3>📋 CÓDIGO DA FASE (JSON)</h3>
                <p>Copie o código para salvar/compartilhar, ou cole um código aqui e clique em Importar:</p>
                <textarea id="jsonTextArea" rows="10"></textarea>
                <div class="modal-buttons">
                    <button id="btnModalImport" class="btn btn-primary">Carregar este Código</button>
                    <button id="btnModalCopy" class="btn">Copiar Código</button>
                    <button id="btnModalClose" class="btn">Fechar</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    initEvents() {
        const btnToggleEditor = document.getElementById('btnToggleEditor');
        const toolbar = document.getElementById('editorToolbar');
        const btnPlayTest = document.getElementById('btnPlayTest');
        const btnClose = document.getElementById('btnCloseEditor');
        const btnSaveLocal = document.getElementById('btnSaveLocal');
        const btnLoadLocal = document.getElementById('btnLoadLocal');
        const btnExportJSON = document.getElementById('btnExportJSON');
        const btnClearMap = document.getElementById('btnClearMap');

        btnToggleEditor.addEventListener('click', () => {
            this.toggleEditor();
        });

        btnPlayTest.addEventListener('click', () => {
            this.startPlayTest();
        });

        btnClose.addEventListener('click', () => {
            this.toggleEditor(false);
        });

        btnSaveLocal.addEventListener('click', () => {
            this.saveToStorage();
        });

        btnLoadLocal.addEventListener('click', () => {
            this.loadFromStorage();
        });

        btnExportJSON.addEventListener('click', () => {
            this.openJSONModal();
        });

        btnClearMap.addEventListener('click', () => {
            if (confirm('Tem certeza de que deseja limpar a fase atual?')) {
                this.initEmptyLevel();
            }
        });

        // Tabs switcher
        document.querySelectorAll('.editor-tabs .tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.editor-tabs .tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');

                const tab = btn.getAttribute('data-tab');
                const tool = btn.getAttribute('data-tool');

                document.getElementById('paletteTiles').style.display = 'none';
                document.getElementById('paletteEntities').style.display = 'none';
                document.getElementById('paletteProps').style.display = 'none';

                if (tool === 'eraser') {
                    this.isErasing = true;
                    return;
                }

                this.isErasing = false;
                if (tab === 'tiles') {
                    this.currentCategory = 'tiles';
                    document.getElementById('paletteTiles').style.display = 'flex';
                } else if (tab === 'entities') {
                    this.currentCategory = 'entities';
                    document.getElementById('paletteEntities').style.display = 'flex';
                } else if (tab === 'props') {
                    this.currentCategory = 'props';
                    document.getElementById('paletteProps').style.display = 'flex';
                }
            });
        });

        // Item selection in palettes
        document.querySelectorAll('#paletteTiles .item-btn').forEach(b => {
            b.addEventListener('click', () => {
                document.querySelectorAll('#paletteTiles .item-btn').forEach(x => x.classList.remove('active'));
                b.classList.add('active');
                this.selectedTileId = parseInt(b.getAttribute('data-tile'));
                this.isErasing = false;
            });
        });

        document.querySelectorAll('#paletteEntities .item-btn').forEach(b => {
            b.addEventListener('click', () => {
                document.querySelectorAll('#paletteEntities .item-btn').forEach(x => x.classList.remove('active'));
                b.classList.add('active');
                this.selectedEntity = b.getAttribute('data-entity');
                this.isErasing = false;
            });
        });

        document.querySelectorAll('#paletteProps .item-btn').forEach(b => {
            b.addEventListener('click', () => {
                document.querySelectorAll('#paletteProps .item-btn').forEach(x => x.classList.remove('active'));
                b.classList.add('active');
                this.selectedProp = b.getAttribute('data-prop');
                this.isErasing = false;
            });
        });

        // Canvas Mouse Events
        this.canvas.addEventListener('contextmenu', (e) => e.preventDefault());

        this.canvas.addEventListener('mousedown', (e) => {
            if (!this.active) return;
            const rect = this.canvas.getBoundingClientRect();
            const scaleX = this.canvas.width / rect.width;
            const scaleY = this.canvas.height / rect.height;

            this.mouseX = (e.clientX - rect.left) * scaleX;
            this.mouseY = (e.clientY - rect.top) * scaleY;
            this.mouseButton = e.button;
            this.isMouseDown = true;

            // Middle button or Shift + Left button pans the camera
            if (e.button === 1 || (e.button === 0 && e.shiftKey)) {
                this.isPanning = true;
                this.panStartX = e.clientX;
                this.panStartCamX = this.camX;
                return;
            }

            if (e.button === 0) {
                this.applyTool();
            } else if (e.button === 2) {
                this.eraseAtCursor();
            }
        });

        window.addEventListener('mousemove', (e) => {
            if (!this.active) return;
            if (this.isPanning) {
                const dx = e.clientX - this.panStartX;
                this.camX = Math.max(0, Math.min((this.widthInTiles * this.tileSize) - 480, this.panStartCamX - dx));
                return;
            }

            const rect = this.canvas.getBoundingClientRect();
            const scaleX = this.canvas.width / rect.width;
            const scaleY = this.canvas.height / rect.height;

            this.mouseX = (e.clientX - rect.left) * scaleX;
            this.mouseY = (e.clientY - rect.top) * scaleY;

            const worldX = this.mouseX + this.camX;
            const worldY = this.mouseY + this.camY;
            this.hoverTileX = Math.floor(worldX / this.tileSize);
            this.hoverTileY = Math.floor(worldY / this.tileSize);

            const coordsEl = document.getElementById('editorCoords');
            if (coordsEl) {
                coordsEl.textContent = `Posição: Bloco [X: ${this.hoverTileX}, Y: ${this.hoverTileY}]  •  Pixel X: ${Math.round(worldX)}`;
            }

            if (this.isMouseDown) {
                if (this.mouseButton === 0 && !e.shiftKey) {
                    this.applyTool();
                } else if (this.mouseButton === 2) {
                    this.eraseAtCursor();
                }
            }
        });

        window.addEventListener('mouseup', () => {
            this.isMouseDown = false;
            this.isPanning = false;
        });

        // Wheel to pan horizontally
        this.canvas.addEventListener('wheel', (e) => {
            if (!this.active) return;
            e.preventDefault();
            this.camX = Math.max(0, Math.min((this.widthInTiles * this.tileSize) - 480, this.camX + e.deltaY * 0.8));
        });

        // Modal buttons
        const modal = document.getElementById('jsonModal');
        document.getElementById('btnModalClose').addEventListener('click', () => {
            modal.style.display = 'none';
        });
        document.getElementById('btnModalCopy').addEventListener('click', () => {
            const ta = document.getElementById('jsonTextArea');
            ta.select();
            navigator.clipboard.writeText(ta.value);
            alert('Código copiado com sucesso!');
        });
        document.getElementById('btnModalImport').addEventListener('click', () => {
            const ta = document.getElementById('jsonTextArea');
            try {
                const data = JSON.parse(ta.value);
                this.loadFromData(data);
                modal.style.display = 'none';
                alert('Fase carregada com sucesso!');
            } catch (err) {
                alert('Erro ao interpretar o código JSON: ' + err.message);
            }
        });
    }

    toggleEditor(forceState = null) {
        this.active = (forceState !== null) ? forceState : !this.active;
        const toolbar = document.getElementById('editorToolbar');
        const btnToggle = document.getElementById('btnToggleEditor');

        if (this.active) {
            toolbar.style.display = 'flex';
            btnToggle.textContent = '🎮 Modo Jogo';
            btnToggle.classList.add('btn-primary');
            this.game.state = 'editing';
        } else {
            toolbar.style.display = 'none';
            btnToggle.textContent = '🛠️ Criar Fase';
            btnToggle.classList.remove('btn-primary');
            this.game.state = 'playing';
        }
    }

    applyTool() {
        if (this.hoverTileX < 0 || this.hoverTileX >= this.widthInTiles ||
            this.hoverTileY < 0 || this.hoverTileY >= this.heightInTiles) {
            return;
        }

        if (this.isErasing) {
            this.eraseAtCursor();
            return;
        }

        const worldPixelX = this.hoverTileX * this.tileSize;
        const worldPixelY = this.hoverTileY * this.tileSize;

        if (this.currentCategory === 'tiles') {
            this.tiles[this.hoverTileY][this.hoverTileX] = this.selectedTileId;
        } else if (this.currentCategory === 'entities') {
            this.placeEntity(worldPixelX, worldPixelY);
        } else if (this.currentCategory === 'props') {
            this.placeProp(worldPixelX, worldPixelY);
        }
    }

    placeEntity(px, py) {
        // Remove entity if clicking near same position
        this.entities.orcs = this.entities.orcs.filter(o => Math.abs(o.x - px) > 20 || Math.abs(o.y - py) > 20);
        this.entities.coins = this.entities.coins.filter(c => Math.abs(c.x - px) > 16 || Math.abs(c.y - py) > 16);
        this.entities.chests = this.entities.chests.filter(ch => Math.abs(ch.x - px) > 24 || Math.abs(ch.y - py) > 24);

        if (this.selectedEntity === 'player') {
            this.entities.playerSpawn = { x: px, y: py };
        } else if (this.selectedEntity === 'orc1' || this.selectedEntity === 'orc2' || this.selectedEntity === 'orc3') {
            this.entities.orcs.push({ x: px, y: py, type: this.selectedEntity });
        } else if (this.selectedEntity === 'coin') {
            this.entities.coins.push({ x: px + 10, y: py + 10 });
        } else if (this.selectedEntity === 'chest') {
            this.entities.chests.push({ x: px, y: py, grantsUpgrade: false });
        } else if (this.selectedEntity === 'chest_upgrade') {
            this.entities.chests.push({ x: px, y: py, grantsUpgrade: true });
        } else if (this.selectedEntity === 'key') {
            this.entities.key = { x: px + 8, y: py + 8 };
        } else if (this.selectedEntity === 'runeGate') {
            this.entities.runeGate = { x: px + 4, y: py };
        } else if (this.selectedEntity === 'goal') {
            this.entities.goal = { x: px, y: py };
        }
    }

    placeProp(px, py) {
        this.entities.props = this.entities.props.filter(p => Math.abs(p.x - px) > 24);
        this.entities.props.push({ x: px, y: py, type: this.selectedProp });
    }

    eraseAtCursor() {
        if (this.hoverTileX < 0 || this.hoverTileX >= this.widthInTiles ||
            this.hoverTileY < 0 || this.hoverTileY >= this.heightInTiles) {
            return;
        }

        // Erase tile
        this.tiles[this.hoverTileY][this.hoverTileX] = 0;

        const px = this.hoverTileX * this.tileSize;
        const py = this.hoverTileY * this.tileSize;

        // Erase entities near cursor
        this.entities.orcs = this.entities.orcs.filter(o => Math.abs(o.x - px) > 24 || Math.abs(o.y - py) > 24);
        this.entities.coins = this.entities.coins.filter(c => Math.abs(c.x - px) > 20 || Math.abs(c.y - py) > 20);
        this.entities.chests = this.entities.chests.filter(ch => Math.abs(ch.x - px) > 28 || Math.abs(ch.y - py) > 28);
        this.entities.props = this.entities.props.filter(pr => Math.abs(pr.x - px) > 32);

        if (this.entities.key && Math.abs(this.entities.key.x - px) < 24 && Math.abs(this.entities.key.y - py) < 24) {
            this.entities.key = null;
        }
        if (this.entities.runeGate && Math.abs(this.entities.runeGate.x - px) < 28 && Math.abs(this.entities.runeGate.y - py) < 28) {
            this.entities.runeGate = null;
        }
    }

    startPlayTest() {
        this.toggleEditor(false);
        this.game.loadCustomCreatedStage(this.exportToData());
    }

    exportToData() {
        return {
            tiles: JSON.parse(JSON.stringify(this.tiles)),
            entities: JSON.parse(JSON.stringify(this.entities))
        };
    }

    loadFromData(data) {
        if (data && data.tiles && data.entities) {
            this.tiles = data.tiles;
            this.entities = data.entities;
        }
    }

    saveToStorage() {
        const data = this.exportToData();
        localStorage.setItem('swordsman_my_custom_stage', JSON.stringify(data));
        alert('Fase salva no seu navegador com sucesso!');
    }

    loadFromStorage() {
        const str = localStorage.getItem('swordsman_my_custom_stage');
        if (str) {
            try {
                const data = JSON.parse(str);
                this.loadFromData(data);
                alert('Fase carregada do navegador com sucesso!');
            } catch (e) {
                alert('Erro ao carregar fase salva.');
            }
        } else {
            alert('Nenhuma fase salva encontrada no navegador.');
        }
    }

    openJSONModal() {
        const modal = document.getElementById('jsonModal');
        const ta = document.getElementById('jsonTextArea');
        ta.value = JSON.stringify(this.exportToData(), null, 2);
        modal.style.display = 'flex';
    }

    draw() {
        if (!this.active) return;

        // 1. Draw Parallax Background
        this.game.level.drawParallax(this.ctx, this.camX, this.camY, 480, 270);

        this.ctx.save();
        this.ctx.translate(-Math.round(this.camX), -Math.round(this.camY));

        // 2. Draw Props
        this.entities.props.forEach(prop => {
            const img = window.sprites.get(prop.type);
            if (img) this.ctx.drawImage(img, Math.round(prop.x), Math.round(prop.y));
        });

        // 3. Draw Tiles
        const tilesetImg = window.sprites.get('tileset');
        if (tilesetImg) {
            for (let ty = 0; ty < this.heightInTiles; ty++) {
                for (let tx = 0; tx < this.widthInTiles; tx++) {
                    const tileId = this.tiles[ty][tx];
                    if (tileId <= 0) continue;
                    const tileIndex = tileId - 1;
                    const sx = (tileIndex % 10) * 32;
                    const sy = Math.floor(tileIndex / 10) * 32;
                    this.ctx.drawImage(tilesetImg, sx, sy, 32, 32, tx * 32, ty * 32, 32, 32);
                }
            }
        }

        // 4. Draw Entities in Editor
        // Player spawn
        const pImg = window.sprites.get('hero1_idle');
        if (pImg) {
            this.ctx.drawImage(pImg, 0, 128, 64, 64, this.entities.playerSpawn.x - 24, this.entities.playerSpawn.y - 18, 64, 64);
            this.ctx.strokeStyle = '#4ecca3';
            this.ctx.strokeRect(this.entities.playerSpawn.x, this.entities.playerSpawn.y, 16, 26);
        }

        // Orcs
        this.entities.orcs.forEach(o => {
            const orcImg = window.sprites.get(o.type + '_idle');
            if (orcImg) {
                this.ctx.save();
                this.ctx.translate(o.x + 10, o.y + 28);
                this.ctx.scale(1, 1);
                this.ctx.drawImage(orcImg, 0, 128, 64, 64, -30, -42, 64, 64);
                this.ctx.restore();
            }
        });

        // Coins
        const coinImg = window.sprites.get('coin');
        if (coinImg) {
            this.entities.coins.forEach(c => {
                this.ctx.drawImage(coinImg, 0, 0, 10, 10, c.x, c.y, 12, 12);
            });
        }

        // Chests
        const chestImg = window.sprites.get('chest');
        if (chestImg) {
            this.entities.chests.forEach(ch => {
                this.ctx.drawImage(chestImg, 0, 0, 32, 32, ch.x, ch.y - 8, 32, 32);
                if (ch.grantsUpgrade) {
                    this.ctx.fillStyle = '#ffd700';
                    this.ctx.font = 'bold 9px monospace';
                    this.ctx.fillText('UPGRADE', ch.x, ch.y - 12);
                }
            });
        }

        // Key
        const keyImg = window.sprites.get('key');
        if (keyImg && this.entities.key) {
            this.ctx.drawImage(keyImg, 0, 0, 8, 8, this.entities.key.x, this.entities.key.y, 16, 16);
        }

        // Rune Gate
        const runeImg = window.sprites.get('rune');
        if (runeImg && this.entities.runeGate) {
            this.ctx.drawImage(runeImg, 0, 0, 16, 16, this.entities.runeGate.x, this.entities.runeGate.y, 24, 24);
        }

        // Goal Flag
        const flagImg = window.sprites.get('flag');
        if (flagImg && this.entities.goal) {
            this.ctx.drawImage(flagImg, 0, 0, 48, 48, this.entities.goal.x, this.entities.goal.y, 48, 48);
        }

        // 5. Grid Overlay
        if (this.showGrid) {
            this.ctx.strokeStyle = 'rgba(255, 255, 255, 0.12)';
            this.ctx.lineWidth = 1;
            for (let x = 0; x <= this.widthInTiles; x++) {
                this.ctx.beginPath();
                this.ctx.moveTo(x * 32, 0);
                this.ctx.lineTo(x * 32, this.heightInTiles * 32);
                this.ctx.stroke();
            }
            for (let y = 0; y <= this.heightInTiles; y++) {
                this.ctx.beginPath();
                this.ctx.moveTo(0, y * 32);
                this.ctx.lineTo(this.widthInTiles * 32, y * 32);
                this.ctx.stroke();
            }
        }

        // 6. Hover Highlight Box
        if (this.hoverTileX >= 0 && this.hoverTileX < this.widthInTiles &&
            this.hoverTileY >= 0 && this.hoverTileY < this.heightInTiles) {
            this.ctx.strokeStyle = this.isErasing ? '#ff4d4d' : '#4ecca3';
            this.ctx.lineWidth = 2;
            this.ctx.strokeRect(this.hoverTileX * 32, this.hoverTileY * 32, 32, 32);
        }

        this.ctx.restore();

        // 7. On-screen Mini-HUD
        this.ctx.fillStyle = 'rgba(0,0,0,0.6)';
        this.ctx.fillRect(8, 8, 220, 24);
        this.ctx.fillStyle = '#4ecca3';
        this.ctx.font = 'bold 11px monospace';
        this.ctx.fillText('🛠️ MODO EDITOR ATIVO', 14, 24);
    }
}
