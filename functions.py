import random
import config 
import pygame 

def spawnar_comida(tipo_comida, imagens_boas, imagens_ruins, obstaculos):
    imagem_sorteada = None
    if tipo_comida == 'boa':
        imagem_sorteada = random.choice(imagens_boas)
    elif tipo_comida == 'ruim':
        imagem_sorteada = random.choice(imagens_ruins)
    
    while True:
        pos_x = random.randint(0, config.LARGURA_TELA - imagem_sorteada.get_width())
        pos_y = random.randint(0, config.ALTURA_TELA - imagem_sorteada.get_height())
        novo_rect = imagem_sorteada.get_rect(topleft=(pos_x, pos_y))
        
        colidiu_obstaculo = False
        for obstaculo in obstaculos:
            if novo_rect.colliderect(obstaculo):
                colidiu_obstaculo = True
                break 
        
        if not colidiu_obstaculo:
            return {'rect': novo_rect, 'imagem': imagem_sorteada}


def iniciar_fase(numero_fase, imagens_boas, imagens_ruins, obstaculos):
    """
    Cria as listas de comidas/itens baseado no número da fase.
    Retorna (lista_comidas_boas, lista_comidas_ruins)
    """
    lista_boas = []
    lista_ruins = []

    if numero_fase == 1:
        #  Fase 1 
        print("Iniciando Fase 1 (Exploração)")
        pass 

    elif numero_fase == 2:
        #  Fase 2 
        print("Iniciando Fase 2 (Coleta Leve)")
        for _ in range(5): 
            lista_boas.append(spawnar_comida('boa', imagens_boas, imagens_ruins, obstaculos))
        for _ in range(3): 
            lista_ruins.append(spawnar_comida('ruim', imagens_boas, imagens_ruins, obstaculos))
            
    elif numero_fase == 3:
        #  Fase 3 
        print("Iniciando Fase 3 (Coleta Média)")
        for _ in range(7):
            lista_boas.append(spawnar_comida('boa', imagens_boas, imagens_ruins, obstaculos))
        for _ in range(5): 
            lista_ruins.append(spawnar_comida('ruim', imagens_boas, imagens_ruins, obstaculos))
            
    elif numero_fase == 4:
        #  Fase 4 
        print("Iniciando Fase 4 (Coleta Difícil)")
        for _ in range(10): 
            lista_boas.append(spawnar_comida('boa', imagens_boas, imagens_ruins, obstaculos))
        for _ in range(7): 
            lista_ruins.append(spawnar_comida('ruim', imagens_boas, imagens_ruins, obstaculos))
            
    elif numero_fase == 5:
        #  Fase 5 
        print("Iniciando Fase 5 (Coleta Final)")
        for _ in range(12): 
            lista_boas.append(spawnar_comida('boa', imagens_boas, imagens_ruins, obstaculos))
        for _ in range(10): 
            lista_ruins.append(spawnar_comida('ruim', imagens_boas, imagens_ruins, obstaculos))
    
    return lista_boas, lista_ruins

def criar_cenario(fase_atual, img):
    """
    Cria e retorna a superfície (imagem) do fundo da fase.
    """
    fundo = pygame.Surface((config.LARGURA_TELA, config.ALTURA_TELA))
    
    terrenos_fase = []
    if fase_atual == 1:
        terrenos_fase = [img['terreno1'], img['terreno2'], img['terreno3']]
    
    elif fase_atual == 2:
        terrenos_fase = [img['terreno1'], img['terreno2']] 
        
    elif fase_atual == 3:
        terrenos_fase = [img['terreno3']]
        
    elif fase_atual == 4:
        terrenos_fase = [img['terreno1'], img['terreno3']]
        
    elif fase_atual == 5:
        terrenos_fase = [img['terreno2'], img['terreno3']]
    
    if terrenos_fase: 
        for y in range(0, config.ALTURA_TELA, config.TAMANHO_TILE): 
            for x in range(0, config.LARGURA_TELA, config.TAMANHO_TILE): 
                tile_aleatorio = random.choice(terrenos_fase)
                fundo.blit(tile_aleatorio, (x, y))
    else:
        # Se nenhuma fase for encontrada, pinta de preto
        fundo.fill((0, 0, 0))
            
    return fundo