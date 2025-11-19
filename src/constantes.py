import pygame
import os

# Dimensões da tela principal
TELA_LARGURA = 720
TELA_ALTURA = 720

# Grid do jogo
GRID_ALTURA = 720
GRID_LARGURA = 450
TAMANHO_QUADRADO = 30
ESPESSURA_BORDA = 5

# Frames por segundo do jogo
FPS = 60

# Cores de fundo, bordas, UI e peças fixadas(RGB)
COR_BACKGROUND = (200,200,200)
COR_BORDA = (0,0,0)
COR_TEXTO = (0,0,0)
COR_GAMEOVER = (200,0,0)
COR_BOTAO = (175,175,175)
COR_BOTAO_CLICADO = (220,220,220)

# Cores das peças do jogo
LISTA_CORES = [
    (41,134,204), # Azul
    (5,22,153), # Azul Escuro
    (0,128,0), # Verde
    (21,81,21), # Verde Escuro
    (74,39,166), # Lilás
    (208,0,0), # Vermelho
    (241,98,2), # Laranja
    (200,200,0) # Amarelo
]

# Formato das peças do jogo
LISTA_PECAS = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1],[1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 0], [1, 1, 1]]
]

# Diretório base dos arquivos
DIR_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho dos assets
CAMINHO_SONS = os.path.join(DIR_BASE, "assets", "sounds")
CAMINHO_FONTES = os.path.join(DIR_BASE, "assets", "fonts")

# Fonte Padrão
pygame.font.init()
FONTE = pygame.font.Font(os.path.join(CAMINHO_FONTES, "BoldPixels.otf"), 40)