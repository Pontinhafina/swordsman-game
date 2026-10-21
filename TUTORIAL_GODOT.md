# 🎮 Guia do Projeto no Godot 4 — Swordsman

O projeto completo do seu jogo de plataforma já está configurado e pronto para ser editado no **Godot Engine 4**!

---

## 🚀 Como Abrir no Godot

1. Dê um duplo clique no arquivo **[`abrir_no_godot.bat`](file:///f:/Coisas%20do%20David/UM%20JOGO%20AI/abrir_no_godot.bat)**.
2. O Godot 4 abrirá diretamente com o projeto carregado!
3. *(Caso queira abrir manualmente)*: Abra o seu Godot, clique em **Importar (Import)** e selecione a pasta `F:\Coisas do David\UM JOGO AI\project.godot`.

---

## 📂 O que já está criado e configurado:

### 🎭 Cenas Prontas (`res://scenes/`):
* **`Player.tscn`**: O herói com física, gravidade, pulo responsivo, ataque de espada, estado de dano e câmera suave.
* **`Orc.tscn`**: Inimigo configurado com IA de patrulha (não cai em buracos com `LedgeCheck`), detecção de jogador, perseguição e ataque. Também suporta virar Chefe marcando a caixa `is_boss`!
* **`Coin.tscn`**: Moeda com animação flutuante e coleta automática.
* **`Chest.tscn`**: Baú interativo com tecla `E` e animação de abertura.
* **`Flag.tscn`**: Bandeira animada de final de fase.
* **`ParallaxBackground.tscn`**: Cenário de floresta em 5 camadas de profundidade com rolagem automática.
* **`Level1.tscn`**: A fase modelo completa montada para você jogar e editar!

### 📜 Scripts em GDScript (`res://scripts/`):
* `player.gd`: Movimentação completa, animações cortadas por código da folha de sprites, colisão e vida.
* `orc.gd`: Comportamento dos orcs, dano recebido e espelhamento correto dos sprites.
* `coin.gd`, `chest.gd`, `flag.gd`: Comportamentos dos itens interativos.

---

## 🎨 Como Criar e Desenhar suas Fases no Godot:

1. No painel **Arquivos (FileSystem)** na esquerda inferior do Godot, dê dois cliques em `scenes/Level1.tscn`.
2. Você verá a fase inteira no editor 2D:
   - **Para mover plataformas:** Clique em qualquer bloco de chão e arraste ou duplique com `Ctrl + D`.
   - **Para colocar mais Inimigos:** Arraste o arquivo `Orc.tscn` da lista de arquivos e solte direto no chão da fase!
   - **Para colocar Moedas ou Baús:** Arraste `Coin.tscn` ou `Chest.tscn` e solte onde quiser.
   - **Para testar o jogo:** Pressione **`F6`** (para rodar a fase atual) ou **`F5`** (para rodar o jogo completo).
   - **Para criar uma Fase Nova:** Clique em `Cena > Nova Cena`, adicione um `Node2D`, arraste o `ParallaxBackground.tscn` e comece a desenhar seu novo mapa!

---

## 🕹️ Controles no Godot:

| Ação | Teclas |
|---|---|
| Mover | `A` / `D` ou `←` / `→` |
| Pular | `ESPAÇO`, `W` ou `↑` |
| Atacar com Espada | `Z` ou `J` |
| Abrir Baú | `E` |
| Testar Fase no Editor | `F6` ou `F5` |
