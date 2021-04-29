import pygame
import numpy as np
from utils import colors
from classes.Peca import Peca
import random
import copy

class Tabuleiro:
	def __init__(self, SCREEN):
		self.SCREEN = SCREEN
		self.quadradinhos = {}
		self.QTD_QUADRADOS_ALTURA = 18
		self.QTD_QUADRADOS_LARGURA = 10

		self.pecas = []					# Lista de instâncias de Pecas()
		#self.novasPecas = self.iniciarPecas()

		self.desenharLinhasTabuleiro()
		self.pecaDescendo = None		# Instancia de Peca()

		self.pontos = 0	# Cada linha que desaparecer, +1 ponto

		self.pecaMantida = None
		self.contMovimento = 0


	def desenharLinhasTabuleiro(self):

		for i in range(self.QTD_QUADRADOS_ALTURA+1):
			pygame.draw.line(self.SCREEN, colors.GRAY, (0, i*50), (500, i*50), 1)

		for i in range(self.QTD_QUADRADOS_LARGURA+1):
			pygame.draw.line(self.SCREEN, colors.GRAY, (i*50, 0), (i*50, 900), 1)			

	def movePecaAtivaEsquerda(self):
		novaPos = []
		pecaSaiuDoTabuleiro = False
		
		for pos in self.pecaDescendo.posicoes:
			if pos[0] == 0:
				#print("Limite do cenário")
				return False

			# Verifica se não há outra peça do lado que impede o movimento
			for peca in self.pecas:
				for pos2 in peca.posicoes:
					if pos[0] == pos2[0]+1 and pos[1] == pos2[1]:
						return False				

			novaPos.append([pos[0]-1, pos[1]])

		# Atualiza nova posição somente se houver espaço para a peça se mover 
		self.pecaDescendo.posicoes = novaPos		
		return True

	def movePecaAtivaDireita(self):
		novaPos = []
		pecaSaiuDoTabuleiro = False
		
		for pos in self.pecaDescendo.posicoes:
			if pos[0] == self.QTD_QUADRADOS_LARGURA-1:
				#print("Limite do cenário")
				return False

			# Verifica se não há outra peça do lado que impede o movimento
			for peca in self.pecas:
				for pos2 in peca.posicoes:
					if pos[0] == pos2[0]-1 and pos[1] == pos2[1]:
						return False

			novaPos.append([pos[0]+1, pos[1]])

		# Atualiza nova posição somente se houver espaço para a peça se mover 
		self.pecaDescendo.posicoes = novaPos
		return True


	# Verifica se a peça rotacionaa não vai colidir com outras peças ao lado
	def verificaColisaoPeca(self, novaPosicao):
		for pos1 in novaPosicao:
			for peca in self.pecas:
				for pos2 in peca.posicoes:
					if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
						return True

		return False



	def rotacionaPecaAtiva(self):

		anguloAntigo = self.pecaDescendo.angulo
		posicaoAntiga = copy.deepcopy(self.pecaDescendo.posicoes)

		self.pecaDescendo.rotate()
		self.pecaDescendo.verificaColisaoParede()	
		
		colidiu = self.verificaColisaoPeca(self.pecaDescendo.posicoes)		

		# Se a peça colide com outra, retorna a posição anterior, neutralizando a correção
		if colidiu:
			
			self.pecaDescendo.posicoes = posicaoAntiga
			self.pecaDescendo.angulo = anguloAntigo


	# Verifica se uma peça que está descendo toca a borda inferior da tela ou toca uma outra
	# peça que já está estacionada no tabuleiro. Se isso acontecer, congela essa peça e cria uma
	# outra que irá começar a descer
	def verificaToquePeca(self):

		for pos in self.pecaDescendo.posicoes:
			if pos[1] == self.QTD_QUADRADOS_ALTURA-1:
				return True

			for index, peca in enumerate(self.pecas):
				for posPeca in peca.posicoes:	
					if pos[1] == posPeca[1]-1 and pos[0] == posPeca[0]:
						return True		


		return False


	# Apaga a linha de quadradinhos atual e copia a linha de cima
	def moverQuadradinhos(self, mat, matIndex):

		# Apaga a linha completa
		for iPeca, peca in enumerate(mat[matIndex, :]):
			if peca is not None:
				for iPos, pos in enumerate(peca.posicoes):
					if pos[1] == matIndex: #or pos[1] == 0:
						del peca.posicoes[iPos]
				mat[matIndex, iPeca] = 0

		for peca in mat[matIndex-1, :]:
			if peca is not None:
				for iPos, pos in enumerate(peca.posicoes):
					if pos[1] == matIndex-1: #or pos[1] == 0:
						peca.posicoes[iPos][1] += 1


	# Percorre todas as linhas, verifica quais precisam ser eliminadas e passa todas as linhas
	# de cima para baixo
	def apagarLinhaMaisAbaixo(self, mat):
		for i in reversed(range(self.QTD_QUADRADOS_ALTURA)):
			while None not in mat[i, :] and 0 not in mat[i, :]:
				# Aqui temos que apagar a linha i e mover uma posição abaixo todos os quadradinhos que exitrm acima

				for j in reversed(range(1, i+1)):
					#if i > 0:
					self.moverQuadradinhos(mat, j)
					mat[j, :] = mat[j-1, :]
				self.pontos += 1


	def verificaExplosaoDaLinha(self):

		mat = np.empty((self.QTD_QUADRADOS_ALTURA, self.QTD_QUADRADOS_LARGURA), dtype=Peca)

		# Preencho a matriz mat com a referência dos objetos das peças
		for peca in self.pecas:
			for pos in peca.posicoes:
				mat[pos[1], pos[0]] = peca

		#if None not in mat[self.QTD_QUADRADOS_ALTURA-1, :]:
		self.apagarLinhaMaisAbaixo(mat)


	# Se, ao surgir uma peça lá em cima, já tenha outra peça em seu espaço, quer dizer que o cara perdeu
	def verificaGameOver(self):
		
		for pos1 in self.pecaDescendo.posicoes:
			for pecas in self.pecas:
				for pos2 in pecas.posicoes:
					if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
						print("Game Over")
						exit()



	def escolheNovaPecaAleatoria(self):
		return random.choice(["jorge", "luiz", "maria", "josi", "zigomar", "zanir", "zeraldo"])

	# Retorna TRUE se a peça encostou em algum lugar
	# Retorna FALSE se a peça continua descendo
	def movimentaPecasBaixo(self, bruteForce = False):

		algumaParteEncostou = False
		self.contMovimento += 1
		if self.verificaToquePeca():
			# Se estivermos buscando o custo mínimo na árvore, vamos voltar aqui
			if bruteForce == True:
				return True
				
			self.pecas.append(copy.deepcopy(self.pecaDescendo))
			self.inserirNovaPeca(self.escolheNovaPecaAleatoria())
			self.verificaGameOver()
			algumaParteEncostou = True
			return True

		else:
			#quantasVezesPecaDesceu = 0	# GameOver se ela encostar em algo quando essa var é 0
			
			for index, pos in enumerate(self.pecaDescendo.posicoes):

				self.pecaDescendo.posicoes[index][1] += 1

			return False


	# Escolhe um tipo de peça e cria uma nova instância
	def inserirNovaPeca(self, tipo):
		vet = {}
		peca = Peca(tipo)
		self.contMovimento = 0

		#self.pecas.append(peca)
		self.pecaDescendo = peca


	def desenha(self):

		#self.desenharLinhasTabuleiro()

		for index, peca in enumerate(self.pecas):
			peca.desenha(self.SCREEN)


		self.pecaDescendo.desenha(self.SCREEN)


	

	def update(self):
		# Movimenta as peças para baixo
		self.contMovimento += 1
		tocouEmBaixo = self.movimentaPecasBaixo()
		self.verificaExplosaoDaLinha()
		return tocouEmBaixo
