import random
import numpy as np
import parameters as pmt

class Household:
	'''Questa è la classe delle famiglie, che sono rappresentate da un lavoratore.'''

	def __init__(self, is_employed, my_group):
		self.is_employed = is_employed
		self.my_group = my_group       
		self.debt = 0 # rata da pagare in caso di investimento
		self.savings = 0
		self.hasInvested = False
		self.nInstallmentsleft = 0
		self.addInvestmentToDemand = False
		self.consumption = 0
		self.wage = 0
        
	def getMyGroup(self):
		return self.my_group        
        
	# calcola il consumo delle famiglie come: c = a + b * wage + u + i (per disoccupati c = wage)
	def calcConsumption(self):
		# decide se investire
		if self.is_employed == True:
			if self.hasInvested == False:
				p = random.uniform(0, 1)
				if p < pmt.pInvestHousehold:
					self.hasInvested = True
					self.debt = pmt.repaymentRate
					self.nInstallmentsleft = pmt.nInstallmentsHouseholds
					self.addInvestmentToDemand = True
		# calcola quanto consumare
		if self.is_employed == True:
			self.wage = pmt.wage[self.my_group]
			# toglie interessi sullo stipendio 
			if self.hasInvested == True:
				self.wage -= self.debt
				self.nInstallmentsleft -= 1
				if self.nInstallmentsleft == 0: # finisce di pagare l'investimento
					self.hasInvested = False
					self.debt = 0
			self.consumption = pmt.a + pmt.b*self.wage + random.normalvariate(0, 0.1)
			if self.consumption > self.wage: # controlla, al netto degli investimenti, di non aver consumato più dello stipendio
				self.consumption = self.wage
				# aggiunge domanda per investimento, solo al ciclo zero dell'investimento
				if self.addInvestmentToDemand == True:
					self.consumption += pmt.demandForInvestmentHouseholds
					self.addInvestmentToDemand = False
		else:
			self.wage = 0           
			self.consumption = pmt.unempBenefit[self.my_group]
			self.debt = 0          
		return self.consumption
    
	# calcolo il possibile risparmio. 
	def calcSavings(self):
		if self.is_employed == True:
			if self.consumption < self.wage:
				self.savings = self.wage - self.consumption
			else:
				self.savings = 0
		else: 
			self.savings = 0
		return self.savings
        
	# setta stato d'impiego
	def setEmploymentStatus(self, value):
		self.is_employed = value

	# setta stato investimenti
	def setInvestmentStatus(self, value):
		self.hasInvested = value
        
	# tendenza acquistare dentro proprio gruppo
	def ProbConsOwn(self, priceItAndEur, nTotWorkers):
		totalWorkers = nTotWorkers[0] + nTotWorkers[1]
		not_my_group = 1 - 1 * self.my_group            
		prob1Part1 = pmt.chauvinismWeight * pmt.chauvinism[self.my_group]
		prob1Part2 = pmt.sensitivityToPriceWeight * (1 - np.tanh(pmt.sensitivityToPrice*(priceItAndEur[self.my_group] - priceItAndEur[not_my_group])))/2
		prob1 = (prob1Part1 + prob1Part2)/(pmt.chauvinismWeight + pmt.sensitivityToPriceWeight)
		prob2 = prob1 * (nTotWorkers[self.my_group]/totalWorkers)*(totalWorkers/(2*prob1*nTotWorkers[self.my_group] - prob1*totalWorkers + totalWorkers - nTotWorkers[self.my_group]))  
		pOwnGr = prob2 * pmt.Indipendence[self.my_group]                                                         
		return pOwnGr           
                       

class Firm:
	'''Questa è la classe delle aziende.'''

	def __init__(self, nWorkers, my_group):
		self.nWorkers = nWorkers
		self.my_group = my_group        
		self.prodPerWorker = pmt.prodPerWorker # prodPerWorker è la produttività di un lavoratore: produzione_azienda = prodPerWorker * nWorkers
		self.firmHealth = 0 # tiene conto dello stato di salute dell'azienda
		self.hasInvested = False
		self.wage = pmt.wage[self.my_group]       
		self.firmPrice = 0
		self.profit = 0
		self.production = 0
		self.debt = 0 # rata da pagare in caso di investimento
		self.nInstallmentsleft = 0
		self.addInvestmentToDemand = False
		self.consumptionForInvestment = 0

	def getNumWorkers(self):
		return self.nWorkers
    
	def getMyGroup(self):
		return self.my_group

	def updateNumWorkers(self, value):
		self.nWorkers += value

	# calcola produzione
	def calcProduction(self):
		self.production = self.prodPerWorker*self.nWorkers
		#print("production =", self.production)
		return self.production

	# calcola consumo dell'azienda, nel caso abbia investito al ciclo precedente
	# il consumo è dato dalla quantità di lavoratori richiesti per far nascere la nuova azienda
	def calcConsumption(self):
		if self.addInvestmentToDemand == True:
			consumption = self.consumptionForInvestment
			self.addInvestmentToDemand = False
		else:
			consumption = 0
		return consumption

	# calcola prezzo dell'azienda
	def setFirmPrice(self, marketPrice):
		self.firmPrice = random.normalvariate(marketPrice, pmt.sigmaPrice*marketPrice)
		#print("Firm Price:", self.firmPrice)
		return self.firmPrice

	# calcola il profitto
	def calcProfit(self):
		# calcola profitti
		self.profit = self.production*self.firmPrice - self.nWorkers*self.wage
		# aggiunge l'interesse sul debito in caso di investimento
		if self.hasInvested == True:
			self.profit -= self.debt
			self.nInstallmentsleft -= 1
			if self.nInstallmentsleft == 0: # finisce di pagare l'investimento
				self.hasInvested = False
				self.debt = 0

		# aggiorna stato salute
		if self.profit < 0:
			self.firmHealth -= 1
		else:
			self.firmHealth += 1

		return self.profit

	# definisce la produzione al ciclo successivo
	def planProduction(self, previousDemand, actualDemand):
		if self.production == 0: # controlla che non sia una nuova azienda
			self.deltaWorkforce = 0
		else:
			plannedProduction = self.production * (float(actualDemand) / previousDemand)
			plannedWorkforce = round(plannedProduction / self.prodPerWorker)
			self.deltaWorkforce = plannedWorkforce - self.nWorkers
		return self.deltaWorkforce

	# controlla stato di salute dell'azienda
	def checkHealth(self):
		if self.firmHealth == pmt.goBankrupt:
			return -1
		if self.firmHealth == pmt.doInvest:
			return 1

	# modifica i valori relativi all'investimento, dopo averlo fatto
	def setInvestmentStatus(self, nNewWorkers):
		self.firmHealth = 0 # riporta il contatore della salute a 0

		self.hasInvested = True
		self.addInvestmentToDemand = True
		self.consumptionForInvestment = nNewWorkers # la quantità da investire è il numero di lavoratori
		self.nInstallmentsleft = nNewWorkers
		self.debt = pmt.repaymentRate
        
	# tendenza acquistare dentro proprio gruppo
	def ProbConsOwn(self, priceItAndEur, nTotWorkers):
		totalWorkers = nTotWorkers[0] + nTotWorkers[1]
		not_my_group = 1 - 1 * self.my_group            
		prob1Part1 = pmt.chauvinismWeight * pmt.chauvinism[self.my_group]
		prob1Part2 = pmt.sensitivityToPriceWeight * (1 - np.tanh(pmt.sensitivityToPrice*(priceItAndEur[self.my_group] - priceItAndEur[not_my_group])))/2
		prob1 = (prob1Part1 + prob1Part2)/(pmt.chauvinismWeight + pmt.sensitivityToPriceWeight)
		prob2 = prob1 * (nTotWorkers[self.my_group]/totalWorkers)*(totalWorkers/(2*prob1*nTotWorkers[self.my_group] - prob1*totalWorkers + totalWorkers - nTotWorkers[self.my_group]))  
		pOwnGr = prob2 * pmt.Indipendence[self.my_group]                                                         
		return pOwnGr 
         

class PubAdm:
	'''Questa è la classe della pubblica amministrazione.'''

	def __init__(self, nWorkers, my_group):
		self.nWorkers = nWorkers
		self.my_group = my_group        
		self.purchasings = 0
		self.PublicExpenditure = 0
		self.deficit = 0
		self.wage = pmt.wage[self.my_group]          
        
	def getNumWorkers(self):
		return self.nWorkers

	def getMyGroup(self):
		return self.my_group    
    
	def calcConsumption(self):
		wages = self.nWorkers*pmt.wage[self.my_group]
		self.purchasings = wages - random.randint(0, round(pmt.percPurchasingsPA*wages))
		return self.purchasings
 
	def PublicExpenditure(self):
		self.PublicExpenditure = self.nWorkers*pmt.wage[self.my_group] + self.purchasings
		return self.PublicExpenditure
    
	def calcDeficit(self, totalSavings, GDP):
		self.deficit = totalSavings - self.PublicExpenditure
		if self.deficit > 0:
			self.deficit = 0                
		ControlMaastr = abs(round(self.deficit/GDP*100)) # verifica trattato di Maastricht
		values = [self.deficit, ControlMaastr]
		return values  
    
                
        
