import numpy as np
import signal
import pygame
import os
from classes.Tabuleiro import Tabuleiro
from classes.Cerebro import Cerebro
import sys
import time
from utils import colors, posicoes
import random

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_d,
    K_s,
    K_a,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)


# globais
TEMPO_ENTRE_CADA_MOVIMENTO = 0.002 #segundos
pygame.init()
SCREEN = 0
BG = 0
ROBO = 0
GAME_AREA = 0
METADATA = 0
METADATA_SPACE1 = 0
METADATA_SPACE2 = 0

METADATA_SPACE1_WIDTH = 350
METADATA_SPACE2_WIDTH = 400
GAME_AREA_WIDTH = 500


WIDTH = 1600
HEIGHT = 900

#ARCHITECTURE = [2, 1]
#NUM_INDIVIDUOS = 16
#MUTATION_PROBABILITY = 10
#NUM_PARTIDAS_POR_INDIVIDUO = 20


def iniciarTela():
	global SCREEN, BG, GAME_AREA, METADATA, ROBO, METADATA_SPACE1, METADATA_SPACE2
	SCREEN = pygame.display.set_mode([WIDTH, HEIGHT], pygame.NOFRAME) #pygame.FULLSCREEN)
	SCREEN.fill(colors.CINZA2)
	METADATA_SPACE1 = pygame.Surface([METADATA_SPACE1_WIDTH, HEIGHT])
	METADATA_SPACE1.fill(colors.CINZA2)
	METADATA_SPACE2 = pygame.Surface([METADATA_SPACE2_WIDTH, HEIGHT])
	METADATA_SPACE2.fill(colors.CINZA2)
	
	#ROBO = pygame.image.load("images/robo.png")
	GAME_AREA = pygame.Surface((GAME_AREA_WIDTH, HEIGHT))
	#GAME_AREA.blit(BG, (METADATA_SPACE, 0))
	#GAME_AREA.blit(ROBO, (0, 0))
	GAME_AREA.fill(colors.CINZA1)
	#GAME_AREA.set_colorkey((0, 255, 0))	# Chroma Key, deleta todas as cores VERDES nesta camada

	SCREEN.blit(GAME_AREA, (550, 0))
	SCREEN.blit(METADATA_SPACE1, (800-250-200-50, 0))
	SCREEN.blit(METADATA_SPACE2, (800+250, 0))


	#SCREEN.blit(BG, (METADATA_SPACE, 0))
	pygame.display.flip()

	# Menu superior dos pontos
	METADATA = pygame.Surface((WIDTH, 0))
	METADATA.fill((255, 255, 255))
	SCREEN.blit(METADATA, (0,0))

def readKeys():

	key_pressed = []
	# As teclas pressionadas são armazenadas em uma pilha no módulo Pygame
	for event in pygame.event.get():
		# O usuário clicou em fechar a janela? Enão para o looping.
		if event.type == QUIT:
			return False	
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_d:
				key_pressed.append("D")
			if event.key == pygame.K_s:
				key_pressed.append("S")
			if event.key == pygame.K_a:
				key_pressed.append("A")
			if event.key == pygame.K_w:
				key_pressed.append("W")		
			if event.key == pygame.K_SPACE:
				key_pressed.append("SPACE")

	return key_pressed

def desenhaTituloMetadata():
	global METADATA_SPACE2
	# if you want to use this module.
	myfont = pygame.font.SysFont('Comic Sans MS', 50)
	textsurface = myfont.render("PRÓXIMAS PEÇAS", False, colors.WHITE)
	METADATA_SPACE2.blit(textsurface, (30,20))

def desenhaTituloMetadata1(tabuleiro, pecaMantida):
	global METADATA_SPACE1


	#desenhaProximasPecas([pecaMantida], METADATA_SPACE1, rank=0, distY = 130)


	# if you want to use this module.
	myfont = pygame.font.SysFont('Comic Sans MS', 50)
	textsurface1 = myfont.render("PONTOS", False, colors.WHITE)
	textsurface2 = myfont.render(str(tabuleiro.pontos), False, colors.WHITE)
	#textsurface3 = myfont.render("AUXILIAR", False, colors.WHITE)

	METADATA_SPACE1.blit(textsurface1, (90,20))	
	METADATA_SPACE1.blit(textsurface2, (160,60))
	#METADATA_SPACE1.blit(textsurface3, (90,130))	


# !!! PUSH ctr c IF THINGS GOING WRONG !!!
def panic_button(sig, frame):
    print('falous')
    sys.exit(0)			

def tempoMinimo(tempo):
	if tempo + TEMPO_ENTRE_CADA_MOVIMENTO < time.time():
		return True
	return False

def afterRunning():
	pygame.quit()

def updateInstantaneo(tabuleiro, keyPressed):

	# Faz o update dos players, levando em consideração os comandos do usuário
	if keyPressed != -1:
		for key in keyPressed:	

			if key == "D":
				tabuleiro.movePecaAtivaDireita()
			if key == "S":
				tabuleiro.movimentaPecasBaixo()
			if key == "A":
				tabuleiro.movePecaAtivaEsquerda()
			if key == "W":
				tabuleiro.rotacionaPecaAtiva()		
			if key == "SPACE":
				tabuleiro.trocaPecaMantida()

def executarComandosDaIA(tabuleiro, melhor_caminho):

	if len(melhor_caminho) > 0:
		if melhor_caminho[0] == "direita":
			tabuleiro.movePecaAtivaDireita()

		if melhor_caminho[0] == "esquerda":
			tabuleiro.movePecaAtivaEsquerda()

		if melhor_caminho[0] == "centro":
			tabuleiro.rotacionaPecaAtiva()
			
		del melhor_caminho[0]	


def update(tabuleiro, keyPressed):

	# Retorna se a tecla tocou em baixo, ou seja, se uma nova peça foi gerada
	return tabuleiro.update()


def desenhaProximasPecas(filaPecas, surface, rank = 1, distY = None):

	peca = filaPecas[rank]

	rank *= 200
	rank += 50

	# GAMBIARRA para definir a posição Y do quadrado esquerdo manualmente
	if distY is not None:
		rank = distY
	
	
	pygame.draw.rect(surface, colors.WHITE, (48,48+rank,264,154))
	pygame.draw.rect(surface, colors.CINZA1, (50,50+rank,260,150))

	if peca == "luiz":
		
		for pos in posicoes.LUIZ:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-45, pos[1]*50+120+rank, 50, 50))
			pygame.draw.rect(surface, colors.AZUL_CLARO, (pos[0]*50+2-45, pos[1]*50+2+120+rank, 46, 45))		

	if peca == "jorge":
		
		for pos in posicoes.JORGE:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-70, pos[1]*50+100+rank, 50, 50))	
			pygame.draw.rect(surface, colors.YELLOW, (pos[0]*50+2-70, pos[1]*50+2+100+rank, 46, 45))		

	if peca == "maria":
		
		for pos in posicoes.MARIA:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-45, pos[1]*50+120+rank, 50, 50))	
			pygame.draw.rect(surface, colors.ROXO, (pos[0]*50+2-45, pos[1]*50+2+120+rank, 46, 45))		

	if peca == "josi":
		
		for pos in posicoes.JOSI:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-40, pos[1]*50+120+rank, 50, 50))	
			pygame.draw.rect(surface, colors.CHROME_KEY, (pos[0]*50+2-40, pos[1]*50+2+120+rank, 46, 45))		

	if peca == "zigomar":
		
		for pos in posicoes.ZIGOMAR:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-40, pos[1]*50+70+rank, 50, 50))	
			pygame.draw.rect(surface, colors.PINK, (pos[0]*50+2-40, pos[1]*50+2+70+rank, 46, 45))		

	if peca == "zanir":
		
		for pos in posicoes.ZANIR:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-40, pos[1]*50+70+rank, 50, 50))	
			pygame.draw.rect(surface, colors.LARANJA, (pos[0]*50+2-40, pos[1]*50+2+70+rank, 46, 45))		

	if peca == "zeraldo":
		
		for pos in posicoes.ZERALDO:
			pygame.draw.rect(surface, colors.BLACK, (pos[0]*50-40, pos[1]*50+70+rank, 50, 50))	
			pygame.draw.rect(surface, colors.AZUL_FLAT, (pos[0]*50+2-40, pos[1]*50+2+70+rank, 46, 45))					

def obtemNovaPeca(filaPeca, tabuleiro):
	#return "jorge"
	peca = filaPeca[0]
	del filaPeca[0]
	filaPeca.append(tabuleiro.escolheNovaPecaAleatoria())

	return peca

def desenha(tabuleiro):
	tabuleiro.desenha()

def main(interface):

	iniciarTela()

	#random.seed(123456)
	print("Semente, semente, semente, semente.. se não mente diga a verdade")
	print(random.seed)

	abaixandoPeca = 0
	tempo = 0
	filaPeca = []	# Sequencia de peças que irá aparecer na lateral da tela do jogo

	tabuleiro = Tabuleiro(GAME_AREA)

	# Inicia com 3 peças aleatórias
	filaPeca.append(tabuleiro.escolheNovaPecaAleatoria())
	filaPeca.append(tabuleiro.escolheNovaPecaAleatoria())
	filaPeca.append(tabuleiro.escolheNovaPecaAleatoria())

	
	novaPeca = obtemNovaPeca(filaPeca, tabuleiro)
	pecaMantida = tabuleiro.escolheNovaPecaAleatoria()
	
	
	#tabuleiro.pecaMantida = novaPeca2	# Feature do TETRIS. O jogador pode trocar a peça atual por esta (a qualquer momento)

	#tabuleiro.inserirNovaPeca("jorge")

	melhor_caminho = None
	cerebro = Cerebro(tabuleiro)
	#cerebro.transladatObjeto()

	# Calcula o Score para a peça original
	tabuleiro.inserirNovaPeca(novaPeca)
	cerebro.transladatObjeto()
	melhor_caminho1, score1 = cerebro.forcaBruta()

	cerebro.resetarArgumentos()
	# Calcula o score para a peça mantida
	tabuleiro.inserirNovaPeca(pecaMantida)
	cerebro.transladatObjeto()
	melhor_caminho2, score2 = cerebro.forcaBruta()	

	# Verifica se troca a peça original para mantida
	cerebro.resetarArgumentos()
	if score1 < score2:
		tabuleiro.inserirNovaPeca(novaPeca)
		melhor_caminho = melhor_caminho1
	else:
		tabuleiro.inserirNovaPeca(pecaMantida)
		melhor_caminho = melhor_caminho2
		
		# Troca
		aux = novaPeca
		novaPeca = pecaMantida
		pecaMantida = aux		
		
		
	#cerebro.transladatObjeto()

	#exit()
	#tabuleiro.inserirNovaPeca("josi")


	running = True
	cont = 0
	while running:

		keyPressed = readKeys()	# Verifica se o usuário pressionou alguma tecla
		if keyPressed == False:
			running = False		

		# atualizaões nas peças que não requerem intervalo de tempo
		updateInstantaneo(tabuleiro, keyPressed)

		if tempoMinimo(tempo):

			if abaixandoPeca is None:
				executarComandosDaIA(tabuleiro, melhor_caminho)
				tocouEmBaixo = update(tabuleiro, keyPressed)
				if tocouEmBaixo:				
					melhor_caminho = None
					score = 0
					novaPeca = obtemNovaPeca(filaPeca, tabuleiro)
					tabuleiro.inserirNovaPeca(novaPeca)
					cerebro.transladatObjeto()

					# Calcula o melhor caminho para a nova peça gerada
					melhor_caminho1, score1 = cerebro.forcaBruta()

					cerebro.resetarArgumentos()
					# Calcula o score para a peça mantida
					tabuleiro.inserirNovaPeca(pecaMantida)
					cerebro.transladatObjeto()
					melhor_caminho2, score2 = cerebro.forcaBruta()	

					cerebro.resetarArgumentos()
					# Verifica se troca a peça original para mantida
					if score1 < score2:
						tabuleiro.inserirNovaPeca(novaPeca)
						melhor_caminho = melhor_caminho1
					else:
						tabuleiro.inserirNovaPeca(pecaMantida)
						melhor_caminho = melhor_caminho2
						
						# Troca
						aux = novaPeca
						novaPeca = pecaMantida
						pecaMantida = aux	
					
					print("Score")
					print(score)
					#print("Todos os caminhos")
					#print(cerebro.listaCaminhos)
					#print(cerebro.listaScores)
					print("Melhor caminho: ")
					print(cerebro.melhorCaminho)
					print("Score melhor caminho: ")
					print(cerebro.scoreMelhorCaminho)
					#print("Qtd de quadrados vazios ")
					#print(cerebro.menor)				
					#print("Quadrado mais alto ")
					#print(cerebro.qtdQuadrados)		
					#print("xCoords")						
					#print(cerebro.xCoords)
					#print("\n")
					
					

					#tabuleiro.inserirNovaPeca(novaPeca)
					#cerebro.transladatObjeto()
					
					abaixandoPeca = 0
			else:
				chegou = cerebro.transladaObjetoGrafico(abaixandoPeca)				
				if chegou:
					abaixandoPeca = None
				else:
					abaixandoPeca += 1

			tempo = time.time()

		desenha(tabuleiro)
		if interface == True:



			SCREEN.fill(colors.CINZA2)
			SCREEN.blit(GAME_AREA, (550, 0))


			METADATA_SPACE1.fill(colors.CINZA2)
			METADATA_SPACE2.fill(colors.CINZA2)

			desenhaTituloMetadata()
			desenhaTituloMetadata1(tabuleiro, pecaMantida)
			desenhaProximasPecas(filaPeca, METADATA_SPACE2, rank = 0)
			desenhaProximasPecas(filaPeca, METADATA_SPACE2, rank = 1)
			desenhaProximasPecas(filaPeca, METADATA_SPACE2, rank = 2)

			SCREEN.blit(METADATA_SPACE1, (800-250-200-150, 0))
			SCREEN.blit(METADATA_SPACE2, (800+250, 0))

			GAME_AREA.fill(colors.CINZA1)
			#SCREEN.blit(METADATA, (0,0))
			pygame.image.save(SCREEN, "frames/"+str(cont)+".png")
			cont += 1
			pygame.display.update()

			METADATA.fill((242, 251, 255))
			SCREEN.blit(METADATA, (0,0))	



	afterRunning()


if __name__ == '__main__':
	signal.signal(signal.SIGINT, panic_button)

	# Allow interface?
	interface = True
	main(interface)
