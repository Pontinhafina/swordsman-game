# ⚔️ Swordsman: Guerra Orc (Native Python Platformer)

Um jogo de plataforma e ação 2D desenvolvido em **Python 3** com a biblioteca **Pygame-CE**, utilizando os sprites originais de alta fidelidade da pasta `SPRITES/`.

O jogo incorpora conceitos modernos de game design pesquisados em títulos renomados como *Hollow Knight*, *Shovel Knight* e a filosofia japonesa de progressão de fases *Kishōtenketsu*.

---

## 🎮 Como Jogar (1 Clique no Windows)

Basta dar um duplo-clique no arquivo:
👉 **[`jogar_python.bat`](file:///f:/Coisas%20do%20David/UM%20JOGO%20AI/jogar_python.bat)**

Ou, se preferir executar pelo terminal / prompt de comando:
```bash
python main.py
```

---

## 🕹️ Controles

| Ação | Teclado | Controle (Xbox / PlayStation / USB) |
|---|---|---|
| **Mover Esquerda / Direita** | `A` / `D` ou `←` / `→` | Analógico Esquerdo / D-Pad |
| **Pular** | `W`, `Espaço` ou `C` | Botão Sul (`A` no Xbox, `X` no PS) |
| **Pogo Attack (Ataque para Baixo)** | Segurar `S` ou `↓` no ar | Analógico / D-Pad para Baixo no ar |
| **Atacar com Espada** | `J` ou `X` | Botão Oeste (`X` no Xbox, `Quadrado` no PS) |
| **Interagir / Abrir Baú** | `E` | Botão Leste (`B` no Xbox, `Círculo` no PS) |
| **Tela Cheia (Full Screen)** | `F` | - |
| **Pausar / Despausar** | `ESC` ou `P` | Botão Start |
| **Reiniciar Fase** | `R` | - |

---

## 🧠 Referências & Mecânicas de Game Design Implementadas

### 1. Sistema de Combate "Juicy" (Inspirado em *Hollow Knight* e *Shovel Knight*)
* **Downthrust Pogo Jump:** Ao atacar no ar segurando para baixo (`S` ou `↓`), o herói executa um golpe para baixo que salta sobre a cabeça dos Orcs, causando dano contínuo e ganhando impulso vertical.
* **Hitstop / Impact Freeze:** A cada golpe de espada que acerta um inimigo ou chefe, o jogo congela por ~0.05 segundos para transmitir sensação de impacto e peso cortante.
* **Screen Shake Procedural:** Tremores dinâmicos de câmera proporcionais ao poder do impacto e ao rugido do chefão.
* **Coyote Time & Jump Buffering:** Janela de tolerância de 120ms para pular mesmo milissegundos após sair da beirada de uma plataforma e buffer de input antes de tocar no chão.

### 2. Design das 5 Fases (Filosofia *Kishōtenketsu*)
As fases foram estruturadas em 4 atos fundamentais:
1. **Fase 1: As Fronteiras da Floresta (Ki - Introdução Segura)**
   - Plataformas baixas, espaçamento seguro de 1 a 2 blocos de elevação, introdução dos Orcs Batedores e primeiras moedas.
2. **Fase 2: As Ruínas do Acampamento (Shō - Desenvolvimento)**
   - Introdução de plataformas semissólidas (atravessáveis por baixo), baú com armadura Nível 2 e Orcs Guerreiros patrulhando.
3. **Fase 3: O Pântano da Névoa (Ten - O Desafio do Pogo)**
   - Ilhas isoladas e lagos tóxicos onde o jogador precisa usar a mecânica de pogo jump sobre inimigos para atravessar abismos maiores.
4. **Fase 4: A Fortaleza de Pedra (Ten - Desafio de Chaves & Runas)**
   - Exploração vertical, chave secreta e o Portão Rúnico ancestral que protege o caminho para o covil do chefe.
5. **Fase 5: O Covil do General Orc (Ketsu - Clímax / Boss Fight)**
   - Batalha contra o General Orc de 2 fases: golpes com screen shake, enrage furioso ao chegar a 50% de HP e invocação de batedores de apoio.

### 3. Motor de Áudio Procedural Sintetizado (Zero Dependências Externas)
* Todos os efeitos sonoros (espada, pulo, pogo, moedas, abertura de baú, impacto, rugido e passos) são gerados em tempo real através de síntese matemática via `numpy` e `pygame.mixer.Sound`. Não há arquivos de áudio faltando ou corrompidos.

---

## 📂 Estrutura do Código Python

```
UM JOGO AI/
├── main.py                  # Loop principal do jogo, máquina de estados, câmera e HUD
├── jogar_python.bat         # Executável em lote (1 clique)
├── game/
│   ├── settings.py          # Constantes de física, resolução interna e controles
│   ├── sprites.py           # Loader com corte automático de spritesheets e cache
│   ├── player.py            # Herói, física, pulo, pogo, armaduras Lv1/Lv2/Lv3
│   ├── enemy.py             # Inteligência Artificial dos Orcs e Chefe
│   ├── level.py             # Design das 5 fases, colisões e parallax
│   ├── objects.py           # Moedas animadas, baús de upgrade, chaves, portões
│   ├── sound.py             # Sintetizador procedural de áudio 8-bit
│   └── particles.py         # Partículas de poeira, faíscas, dano flutuante e screen shake
└── SPRITES/                 # Spritesheets originais do projeto
```

---

## 🌐 Salvar no GitHub

Para subir todas as alterações para o seu repositório remoto no GitHub:
```bash
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git branch -M main
git push -u origin main
```
