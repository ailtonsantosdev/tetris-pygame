import pygame
from src.jogo import jogar

def main():
    jogando = True

    while jogando:
        jogando = jogar()

    pygame.quit()
    quit()

if __name__ == "__main__":
    main()