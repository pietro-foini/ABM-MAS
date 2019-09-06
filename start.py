from ModelSwarm import *
import pandas as pd
import matplotlib.pyplot as plt

nFirms = 1000#eval(input("How many firms?"))
nHouseholds = 100000#eval(input("How many households?"))
nCycles = 100#eval(input("How many cycles?"))

modelSwarm = ModelSwarm(nFirms, nHouseholds, nCycles)

# descrive parametri iniziali del modell9
modelSwarm.describeModel()

# crea agenti
modelSwarm.buildObjects()

# crea azioni
#modelSwarm.buildActions()

# run
observerDict = modelSwarm.run()

df = pd.DataFrame(observerDict)
df['Employment rate Italy'] = df.nWorkersItaly.astype(float) / (df.nWorkersItaly + df.nNotWorkersItaly)
df['Unmployment rate Italy'] = df.nNotWorkersItaly.astype(float) / (df.nWorkersItaly + df.nNotWorkersItaly)
df['Employment rate Europe'] = df.nWorkersEurope.astype(float) / (df.nWorkersEurope + df.nNotWorkersEurope)
df['Unmployment rate Europe'] = df.nNotWorkersEurope.astype(float) / (df.nWorkersEurope + df.nNotWorkersEurope)
df['GDPcapitaIta'] = df.GDPIta.astype(float) / (df.nWorkersItaly + df.nNotWorkersItaly)
df['GDPcapitaEur'] = df.GDPEur.astype(float) / (df.nWorkersEurope + df.nNotWorkersEurope)
df.set_index('time', inplace=True, drop=True)

# fig, axes = plt.subplots(nrows=3, ncols=1)
# df['nFirms'].plot(ax=axes[0], c='g')
# df[['Employment rate','Unmployment rate']].plot(ax=axes[1])
# df['marketPrice'].plot(ax=axes[2], c='r')
# plt.show()

df[['nFirmsItaly','Employment rate Italy','marketPriceItaly','newFirmsItaly','percDeficitItaly','GDPcapitaIta','tradeBalanceOverGDPIta']].plot(subplots=True)
plt.show()

df[['nFirmsEurope','Employment rate Europe','marketPriceEurope','newFirmsEurope','percDeficitEurope', 'GDPcapitaEur','tradeBalanceOverGDPEur']].plot(subplots=True)
plt.show()

#print()
#print("\nSimulation stopped after", nCycles, "cycles")