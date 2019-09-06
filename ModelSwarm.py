from Agent import *
from Tools import *
import parameters as pmt

class ModelSwarm(object):
	'''Questa classe definisce le funzionalità del modello.'''

	# inizializza l'ambiente
	def __init__(self, nFirms, nHouseholds, nCycles):
		self.nFirms = nFirms
		self.nHouseholds = nHouseholds       
		self.firmsDict = {}
		self.householdsDict = {}  
		self.PADict = {}
		# in generale indice 0 per Italia e indice 1 per Europa 
		self.nu = []        
		self.nTotWorkers = [] 
		self.workersPubAdm = [] 
		self.nTotFirms = []  
		self.nUnemployed = []     
		self.idFirm = 4   
		self.demand = {0: [], 1: []} # domanda alle aziende italiane ed europee       
        
		self.supply = [0, 0]
		self.marketPrice = [0.9, 1]
		self.PublicExpenditure = [0, 0]  
		self.GDP = [0, 0]
		self.publicDebt = [0, 0]  
		self.percDeficit = [0, 0] 
		self.totProfit = [0, 0]
		self.nNewFirms = [0, 0]  
        
		self.importExportIta = [0, 0] # il primo è l'import italiano, il secondo l'import europeo (export italiano)                
		self.counterIta = 0       
		self.tradeBalanceOverGDP = [0, 0]        
             
		self.nCycles = nCycles
		self.t = 0
		self.conclude = False

		# quantità da osservare
		self.observer = {'time':[], 'nFirmsItaly':[], 'nFirmsEurope':[], 'nWorkersItaly':[], 'nWorkersEurope':[], 'nNotWorkersItaly':[], 'nNotWorkersEurope':[], 'marketPriceItaly':[], 'marketPriceEurope':[], 'newFirmsItaly':[], 'newFirmsEurope':[], 'totalProfitItaly':[], 'totalProfitEurope':[], 'percDeficitItaly':[], 'percDeficitEurope':[], 'importIta':[], 'exportIta':[], 'importEur':[], 'exportEur':[], 'tradeBalanceOverGDPIta':[], 'tradeBalanceOverGDPEur':[], 'GDPIta':[], 'GDPEur':[]}

	# descrive i parametri iniziali del modello
	def describeModel(self):
		print("Simulation starting at t=%d with:" % (self.t))
		print(self.nFirms, "firms (italian and european)")
		print(self.nHouseholds, "households (italian and european)")
		print("Unemployment rate in Italy ≃", round(pmt.unemploymentRateItaly*100), "% and unemployment rate in Europe ≃", round(pmt.unemploymentRateEurope*100), "%")
		print()

	# inizializza gli agenti
	def buildObjects(self):
        
		#Italy
		totHouseholdsItaly = round(self.nHouseholds * (pmt.percIta)) 
		nTotWorkersItaly = round(totHouseholdsItaly * (1 - pmt.unemploymentRateItaly))        
		nTotFirmsItaly = round(self.nFirms * (pmt.percIta))
		self.nTotFirms.append(nTotFirmsItaly) 
		#Europe 
		totHouseholdsEurope = self.nHouseholds - totHouseholdsItaly
		nTotWorkersEurope = round(totHouseholdsEurope * (1 - pmt.unemploymentRateEurope))        
		nTotFirmsEurope = self.nFirms - nTotFirmsItaly
		self.nTotFirms.append(nTotFirmsEurope)         
 

		# crea PubAdm italiana
		workersPubAdmItaly = round(nTotWorkersItaly * pmt.publicEmploymentRateItaly)
		self.workersPubAdm.append(workersPubAdmItaly)     
		self.PADict[0] = PubAdm(nWorkers = workersPubAdmItaly, my_group = 0) 
		hList = []
		for i in range(workersPubAdmItaly):
			hList.append(Household(is_employed = True, my_group = 0))
		self.householdsDict[2] = hList  # l'azienda 2 equivale all'agente PA italiana
		print("PubAdm in Italy created with", askAgent(self.PADict[0], PubAdm.getNumWorkers), "workers")         
		# crea PubAdm europea
		workersPubAdmEurope = round(nTotWorkersEurope * pmt.publicEmploymentRateEurope)
		self.workersPubAdm.append(workersPubAdmEurope)            
		self.PADict[1] = PubAdm(nWorkers = workersPubAdmEurope, my_group = 1)
		hList = []
		for i in range(workersPubAdmEurope):
			hList.append(Household(is_employed = True, my_group = 1))
		self.householdsDict[3] = hList  # l'azienda 3 equivale all'agente PA europea
		print("PubAdm in Europe created with", askAgent(self.PADict[1], PubAdm.getNumWorkers), "workers")
                        
		# crea aziende italiane
		self.nu.append(round((nTotWorkersItaly/nTotFirmsItaly) * (1 - pmt.publicEmploymentRateItaly))) # numero medio lavoratori per azienda in Italia
		nTotWorkersItaly = 0 # lo riconto in un altro modo
		for i in range(nTotFirmsItaly):
			aFirm = Firm(nWorkers = self.nu[0] + random.randint(-10, 10), my_group = 0) # genero azienda
			self.firmsDict[self.idFirm] = aFirm # aggiungo azienda al dizionario delle aziende, con rispettivo identificatore
			print("Firm num.", self.idFirm, "created in Italy with", askAgent(aFirm, Firm.getNumWorkers), "workers")
			nTotWorkersItaly += askAgent(aFirm, Firm.getNumWorkers)
			# assume dipendenti
			hList = []
			for j in range(askAgent(aFirm, Firm.getNumWorkers)):
				hList.append(Household(is_employed = True, my_group = 0))
			self.householdsDict[self.idFirm] = hList # associa ai lavoratori impiegati l'identificatore dell'azienda
			self.idFirm += 1 # cambia identificatore
		nTotWorkersItaly += workersPubAdmItaly
		self.nTotWorkers.append(nTotWorkersItaly)        
		# crea disoccupati italiani
		nUnemployedItaly = totHouseholdsItaly - nTotWorkersItaly   
		self.nUnemployed.append(nUnemployedItaly)        
		hList = []
		for i in range(nUnemployedItaly):
			hList.append(Household(is_employed = False, my_group = 0))
		self.householdsDict[0] = hList # l'azienda 0 equivale alla "disoccupazione" italiana       

		print()        
          
		# crea aziende europee
		self.nu.append(round((nTotWorkersEurope/nTotFirmsEurope) * (1 - pmt.publicEmploymentRateEurope))) # numero medio lavoratori per azienda in Europa
		nTotWorkersEurope = 0 # lo riconto in un altro modo 
		for i in range(nTotFirmsEurope):
			aFirm = Firm(nWorkers = self.nu[1] + random.randint(-10, 10), my_group = 1) # genero azienda
			self.firmsDict[self.idFirm] = aFirm # aggiungo azienda al dizionario delle aziende, con rispettivo identificatore
			print("Firm num.", self.idFirm, "created in Europe with", askAgent(aFirm, Firm.getNumWorkers), "workers")
			nTotWorkersEurope += askAgent(aFirm, Firm.getNumWorkers)
			# assume dipendenti
			hList = []
			for j in range(askAgent(aFirm, Firm.getNumWorkers)):
				hList.append(Household(is_employed = True, my_group = 1))
			self.householdsDict[self.idFirm] = hList # associa ai lavoratori impiegati l'identificatore dell'azienda
			self.idFirm += 1 # cambia identificatore
		nTotWorkersEurope += workersPubAdmEurope
		self.nTotWorkers.append(nTotWorkersEurope)          
		# crea disoccupati europei
		nUnemployedEurope = totHouseholdsEurope - nTotWorkersEurope 
		self.nUnemployed.append(nUnemployedEurope)         
		hList = []
		for i in range(nUnemployedEurope):
			hList.append(Household(is_employed = False, my_group = 1))
		self.householdsDict[1] = hList # l'azienda 1 equivale alla "disoccupazione" europea

	# update observer
	def updateObserver(self):
		self.observer['time'].append(self.t)
		self.observer['nFirmsItaly'].append(self.nTotFirms[0])
		self.observer['nFirmsEurope'].append(self.nTotFirms[1])        
		self.observer['nWorkersItaly'].append(self.nTotWorkers[0])
		self.observer['nWorkersEurope'].append(self.nTotWorkers[1])        
		self.observer['nNotWorkersItaly'].append(self.nUnemployed[0])
		self.observer['nNotWorkersEurope'].append(self.nUnemployed[1])        
		self.observer['marketPriceItaly'].append(self.marketPrice[0])
		self.observer['marketPriceEurope'].append(self.marketPrice[1])        
		self.observer['newFirmsItaly'].append(self.nNewFirms[0])
		self.observer['newFirmsEurope'].append(self.nNewFirms[1])        
		self.observer['totalProfitItaly'].append(self.totProfit[0])
		self.observer['totalProfitEurope'].append(self.totProfit[1])        
		self.observer['percDeficitItaly'].append(self.percDeficit[0])
		self.observer['percDeficitEurope'].append(self.percDeficit[1]) 
		self.observer['importIta'].append(self.importExportIta[0])
		self.observer['exportIta'].append(self.importExportIta[1]) 
		self.observer['importEur'].append(self.importExportIta[1])
		self.observer['exportEur'].append(self.importExportIta[0])
		self.observer['tradeBalanceOverGDPIta'].append(self.tradeBalanceOverGDP[0])
		self.observer['tradeBalanceOverGDPEur'].append(self.tradeBalanceOverGDP[1])        
		self.observer['GDPIta'].append(self.GDP[0])
		self.observer['GDPEur'].append(self.GDP[1])        

	# calcola il prezzo dato dall'intersezione di domanda e offerta
	def setMarketPrice(self, Idx_group):
		self.marketPrice[Idx_group] = float(self.demand[Idx_group][self.t]) / self.supply[Idx_group]    

	# controlla lo stato di salute delle aziende e decide quante falliscono e quante nuove ne nascono
	def checkFirmsHealth(self, Idx_group):
		idxToDel = []
		newFirms = []        
		for key, aFirm in {key:self.firmsDict[key] for key in list(self.firmsDict.keys()) if self.firmsDict[key].my_group is Idx_group}.items():            
			if askAgent(aFirm, Firm.checkHealth) == -1:
				idxToDel.append(key)
			if askAgent(aFirm, Firm.checkHealth) == 1:
				newFirms.append(key)                    
		return (idxToDel, newFirms)

	# rimuove aziende fallite e mette in disoccupazione i lavoratori
	def removeFirms(self, idxToDel, Idx_group):     
		self.firmsDict = {key:self.firmsDict[key] for key in list(self.firmsDict.keys()) if key not in idxToDel} # rimuovo aziende
		self.nTotFirms[Idx_group] = len(list({key:self.firmsDict[key] for key in list(self.firmsDict.keys()) if self.firmsDict[key].my_group is Idx_group})) # aggiorno numero aziende 
		print()

		for key in idxToDel:
			for worker in self.householdsDict[key]: # aggiungo lavoratori disoccupati all'azienda 0                 
				askAgent(worker, Household.setEmploymentStatus, False)
				askAgent(worker, Household.setInvestmentStatus, False)
				self.householdsDict[Idx_group].append(worker)
				self.nUnemployed[Idx_group] += 1
				self.nTotWorkers[Idx_group] -= 1
			del[self.householdsDict[key]] # elimino azienda key dalla lista delle households
     
	# genera una nuova azienda
	def addFirms(self, newFirms, Idx_group):     
		self.nNewFirms[Idx_group] = 0        
		for key in newFirms:
			# la nuova azienda ha lo stesso numero di lavoratori di quella vecchia
			nNewWorkers = self.nu[Idx_group] + random.randint(-10, 10)

			if nNewWorkers <= self.nUnemployed[Idx_group]: # controllo che ci sia abbastanza forza lavoro
				newFirm = Firm(nWorkers = nNewWorkers, my_group = Idx_group) # genero azienda
				self.nNewFirms[Idx_group] += 1
				self.idFirm += 1 # associo un identificativo alla nuova azienda
				self.firmsDict[self.idFirm] = newFirm
				self.nTotFirms[Idx_group] += 1

				# modifico percentuale occupazione
				self.nTotWorkers[Idx_group] += nNewWorkers # aggiorno contatore occupati
				self.householdsDict[self.idFirm] = self.householdsDict[Idx_group][:nNewWorkers] # aggiungo lavoratori alla nuova azienda
				for newWorker in self.householdsDict[self.idFirm]:
					askAgent(newWorker, Household.setEmploymentStatus, True)
					self.nUnemployed[Idx_group] -= 1
				self.householdsDict[Idx_group] = self.householdsDict[Idx_group][nNewWorkers:] # tolgo gli stessi lavoratori da azienda 0

				# l'azienda che investe deve ripagare il debito
				askAgent(self.firmsDict[key], Firm.setInvestmentStatus, nNewWorkers)              
                
	# assume/licenzia lavoratori
	def planProductionAndHireFire(self, Idx_group):
		for key, aFirm in {key:self.firmsDict[key] for key in list(self.firmsDict.keys()) if self.firmsDict[key].my_group is Idx_group}.items():
			extraWorkforce = aFirm.planProduction(previousDemand=self.demand[Idx_group][self.t - 1], actualDemand=self.demand[Idx_group][self.t])

			# assunzioni
			if extraWorkforce > 0:
				for i in range(extraWorkforce):
					if self.nUnemployed[Idx_group] > 0:
						newWorker = self.householdsDict[Idx_group][0]
						askAgent(newWorker, Household.setEmploymentStatus, True)
						self.householdsDict[key].append(newWorker)
						del(self.householdsDict[Idx_group][0])
						askAgent(aFirm, Firm.updateNumWorkers, 1)
						self.nTotWorkers[Idx_group] += 1
						self.nUnemployed[Idx_group] -= 1

			# licenziamenti
			if extraWorkforce < 0:
				for i in range(extraWorkforce):
					newUnemployed = self.householdsDict[key][0]
					askAgent(newUnemployed, Household.setEmploymentStatus, False)
					askAgent(newUnemployed, Household.setInvestmentStatus, False)
					self.householdsDict[Idx_group].append(newUnemployed)
					del(self.householdsDict[key][0])
					askAgent(aFirm, Firm.updateNumWorkers, -1)
					self.nTotWorkers[Idx_group] -= 1
					self.nUnemployed[Idx_group] += 1           

	def setGDP(self, demand, Idx_group):
		tradeBalance = (1-2*Idx_group)*(self.importExportIta[1] - self.importExportIta[0])
		GDP = demand + self.PublicExpenditure[Idx_group] + tradeBalance 
		self.tradeBalanceOverGDP[Idx_group] = ((tradeBalance/GDP)*100)        
		return GDP
    
	def calcDemand(self): 
		demandItaly = 0
		demandEurope = 0
		self.importExportIta[0] = 0
		self.importExportIta[1] = 0
		for key in self.householdsDict:
			for worker in self.householdsDict[key]:
				c = askAgent(worker, Household.calcConsumption)
				p = askAgent(worker, Household.ProbConsOwn, self.marketPrice, self.nTotWorkers)  
				group = askAgent(worker, Household.getMyGroup)  
				if group == 0:                
					if random.uniform(0,1) < p:
						demandItaly += c
					else: 
						demandEurope += c
						self.importExportIta[0] += c                         
				if group == 1:                
					if random.uniform(0,1) < p:
						demandEurope += c
					else: 
						demandItaly += c
						self.importExportIta[1] += c                        

		for firm in self.firmsDict.values():
			c = askAgent(firm, Firm.calcConsumption)
			p = askAgent(firm, Firm.ProbConsOwn, self.marketPrice, self.nTotWorkers)  
			group = askAgent(firm, Firm.getMyGroup)  
			if group == 0:                
				if random.uniform(0,1) < p:
					demandItaly += c
				else: 
					demandEurope += c
					self.importExportIta[0] += c                    
			if group == 1:                
				if random.uniform(0,1) < p:
					demandEurope += c
				else: 
					demandItaly += c 
					self.importExportIta[1] += c                    
 
		demand = [demandItaly, demandEurope]
		return demand

	#proibisce acquisti PA nel caso non rispetti trattato di Maastricht
	def controlMaasForItalyPA(self): 
		if self.t > 0 and self.percDeficit[0] > pmt.controlPercMaas:           
			self.counterIta += 1           
			classicPurchasings = askAgent(self.PADict[0], PubAdm.calcConsumption)          
			self.PADict[0].purchasings = classicPurchasings - pmt.percPurchasingsPA*self.counterIta*classicPurchasings
			demand = self.PADict[0].purchasings         
		else: 
			if self.counterIta > 0: 
				self.counterIta -= 1                
			classicPurchasings = askAgent(self.PADict[0], PubAdm.calcConsumption)          
			self.PADict[0].purchasings = classicPurchasings - pmt.percPurchasingsPA*self.counterIta*classicPurchasings
			demand = self.PADict[0].purchasings             
		return demand           
        
	# simulazione
	def run(self):

		while not self.conclude:
			print()
			print("Step t =", self.t)
			print("Workers unemployed in Italy:", self.nUnemployed[0], ", workers unemployed in Europe:", self.nUnemployed[1])
			print("Workers employed in Italy:", self.nTotWorkers[0], ";", self.nTotWorkers[0] - self.workersPubAdm[0], "for private and ", self.workersPubAdm[0], "for public")
			print("Firms in Italy:", self.nTotFirms[0])
			print("Workers employed in Europe:", self.nTotWorkers[1], ";", self.nTotWorkers[1] - self.workersPubAdm[1], "for private and ", self.workersPubAdm[1], "for public")
			print("Firms in Europe:", self.nTotFirms[1])

			# calcolo offerta
			supplyItaly = askEachItalianAgentIn(list(self.firmsDict.values()), Firm.calcProduction)
			self.supply[0] = supplyItaly           
			supplyEurope = askEachEuropeanAgentIn(list(self.firmsDict.values()), Firm.calcProduction)  
			self.supply[1] = supplyEurope                    
                        
			# calcolo domanda, risparmi, PIL
            
			listdemand = self.calcDemand()
			demandPubAdmItaly = self.controlMaasForItalyPA()
			demandPubAdmEurope = askAgent(self.PADict[1], PubAdm.calcConsumption)
			self.demand[0].append(listdemand[0] + demandPubAdmItaly)
			self.demand[1].append(listdemand[1] + demandPubAdmEurope)
            
			# calcolo prezzo di mercato
			self.setMarketPrice(Idx_group = 0)
			self.setMarketPrice(Idx_group = 1)            

			# setta prezzo aziende
			askEachItalianAgentIn(list(self.firmsDict.values()), Firm.setFirmPrice, self.marketPrice[0])
			askEachEuropeanAgentIn(list(self.firmsDict.values()), Firm.setFirmPrice, self.marketPrice[1])            

			# calcola profitto aziende (e aggiorna stato salute di conseguenza)
			self.totProfit[0] = askEachItalianAgentIn(list(self.firmsDict.values()), Firm.calcProfit)
			self.totProfit[1] = askEachEuropeanAgentIn(list(self.firmsDict.values()), Firm.calcProfit)            
            
			# controlla stato salute
			idxToDelItaly, newFirmsItaly = self.checkFirmsHealth(0)
			idxToDelEurope, newFirmsEurope = self.checkFirmsHealth(1)            

			# rimuove aziende fallite  
			self.removeFirms(idxToDelItaly, 0)
			self.removeFirms(idxToDelEurope, 1)            

			# genera nuove aziende
			self.addFirms(newFirmsItaly, 0) # Aggiungo firms in Italia
			self.addFirms(newFirmsEurope, 1) # Aggiungo firms in Europa            

			# pianifica produzione al tempo successivo, per t > 0
			if self.t > 0:
				# le aziende assumono/licenziano a seconda della produzione pianificata
				self.planProductionAndHireFire(0)
				self.planProductionAndHireFire(1) 
                
			self.PublicExpenditure[0] = askAgent(self.PADict[0], PubAdm.PublicExpenditure)         
			self.PublicExpenditure[1] = askAgent(self.PADict[1], PubAdm.PublicExpenditure)           
			self.GDP[0] = self.setGDP(demand = listdemand[0], Idx_group = 0)
			self.GDP[1] =self.setGDP(demand = listdemand[1], Idx_group = 1)
            
			totalSavingsItaly = askEachItalianAgentIn(list(self.householdsDict.values()), Household.calcSavings)
			totalSavingsEurope = askEachEuropeanAgentIn(list(self.householdsDict.values()), Household.calcSavings)
			deficAndMaasIta = askAgent(self.PADict[0], PubAdm.calcDeficit, totalSavingsItaly, self.GDP[0])
			self.publicDebt[0] += deficAndMaasIta[0]
			self.percDeficit[0] = deficAndMaasIta[1]
			deficAndMaasEur = askAgent(self.PADict[1], PubAdm.calcDeficit, totalSavingsEurope, self.GDP[1])
			self.publicDebt[1] += deficAndMaasEur[0]
			self.percDeficit[1] = deficAndMaasEur[1]        

			print("Italian supply", supplyItaly, "and european supply", supplyEurope)            
			print("Total demand Italy:", self.demand[0][self.t])
			print("Total demand Europe:", self.demand[1][self.t])
			print("Market price Italy:", self.marketPrice[0])
			print("Market price Europe:", self.marketPrice[1])            
			print("PublicExpenditure Italy:", self.PublicExpenditure[0])
			print("PublicExpenditure Europe:", self.PublicExpenditure[1])            
			print("GDP Italy:", self.GDP[0])
			print("GDP Europe:", self.GDP[1])            
			print("Total savings Italy:", totalSavingsItaly)
			print("Total savings Europe:", totalSavingsEurope)                       
			print("Public debt Italy:", self.publicDebt[0])
			print("Public debt Europe:", self.publicDebt[1])            
			print("Percentage Maastricht Italy:", self.percDeficit[0], "%")
			print("Percentage Maastricht Europe:", self.percDeficit[1], "%")   
            
			# update observer
			self.updateObserver()                        

			# check if all firms went bankrupt!
			if self.nTotFirms[0] == 0:
				print("All the firms in Italy went bankrupt! :(")
				return self.observer            
			if self.nTotFirms[1] == 0:
				print("All the firms in Europe went bankrupt! :(")
				return self.observer

			# update time
			self.t += 1
			if self.t == self.nCycles:
				self.conclude = True

		return self.observer