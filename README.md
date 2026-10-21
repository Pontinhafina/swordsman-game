# ⚔️ Swordsman: A Saga das 5 Fases (Python Native Edition)

Um jogo de plataforma e ação 2D de ritmo acelerado desenvolvido em **Python 3** com **Pygame-CE**, inspirado diretamente nas obras-primas do gênero de plataforma:
* **Hollow Knight & Shovel Knight:** Mecânica de *Pogo Jump* (quicar na cabeça de inimigos, espinhos e lâminas de serra), *Hitstop / Micro-Freeze* de 0.06s para impacto cortante, e *Screen Shake*.
* **Dead Cells:** Movimentação ágil com *Dash* horizontal com invencibilidade momentânea, fantasmas de rastro de movimento e corte correndo (*Run Attack*).
* **Castlevania & Metroidvania:** Paredes secretas rachadas quebráveis com espada (*Cracked Walls*), bifurcações de rotas (alta/baixa), tochas de *Checkpoint* que curam e salvam o renascimento, e baús com upgrades de armadura (**NV.1 Padrão → NV.2 Ferro → NV.3 Ouro**).
* **Wonder Boy & Celeste:** Salto na parede (*Wall Slide* e *Wall Jump*), plataformas móveis verticais e horizontais (*Moving Platforms*), e controle micro-ajustável de salto variável com flutuação de ápice.

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
| **Pular (Segure para alto, solte para curto)** | `Espaço`, `W` ou `↑` | Botão Sul (`A` no Xbox, `X` no PS) |
| **Dash (Arrancada Rápida com Invulnerabilidade)** | `Shift Esquerdo`, `K` ou `C` | Botão Leste (`B` no Xbox) ou Gatilho `RB` |
| **Atacar com Espada (Corta Correndo!)** | `J` ou `Z` | Botão Oeste (`X` no Xbox, `Quadrado` no PS) |
| **Pogo Attack (Golpe para Baixo no Ar)** | `S` ou `↓` no ar + Ataque | Analógico/D-Pad para baixo no ar + Ataque |
| **Wall Slide & Wall Jump** | Pressione na parede no ar + Pulo | Analógico na parede + Botão de Pulo |
| **Interagir / Abrir Baú** | `E` | Botão Norte (`Y` no Xbox, `Triângulo` no PS) |
| **Alternar Tela Cheia (Fullscreen)** | `F` | - |
| **Pausar / Despausar** | `ESC` ou `P` | Botão Start |
| **Reiniciar Fase Atual** | `R` | - |

---

## 🎨 Novos Sprites Criados (Pixel Art Original)

Foram gerados novos spritesheets respeitando a paleta e a resolução de 32x32 do tileset:
1. **Espinhos de Aço (`spikes.png`):** Dano ao encostar, mas podem ser usados para saltar com o golpe de Pogo!
2. **Lâminas de Serra Giratórias (`saw_blade.png`):** Armadilhas rotativas animadas que patrulham pontes e desfiladeiros.
3. **Plataformas Móveis Flutuantes (`moving_plat.png`):** Pranchas de madeira reforçadas com ferro que se movem em eixos X e Y transportando o jogador.
4. **Paredes Secretas Rachadas (`cracked_wall.png`):** Blocos de pedra com fissuras que quebram com golpes de espada, revelando câmaras secretas.
5. **Tochas de Checkpoint (`checkpoint_torch.png`):** Totens com chamas animadas que curam o herói ao passar e salvam o ponto de renascimento.
6. **Frascos de Poção de Vida (`potion.png`):** Elixir vermelho brilhante que recupera corações de vida.
7. **Gemas de Relíquia (`gem.png`):** Esmeraldas e rubis lapidados com brilho animado que concedem pontuações bônus.
8. **Efeitos Visuais de Corte (`slash_vfx.png`):** Arcos de energia em meia-lua cortante com brilho ciano.
9. **Animação de Corte Correndo (`Swordsman_lvlX_Run_Attack`):** Agora o personagem ataca sem travar os pés no chão!

---

## 🗺️ As 5 Fases Recriadas

1. **Fase 1: As Fronteiras da Floresta & Torre de Vigia**
   - Poço de espinhos inicial, câmara secreta com parede rachada contendo Poção de Vida e Gema, escalada vertical na torre de vigia com wall jump para o baú da **Armadura Nível 2 de Ferro**, e plataforma móvel sobre o desfiladeiro.
2. **Fase 2: As Ruínas do Entardecer & Lâminas de Serra**
   - Rota alta (plataformas sobre espinhos) vs rota baixa (combate direto), armadilha de serra giratória em patrulha, chave dourada no topo da torre, Tocha de Checkpoint e o Portão Rúnico ancestral.
3. **Fase 3: O Desfiladeiro dos Salgueiros & Escalada Vertical**
   - Elevador móvel vertical no abismo, fenda estreita com serra vertical exigindo wall slide alternado, plataformas móveis sincronizadas e câmara secreta na copa das árvores.
4. **Fase 4: O Pântano da Lua de Sangue & Castelo Interior**
   - Corredores do castelo com serras móveis, armaria secreta atrás de parede quebrável guardando a **Armadura Nível 3 do Cavaleiro Dourado**, travessia de plataformas sobre o lago de espinhos, chave secreta e grande portão rúnico.
5. **Fase 5: A Fortaleza do General Orc (Clímax / Arena)**
   - Ponte fortificada com serras, santuário pré-batalha com Tocha de Checkpoint e Poções, e a **Arena do Trono** em múltiplos andares onde o jogador pode pular nos patamares elevados para desviar dos tremores de terra e golpear o General Orc em suas duas fases furiosas!

---

## 🌐 Salvar no GitHub

Configuração do usuário do Git:
* Email: `davidbrunopatriota205@gmail.com`

Para subir o código para o seu repositório remoto no GitHub:
```powershell
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```
