import pygame
import config 

def carregar_assets():
    assets = {}
    
    # Jogador 
    assets['boneco1'] = pygame.image.load("assets/Boneco1.png").convert_alpha()
    assets['boneco2'] = pygame.image.load("assets/Boneco2.png").convert_alpha()
    
    # Terreno 
    assets['terreno1'] = pygame.image.load("assets/Terreno01.png").convert()
    assets['terreno2'] = pygame.image.load("assets/Terreno02.png").convert()
    assets['terreno3'] = pygame.image.load("assets/Terreno03.png").convert()
    
    # Decoração  
    assets['coqueiro'] = pygame.image.load("assets/Coqueiro.png").convert_alpha()
    assets['agua'] = pygame.image.load("assets/AguaHorizontal.png").convert()
    
    # NPCs 
    assets['cachorro'] = pygame.image.load("assets/Cachorro.png").convert_alpha()
    
    # Comidas 
    assets['maca'] = pygame.image.load("assets/Maca.png").convert_alpha()
    assets['alface'] = pygame.image.load("assets/Alface.png").convert_alpha()
    assets['hamburguer'] = pygame.image.load("assets/Hamburguer.png").convert_alpha()
    assets['refrigerante'] = pygame.image.load("assets/Refrigerante.png").convert_alpha()
    assets['banana'] = pygame.image.load("assets/Banana.png").convert_alpha()
    assets['sorvete'] = pygame.image.load("assets/Sorvete.png").convert_alpha()
    
    # Fontes 
    assets['fonte_titulo'] = pygame.font.Font(None, config.TAMANHO_FONTE_TITULO)
    assets['fonte_instrucao'] = pygame.font.Font(None, config.TAMANHO_FONTE_INSTRUCAO)
    assets['fonte_placar'] = pygame.font.Font(None, config.TAMANHO_FONTE_PLACAR)
    assets['fonte_dialogo'] = pygame.font.Font(None, config.TAMANHO_FONTE_DIALOGO)
    
    return assets