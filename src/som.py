import pygame
from src.constantes import CAMINHO_SONS

def iniciar_musica():
    """Inicia a música da partida."""
    pygame.mixer.init()

    # Para carregar a música
    pygame.mixer.music.load(f"{CAMINHO_SONS}/Tetris_Theme.ogg")

    # Define o volume (0.0 a 1.0)
    pygame.mixer.music.set_volume(0.2)

    # Toca a música em loop infinito (-1)
    pygame.mixer.music.play(-1)

def tocar_som(nome_som):
    """Executa o som determinado pelo parâmetro."""
    som_linha = pygame.mixer.Sound(f"{CAMINHO_SONS}/{nome_som}.ogg")
    som_linha.play()