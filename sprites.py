# -*- coding: utf-8 -*-
"""
Sprites do jogo Atari 2D.
Define as classes Nave (jogador), Projetil (tiros) e Asteroide com visual retrô.
"""

import pygame
import random
import math
from config import (
    LARGURA_TELA, ALTURA_TELA, PRETO, VERDE_RETRO, ROXO_NEON, 
    AMARELO_NEON, VERMELHO_NEON, VELOCIDADE_JOGADOR, VELOCIDADE_PROJETIL,
    ASTEROIDE_MIN_VEL, ASTEROIDE_MAX_VEL, COOLDOWN_TIRO
)

class Nave(pygame.sprite.Sprite):
    """
    Representa a nave controlada pelo jogador.
    Pode se mover para a esquerda e direita e disparar projéteis com tempo de recarga.
    """
    def __init__(self):
        super().__init__()
        # Registro do tempo do último disparo para controle de cooldown
        self.ultimo_tiro = 0
        # Define o tamanho da nave
        self.largura = 46
        self.altura = 38
        
        # Cria a superfície transparente para a nave
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # Desenha a nave no estilo vetor clássico do Atari (linhas verdes brilhantes)
        # Pontos relativos à superfície da nave (formato de triângulo/nave clássica)
        pontos = [
            (self.largura // 2, 2),                   # Bico da nave
            (self.largura - 2, self.altura - 2),      # Asa direita externa
            (self.largura - 12, self.altura - 10),    # Asa direita interna
            (self.largura // 2, self.altura - 4),     # Centro traseiro
            (12, self.altura - 10),                   # Asa esquerda interna
            (2, self.altura - 2)                      # Asa esquerda externa
        ]
        
        # Desenha o contorno da nave
        pygame.draw.polygon(self.image, VERDE_RETRO, pontos, 2)
        
        # Desenha detalhes extras no centro (como uma cabine retro)
        pygame.draw.circle(self.image, VERDE_RETRO, (self.largura // 2, self.altura // 2 + 2), 4, 1)
        
        # Define a posição inicial no centro inferior da tela
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 20
        
    def update(self):
        """
        Atualiza a posição da nave baseado nas teclas de direção pressionadas.
        Garante que a nave permaneça dentro dos limites horizontais da tela.
        """
        teclas = pygame.key.get_pressed()
        
        # Movimentação para a esquerda (Setas ou tecla A)
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= VELOCIDADE_JOGADOR
            
        # Movimentação para a direita (Setas ou tecla D)
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += VELOCIDADE_JOGADOR
            
        # Limita a nave dentro das bordas laterais da tela
        if self.rect.left < 5:
            self.rect.left = 5
        if self.rect.right > LARGURA_TELA - 5:
            self.rect.right = LARGURA_TELA - 5

    def atirar(self, tempo_atual):
        """
        Cria e retorna um novo Projétil disparado do bico da nave se o cooldown permitir.
        """
        if tempo_atual - self.ultimo_tiro >= COOLDOWN_TIRO:
            self.ultimo_tiro = tempo_atual
            # O tiro sai da ponta superior central da nave
            return Projetil(self.rect.centerx, self.rect.top)
        return None


class Projetil(pygame.sprite.Sprite):
    """
    Representa o tiro disparado pela nave do jogador.
    Se move verticalmente para cima e é destruído ao sair da tela.
    """
    def __init__(self, x, y):
        super().__init__()
        self.largura = 4
        self.altura = 16
        
        # Cria a superfície transparente para o projétil
        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # Desenha uma linha laser neon roxa
        pygame.draw.line(self.image, ROXO_NEON, (self.largura // 2, 0), (self.largura // 2, self.altura), 2)
        
        # Posiciona o tiro na coordenada de disparo
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        """
        Move o tiro para cima. Destrói o sprite se sair do topo da tela.
        """
        self.rect.y -= VELOCIDADE_PROJETIL
        
        # Destrói o projétil ao sair completamente da área visível
        if self.rect.bottom < 0:
            self.kill()


class Asteroide(pygame.sprite.Sprite):
    """
    Representa um asteroide inimigo.
    Cai em velocidade constante do topo da tela e tem formato poligonal irregular procedural.
    Asteroides maiores possuem mais vida e exigem mais tiros para quebrar.
    """
    def __init__(self, multiplicador_velocidade=1.0):
        super().__init__()
        # Define um raio aleatório maior para incluir asteroides pequenos e gigantes
        self.raio = random.randint(14, 38)
        self.tamanho = self.raio * 2 + 6
        
        # Determina a vida e espessura da linha baseada no tamanho do asteroide
        # Asteroides com raio maior ou igual a 26 necessitam de 2 tiros (vida = 2) e têm borda grossa
        if self.raio >= 26:
            self.vida = 2
            self.espessura = 3
        else:
            self.vida = 1
            self.espessura = 1
            
        # Cria a superfície transparente
        self.image = pygame.Surface((self.tamanho, self.tamanho), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        
        # Gera vértices procedurais para um visual clássico e único de asteroide vetorial
        self.pontos = []
        num_lados = random.randint(8, 12)
        centro = self.tamanho // 2
        
        # Gera pontos ao redor de uma circunferência com variações de distância (raio)
        for i in range(num_lados):
            angulo = i * (2 * math.pi / num_lados)
            # Adiciona variação aleatória no raio para deixar a forma irregular
            raio_var = self.raio * random.uniform(0.7, 1.2)
            px = centro + int(raio_var * math.cos(angulo))
            py = centro + int(raio_var * math.sin(angulo))
            self.pontos.append((px, py))
            
        # Desenha o contorno inicial do asteroide com linhas neon amarelas
        pygame.draw.polygon(self.image, AMARELO_NEON, self.pontos, self.espessura)
        
        # Define velocidade de queda (com base no multiplicador de dificuldade) e posição inicial
        self.speed_y = random.uniform(ASTEROIDE_MIN_VEL, ASTEROIDE_MAX_VEL) * multiplicador_velocidade
        
        # Spawn horizontal aleatório no topo da tela, fora da área visível inicialmente
        self.rect.centerx = random.randint(self.raio, LARGURA_TELA - self.raio)
        self.rect.bottom = 0

    def receber_dano(self):
        """
        Reduz a vida do asteroide.
        Se ainda estiver ativo, muda a sua cor para vermelho neon para dar feedback de dano.
        Retorna True se o asteroide foi destruído, False caso contrário.
        """
        self.vida -= 1
        if self.vida > 0:
            # Limpa a superfície do sprite e redesenha com contorno vermelho neon
            self.image.fill((0, 0, 0, 0))
            pygame.draw.polygon(self.image, VERMELHO_NEON, self.pontos, self.espessura)
            return False
        return True

    def update(self):
        """
        Move o asteroide verticalmente para baixo.
        O controle de colisão com o fundo da tela é feito no loop principal.
        """
        self.rect.y += self.speed_y
        
        # Destrói o asteroide se passar do limite inferior (caso não seja pego pelo game over)
        if self.rect.top > ALTURA_TELA:
            self.kill()
