import pygame
import random
from configuracoes import (
    largura, altura, branco, cinza, cinza_claro, azul, roxo, verde, vermelho, preto_nave, amarelo, fonte_media
)

# classes do jogo
class Nave:
    def __init__(self):
        self.largura = 50
        self.altura = 40
        self.x = largura // 2 - self.largura // 2
        self.y = altura - 70
        self.velocidade = 7

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < largura - self.largura:
            self.x += self.velocidade

    def desenhar(self, tela):
        # desenha a nave como um foguete
        cx = self.x + self.largura / 2
        topo = self.y
        larg = self.largura
        alt = self.largura

        # pontos verticais de cima para baixo da nave
        y_nariz_base = topo + alt * 0.22
        y_asas = topo + alt * 0.55
        y_corpo_base = topo + alt * 0.82
        y_motor = topo + alt

        # asas (esquerda)
        asa_esq = [
            (cx - larg * 0.10, y_asas),
            (self.x - larg * 0.35, y_corpo_base + alt * 0.05),
            (self.x - larg * 0.05, y_corpo_base + alt * 0.14),
            (cx - larg * 0.05, y_corpo_base),
        ]

        # asas (direita)
        asa_dir = [
            (cx + larg * 0.10, y_asas),
            (self.x + larg + larg * 0.35, y_corpo_base + alt * 0.05),
            (self.x + larg + larg * 0.05, y_corpo_base + alt * 0.14),
            (cx + larg * 0.05, y_corpo_base),
        ]
        pygame.draw.polygon(tela, branco, asa_esq)
        pygame.draw.polygon(tela, branco, asa_dir)
        pygame.draw.polygon(tela, cinza, asa_esq, 3)
        pygame.draw.polygon(tela, cinza, asa_dir, 3)

        # nariz da nave
        nariz = [
            (cx, topo),
            (cx - larg * 0.05, y_nariz_base),
            (cx + larg * 0.05, y_nariz_base),
        ]
        pygame.draw.polygon(tela, cinza_claro, nariz)
        pygame.draw.polygon(tela, azul, nariz, 2)

        # corpo central / fuselagem
        corpo = [
            (cx - larg * 0.05, y_nariz_base),
            (cx - larg * 0.16, y_asas),
            (cx - larg * 0.13, y_corpo_base),
            (cx + larg * 0.13, y_corpo_base),
            (cx + larg * 0.16, y_asas),
            (cx + larg * 0.05, y_nariz_base),
        ]
        pygame.draw.polygon(tela, roxo, corpo)
        pygame.draw.polygon(tela, branco, corpo, 2)

        # cockpit
        raio_cockpit = max(3, int(larg * 0.05))
        centro_cockpit = (int(cx), int(y_nariz_base + (y_asas - y_nariz_base) * 0.45))
        pygame.draw.circle(tela, verde, centro_cockpit, raio_cockpit)
        pygame.draw.circle(tela, branco, centro_cockpit, raio_cockpit, 1)

        # detalhe vermelho
        pygame.draw.polygon(tela, vermelho, [
            (cx, y_asas + alt * 0.02),
            (cx - larg * 0.04, y_asas + alt * 0.09),
            (cx + larg * 0.04, y_asas + alt * 0.09),
        ])

        # motores
        motor_largura = larg * 0.10
        motor_altura = alt * 0.08
        pygame.draw.rect(
            tela, preto_nave,
            (int(cx - larg * 0.08), int(y_corpo_base), int(motor_largura), int(motor_altura))
        )
        pygame.draw.rect(
            tela, preto_nave,
            (int(cx + larg* 0.08), int(y_corpo_base), int(motor_largura), int(motor_altura))
        )

        # chamas do propulsor
        pygame.draw.polygon(tela, vermelho, [
            (cx - larg * 0.18, y_corpo_base + motor_altura),
            (cx - larg * 0.23, y_motor),
            (cx - larg * 0.08, y_corpo_base + motor_altura),
        ])
        pygame.draw.polygon(tela, vermelho, [
            (cx + larg * 0.18, y_corpo_base + motor_altura),
            (cx + larg * 0.23, y_motor),
            (cx + larg * 0.08, y_corpo_base + motor_altura),    
        ])
        pygame.draw.polygon(tela, vermelho, [
            (cx - larg * 0.15, y_corpo_base + motor_altura),
            (cx - larg * 0.18, y_motor),
            (cx - larg * 0.10, y_corpo_base + motor_altura),
        ])
        pygame.draw.polygon(tela, vermelho, [
            (cx + larg * 0.15, y_corpo_base + motor_altura),
            (cx + larg * 0.18, y_motor),
            (cx + larg * 0.10, y_corpo_base + motor_altura),    
        ])

class Projetil:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 5
        self.velocidade = 8

    def mover(self):
        self.y -= self.velocidade
        
    def desenhar(self, tela):
        pygame.draw.circle(tela, amarelo, (self.x, self.y), self.raio)

class LetraFlutuante:
    def __init__(self, letras_restantes, chance_letra_certa, multiplicador_velocidade, ):
        # sorteia uma letra qualquer do alfabeto
        if random.random() < chance_letra_certa and letras_restantes: 
            self.caractere = letras_restantes[0]
        else:
            self.caractere = chr(random.randint(65, 90)) # A-Z 

        self.x = random.randint(50, largura - 50) 
        self.y = random.randint(-100, -40)
        self.velocidade = random.uniform(1.5, 3.5) * multiplicador_velocidade
        self.tamanho = 40

        # estados de feedback: "normal", "correto", "incorreto"
        self.estado = "normal"
        self.cronometro_estado = 0

    def mover(self):
        if self.estado == "normal":
            self.y += self.velocidade
        else:
            self.cronometro_estado -= 1 # trava a letra por alguns frames

    def desenhar(self, tela):
        texto = fonte_media.render(self.caractere, True, branco)

        # define a cor do relevo com base no estado
        if self.estado == "correto":
            cor_relevo = verde
            espesura_relevo = 5
        elif self.estado == "incorreto":
            cor_relevo = vermelho
            espesura_relevo = 5
        else:
            cor_relevo = cinza
            espesura_relevo = 2

        # efeito de relevo (borda/sombra expandida)
        for dx in [-espesura_relevo, espesura_relevo]:
            for dy in [-espesura_relevo, espesura_relevo]:
                tela.blit(fonte_media.render(self.caractere, True, cor_relevo), (self.x + dx, self.y + dy))

        # texto principal
        tela.blit(texto, (self.x, self.y))

    def obter_retangulo(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)