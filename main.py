# -*- coding: utf-8 -*-
"""
Fluxo principal e loop do jogo Atari 2D.
Gerencia telas de menu, jogo ativo, game over, colisões e pontuação.
"""

import sys
import random
import pygame
from config import (
    LARGURA_TELA, ALTURA_TELA, FPS, PRETO, VERDE_RETRO, BRANCO,
    ROXO_NEON, AMARELO_NEON, VERMELHO_NEON, ASTEROIDE_INTERVALO_SPAWN,
    PONTUACAO_POR_ASTEROIDE
)
from sprites import Nave, Asteroide

# =====================================================================
# Inicialização do Pygame
# =====================================================================
pygame.init()
pygame.font.init()

# Configuração da janela do jogo
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Atari Space Defender")
relogio = pygame.time.Clock()

# =====================================================================
# Variáveis Globais de Estado do Jogo
# =====================================================================
estado_jogo = "MENU"  # Valores possíveis: "MENU", "JOGANDO", "GAME_OVER"
pontuacao = 0

# Grupos de Sprites
sprites_todas = pygame.sprite.Group()
grupo_asteroides = pygame.sprite.Group()
grupo_projeteis = pygame.sprite.Group()

# Referência da nave do jogador
nave = None

# Registro de tempo para spawn de asteroides
ultimo_spawn_asteroide = 0

# =====================================================================
# Fundo Estrelado Dinâmico (Efeito Parallax Retro)
# =====================================================================
# Lista para armazenar as estrelas do fundo: [posicao_x, posicao_y, velocidade, tamanho]
estrelas = []
for _ in range(60):
    estrelas.append([
        random.randint(0, LARGURA_TELA),
        random.randint(0, ALTURA_TELA),
        random.uniform(0.5, 2.0),
        random.randint(1, 3)
    ])


def atualizar_e_desenhar_estrelas():
    """
    Atualiza a posição vertical das estrelas para criar um efeito de movimento espacial.
    Desenha cada estrela na tela.
    """
    for estrela in estrelas:
        # Move a estrela para baixo de acordo com sua velocidade individual
        estrela[1] += estrela[2]
        
        # Se a estrela passar da parte inferior, recomeça no topo com nova posição X
        if estrela[1] > ALTURA_TELA:
            estrela[0] = random.randint(0, LARGURA_TELA)
            estrela[1] = 0
            estrela[2] = random.uniform(0.5, 2.0)
            estrela[3] = random.randint(1, 3)
            
        # Determina a intensidade da cor baseada na velocidade (estrelas mais rápidas brilham mais)
        brilho = int(100 + (estrela[2] / 2.0) * 155)
        cor_estrela = (brilho, brilho, brilho)
        
        # Desenha a estrela
        pygame.draw.circle(tela, cor_estrela, (int(estrela[0]), int(estrela[1])), estrela[3])


# =====================================================================
# Funções Auxiliares de Renderização e Controle
# =====================================================================
def desenhar_texto(texto, tamanho, cor, x, y, centralizado=True):
    """
    Auxiliar para renderizar textos na tela usando a fonte Courier New (estilo retro/monospaced).
    """
    # Usa Courier New em negrito para manter a fidelidade retro dos jogos de arcade
    fonte = pygame.font.SysFont("Courier New", tamanho, bold=True)
    superficie_texto = fonte.render(texto, True, cor)
    retangulo_texto = superficie_texto.get_rect()
    
    if centralizado:
        retangulo_texto.center = (x, y)
    else:
        retangulo_texto.topleft = (x, y)
        
    tela.blit(superficie_texto, retangulo_texto)


def reiniciar_jogo():
    """
    Reseta o estado do jogo para iniciar uma nova partida.
    Cria uma nova nave e limpa todos os asteroides e projéteis da rodada anterior.
    """
    global nave, pontuacao, sprites_todas, grupo_asteroides, grupo_projeteis, ultimo_spawn_asteroide
    
    pontuacao = 0
    ultimo_spawn_asteroide = pygame.time.get_ticks()
    
    # Esvazia os grupos de sprites antigos
    sprites_todas.empty()
    grupo_asteroides.empty()
    grupo_projeteis.empty()
    
    # Instancia a nave e adiciona ao grupo de renderização
    nave = Nave()
    sprites_todas.add(nave)


def gerenciar_eventos():
    """
    Captura e processa as entradas do teclado e eventos do sistema.
    """
    global estado_jogo
    
    for evento in pygame.event.get():
        # Fechamento da janela
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        # Teclas pressionadas
        elif evento.type == pygame.KEYDOWN:
            # Sair do jogo pressionando ESC
            if evento.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
                
            # Controle de fluxo por estados
            if estado_jogo == "MENU":
                if evento.key == pygame.K_SPACE:
                    reiniciar_jogo()
                    estado_jogo = "JOGANDO"
                    
            elif estado_jogo == "JOGANDO":
                if evento.key == pygame.K_SPACE:
                    # Tenta atirar fornecendo o tempo atual para controle do cooldown
                    projetil = nave.atirar(pygame.time.get_ticks())
                    if projetil:
                        sprites_todas.add(projetil)
                        grupo_projeteis.add(projetil)
                    
            elif estado_jogo == "GAME_OVER":
                if evento.key == pygame.K_r:
                    reiniciar_jogo()
                    estado_jogo = "JOGANDO"


# =====================================================================
# Loop Principal do Jogo
# =====================================================================
def main():
    global estado_jogo, pontuacao, ultimo_spawn_asteroide
    
    while True:
        # Captura entradas do usuário
        gerenciar_eventos()
        
        # Limpa a tela com o tom espacial escuro
        tela.fill(PRETO)
        
        # Desenha o fundo estrelado (ativo em todas as telas)
        atualizar_e_desenhar_estrelas()
        
        tempo_atual = pygame.time.get_ticks()
        
        # Executa a lógica com base no estado do jogo
        if estado_jogo == "MENU":
            # Título principal do jogo
            desenhar_texto("ATARI SPACE DEFENDER", 40, VERDE_RETRO, LARGURA_TELA // 2, ALTURA_TELA // 3)
            
            # Instruções para começar
            desenhar_texto("PRESSIONE ESPACO PARA INICIAR", 22, BRANCO, LARGURA_TELA // 2, ALTURA_TELA // 2)
            
            # Controles
            desenhar_texto("SETAS / A-D : MOVER NAVE", 16, ROXO_NEON, LARGURA_TELA // 2, ALTURA_TELA // 2 + 80)
            desenhar_texto("BARRA ESPACO : ATIRAR", 16, ROXO_NEON, LARGURA_TELA // 2, ALTURA_TELA // 2 + 110)
            
        elif estado_jogo == "JOGANDO":
            # 1. Gerenciamento de Spawn e Velocidade Dinâmica dos Asteroides (Dificuldade Progressiva)
            # Reduz o intervalo de spawn e aumenta o multiplicador de velocidade conforme o score cresce
            intervalo_spawn_atual = max(450, ASTEROIDE_INTERVALO_SPAWN - int(pontuacao * 2.5))
            multiplicador_velocidade = min(2.5, 1.0 + (pontuacao / 200.0))
            
            if tempo_atual - ultimo_spawn_asteroide > intervalo_spawn_atual:
                novo_asteroide = Asteroide(multiplicador_velocidade)
                sprites_todas.add(novo_asteroide)
                grupo_asteroides.add(novo_asteroide)
                ultimo_spawn_asteroide = tempo_atual
                
            # 2. Atualização dos Sprites (posições, lógicas internas)
            sprites_todas.update()
            
            # 3. Verificação de Colisões (Projetil x Asteroide)
            # O projétil é destruído (True), mas o asteroide não é destruído imediatamente (False)
            colisoes = pygame.sprite.groupcollide(grupo_projeteis, grupo_asteroides, True, False)
            for projetil, asteroides_atingidos in colisoes.items():
                for asteroide in asteroides_atingidos:
                    destruido = asteroide.receber_dano()
                    if destruido:
                        # Se o asteroide foi destruído, soma a pontuação correspondente
                        # Asteroides grandes (raio >= 26) dão o dobro de pontos
                        if asteroide.raio >= 26:
                            pontuacao += PONTUACAO_POR_ASTEROIDE * 2
                        else:
                            pontuacao += PONTUACAO_POR_ASTEROIDE
                        asteroide.kill()
            
            # 4. Verificação de Colisão (Nave x Asteroide) -> Fim de Jogo
            colisoes_nave = pygame.sprite.spritecollide(nave, grupo_asteroides, False)
            if colisoes_nave:
                estado_jogo = "GAME_OVER"
                
            # 5. Verificação se algum asteroide passou da parte inferior (fundo da tela) -> Fim de Jogo
            for asteroide in grupo_asteroides:
                if asteroide.rect.bottom >= ALTURA_TELA:
                    estado_jogo = "GAME_OVER"
                    break
            
            # 6. Renderização dos Sprites ativos
            sprites_todas.draw(tela)
            
            # 7. Exibição da pontuação atual (canto superior esquerdo)
            desenhar_texto(f"SCORE: {pontuacao:05d}", 22, BRANCO, 20, 20, centralizado=False)
            
        elif estado_jogo == "GAME_OVER":
            # Título de Fim de Jogo em Vermelho Neon
            desenhar_texto("GAME OVER", 48, VERMELHO_NEON, LARGURA_TELA // 2, ALTURA_TELA // 3)
            
            # Pontuação final conquistada
            desenhar_texto(f"PONTUACAO FINAL: {pontuacao:05d}", 24, BRANCO, LARGURA_TELA // 2, ALTURA_TELA // 2 - 20)
            
            # Pergunta se quer reiniciar
            desenhar_texto("DESEJA JOGAR NOVAMENTE?", 20, ROXO_NEON, LARGURA_TELA // 2, ALTURA_TELA // 2 + 30)
            
            # Instrução de reinício
            desenhar_texto("PRESSIONE 'R' PARA REINICIAR OU 'ESC' PARA SAIR", 16, VERDE_RETRO, LARGURA_TELA // 2, ALTURA_TELA // 2 + 90)
            
        # Atualiza a tela
        pygame.display.flip()
        
        # Garante a taxa de quadros (FPS) constante
        relogio.tick(FPS)


if __name__ == "__main__":
    main()
