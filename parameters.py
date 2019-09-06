# Si definiscono i parametri principali del modello

import random
import math

## parametri modello
unemploymentRateItaly = 0.11 # percentuale disoccupazione italia
unemploymentRateEurope = 0.07 # percentuale disoccupazione Europa

## parametri firms
prodPerWorker = 1

# prezzo
sigmaPrice = 0.05 #0.2

# investimento o fallimento
doInvest = 5 #5
goBankrupt = -2 

## parametri households
wageIt = 0.9
wageEur = 1
wage = [wageIt, wageEur]
unempBenefitIt = 0.3*wageIt
unempBenefitEur = 0.3*wageEur
unempBenefit = [unempBenefitIt, unempBenefitEur]

# consumo
a = 0.1
b = 0.4

# investimenti
pInvestHousehold = 0.05
repaymentRate = 0.2
nInstallmentsHouseholds = 10
demandForInvestmentHouseholds = 5

#percentuale lavoratori PubAdm Italia ed Europa
publicEmploymentRateItaly = 0.27
publicEmploymentRateEurope = 0.25

#percentuale per acquisti PA
percPurchasingsPA = 0.1

#parametro trattato di Maastricht
controlPercMaas = 5

#parametro percentuale cittadini e aziende italiane
percIta = 0.25

#parametro di nazionalismo: propensione nazionalistica ad acquistare all'interno del proprio paese
chauvinism = [0.5, 0.5]

#normalizzazione funzione tanh
sensitivityToPrice = 1.5

# parametri importanza rispettivamente per chauvinism e sensitivityToPrice
chauvinismWeight = 1
sensitivityToPriceWeight = 0

#parametro che indica indipendenza statale per l'Italia nella produzione di beni
Indipendence = [1, 1]
