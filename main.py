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
fonte_media = pygame.font.SysFont("Arial", 32, bold=True) # Corrected: defined fonte_media

# efeitos sonoros
def gerar_som(tipo):
    """Gera um som de acerto (agudo) ou erro (grave)"""
    frequencia = 880 if tipo == "acerto" else 220
    duracao = 0.1 if tipo == "acerto" else 0.3
    amostragem = 44100
    num_amostras = int(duracao * amostragem) # Corrected: init changed to int

    buffer = bytearray()
    for i in range(num_amostras):
        t = i / amostragem
        # onda quadrada básica
        valor = 127 if math.sin(2 * math.pi * frequencia * t) > 0 else -128
        buffer.append(valor & 0xFF)

    som = pygame.mixer.Sound(buffer=bytes(buffer))
    som.set_volume(0.2)
    return som

som_acerto = gerar_som("acerto")
som_erro = gerar_som("erro")

# lógica da frase
frase_alvo = "A BOLA E AZUL"
letras_restantes = [c for c in frase_alvo if c != " "]
letras_acertadas = []

# classes do jogo
class Nave:
    def __init__(self):
        self.largura = 50
        self.altura = 40
        self.x = largura // 2 - self.largura // 2
        self.y = altura - 70
        self.velocidade = 7

    def mover(self, teclas):
        if teclas[pygame.K_left] and self.x > 0: # Corrected: added . to self.x
            self.x -= self.velocidade
        if teclas[pygame.K_right] and self.x < largura - self.largura:
            self.x += self.velocidade

    def desenhar(self):
        # desenha a nave como um foguete
        pontos = [
            (self.x + self.largura // 2, self.y),
            (self.x, self.y + self.altura),
            (self.x + self.largura, self.y + self.altura)
        ]
        pygame.draw.polygon(tela, azul, pontos)
        pygame.draw.polygon(tela, branco, pontos, 2)

class Projetil:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = 5
        self.velocidade = 8

    def mover(self):
        self.y -= self.velocidade
        
    def desenhar(self):
        pygame.draw.circle(tela, amarelo, (self.x, self.y), self.raio)

class LetraFlutuante:
    def __init__(self):
        # sorteia uma letra qualquer do alfabeto
        if random.random() < 0.4 and letras_restantes: # Corrected: letras_restates changed to letras_restantes
            self.caractere = letras_restantes[0]
        else:
            self.caractere = chr(random.randint(65, 90)) # A-Z # Corrected: randit changed to randint

        self.x = random.randint(50, largura - 50) # Corrected: randit changed to randint
        self.y = random.randint(-100, -40) # Corrected: randit changed to randint
        self.velocidade = random.uniform(1.5, 3.5)
        self.tamanho = 40

        # estados de feedback: "normal", "correto", "incorreto"
        self.estado = "normal"
        self.cronometro_estado = 0

    def mover(self):
        if self.estado == "normal":
            self.y += self.velocidade
        else:
            self.cronometro_estado -= 1 # trava a letra por alguns frames

    def desenhar(self):
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

        # texti orubcuoak oir cuna
        tela.blit(texto, (self.x, self.y))

    def obter_retangulo(self):
        return pygame.Rect(self.x, self.y, self.tamanho, self.tamanho)

# inicialização dos objetos
nave = Nave()
projeteis = []
letras = []
tempo_spawn = 0

# loop principal do jogo
jogando = True
while jogando:
    tela.fill(preto)
    teclas = pygame.key.get_pressed()

    # eventos
    for evento in pygame.event.get(): # Corrected: pygame.get_event_loop() changed to pygame.event.get()
        if evento.type == pygame.QUIT: # Corrected: pygame.quit changed to pygame.QUIT
            jogando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_space and len(letras_restantes) > 0:
                # dispara o projétil a partir do bico da nave
                projeteis.append(Projetil(nave.x + nave.largura // 2, nave.y))

    # atualização de lógica (caso o jogo não tenha acabado)
    if letras_restantes:
        nave.mover(teclas)

        # criar novas letras na tela periodicamente
        tempo_spawn += 1
        if tempo_spawn > 45:
            letras.append(LetraFlutuante())
            tempo_spawn = 0

        # movimentação dos projéteis
        for p in projeteis[:]:
            p.mover()
            if p.y < 0:
                projeteis.remove(p)

        # movimentação e limpeza das letras
        for l in letras[:]:
            l.mover()
            # remove letras que saíram da tela ou cujo tempo de feedback acabou
            if l.y > altura:
                letras.remove(l)
            elif l.estado != "normal" and l.cronometro_estado <= 0:
                letras.remove(l)

        # sistema de colisão e validação
        for p in projeteis[:]:
            for l in letras[:]:
                if l.estado == "normal" and l.obter_retangulo().collidepoint(p.x, p.y):
                    # remove o projeto que colidiu
                    if p in projeteis: projeteis.remove(p)

                    # valida se é a letra correta que o aluno precisava acertar
                    if l.caractere == letras_restantes[0]:
                        l.estado = "correto"
                        l.cronometro_estado = 20 # exibe por 20 frames
                        som_acerto.play()
                        letras_acertadas.append(letras_restantes.pop(0))
                    else:
                        l.estado = "incorreto"
                        l.cronometro_estado = 20
                        som_erro.play()

    # renderização / desenhos
    # 1- desenha frase alvo (central superior)
    # monta a string visual mostrando o progresso do aluno (ex: "A B_ _ _")
    string_progresso = ""
    indice_letras_acertadas = 0

    for caractere in frase_alvo:
        if caractere == " ":
            string_progresso += "  "
        elif indice_letras_acertadas < len(letras_acertadas) and caractere == letras_acertadas[indice_letras_acertadas]:
            string_progresso += caractere + " "
            indice_letras_acertadas += 1
        else:
            string_progresso += "_ "

    texto_frase = fonte_gigante.render(string_progresso, True, amarelo)
    rect_frase = texto_frase.get_rect(center=(largura // 2, 50))
    tela.blit(texto_frase, rect_frase)

    # 2- desenha elementos do jogo
    for l in letras: l.desenhar()
    for p in projeteis: p.desenhar()
    nave.desenhar()

    # 3- tela de vitória
    if not letras_restantes:
        texto_vitoria = fonte_gigante.render("PARABÉNS! VOCÊ CONSEGUIU!", True, verde)
        rect_vitoria = texto_vitoria.get_rect(center=(largura //2, altura // 2))
        tela.blit(texto_vitoria, rect_vitoria)

    # atualiza a tela
    pygame.display.flip()
    relogio.tick(60) # mantém o jogo a 60fps

pygame.quit()