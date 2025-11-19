import pygame
import src.som as som
import src.tabuleiro as tabuleiro
import src.ui as ui
from src.peca import Peca
from src.constantes import TELA_LARGURA, TELA_ALTURA, FPS

def reiniciar_jogo(tela):
    """Restaura todas as variáveis para o estado inicial. Retorna os valores iniciais da nova partida."""
    grid = tabuleiro.desenhar_grid(tela)
    lista_pecas = [Peca()]
    tem_peca = False
    peca_encostou = False
    tempo_no_chao = 0
    pontos = 0
    nivel = 1
    linhas = 0
    tempo_desde_ultimo = 0
    intervalo = 1
    estado = "jogando"
    relogio = pygame.time.Clock()
    rodando = True
    velocidade_game = 1000
    nivel_anterior = 1
    troca_cor = True
    tela_gameover_desenhada = False
    clicando_reiniciar = False
    clicando_sair = False
    tempo_animacao = 0
    tempo_click = 0
    botao_clicado = None
    som.iniciar_musica()

    return grid, lista_pecas, pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo, estado, relogio, rodando, velocidade_game, nivel_anterior, troca_cor, tela_gameover_desenhada, clicando_reiniciar, clicando_sair, tempo_animacao, tempo_click, botao_clicado

def atualizar_jogo(tela, eventos, grid, lista_pecas, pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo):
    """Atualiza a lógica do jogo durante o estado 'jogando'."""

    # Forma de simular que um botão está sendo segurado e não apenas apertado
    pygame.key.set_repeat(200, 50)

    for evento in eventos:
        if evento.type == pygame.KEYDOWN:
            moveu = False

            if evento.key == pygame.K_UP:
                lista_pecas[0].girar(tela, grid)
                moveu = True
            elif evento.key == pygame.K_LEFT:
                lista_pecas[0].mover(tela, grid, 1)
                moveu = True
            elif evento.key == pygame.K_RIGHT:
                lista_pecas[0].mover(tela, grid, 2)
                moveu = True
            elif evento.key == pygame.K_DOWN:
                lista_pecas[0].mover(tela, grid, 3)
                moveu = True

            if moveu and peca_encostou:
                if not lista_pecas[0].no_chao(grid):
                    lista_pecas[0].cair(tela)
                    peca_encostou = False
                    tempo_no_chao = 0
    
    if not tem_peca:
        lista_pecas[0].iniciar_peca(tela)
        tabuleiro.peca_em_jogo(tela, grid, lista_pecas[0])
        lista_pecas.append(Peca())
        lista_pecas[1].iniciar_peca(tela)
        pontos, nivel, linhas = tabuleiro.verificar_tabuleiro(tela, grid, pontos, nivel, linhas)
        tem_peca = True
        tempo_desde_ultimo = 0
        peca_encostou = False
        tempo_no_chao = 0
    else:
        if not lista_pecas[0].no_chao(grid):
            peca_encostou = False
            tempo_no_chao = 0

            if tempo_desde_ultimo > intervalo:
                lista_pecas[0].cair(tela)
                tempo_desde_ultimo = 0
        else:
            if not peca_encostou:
                peca_encostou = True
                tempo_no_chao = 0
            else:
                tempo_no_chao += 1 / FPS # Tempo baseado no frame

            if tempo_no_chao >= 1:
                lista_pecas[0].fixar_peca(tela, grid)
                lista_pecas.pop(0)
                pontos, nivel, linhas = tabuleiro.verificar_tabuleiro(tela, grid, pontos, nivel, linhas)
                lista_pecas.append(Peca())
                lista_pecas[1].iniciar_peca(tela)
                if tabuleiro.peca_em_jogo(tela, grid, lista_pecas[0]):
                    return "gameover", pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo
                tem_peca = True
                peca_encostou = False
                tempo_no_chao = 0
                tempo_desde_ultimo = 0
                        
    return "jogando", pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo

def jogar():
    """Inicia as variáveis, e mantém o jogo em execução enquanto não for fechado pelo usuário."""
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))
    pygame.display.set_caption("Tetris")

    grid, lista_pecas, pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo, estado, relogio, rodando, velocidade_game, nivel_anterior, troca_cor, tela_gameover_desenhada, clicando_reiniciar, clicando_sair, tempo_animacao, tempo_click, botao_clicado = reiniciar_jogo(tela)

    while rodando:
        dt = relogio.tick(FPS) / velocidade_game
        tempo_desde_ultimo += dt

        eventos = pygame.event.get()

        for evento in eventos:
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()

        if estado == "jogando":
            estado, pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo = atualizar_jogo(
                tela, eventos, grid, lista_pecas, pontos, nivel, linhas, tem_peca, peca_encostou, tempo_no_chao, tempo_desde_ultimo, intervalo
            )

            # Diminui o tempo de queda a cada nível
            if nivel > nivel_anterior:
                velocidade_game *= 0.8
                nivel_anterior = nivel

        elif estado == "gameover":
            if not tela_gameover_desenhada:
                ui.desenhar_tela_gameover(tela, pontos)
                tela_gameover_desenhada = True
                rect_reiniciar = ui.desenhar_botao(tela, "REINICIAR", (TELA_LARGURA - 200) // 2, 350, 200, 80, clicando_reiniciar)
                rect_sair = ui.desenhar_botao(tela, "SAIR", (TELA_LARGURA - 200) // 2, 470, 200, 80, clicando_sair)
            
            if pygame.time.get_ticks() - tempo_animacao > 500:
                troca_cor = not troca_cor
                ui.animar_gameover(tela, troca_cor)
                tempo_animacao = pygame.time.get_ticks()

            mouse_pos = pygame.mouse.get_pos()

            for evento in eventos:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if rect_reiniciar.collidepoint(evento.pos):
                        clicando_reiniciar = True
                    elif rect_sair.collidepoint(evento.pos):
                        clicando_sair = True

                elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                    if clicando_reiniciar and rect_reiniciar.collidepoint(evento.pos):
                        botao_clicado = "reiniciar"
                        tempo_click = pygame.time.get_ticks()
                        print(tempo_click)
                        rect_reiniciar = ui.desenhar_botao(tela, "REINICIAR", (TELA_LARGURA - 200) // 2, 350, 200, 80, False)
                    
                    elif clicando_sair and rect_sair.collidepoint(evento.pos):
                        botao_clicado = "sair"
                        tempo_click = pygame.time.get_ticks()
                        rect_sair = ui.desenhar_botao(tela, "SAIR", (TELA_LARGURA - 200) // 2, 470, 200, 80, False)
                    
                    clicando_reiniciar = False
                    clicando_sair = False

                if clicando_reiniciar:
                    rect_reiniciar = ui.desenhar_botao(tela, "REINICIAR", (TELA_LARGURA - 200)//2, 350, 200, 80, True, 3)
                else:
                    rect_reiniciar = ui.desenhar_botao(tela, "REINICIAR", (TELA_LARGURA - 200)//2, 350, 200, 80, rect_reiniciar.collidepoint(mouse_pos))

                if clicando_sair:
                    rect_sair = ui.desenhar_botao(tela, "SAIR", (TELA_LARGURA - 200)//2, 470, 200, 80, True, 3)
                else:
                    rect_sair = ui.desenhar_botao(tela, "SAIR", (TELA_LARGURA - 200)//2, 470, 200, 80, rect_sair.collidepoint(mouse_pos))

        pygame.display.update()

        if botao_clicado is not None:
            if pygame.time.get_ticks() - tempo_click > 300:
                if botao_clicado == "reiniciar":
                    return True
                else:
                    return False