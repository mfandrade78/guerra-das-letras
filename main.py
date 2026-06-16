import pygame
import random
import math

# chamando o pygame e os efeitos sonoros
pygame.init()
pygame.mixer.init()

# layout da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

# cores
preto = (10, 10, 20)
branco = (255, 255, 255)
amarelo = (255, 234, 0)
azul = (50, 150, 255)
verde = (0, 255, 100)
vermelho = (255, 50, 50)
cinza = (100, 100, 100)

# fontes
fonte_gigante = pygame.font.SysFont("Arial", 45, bold=True)
fonte_gigante = pygame.font.SysFont("Arial", 32, bold=True)

# efeitos sonoros
def gerar_som(tipo):
    """Gera um som de acerto (agudo) ou erro (grave)"""
    frequencia = 880 if tipo == "acerto" else 220
    duracao = 0.1 if tipo == "acerto" else 0.3
    amostragem = 44100
    num_amostras = init(duracao * amostragem)

    buffer = bytearray()
    for i in range(num_amostras):
        t = i / amostragem
        # onda quadrada básica
        valor = 127 if math.sin(2 * math.pi * frequencia * t) > 0 else -128
        buffer.append(valor & 0xFF)

    som = pygame.mixer.Sound(buffer=bytes(buffer))
    