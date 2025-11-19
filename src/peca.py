import pygame
import random
from src.constantes import LISTA_CORES, LISTA_PECAS, COR_BACKGROUND, COR_BORDA, GRID_LARGURA, GRID_ALTURA, ESPESSURA_BORDA
from src.som import tocar_som

class Peca:
    def __init__(self):
        self.altura = 0
        self.largura = 0
        self.posicao_x = 0
        self.posicao_y = 0
        self.cor_peca = None
        self.espessura_borda = 2
        self.tamanho_quadrado = 30
        self.indice_tipo_peca = 0
        self.tipo_peca = None
        self.cont_giro = 0
    
    def iniciar_peca(self, tela):
        """Cria a peça e a coloca na lateral, mostrando qual será a próxima peça."""
        self.indice_tipo_peca = random.randrange(0, 7)

        self.tipo_peca = LISTA_PECAS[self.indice_tipo_peca]

        if self.indice_tipo_peca == 0:
            x = 540
            y = 75
            self.altura = 1
            self.largura = 4
        elif self.indice_tipo_peca == 3:
            x = 570
            y = 60
            self.altura = 2
            self.largura = 2
        else:
            x = 555
            y = 60
            self.altura = 2
            self.largura = 3

        indice_cor_peca = random.randrange(0, 8)
        self.cor_peca = LISTA_CORES[indice_cor_peca]

        # Apaga a peça que está ao lado
        pygame.draw.rect(tela, (COR_BACKGROUND), (520, 40, 160, 100))

        for a, linha in enumerate(self.tipo_peca):
            for b, valor in enumerate(linha):
                if valor:
                    valor = self.cor_peca
                    self.tipo_peca[a][b] = valor
                    pygame.draw.rect(tela, valor, (x, y, self.tamanho_quadrado, self.tamanho_quadrado))
                x += self.tamanho_quadrado
            y += self.tamanho_quadrado

            x -= len(linha) * self.tamanho_quadrado
    
    def set_posicao_inicial(self):
        """Define a posição inicial X da peça ao iniciá-la no grid."""
        self.posicao_x = 6
    
    def cair(self, tela):
        """Altera a posição Y da peça."""
        self.atualizar_peca(tela, 0, 1)

    def fixar_peca(self, tela, grid):
        """Fixa a peça ao final do grid."""
        x = self.posicao_x * self.tamanho_quadrado
        y = self.posicao_y * self.tamanho_quadrado

        for a, linha in enumerate(self.tipo_peca):
            for b, valor in enumerate(linha):
                if valor != 0:
                    grid[self.posicao_y + a][self.posicao_x + b] = self.cor_peca
                    pygame.draw.rect(tela, self.cor_peca, (x, y, self.tamanho_quadrado, self.tamanho_quadrado))
                x += self.tamanho_quadrado
            y += self.tamanho_quadrado
            x = self.posicao_x * self.tamanho_quadrado

        tocar_som("Efeito_Chao")

    def atualizar_peca(self, tela, novo_x, novo_y, novo_tipo_peca=None):
        """Atualiza a posição atual da peça, quando ela cai, é movida ou girada."""
        x = self.posicao_x * self.tamanho_quadrado
        y = self.posicao_y * self.tamanho_quadrado

        for linha in self.tipo_peca:
            for valor in linha:
                if valor != 0:
                    pygame.draw.rect(tela, COR_BACKGROUND, (x, y, self.tamanho_quadrado, self.tamanho_quadrado))
                x += self.tamanho_quadrado
            y += self.tamanho_quadrado

            x = self.posicao_x * self.tamanho_quadrado

        if novo_tipo_peca is None:
            self.posicao_x += novo_x
            self.posicao_y += novo_y
        else:
            self.tipo_peca = novo_tipo_peca
            self.posicao_x = novo_x
            self.posicao_y = novo_y

        x = self.posicao_x * self.tamanho_quadrado
        y = self.posicao_y * self.tamanho_quadrado

        for linha in self.tipo_peca:
            for valor in linha:
                if valor != 0:
                    pygame.draw.rect(tela, self.cor_peca, (x, y, self.tamanho_quadrado, self.tamanho_quadrado))
                x += self.tamanho_quadrado
            y += self.tamanho_quadrado

            x = self.posicao_x * self.tamanho_quadrado

        # Retângulo do Tetris
        pygame.draw.rect(tela, COR_BORDA, (0, 0, GRID_LARGURA, GRID_ALTURA), ESPESSURA_BORDA)

    def no_chao(self, grid):
        """Verifica se a peça está na última posição possivel de descer. Retorna TRUE ou FALSE."""
        if self.tipo_peca is not None:

            if self.posicao_y + self.altura >= len(grid):
                return True

            for a, linha in enumerate(self.tipo_peca):
                for b, valor in enumerate(linha):
                    if valor != 0:
                        if grid[self.posicao_y + a + 1][self.posicao_x + b] != 0:
                            return True
            return False

    def colicao_lateral(self, grid, direcao):
        """Verifica se é possível a peça mover-se para os lados. Retorna TRUE ou FALSE."""
        for a, linha in enumerate(self.tipo_peca):
            for b, valor in enumerate(linha):
                if valor != 0:
                    if direcao == 1:
                        if self.posicao_x + b - 1 < 0:
                            return True
                        if grid[self.posicao_y + a][self.posicao_x + b - 1] != 0:
                            return True
                    elif direcao == 2:
                        if self.posicao_x + b + 1 >= (GRID_LARGURA // self.tamanho_quadrado):
                            return True
                        if grid[self.posicao_y + a][self.posicao_x + b + 1] != 0:
                            return True
        return False


    def mover(self, tela, grid, direcao):
        """Move a peça para os lados ou para baixo, desde que seja possível."""
        if self.tipo_peca is not None:
            if direcao == 1 and not self.colicao_lateral(grid, direcao):
                self.atualizar_peca(tela, -1, 0)
            elif direcao == 2 and not self.colicao_lateral(grid, direcao):
                self.atualizar_peca(tela, 1, 0)
            elif direcao == 3 and not self.no_chao(grid):
                self.atualizar_peca(tela, 0, 1)

    def pode_girar(self, grid, peca_girada, posicao_x, posicao_y):
        """Verifica se é possível efetuar o movimento de girar, mantendo-se dentro dos limites do grid, e sem transpassar peças já fixadas. Retorna TRUE ou FALSE."""
        if self.indice_tipo_peca == 3: # Caso seja o quadrado, não precisa girar
            return False

        for a, linha in enumerate(peca_girada):
            for b, valor in enumerate(linha):
                if valor != 0:
                    x = posicao_x + b
                    y = posicao_y + a

                    if x < 0 or x >= GRID_LARGURA // self.tamanho_quadrado or y < 0 or y >= len(grid):
                        return False

                    if grid[y][x] != 0:
                        return False
        return True

    def girar(self, tela, grid):
        """Efetua o movimento de girar a peça, desde que seja possível."""
        if self.tipo_peca is not None:
            if not self.no_chao(grid):

                nova_pos_x = self.posicao_x
                nova_pos_y = self.posicao_y

                if self.indice_tipo_peca == 0:
                    if self.cont_giro % 2 == 1:
                        nova_pos_x = self.posicao_x - 1
                        nova_pos_y = self.posicao_y + 1
                    else:
                        nova_pos_x = self.posicao_x + 1
                        nova_pos_y = self.posicao_y - 1

                if self.indice_tipo_peca in (4, 5):
                    if self.cont_giro % 2 == 1:
                        nova_pos_x = self.posicao_x - 1
                        nova_pos_y = self.posicao_y + 1
                    else:
                        nova_pos_x = self.posicao_x + 1
                        nova_pos_y = self.posicao_y - 1
                if self.indice_tipo_peca in (1, 2, 6):

                    if self.cont_giro == 0:
                        nova_pos_x = self.posicao_x + 1
                    elif self.cont_giro == 1:
                        nova_pos_x = self.posicao_x - 1
                        nova_pos_y = self.posicao_y + 1
                    elif self.cont_giro == 2:
                        nova_pos_y = self.posicao_y - 1
                    elif self.cont_giro == 3:
                        nova_pos_x = self.posicao_x

                nova_peca = [[0] * self.altura for _ in range(self.largura)]
                for a in range(self.altura):
                    for b in range(self.largura):
                        nova_peca[b][self.altura - 1 - a] = self.tipo_peca[a][b]

                if self.pode_girar(grid, nova_peca, nova_pos_x, nova_pos_y):
                    self.altura, self.largura = self.largura, self.altura
                    self.cont_giro = (self.cont_giro + 1) % 4
                    self.atualizar_peca(tela, nova_pos_x, nova_pos_y, nova_peca)
                    tocar_som("Efeito_Girar")