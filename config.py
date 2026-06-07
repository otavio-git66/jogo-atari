# -*- coding: utf-8 -*-
"""
Configurações globais do jogo Atari 2D.
Contém definições de tela, cores, velocidades e taxas de atualização.
"""

# =====================================================================
# Configurações da Janela e FPS
# =====================================================================
LARGURA_TELA = 800
ALTURA_TELA = 600
FPS = 60

# =====================================================================
# Definição de Cores (Estilo Retro Arcade/Neon)
# =====================================================================
PRETO = (10, 10, 15)          # Fundo quase preto (espacial profundo)
VERDE_RETRO = (57, 255, 20)    # Verde Neon Phosphor (clássico Atari)
BRANCO = (240, 240, 240)       # Branco suave para textos e detalhes
ROXO_NEON = (188, 19, 254)     # Projéteis / detalhes
AMARELO_NEON = (255, 234, 0)   # Asteroides
VERMELHO_NEON = (255, 0, 127)  # Explosões / Vida / Game Over

# =====================================================================
# Parâmetros de Balanceamento do Jogo
# =====================================================================
VELOCIDADE_JOGADOR = 6        # Velocidade de movimentação lateral da nave
VELOCIDADE_PROJETIL = 8       # Velocidade de subida do tiro
COOLDOWN_TIRO = 300           # Tempo mínimo entre tiros (em ms)
ASTEROIDE_MIN_VEL = 1.5       # Velocidade mínima inicial dos asteroides
ASTEROIDE_MAX_VEL = 3.0       # Velocidade máxima inicial dos asteroides
ASTEROIDE_INTERVALO_SPAWN = 1600  # Intervalo inicial de surgimento (em ms)
PONTUACAO_POR_ASTEROIDE = 10  # Pontos ganhos ao destruir um asteroide
