# ⚔️ Swordsman: A Saga das 8 Fases (Python Native Edition)

Um jogo de plataforma e ação 2D completo desenvolvido em **Python 3** com **Pygame-CE**, inspirado diretamente nas mecânicas consagradas de *Hollow Knight*, *Shovel Knight*, *Dead Cells*, *Castlevania* e *Celeste*.

---

## 🎮 Como Jogar (1 Clique no Windows)

Dê um duplo clique no arquivo:
👉 **[`jogar_python.bat`](file:///f:/Coisas%20do%20David/UM%20JOGO%20AI/jogar_python.bat)**

Ou execute pelo terminal:
```bash
python main.py
```

---

## 🕹️ Controles Completos

| Ação | Teclado | Controle (Xbox / PlayStation / USB) |
|---|---|---|
| **Mover Esquerda / Direita** | `A` / `D` ou `←` / `→` | Analógico Esquerdo / D-Pad |
| **Pular (Toque rápido para pulo curto)** | `Espaço`, `W` ou `↑` | Botão Sul (`A` no Xbox, `X` no PS) |
| **Dash (Arrancada Rápida com Invulnerabilidade)** | `Shift`, `K` ou `C` | Botão Leste (`B` no Xbox) ou Gatilho `RB` |
| **Atacar com Espada (Corta Correndo!)** | `J` ou `Z` | Botão Oeste (`X` no Xbox, `Quadrado` no PS) |
| **Pogo Strike (Golpe para Baixo no Ar)** | `S` ou `↓` no ar + Ataque | Analógico para baixo no ar + Ataque |
| **Wall Slide & Wall Jump** | Deslize na parede + Pulo | Analógico na parede + Botão de Pulo |
| **Interagir / Abrir Baú** | `E` | Botão Norte (`Y` no Xbox, `Triângulo` no PS) |
| **Ligar / Desligar Música Chiptune** | `M` | - |
| **Alternar Tela Cheia (Fullscreen)** | `F` | - |
| **Pausar / Despausar** | `ESC` ou `P` | Botão Start |
| **Reiniciar Fase Atual** | `R` | - |

---

## 🦉 A Coruja Sábia de Ajuda (*Owl Helper*)

Em cada uma das 8 fases, você encontrará a **Coruja Sábia** pousada em galhos e totens ancestrais:
* **Balões de Fala e Dicas Táticas:** Ao se aproximar, ela pia (`owl_hoot`), bate as asas e ensina os controles e segredos da fase atual.
* **Presente de Cura em Perigo:** Se o herói estiver com a vida baixa (2 corações ou menos), a coruja solta uma **Poção de Vida** para salvá-lo!

---

## 👑 O Chefão Inteligente: General Orc

O General Orc (Fase 8) foi reformulado com inteligência artificial avançada:
1. **Impacto de Chão e Ondas de Choque (*Ground Slam Shockwave*):**
   * O General pula alto e desce com um estrondo na arena, emitindo **ondas de choque cortantes** que viajam pelo chão para a esquerda e para a direita. O jogador deve pular ou subir nas plataformas elevadas para desviar!
2. **Carga de Escudo Furiosa (*Shield Charge*):**
   * O General sinaliza um alerta vermelho e avança em disparada pelo chão com o escudo em riste. É necessário saltar por cima ou usar o *Dash* para atravessá-lo ileso.
3. **Salto de Guerra (*Leap Cleave*):**
   * Se o jogador tentar ficar escondido nas plataformas altas, o chefe pula até a plataforma para desferir um corte pesado!
4. **Recuo Tático (*Tactical Leap Back*):**
   * Se você acertar múltiplos golpes rápidos no chefe, ele salta para trás para restabelecer distância.
5. **Fase 2 Enfurecida (Abaixo de 50% de Vida):**
   * O General solta um rugido aterrorizante, ganha um halo vermelho furioso, fica 40% mais rápido e invoca soldados orcs batedores para a batalha!

---

## 🎵 Motor de Áudio Procedural com Trilha Sonora Chiptune

O sistema de áudio foi expandido e sintetiza em tempo real:
* **Trilha Sonora Retrô de Aventura (*BGM Stage*):** Linha de baixo e arpeggios dinâmicos de 8 bits que tocam durante a exploração.
* **Trilha Sonora de Batalha de Chefe (*BGM Boss*):** Ritmo acelerado e tenso durante a batalha contra o General Orc.
* Efeitos sonoros para piado da coruja, estrondo do choque no chão, rugido do chefe, passos e estilhaçamento de rochas.
* Pressione **`M`** a qualquer momento para ligar ou desligar a música!

---

## 🗺️ A Campanha Completa das 8 Fases

1. **Fase 1: As Fronteiras da Floresta & Torre de Vigia** (Introdução, espinhos, sala secreta e armadura de ferro Nv.2)
2. **Fase 2: As Ruínas do Entardecer & Lâminas de Serra** (Armadilhas de serra, rotas alta/baixa, chave da torre e portão rúnico)
3. **Fase 3: O Desfiladeiro dos Salgueiros & Escalada** (Elevadores verticais no precipício, canyon estreito com wall-jumps)
4. **Fase 4: As Catacumbas Subterrâneas Alagadas** (Cripta de pedra com poços e passagens secretas atrás de paredes rachadas)
5. **Fase 5: O Pântano da Lua de Sangue & Castelo Interior** (Pogo jumps sobre orcs e armaria com a **Armadura Nível 3 de Ouro**)
6. **Fase 6: O Pico Congelado dos Ventos** (Montanhas nevadas com pontes suspensas e saltos longos combinados com Dash)
7. **Fase 7: A Fundição Vulcânica dos Orcs** (Lagos de lava, plataformas sincronizadas e guardas de elite com escudos)
8. **Fase 8: A Grande Fortaleza do General Orc (O Clímax Final)** (Arena do trono em 3 andares com ondas de choque e chefe de 2 fases)

---

## 🌐 Salvar no GitHub

Configuração do usuário do Git:
* Email: `davidbrunopatriota205@gmail.com`

Para sincronizar com seu repositório remoto:
```powershell
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```
