#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-;
#Importando pysco se tiver

from copy import *
class Grafo( object ):

	def __init__( self, var):
		"""
		Instancia um grafo
		- 'entrada' nome do arquivo que contém o grafo
		- 'qtd_nos' armaneza a quantidade de nós do grafo
		- 'grafo' 	armazena a estrutura de dados (dictionary) do grafo
		- 
		"""
		self.entrada = var['GRAFO']
		self.qtd_nos = 0 
		self.peso = {}
		self.feromonio = {}
		self.visibilidade = {}
		self.visibilidade_beta = {}
		self.divisor = {}
		self.deltaTao = {}
		self.cidadesDisponiveis = []
		self.alfa = var['ALFA']
		self.beta = var['BETA']
		self.ro = var['RO']
		self.q = var['Q']
		self.t0 = var['T0']

		self.__tamPool = 5		# Tamanho do pool caronas + motorista. por exemplo: 5 = 1 (motorista) + 4 (caronas)
		self.__tamCaminho = 0	# q pode ser no máximo = pool
		self.__restaCidades = 0


	# Tamanho do caminho / set / property
	def getTamCaminho( self ):
		return self.__tamCaminho
	def setTamCaminho( self, tamCaminho ):
		self.__tamCaminho = tamCaminho

	# Tamanho do pool / set / property
	def getTamPool( self ):
		return self.__tamPool
	def setTamPool( self, tamPool ):
		self.__tamPool = tamPool

	# tamPool = property(getTamPool, setTamPool)

	# Tamanho do RestaCidades / set / property
	def getRestaCidades( self ):
		return self.__restaCidades 
	def setRestaCidades( self, restaCidades  ):
		self.__restaCidades = restaCidades 

	#restaCidades  = property(getRestaCidades, setRestaCidades)

	def getQtdNos( self ):
		return self.qtd_nos

	def getCidadesDisponiveis( self ):
		return copy(self.cidadesDisponiveis)

	def carregaGrafo( self ):
		global FEROMONIO
		"""
		Carrega os dados na estrutura do grafo		
		"""
		arquivo = open(''.join(["GRAPHS/", self.entrada, "/", self.entrada, "_03_weight_graphs.txt"]), "r")
		linha = arquivo.readline()
		self.qtd_nos = int(linha.split(" ")[0])

		for p1 in range( 0, self.qtd_nos):
			for p2 in range( 0, self.qtd_nos):
				linha = arquivo.readline()
				itens = linha.split(" ")
				no1 = int(itens[0])
				no2 = int(itens[1])
				peso = float(itens[2])
				
				if not self.peso.has_key(no1):
					self.peso[no1] 			= {}
					self.feromonio[no1]		= {}
					self.visibilidade[no1] 	= {}
					self.visibilidade_beta[no1] = {}
					self.deltaTao[no1]			= {}

				self.deltaTao[no1][no2] 		= 0
				
				self.peso[no1][no2] 		= peso
				self.feromonio[no1][no2] 	= float(self.t0)

				# Equivale à if no1 != no2:
				if peso > 0:
					self.visibilidade[no1][no2] = 1.0/peso
					self.visibilidade_beta[no1][no2] = pow(1.0/peso,2)
				else:
					self.visibilidade[no1][no2] = 0
					self.visibilidade_beta[no1][no2] = 0
				
		# Carrega uma lista com as cidades existentes
		for i in range(0,self.getQtdNos()):
			self.cidadesDisponiveis.append(i)
		arquivo.close()

	def depositaFeromonio( self ):
		""" Deposita feromonio nas arestas do caminho percorrido """
		RO  = self.ro
		
		# Deposita o feromonio
		# Para cada aresta do grafo, atualiza o feromonio
		for i in range(self.qtd_nos):
		    for j in range(self.qtd_nos):
				if i!=j:
					Tij = self.feromonio[i][j]
					DTij = self.deltaTao[i][j]
					self.feromonio[i][j] = (1.0 - RO)*float(Tij)+float(DTij)
					self.feromonio[i][j] = (1.0 - RO)*float(Tij)+float(DTij)
