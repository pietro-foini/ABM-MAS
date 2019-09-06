# Strumenti sempre utili che possiamo aggiornare in base alle nostre esigenze. Richiamabili con un colpo solo da comando "from Tools import *".
import random
from numpy import *
from matplotlib import *

# ask a single agent to do something
def askAgent(agent, method, *k):
    return method(agent, *k)

# ask each agent in list to do something
def askEachAgentIn(agentList, method, *k):
	# estrae le households dalle liste a cui appartengono e fa una lista unica
	if type(agentList[0]) == list: 
		listOfAgents = []
		for subList in agentList:
			for anAgent in subList:
				listOfAgents.append(anAgent)
		agentList = listOfAgents
				
	#random.shuffle(agentList)
	tot = 0
	for anAgent in agentList:
		tot += method(anAgent, *k)
	return tot

def askEachItalianAgentIn(agentList, method, *k):
	# estrae le households dalle liste a cui appartengono e fa una lista unica
	if type(agentList[0]) == list: 
		listOfAgents = []
		for subList in agentList:
			for anAgent in subList:
				listOfAgents.append(anAgent)
		agentList = listOfAgents
				
	#random.shuffle(agentList)
	tot = 0
	for anAgent in agentList:
		if anAgent.my_group == 0:       
			tot += method(anAgent, *k)
	return tot

def askEachEuropeanAgentIn(agentList, method, *k):
	# estrae le households dalle liste a cui appartengono e fa una lista unica
	if type(agentList[0]) == list: 
		listOfAgents = []
		for subList in agentList:
			for anAgent in subList:
				listOfAgents.append(anAgent)
		agentList = listOfAgents
				
	#random.shuffle(agentList)
	tot = 0
	for anAgent in agentList:
		if anAgent.my_group == 1:       
			tot += method(anAgent, *k)
	return tot