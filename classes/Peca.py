from utils import colors, posicoes
import pygame
import copy


class Peca:
	def __init__(self, tipo):
		self.posicoes = []
		self.color = colors.BLUE
		self.tipo = tipo
		self.angulo = 0
		self.QTD_QUADRADOS_ALTURA = 18

		self.iniciarCoordenadas()

	def iniciarCoordenadas(self):

		if self.tipo == "jorge": # Peça horizontal reta	

			self.posicoes = copy.deepcopy(posicoes.JORGE) 
			self.color = colors.YELLOW


		elif self.tipo == "luiz": # Peça em formato de T
			self.posicoes = copy.deepcopy(posicoes.LUIZ) 
			self.color = colors.AZUL_CLARO

		elif self.tipo == "maria": # Peça em formato de L
			self.posicoes = copy.deepcopy(posicoes.MARIA) 
			self.color = colors.ROXO

		elif self.tipo == "josi": # Peça em formato de L refletido
			self.posicoes = copy.deepcopy(posicoes.JOSI) 
			self.color = colors.CHROME_KEY

		elif self.tipo == "zigomar": # Peça em formato de Z
			self.posicoes = copy.deepcopy(posicoes.ZIGOMAR) 
			self.color = colors.PINK

		elif self.tipo == "zanir": # Peça em formato de Z
			self.posicoes = copy.deepcopy(posicoes.ZANIR) 		
			self.color = colors.LARANJA	

		elif self.tipo == "zeraldo":
			self.posicoes = copy.deepcopy(posicoes.ZERALDO) 		
			self.color = colors.AZUL_FLAT				


	# Cada peça tem um pivo, e em cada posição, o pivot muda.
	# TODO: Ver um jeito de calcular o pivot automaticamente independente da posição
	def getPivot(self, tipo):
		
		if tipo == "jorge":
			if self.angulo == 0:
				return [self.posicoes[2][0], self.posicoes[2][1]+1]
			elif self.angulo == 90:
				return [self.posicoes[2][0], self.posicoes[2][1]]
			elif self.angulo == 180:
				# Se o objeto está em 180º, então a lista de partes está invertida. Isso é muito importante para pegar o pivô correto durante a rotação
				return [self.posicoes[1][0], self.posicoes[1][1]]	
			elif self.angulo == 270:
				return [self.posicoes[1][0]+1, self.posicoes[1][1]]

		if tipo == "luiz":
			if self.angulo == 0:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 90:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 180:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 270:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]

		if tipo == "zigomar":
			if self.angulo == 0:
				return [self.posicoes[3][0]+0.5, self.posicoes[3][1]+0.5]
			elif self.angulo == 90:
				return [self.posicoes[3][0]+0.5, self.posicoes[3][1]+0.5]
			elif self.angulo == 180:
				return [self.posicoes[3][0]+0.5, self.posicoes[3][1]+0.5]
			elif self.angulo == 270:
				return [self.posicoes[3][0]+0.5, self.posicoes[3][1]+0.5]	

		if tipo == "zanir":
			if self.angulo == 0:
				return [self.posicoes[2][0]+0.5, self.posicoes[2][1]+0.5]
			elif self.angulo == 90:
				return [self.posicoes[2][0]+0.5, self.posicoes[2][1]+0.5]
			elif self.angulo == 180:
				return [self.posicoes[2][0]+0.5, self.posicoes[2][1]+0.5]
			elif self.angulo == 270:
				return [self.posicoes[2][0]+0.5, self.posicoes[2][1]+0.5]		

		if tipo == "maria":
			if self.angulo == 0:
				return [self.posicoes[1][0]+0.5, self.posicoes[2][1]+0.5]
			elif self.angulo == 90:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 180:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 270:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]	

		if tipo == "josi":
			if self.angulo == 0:
				return [self.posicoes[1][0]+0.5, self.posicoes[2][1]+0.5]
			elif self.angulo == 90:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 180:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]
			elif self.angulo == 270:
				return [self.posicoes[1][0]+0.5, self.posicoes[1][1]+0.5]		

		if tipo == "zeraldo":
			if self.angulo == 0:
				return [self.posicoes[1][0], self.posicoes[3][1]]
			elif self.angulo == 90:
				return [self.posicoes[1][0], self.posicoes[3][1]]
			elif self.angulo == 180:
				return [self.posicoes[1][0], self.posicoes[3][1]]
			elif self.angulo == 270:
				return [self.posicoes[1][0], self.posicoes[3][1]]			


	def rotate(self):

		xPivot, yPivot = self.getPivot(self.tipo)


		#if self.tipo=="jorge":
		#	xPivot = self.posicoes[2][0]
		#	yPivot = self.posicoes[2][1]+1

		#novaPosicao = []
		for i, pos in enumerate(self.posicoes):


			novaX = pos[0]+0.5 - xPivot 
			novaY = pos[1]+0.5 - yPivot 


			oiX = -novaY
			oiY = novaX



			kkX = oiX + xPivot - 0.5
			kkY = oiY + yPivot - 0.5


			#oi = [int(kkX), int(kkY)]
			#novaPosicao.append(oi)
			#novaPosicao.append([])
			#novaPosicao.append([])
			#novaPosicao[0] .append(int(kkX))
			#novaPosicao.append(int(kkY))

			self.posicoes[i][0] = int(kkX)
			self.posicoes[i][1] = int(kkY)

		self.angulo += 90
		if self.angulo == 360:
			self.angulo = 0			

		#return novaPosicao




	def verificaColisaoParede(self):
		menor = 999

		""" 
		Colisão com a borda esquerda do tabuleiro
		"""
		for pos in self.posicoes:
			if pos[0] < 0 and pos[0] < menor:
				menor = pos[0]		

		if menor is not 999:	
			# Devemos deslocar o objeto 'menor' posições para a direita
			for pos in self.posicoes:
				pos[0] += abs(menor)

		"""
		Colisão com a borda direita do tabuleiro
		"""

		maior = 0
		for pos in self.posicoes:
			if pos[0] >= 10 and pos[0] > maior:
				maior = pos[0] - 9

		if maior != 0:	
			# Devemos deslocar o objeto 'maior' posições para a esquerda
			for pos in self.posicoes:
				pos[0] -= abs(maior)		



		"""
		Colisão com a borda de baixo. Se o jogador rotacionar com a peça encostado em baixo, pode ser que dê erro. Isso aqui corrige
		"""
		menor = self.QTD_QUADRADOS_ALTURA-1
		for pos in self.posicoes:
			if pos[1] > menor:
				menor = pos[1]

		if menor > self.QTD_QUADRADOS_ALTURA-1:

			# Devemos deslocar o objeto 'menor-QTD_QUADRADOS_ALTURA-1' posições para cima
			for iPos, pos in enumerate(self.posicoes):
				self.posicoes[iPos][1] -= menor - (self.QTD_QUADRADOS_ALTURA-1)




		# Se houver mais objetos em baixo, evita a rotação
		#maior = 0
		#colisaoAux = []
		#for pos in self.posicoes:
		#	if pos[1] > maior:
		#		maior = pos[1]


		#parteMaiaAlta = 999
		# Qual a parte da peça descendo que está mais alto?
		#for pos in self.posicoes:
		#	if 

		"""
		menorKkk = -1
		lista = []
		for pos1 in self.posicoes:
			for peca in tabuleiro.pecas:
				for pos2 in peca.posicoes:
					# Se colidir com algum outro objeto na rotação
					if pos1[1] == pos2[1] and pos1[0] == pos2[0]:
						lista.append(pos1)
 		# Qual das coordenadas que se colidem está mais em baixo e qual está mais em cima?
 		menorLista = 0
 		maiorLista = 9999
 		for pos in lista:
 			if pos[1] > menorLista
 				menorLista = pos[1]

 			if pos[1] < maiorLista:
 				maiorLista = pos[1]

 		# Desloca o objeto (menorLista - maiorLista - 1) unidades para cima
 		deslocamento = menorLista - maiorLista - 1
 		for pos in self.posicoes:
 			pos[1] -= deslocamento


		maior2 = 
		for pecas in tabuleiro.pecas
			for pos in pecas.posicoes:
				if pos[1]


		if menor > self.QTD_QUADRADOS_ALTURA-1:	

			# Devemos deslocar o objeto 'menor-QTD_QUADRADOS_ALTURA-1' posições para cima
			for iPos, pos in enumerate(self.posicoes):
				self.posicoes[iPos][1] -= menor - (self.QTD_QUADRADOS_ALTURA-1)
		"""

	def desenha(self, SCREEN, coordenadas = None):

		if coordenadas is not None:
			posicoes = coordenadas
		else:
			posicoes = self.posicoes
			
		for pos in self.posicoes:

			pygame.draw.rect(SCREEN, colors.BLACK, (pos[0]*50,
														pos[1]*50, 
														50, 50))	
			pygame.draw.rect(SCREEN, self.color, (pos[0]*50+2,
														pos[1]*50+2, 
														46, 45))

	def update(self):
		pass 
