import pygame
from src.som import tocar_som
from src.constantes import *

def desenhar_grid(tela):
    """Cria a tela inicial e o grid do Tetris."""

    LINHAS_GRID = GRID_ALTURA // TAMANHO_QUADRADO
    COLUNAS_GRID = GRID_LARGURA // TAMANHO_QUADRADO

    grid = [[0 for _ in range(COLUNAS_GRID)] for _ in range(LINHAS_GRID)]

    # Retângulo inteiro da tela / Retângulo do Tetris
    pygame.draw.rect(tela, COR_BACKGROUND, (0, 0, TELA_LARGURA, TELA_ALTURA))
    pygame.draw.rect(tela, COR_BORDA, (0, 0, GRID_LARGURA, GRID_ALTURA), ESPESSURA_BORDA)

    # Próxima Peça / Pontos / Nível / Linhas
    pygame.draw.rect(tela, COR_BORDA, (510, 30, 180, 120), ESPESSURA_BORDA)
    pygame.draw.rect(tela, COR_BORDA, (510, 180, 180, 100), ESPESSURA_BORDA)
    pygame.draw.rect(tela, COR_BORDA, (510, 310, 180, 100), ESPESSURA_BORDA)
    pygame.draw.rect(tela, COR_BORDA, (510, 440, 180, 100), ESPESSURA_BORDA)

    titulo_pontos = FONTE.render("Pontos", True, COR_TEXTO)
    titulo_nivel = FONTE.render("Nível", True, COR_TEXTO)
    titulo_linhas = FONTE.render("Linhas", True, COR_TEXTO)

    tela.blit(titulo_pontos, titulo_pontos.get_rect(center=(600, 210)))
    tela.blit(titulo_nivel, titulo_nivel.get_rect(center=(600, 340)))
    tela.blit(titulo_linhas, titulo_linhas.get_rect(center=(600, 470)))

    return grid

def peca_em_jogo(tela, grid, peca):
    """Desenha a peça na posição inicial do grid. Retorna TRUE ou FALSE."""
    peca.set_posicao_inicial() # Define a posição inicial da posição X da peça.

    gameover = True if verificar_gameover(grid, peca) else False

    peca.atualizar_peca(tela, 0, 0)
    return gameover

def verificar_tabuleiro(tela, grid, pontos, nivel, linhas):
    """Verifica se há linhas completas e atualiza a pontuação e nível."""
    linhas_por_vez = 0
    tam_quadrado = 30

    for linha in grid:
        if not 0 in linha:
            tocar_som("Efeito_Linha")
            linhas_por_vez += 1
            linhas += 1
            grid.remove(linha)
            linha_nova = [0 for _ in range(len(grid[0]))]
            grid.insert(0, linha_nova)

            for a, linha in enumerate(grid):
                for b, valor in enumerate(linha):
                    x = b * tam_quadrado
                    y = a * tam_quadrado

                    if valor == 0:
                        pygame.draw.rect(tela, COR_BACKGROUND, (x, y, tam_quadrado, tam_quadrado))
                    else:
                        pygame.draw.rect(tela, valor, (x, y, tam_quadrado, tam_quadrado))

    # Retângulo do Tetris
    pygame.draw.rect(tela, COR_BORDA, (0, 0, GRID_LARGURA, GRID_ALTURA), ESPESSURA_BORDA)

    match linhas_por_vez:
        case 1: pontos += 40
        case 2: pontos += 100
        case 3: pontos += 300
        case 4: pontos += 1000

    nivel = linhas // 10 + 1

    atualizar_placar(tela, pontos, nivel, linhas)

    return pontos, nivel, linhas

def atualizar_placar(tela, pontos, nivel, linhas):
    """Atualiza o placar na lateral."""
    pygame.draw.rect(tela, COR_BACKGROUND, (520, 230, 160, 40))
    pygame.draw.rect(tela, COR_BACKGROUND, (520, 360, 160, 40))
    pygame.draw.rect(tela, COR_BACKGROUND, (520, 490, 160, 40))

    texto_pontos = FONTE.render(f"{pontos}", True, COR_TEXTO)
    texto_nivel = FONTE.render(f"{nivel}", True, COR_TEXTO)
    texto_linhas = FONTE.render(f"{linhas}", True, COR_TEXTO)

    tela.blit(texto_pontos, texto_pontos.get_rect(center=(600, 250)))
    tela.blit(texto_nivel, texto_nivel.get_rect(center=(600, 380)))
    tela.blit(texto_linhas, texto_linhas.get_rect(center=(600, 510)))

def verificar_gameover(grid, peca):
    """Verifica se ocorreu a condição de fim de jogo. Retorna TRUE ou FALSE."""
    for a, linha in enumerate(peca.tipo_peca):
        for b, valor in enumerate(linha):
            if valor:
                x = peca.posicao_x + b
                y = peca.posicao_y + a
                if y >= 0 and grid[y][x] != 0:
                    return True
    return False