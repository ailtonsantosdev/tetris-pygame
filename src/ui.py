import pygame
import src.som as som
from src.constantes import *

def desenhar_tela_gameover(tela, pontos):
    """Exibe a tela de Game Over."""
    if som.pygame.mixer.music.get_busy:
        som.pygame.mixer.music.stop()
    som.tocar_som("Efeito_GameOver")

    nova_tela = pygame.Surface((TELA_LARGURA, TELA_ALTURA), pygame.SRCALPHA)
    nova_tela.set_alpha(150)
    nova_tela.fill(COR_BACKGROUND)

    tela.blit(nova_tela,(0,0))

    largura_janela, altura_janela = 500, 500
    x = (TELA_LARGURA - largura_janela) // 2
    y = (TELA_ALTURA - altura_janela) // 2

    pygame.draw.rect(tela, COR_BACKGROUND, (x, y, largura_janela, altura_janela))
    pygame.draw.rect(tela, COR_BORDA, (x, y, largura_janela, altura_janela), 20)

    animar_gameover(tela, True) # inicia o texto 'Game Over' com a cor preta padrão

    fonte_pontos = _tamanho_fonte(50)

    texto_pontos = fonte_pontos.render("PONTOS:", True, COR_TEXTO)
    valor_pontos = fonte_pontos.render(str(pontos), True, COR_TEXTO)

    tela.blit(texto_pontos, texto_pontos.get_rect(center=(TELA_LARGURA//2, 260)))
    tela.blit(valor_pontos, valor_pontos.get_rect(center=(TELA_LARGURA//2, 310)))

def desenhar_botao(tela, nome, x, y, largura, altura, clicando, deslocamento_y = 0):
    """Desenha um botão e retorna os parâmetros de seu retângulo."""
    mouse_posicao = pygame.mouse.get_pos()

    #Rect original do botão
    botao_rect = pygame.Rect(x, y, largura, altura)

    # Com deslocamento para baixo, simulando um "pressionado"
    botao_rect_deslocado = pygame.Rect(x, y + deslocamento_y, largura, altura)

    cor = COR_BOTAO
    if botao_rect.collidepoint(mouse_posicao) and clicando:
        cor = COR_BOTAO_CLICADO
        pygame.draw.rect(tela, COR_BACKGROUND, botao_rect)
    
    pygame.draw.rect(tela, cor, botao_rect_deslocado)
    pygame.draw.rect(tela, COR_BORDA, botao_rect_deslocado, 5)
    pygame.draw.line(tela, COR_BORDA, (x, y + altura), (x + largura - 1, y + altura), 5) # Uma linha abaixo do botão para dar impressão de profundidade

    fonte_botao = _tamanho_fonte(30)
    texto = fonte_botao.render(nome, True, COR_TEXTO)
    tela.blit(texto, texto.get_rect(center=(x + largura//2, y + altura//2 + deslocamento_y)))

    return botao_rect

def _tamanho_fonte(tamanho):
    """Função interna para definir um tamanho específico para a fonte utilizada."""
    fonte = pygame.font.Font(f"{CAMINHO_FONTES}/BoldPixels.otf", tamanho)
    return fonte

def animar_gameover(tela, troca_cor):
    """Alterna as cores do texto 'GAME OVER'."""
    cor = COR_TEXTO if troca_cor else COR_GAMEOVER
    fonte_gameover = _tamanho_fonte(80)
    texto_gameover = fonte_gameover.render("GAME OVER", True, cor)
    tela.blit(texto_gameover, texto_gameover.get_rect(center=(TELA_LARGURA//2, 190)))