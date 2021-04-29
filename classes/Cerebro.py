import numpy as np
from anytree import Node, RenderTree, AnyNode
import copy
import time
import sys
from classes.Peca import Peca

class Cerebro:
	def __init__(self, tabuleiro):
		self.listaDeMovimentos = ["esquerda", "direita", "rotacionar"]
		self.tabuleiro = tabuleiro
		
		self.caminho = []

		self.melhorCaminho = []
		self.scoreMelhorCaminho = 99999 #-1 # Quanto maior, melhor

		self.aux = 0

		self.menor = 0
		self.qtdQuadrados = 0

		self.alturaArvore = 7 # Altura da árvore

		self.mat = np.zeros((self.tabuleiro.QTD_QUADRADOS_ALTURA, self.tabuleiro.QTD_QUADRADOS_LARGURA))
		self.linha = np.zeros(self.tabuleiro.QTD_QUADRADOS_LARGURA)
		#self.transladatObjeto()
		#self.criarArvoreInicial()

		self.listaScores = []
		self.listaCaminhos = []
		self.xCoords = []

		self.noiz = 10

	def resetarArgumentos(self):
		self.scoreMelhorCaminho = 99999
		self.melhorCaminho = []
		self.menor = 0
		self.qtdQuadrados = 0
		self.caminho = []
		self.listaScores = []
		self.listaCaminhos = []
		self.xCoords = []

	# Verifica qual a posição do quadrado mais alto no tabuleiro
	def pecaMaisAlta(self):
		menor = 9999

		if len(self.tabuleiro.pecas) == 0:
			menor = 17
		else:
			for pecas in self.tabuleiro.pecas:
				for pos in pecas.posicoes:
					if pos[1] < menor:
						menor = pos[1]		
		return menor


	# A árvore de decisão começa apenas 6 quadrados acima do quadrado mais alto. 
	# Entretanto, precisamos simular o objeto descendo até o ponto de partida de árvore
	def transladaObjetoGrafico(self, cont):
		menor = self.pecaMaisAlta()		

		transladado = menor-self.alturaArvore
		if transladado <= 0:
			return True


		for iPos, pos in enumerate(self.tabuleiro.pecaDescendo.posicoes):
			self.tabuleiro.pecaDescendo.posicoes[iPos][1] += 1

		return cont == transladado-1
		# Quando transladado for 0, quer dizer que a peça chegou a seu destino ;)
		#return transladado

	# Translada oobjeto para 6 segmentos antes do último ponto mais alto
	def transladatObjeto(self):
		# Quanto mais alto, mais próximo de 0 as corrdenadas do objeto estarão. Então
		# temos que encontrar a MENOR coordenada

		menor = self.pecaMaisAlta()

		transladado = menor-self.alturaArvore
		if transladado < 0:
			transladado = 0

		# A coordenada menor possui o quadradinho mais alto na tela
		for iPos, pos in enumerate(self.tabuleiro.pecaDescendo.posicoes):
			self.tabuleiro.pecaDescendo.posicoes[iPos][1] = self.tabuleiro.pecaDescendo.posicoes[iPos][1] + transladado
			#self.tabuleiro.pecaDescendo.posicoes[iPos][1] = (menor - 6)

	def criarArvoreInicial(self):
		noInicial = AnyNode(id="inicial", custo = 0)
		esquerda = AnyNode(id="esquerda", parent = noInicial, custo = 0)
		rotaciona = AnyNode(id="rotaciona", parent = noInicial, custo = 0)
		direita = AnyNode(id="direita", parent = noInicial, custo = 0)


	def forcaBruta(self):
		
		melhorScore = 0
		melhorCaminho = []	# Vai ser uma pilha para armazenar os caminhos da árvore

		# Enquanto a peça não encostar em algum lugar
		#while not tabuleiro.movimentaPecasBaixo()

		"""
		Ordem do percurso: Esquerda, Centro (Roaciona), Direita
		Busca por profundidade
				  Início
				   /|\
				  / | \
		      Esq. Rot. Dir. 
		"""
		self.recursao("")
		return [self.melhorCaminho, self.scoreMelhorCaminho]

	def recursao(self, movimento):
		#print("entrou na recursão")
		#self.tabuleiro.desenha()

		#if self.noiz == 10:
		#	return
		#else:
			#self

		deuEsquerda = True
		deuDireita = True
		if movimento == "esquerda":
			#print("Movendo para a esquerda")
			deuEsquerda = self.tabuleiro.movePecaAtivaEsquerda()
			self.caminho.append("esquerda")

		elif movimento == "rotaciona":
			#print("Rotacionando")
			self.tabuleiro.rotacionaPecaAtiva()
			self.caminho.append("centro")

		elif movimento == "direita":
			#print("Movendo para a direita")
			deuDireita = self.tabuleiro.movePecaAtivaDireita()
			self.caminho.append("direita")

		#print(oi)
		if not self.tabuleiro.movimentaPecasBaixo(bruteForce = True):
			#print("oi")


			#if deuEsquerda:
			self.recursao("esquerda")
			self.novaTentativa()

			self.recursao("rotaciona")
			self.novaTentativa()

			#if deuDireita:
			self.recursao("direita")
			self.novaTentativa()
		else:
			#print("Bateu embaixo")
			#score, qtd, maisAlto, xCoords = self.calculaScore3()
			score, buracosGlobais, quadradoMaisBaixo = self.calculaScore3()


			self.listaScores.append(score)
			self.listaCaminhos.append(copy.deepcopy(self.caminho))

			if score < self.scoreMelhorCaminho:
				self.melhorCaminho = copy.deepcopy(self.caminho)
				self.scoreMelhorCaminho = score

				#self.menor = qtd
				#self.qtdQuadrados = maisAlto				
				#self.xCoords = xCoords

	def novaTentativa(self):
		# Desempilha o movimento mais recente da pilha de movimentos
		self.caminho.pop()

		# Cria nova peça e coloca ela no início
		self.tabuleiro.inserirNovaPeca(self.tabuleiro.pecaDescendo.tipo)
		self.transladatObjeto()

		# Refaz todo o caminho até agora (lembre-se que nós tiramos o último movimento no início dessa função)
		self.sequenciaMovimento()


	def sequenciaMovimento(self):
		for movimento in self.caminho:
			if movimento == "esquerda":
				self.tabuleiro.movePecaAtivaEsquerda()	
			elif movimento == "centro":	# Rotaciona
				self.tabuleiro.rotacionaPecaAtiva()			
			elif movimento == "direita":
				self.tabuleiro.movePecaAtivaDireita()	
			self.tabuleiro.movimentaPecasBaixo(bruteForce = True)						


	def verificaSeCoordenadaExiste(self, lista, num):

		for coord in lista:
			if coord[0] == num:
				return True
		return False

	def calculaLinhasQueIraoExplodir(self):
		qtdLinhaExplidir = 0
		for i in reversed(range(self.tabuleiro.QTD_QUADRADOS_ALTURA)):
			if None not in self.mat[i, :] and 0 not in self.mat[i, :]:		
				qtdLinhaExplidir += 1
		return qtdLinhaExplidir

	def buracosAbertos(self):

		xCoords = []
		quadradoMaisAlto = 9999
		quadradoMaisBaixo = -1
		for pos in self.tabuleiro.pecaDescendo.posicoes:
			self.mat[pos[1], pos[0]] = -1

			if len(xCoords) == 0 or not self.verificaSeCoordenadaExiste(xCoords, pos[0]): #pos[0] not in xCoords[0,:]:	# Se existir alguma coordenada com o x valendo pos[0]
				xCoords.append(pos)
 
			if pos[1] < quadradoMaisAlto:
				quadradoMaisAlto = pos[1]

			if pos[1] > quadradoMaisBaixo:
				quadradoMaisBaixo = pos[1]

		qtd = 0	# Quantidade de quadrados vazios em baixo da peça descendo
		qtdAberto = 0
		for pos in xCoords:
			x = pos[0]
			if quadradoMaisBaixo+2 < 18:
				for y in range(pos[1], quadradoMaisBaixo+2 ):#self.tabuleiro.QTD_QUADRADOS_ALTURA):
					if self.mat[y,x] == 0:
						if x < self.tabuleiro.QTD_QUADRADOS_LARGURA-1 and x > 0 and (self.mat[y, x+1] == 0 or self.mat[y, x-1] == 0):
							qtdAberto += 1
						#else:
							#qtd += 1
						qtd += 1
					elif self.mat[y,x] == 1:
						break				

		return qtdAberto

	# Simplesmente diminui o número de quadrados global
	def calculaScore3(self):
		# Diminui a quantidade global de buracos
		# Preencho a matriz mat com a referência dos objetos das peças

		"""
		Score 106
		multiplicadorBuracosGlobais = 20
		multiplicadorAltura = 6
		multiplicadorAlturaGlobal = 1
		multiplicadorLinhasExplidir = -20 # negativo pq vai diminuir o custo (quanto menor, melhor)
		multiplicadorBuracosAbertos = 15 #-2  # negativo pq vai diminuir o custo
		
		multiplicadorBuracosGlobais = 6
		multiplicadorAltura = 6
		multiplicadorAlturaGlobal = 1
		multiplicadorLinhasExplidir = -20 # negativo pq vai diminuir o custo (quanto menor, melhor)
		multiplicadorBuracosAbertos = 5 #-2  # negativo pq vai diminuir o custo
		"""

		
		multiplicadorBuracosGlobais = 20
		multiplicadorAltura = 10
		multiplicadorAlturaGlobal = 1
		multiplicadorLinhasExplidir = -150 # negativo pq vai diminuir o custo (quanto menor, melhor)
		multiplicadorBuracosAbertos = 19 #-2  # negativo pq vai diminuir o custo
		multiplicadorDifAlturaColunas = 0
		
		self.mat.fill(0)
		#self.linha.fill(0)

		#pecasAux = copy.deepcopy(self.tabuleiro.pecas)
		#pecasAux.append(copy.deepcopy(self.tabuleiro.pecaDescendo))

		qtdTotalPecas = 0

		maisAltoGlobal = 9999
		for peca in self.tabuleiro.pecas:
			for pos in peca.posicoes:
				self.mat[pos[1], pos[0]] = 1
				qtdTotalPecas += 1

				if pos[1] < maisAltoGlobal:
					maisAltoGlobal = pos[1]

				#if pos[1] > quadradoMaisBaixo:
				#	quadradoMaisBaixo = pos[1]					

		#if maisAltoGlobal <= 7:
		#	multiplicadorAlturaGlobal = 40


		quadradoMaisBaixo = -99
		quadradoMaisAlto = 999
		for pos in self.tabuleiro.pecaDescendo.posicoes:
			self.mat[pos[1], pos[0]] = 1
			qtdTotalPecas += 1

			if pos[1] < maisAltoGlobal:
				maisAltoGlobal = pos[1]		

			if pos[1] < quadradoMaisAlto:
				quadradoMaisAlto = pos[1]					


			if pos[1] > quadradoMaisBaixo:
				quadradoMaisBaixo = pos[1]	

		pontoMedioObj = (quadradoMaisAlto + quadradoMaisBaixo) / 2

		qtdLinhasExplodir = self.calculaLinhasQueIraoExplodir()

		buracosGlobais = 0
		buracosAbertos = 0
		#linha = np.zeros(self.tabuleiro.QTD_QUADRADOS_LARGURA)
		linha = []
		for x in range(self.tabuleiro.QTD_QUADRADOS_LARGURA):
			contFlag = False

			for y in range(self.tabuleiro.QTD_QUADRADOS_ALTURA):
				
				if contFlag == False and self.mat[y,x] == 1:
					contFlag = True
					linha.append(y)

				if contFlag == True and self.mat[y,x] == 0:
					if x < self.tabuleiro.QTD_QUADRADOS_LARGURA-1 and x > 0 and (self.mat[y, x+1] == 0 or self.mat[y, x-1] == 0) : # é um buraco aberto
						buracosAbertos += 1
					else:
						buracosGlobais += 1
			if contFlag == False:
				# Se não houver qualquer peça na coluna, coloca a base na lista
				linha.append(self.tabuleiro.QTD_QUADRADOS_ALTURA-1)

		diferencaAlturaColunas = max(linha) - min(linha)

		#if diferencaAlturaColunas > 3:
		#	multiplicadorDifAlturaColunas = 15
		#	multiplicadorBuracosGlobais = 5
		#	multiplicadorBuracosAbertos = 4


		#buracosAbertos = self.buracosAbertos()

		return multiplicadorBuracosGlobais * buracosGlobais + multiplicadorAltura * (self.tabuleiro.QTD_QUADRADOS_ALTURA-1 - pontoMedioObj) + multiplicadorLinhasExplidir*qtdLinhasExplodir + multiplicadorAlturaGlobal * (self.tabuleiro.QTD_QUADRADOS_ALTURA-1 - maisAltoGlobal) + multiplicadorBuracosAbertos * buracosAbertos + multiplicadorDifAlturaColunas * diferencaAlturaColunas, buracosGlobais, quadradoMaisBaixo


	def calculaScore2(self):

		self.mat.fill(0)

		#pecasAux = copy.deepcopy(self.tabuleiro.pecas)
		#pecasAux.append(copy.deepcopy(self.tabuleiro.pecaDescendo))

		qtdTotalPecas = 0
		maisAltoGlobal = 9999

		# Preencho a matriz mat com a referência dos objetos das peças
		for peca in self.tabuleiro.pecas:
			for pos in peca.posicoes:
				self.mat[pos[1], pos[0]] = 1
				qtdTotalPecas += 1

				if pos[1] < maisAltoGlobal:
					maisAltoGlobal = pos[1]

		for pos in self.tabuleiro.pecaDescendo.posicoes:
			self.mat[pos[1], pos[0]] = 1
			qtdTotalPecas += 1

			if pos[1] < maisAltoGlobal:
				maisAltoGlobal = pos[1]			


		qtdQuadradosNaAreaAcessivel = (self.tabuleiro.QTD_QUADRADOS_ALTURA - maisAltoGlobal) * self.tabuleiro.QTD_QUADRADOS_LARGURA
		qtdBuraco = qtdQuadradosNaAreaAcessivel - qtdTotalPecas
		
		# Coloco -1 em todos os lugares que a peça existir
		xCoords = []
		quadradoMaisAlto = 9999
		quadradoMaisBaixo = -1
		for pos in self.tabuleiro.pecaDescendo.posicoes:
			self.mat[pos[1], pos[0]] = -1

			if len(xCoords) == 0 or not self.verificaSeCoordenadaExiste(xCoords, pos[0]): #pos[0] not in xCoords[0,:]:	# Se existir alguma coordenada com o x valendo pos[0]
				xCoords.append(pos)
 
			if pos[1] < quadradoMaisAlto:
				quadradoMaisAlto = pos[1]

			if pos[1] > quadradoMaisBaixo:
				quadradoMaisBaixo = pos[1]

		qtd = 0	# Quantidade de quadrados vazios em baixo da peça descendo
		for pos in xCoords:
			x = pos[0]
			if quadradoMaisBaixo+2 < 18:
				for y in range(pos[1], quadradoMaisBaixo+2 ):#self.tabuleiro.QTD_QUADRADOS_ALTURA):
					if self.mat[y,x] == 0:
						qtd += 1
					elif self.mat[y,x] == 1:
						break


		#return 2*qtd + 1*(self.tabuleiro.QTD_QUADRADOS_ALTURA-1 - quadradoMaisBaixo), qtd, quadradoMaisBaixo, xCoords
		return 10*qtd, qtd, quadradoMaisBaixo

	def calculaScore(self):

		#print(self.caminho)

		pecasAux = copy.deepcopy(self.tabuleiro.pecas)
		pecasAux.append(copy.deepcopy(self.tabuleiro.pecaDescendo))

		menor = 999
		qtdQuadrados = 0

		if len(pecasAux) == 0:
			menor = self.tabuleiro.QTD_QUADRADOS_ALTURA-1
		else:
			for peca in pecasAux:
				for pos in peca.posicoes:
					qtdQuadrados += 1
					if pos[1] < menor:
						menor = pos[1]


		qtdQuadradosNaAreaAcessivel = (self.tabuleiro.QTD_QUADRADOS_ALTURA - menor) * self.tabuleiro.QTD_QUADRADOS_LARGURA
		espacosVazios = qtdQuadrados / qtdQuadradosNaAreaAcessivel

		# Vamos penalizar o movimento se houver espaço exatamente em baxo da peça

		score = espacosVazios + (1 - ((self.tabuleiro.QTD_QUADRADOS_ALTURA-1 - menor) / self.tabuleiro.QTD_QUADRADOS_ALTURA-1))

		return espacosVazios, menor, qtdQuadrados
