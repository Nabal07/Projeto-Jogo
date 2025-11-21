import pygame
import sys
import random 

import config      
import assets      
import functions   

pygame.init()
pygame.font.init() 

tela = pygame.display.set_mode((config.LARGURA_TELA, config.ALTURA_TELA))
pygame.display.set_caption("Missão Saúde")
relogio = pygame.time.Clock()

img = assets.carregar_assets()

animacao_magro = [img['boneco1'], img['boneco2']]
animacao_gordinho = [img['boneco_gordinho1'], img['boneco_gordinho2']]
animacao_gordo = [img['boneco_gordo1'], img['boneco_gordo2']]

animacao_jogador = animacao_magro
frame_atual = 0
jogador_rect = img['boneco1'].get_rect()
ultimo_update_animacao = pygame.time.get_ticks()
jogador_esta_virado_esquerda = False

velocidade_atual = config.VELOCIDADE_MAGRO 

lista_obstaculos = [] 

imagens_comidas_boas = [img['maca'], img['alface'], img['banana']]
imagens_comidas_ruins = [img['hamburguer'], img['refrigerante'], img['sorvete']]

pontos = 0 
contador_besteiras = 0 
fonte_placar = img['fonte_placar'] 

fase_atual = 1
proxima_fase = 0 

COR_BRANCA = (255, 255, 255)
COR_PRETA = (0, 0, 0)
COR_VERDE_BOM = (100, 255, 100)
COR_VERMELHO_RUIM = (255, 100, 100)
COR_DIALOGO_FUNDO = config.COR_DIALOGO_FUNDO

fonte_dialogo = img['fonte_dialogo']
jogador_perto_do_cachorro = False
indice_dialogo_cachorro = 0 
DIALOGO_FASE_1 = [
    "Colete frutas para aumentar sua pontuação...",
    "...e evite as besteiras!",
    "Se comer muito, você vai ficar lento e pesado!",
    "Vá para a passagem na praia."
]


fundo_cenario = functions.criar_cenario(fase_atual, img) 

# Coqueiros
largura_coqueiro = img['coqueiro'].get_width()
altura_coqueiro = img['coqueiro'].get_height()
LARGURA_BONECO_REF = img['boneco1'].get_width()
ESPACO_PASSAGEM = int(LARGURA_BONECO_REF * 2.5) 
pos_x_coqueiro_dir = config.LARGURA_TELA - largura_coqueiro - config.MARGEM_CANTO
centro_passagem_y = (config.ALTURA_TELA // 2) - 50 

coqueiro_passagem_superior_rect = img['coqueiro'].get_rect(
    topleft=(pos_x_coqueiro_dir, centro_passagem_y - ESPACO_PASSAGEM // 2 - altura_coqueiro)
)
lista_obstaculos.append(coqueiro_passagem_superior_rect)

coqueiro_passagem_inferior_rect = img['coqueiro'].get_rect(
    topleft=(pos_x_coqueiro_dir, centro_passagem_y + ESPACO_PASSAGEM // 2)
)
lista_obstaculos.append(coqueiro_passagem_inferior_rect)

img_agua = img['agua']
largura_agua_tile = img_agua.get_width()
altura_agua_tile = img_agua.get_height()
pos_y_agua = config.ALTURA_TELA - altura_agua_tile
lista_agua_tiles = [] 
for pos_x in range(0, config.LARGURA_TELA, largura_agua_tile):
    agua_rect = img_agua.get_rect(topleft=(pos_x, pos_y_agua))
    lista_obstaculos.append(agua_rect)
    lista_agua_tiles.append(agua_rect)
    
pos_x_cachorro = config.MARGEM_CANTO + 30 
pos_y_cachorro = config.ALTURA_TELA // 2 
cachorro_rect = img['cachorro'].get_rect(topleft=(pos_x_cachorro, pos_y_cachorro))
lista_obstaculos.append(cachorro_rect)
cachorro_raio_interacao = cachorro_rect.inflate(100, 100) 


altura_passagem = coqueiro_passagem_inferior_rect.top - coqueiro_passagem_superior_rect.bottom
pos_y_passagem = coqueiro_passagem_superior_rect.bottom
pos_x_passagem = config.LARGURA_TELA - 10 
porta_fase_rect = pygame.Rect(pos_x_passagem, pos_y_passagem, 10, altura_passagem)

lista_comidas_boas = []
lista_comidas_ruins = []

estado_jogo = 'inicio' 
fonte_titulo = img['fonte_titulo']
fonte_instrucao = img['fonte_instrucao']
bob_y = 0
bob_direcao = 1

wipe_surface = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
wipe_surface.set_colorkey(config.WIPE_KEY)
wipe_radius = 0 
tela_centro = (config.LARGURA_TELA // 2, config.ALTURA_TELA // 2)


while True:
    
    if estado_jogo == 'inicio':
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    estado_jogo = 'jogando'
                    fase_atual = 1
                    pontos = 0 
                    contador_besteiras = 0 
                    animacao_jogador = animacao_magro 
                    velocidade_atual = config.VELOCIDADE_MAGRO 
                    
                    jogador_rect.center = (config.LARGURA_TELA // 2, config.ALTURA_TELA // 2)
                    fundo_cenario = functions.criar_cenario(fase_atual, img) 
                    lista_comidas_boas, lista_comidas_ruins = functions.iniciar_fase(
                        fase_atual, imagens_comidas_boas, imagens_comidas_ruins, lista_obstaculos
                    )
        
        bob_y += bob_direcao
        if bob_y > 15 or bob_y < -15: bob_direcao *= -1 
        
        tela.blit(fundo_cenario, (0, 0)) 
        texto_titulo = fonte_titulo.render("Missão Saúde", True, COR_PRETA)
        rect_titulo = texto_titulo.get_rect(center=(config.LARGURA_TELA // 2, 150))
        tela.blit(texto_titulo, rect_titulo)
        
        pos_boneco_inicio_x = config.LARGURA_TELA // 2
        pos_boneco_inicio_y = (config.ALTURA_TELA // 2) + bob_y 
        img_boneco_inicio = img['boneco1']
        rect_boneco_inicio = img_boneco_inicio.get_rect(center=(pos_boneco_inicio_x, pos_boneco_inicio_y))
        tela.blit(img_boneco_inicio, rect_boneco_inicio)
        
        texto_instrucao = fonte_instrucao.render("Aperte ESPAÇO para começar!", True, COR_BRANCA)
        rect_instrucao = texto_instrucao.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA - 100))
        tela.blit(texto_instrucao, rect_instrucao)

    
    elif estado_jogo == 'jogando':
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()    
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if jogador_perto_do_cachorro:
                        indice_dialogo_cachorro += 1
                        if indice_dialogo_cachorro > len(DIALOGO_FASE_1):
                            indice_dialogo_cachorro = 0
                
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5]:
                    if event.key == pygame.K_1: fase_atual = 1
                    elif event.key == pygame.K_2: fase_atual = 2
                    elif event.key == pygame.K_3: fase_atual = 3
                    elif event.key == pygame.K_4: fase_atual = 4
                    elif event.key == pygame.K_5: fase_atual = 5
                    
                    pontos = 0 
                    contador_besteiras = 0 
                    # Reseta animacao e velocidade
                    animacao_jogador = animacao_magro 
                    velocidade_atual = config.VELOCIDADE_MAGRO 
                    
                    fundo_cenario = functions.criar_cenario(fase_atual, img) 
                    lista_comidas_boas, lista_comidas_ruins = functions.iniciar_fase(
                        fase_atual, imagens_comidas_boas, imagens_comidas_ruins, lista_obstaculos
                    )

        esta_movendo = False
        teclas = pygame.key.get_pressed()
        
        if teclas[pygame.K_LEFT]:
            jogador_rect.x -= velocidade_atual
            jogador_esta_virado_esquerda = True
            esta_movendo = True
        if teclas[pygame.K_RIGHT]:
            jogador_rect.x += velocidade_atual
            jogador_esta_virado_esquerda = False
            esta_movendo = True
            
        for obstaculo in lista_obstaculos:
            if jogador_rect.colliderect(obstaculo):
                if teclas[pygame.K_LEFT]: jogador_rect.left = obstaculo.right
                if teclas[pygame.K_RIGHT]: jogador_rect.right = obstaculo.left
        
        if jogador_rect.left < 0: jogador_rect.left = 0
        if jogador_rect.right > config.LARGURA_TELA: jogador_rect.right = config.LARGURA_TELA

        if teclas[pygame.K_UP]:
            jogador_rect.y -= velocidade_atual
            esta_movendo = True
        if teclas[pygame.K_DOWN]:
            jogador_rect.y += velocidade_atual
            esta_movendo = True

        for obstaculo in lista_obstaculos:
            if jogador_rect.colliderect(obstaculo):
                if teclas[pygame.K_UP]: jogador_rect.top = obstaculo.bottom
                if teclas[pygame.K_DOWN]: jogador_rect.bottom = obstaculo.top

        if jogador_rect.top < 0: jogador_rect.top = 0
        if jogador_rect.bottom > config.ALTURA_TELA: jogador_rect.bottom = config.ALTURA_TELA

        # Passar de Fase
        if jogador_rect.colliderect(porta_fase_rect):
            if fase_atual < 5: 
                proxima_fase = fase_atual + 1
            else: 
                proxima_fase = -1 
            estado_jogo = 'transicao_out' 
            wipe_radius = 0 
        
        for comida in lista_comidas_boas[:]:
            if jogador_rect.colliderect(comida['rect']):
                lista_comidas_boas.remove(comida) 
                pontos += 10 
                if contador_besteiras > 0:
                    contador_besteiras -= 1
        
        for comida in lista_comidas_ruins[:]:
            if jogador_rect.colliderect(comida['rect']):
                lista_comidas_ruins.remove(comida) 
                pontos -= 10 
                contador_besteiras += 1 
        
        # Velocidade Gordos
        if contador_besteiras >= 10:
            estado_jogo = 'game_over'
        elif contador_besteiras >= 8:
            animacao_jogador = animacao_gordo
            velocidade_atual = config.VELOCIDADE_GORDO 
        elif contador_besteiras >= 5:
            animacao_jogador = animacao_gordinho
            velocidade_atual = config.VELOCIDADE_GORDINHO 
        else:
            animacao_jogador = animacao_magro
            velocidade_atual = config.VELOCIDADE_MAGRO 
                
        # Interação Cachorro
        if fase_atual == 1:
            if jogador_rect.colliderect(cachorro_raio_interacao):
                jogador_perto_do_cachorro = True
            else:
                jogador_perto_do_cachorro = False
                indice_dialogo_cachorro = 0 
        else:
            jogador_perto_do_cachorro = False
            
        # Animacao
        agora = pygame.time.get_ticks()
        if esta_movendo:
            if agora - ultimo_update_animacao > config.VELOCIDADE_ANIMACAO:
                ultimo_update_animacao = agora 
                frame_atual = (frame_atual + 1) % 2 
        else:
            frame_atual = 0
        
        imagem_base_atual = animacao_jogador[frame_atual]
        if jogador_esta_virado_esquerda:
            imagem_para_desenhar = pygame.transform.flip(imagem_base_atual, True, False)
        else:
            imagem_para_desenhar = imagem_base_atual
        
        # Renderizacao Jogo
        tela.blit(fundo_cenario, (0, 0))
        tela.blit(img['coqueiro'], coqueiro_passagem_superior_rect) 
        tela.blit(img['coqueiro'], coqueiro_passagem_inferior_rect) 
        for agua_rect in lista_agua_tiles: tela.blit(img['agua'], agua_rect)
        for comida in lista_comidas_boas: tela.blit(comida['imagem'], comida['rect'])
        for comida in lista_comidas_ruins: tela.blit(comida['imagem'], comida['rect'])
            
        if fase_atual == 1: tela.blit(img['cachorro'], cachorro_rect)
        
        if jogador_perto_do_cachorro:
            texto_para_mostrar = ""
            if indice_dialogo_cachorro == 0: texto_para_mostrar = "(Aperte ESPAÇO)"
            else: texto_para_mostrar = DIALOGO_FASE_1[indice_dialogo_cachorro - 1]
            
            texto_render = fonte_dialogo.render(texto_para_mostrar, True, COR_BRANCA)
            rect_texto = texto_render.get_rect()
            rect_fundo = rect_texto.inflate(20, 20) 
            rect_fundo.midleft = (cachorro_rect.right + 5, cachorro_rect.centery) 
            rect_texto.center = rect_fundo.center
            pygame.draw.rect(tela, COR_DIALOGO_FUNDO, rect_fundo, border_radius=5)
            tela.blit(texto_render, rect_texto)

        tela.blit(imagem_para_desenhar, jogador_rect)

        # Placar de Pontos
        texto_placar = fonte_placar.render(f"Pontos: {pontos}", True, COR_BRANCA)
        tela.blit(texto_placar, (10, 10))
        
        # Placar de Besteiras
        texto_besteiras = fonte_placar.render(f"Besteiras: {contador_besteiras}/10", True, COR_VERMELHO_RUIM)
        tela.blit(texto_besteiras, (10, 50))

    elif estado_jogo == 'transicao_out':
        wipe_radius += config.WIPE_SPEED 
        if wipe_radius > config.WIPE_MAX_RADIUS: 
            wipe_radius = 0 
            estado_jogo = 'transicao_in' 
            if proxima_fase == -1: fase_atual = 5 
            else:
                fase_atual = proxima_fase
                jogador_rect.center = (50, config.ALTURA_TELA // 2) 
                fundo_cenario = functions.criar_cenario(fase_atual, img)
                lista_comidas_boas, lista_comidas_ruins = functions.iniciar_fase(
                    fase_atual, imagens_comidas_boas, imagens_comidas_ruins, lista_obstaculos
                )

        tela.blit(fundo_cenario, (0, 0))
        tela.blit(img['coqueiro'], coqueiro_passagem_superior_rect) 
        tela.blit(img['coqueiro'], coqueiro_passagem_inferior_rect) 
        for agua_rect in lista_agua_tiles: tela.blit(img['agua'], agua_rect)
        for comida in lista_comidas_boas: tela.blit(comida['imagem'], comida['rect'])
        for comida in lista_comidas_ruins: tela.blit(comida['imagem'], comida['rect'])
        tela.blit(imagem_para_desenhar, jogador_rect)
        
        wipe_surface.fill(config.WIPE_KEY) 
        pygame.draw.circle(wipe_surface, COR_PRETA, tela_centro, wipe_radius) 
        tela.blit(wipe_surface, (0,0)) 

    elif estado_jogo == 'transicao_in':
        wipe_radius += config.WIPE_SPEED 
        if wipe_radius > config.WIPE_MAX_RADIUS: 
            wipe_radius = config.WIPE_MAX_RADIUS 
            if proxima_fase == -1: estado_jogo = 'fim' 
            else: estado_jogo = 'jogando' 
            proxima_fase = 0

        tela.blit(fundo_cenario, (0, 0))
        tela.blit(img['coqueiro'], coqueiro_passagem_superior_rect) 
        tela.blit(img['coqueiro'], coqueiro_passagem_inferior_rect) 
        for agua_rect in lista_agua_tiles: tela.blit(img['agua'], agua_rect)
        for comida in lista_comidas_boas: tela.blit(comida['imagem'], comida['rect'])
        for comida in lista_comidas_ruins: tela.blit(comida['imagem'], comida['rect'])
        tela.blit(imagem_para_desenhar, jogador_rect)
        
        wipe_surface.fill(COR_PRETA) 
        pygame.draw.circle(wipe_surface, config.WIPE_KEY, tela_centro, wipe_radius) 
        tela.blit(wipe_surface, (0,0)) 

        if fase_atual == 1:
            texto_fase = fonte_titulo.render(f"Fase {fase_atual}", True, COR_BRANCA)
            rect_fase = texto_fase.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 - 40))
            texto_aviso = fonte_instrucao.render("Fale com o cachorro!", True, COR_BRANCA)
            rect_aviso = texto_aviso.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 + 20))
            tela.blit(texto_fase, rect_fase)
            tela.blit(texto_aviso, rect_aviso)


    elif estado_jogo == 'fim':
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: estado_jogo = 'inicio'; proxima_fase = 0 
        
        tela.blit(fundo_cenario, (0, 0)) 
        texto_final_pontos = fonte_titulo.render(f"Pontuação Final: {pontos}", True, COR_PRETA)
        rect_final_pontos = texto_final_pontos.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 - 50))
        
        if pontos >= 0: texto_resultado = fonte_instrucao.render("Parabéns! Você se cuidou bem!", True, COR_VERDE_BOM)
        else: texto_resultado = fonte_instrucao.render("Cuide melhor da sua saúde!", True, COR_VERMELHO_RUIM)
        rect_resultado = texto_resultado.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 + 20))

        texto_reiniciar = fonte_instrucao.render("Aperte ESPAÇO para jogar de novo", True, COR_BRANCA)
        rect_reiniciar = texto_reiniciar.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA - 100))

        tela.blit(texto_final_pontos, rect_final_pontos)
        tela.blit(texto_resultado, rect_resultado)
        tela.blit(texto_reiniciar, rect_reiniciar)

    # Game Over
    elif estado_jogo == 'game_over':
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: estado_jogo = 'inicio'
                    
        tela.fill(COR_PRETA)
        
        texto_gameover = fonte_titulo.render("GAME OVER", True, COR_VERMELHO_RUIM)
        rect_gameover = texto_gameover.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 - 50))
        
        texto_motivo = fonte_instrucao.render("Você comeu muitas besteiras!", True, COR_BRANCA)
        rect_motivo = texto_motivo.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA // 2 + 20))

        texto_reiniciar = fonte_instrucao.render("Aperte ESPAÇO para tentar de novo", True, COR_BRANCA)
        rect_reiniciar = texto_reiniciar.get_rect(center=(config.LARGURA_TELA // 2, config.ALTURA_TELA - 100))

        tela.blit(texto_gameover, rect_gameover)
        tela.blit(texto_motivo, rect_motivo)
        tela.blit(texto_reiniciar, rect_reiniciar)

    # --- Atualização final da tela ---
    pygame.display.flip()
    relogio.tick(60)