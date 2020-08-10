import pandas as pd
import csv

# Depart is TRUE for Source Node only.
# Arrive is TRUE for Sink Node only.
# All other nodes are the Nodes in the Network.
class AirportNode:
	def __init__( self, name, depart = False, arrive = False):
		self.name = name
		self.depart = depart
		self.arrive = arrive

	# Function to check whether the list of Nodes has a Source or not.
	def getDepart( airportNodes):
		for node in airportNodes:
			if node.depart == True:
				return node
		return None

	# Function to check whether the list of Nodes has a Sink or not.
	def getArrive( airportNodes):
		for node in airportNodes:
			if node.arrive == True:
				return node
		return None

	# Function to get a particular Node with the corresponding name of the airport.
	def getNode( airportNodes, name):
		for node in airportNodes:
			if node.name == name:
				return node

	# Function to check whether the Node with the corresponding name of the airport
	# exists or not.
	def checkNode( airportNodes, name):
		for node in airportNodes:
			if node.name == name:
				return True
		return False

# Class which creates all the necessary attributes for a given edge in the network.
class RouteEdge:
	def __init__( self, depNode, arrNode, capacity, depTime = 0, arrTime = 0):
		self.depNode = depNode
		self.arrNode = arrNode
		self.capacity = capacity
		self.flow = 0
		self.backEdge = None
		self.depTime = depTime
		self.arrTime = arrTime

# Class which defines and creates the nodes and edges in the network.
class FlowNetwork:
	def __init__( self):
		self.airportNodes = []
		self.flowNetwork = {}

	def getEdges( self):
		allEdges = []
		for node in self.flowNetwork:
			for edge in self.flowNetwork[ node]:
				allEdges.append((edge.depNode, edge.arrNode, edge.capacity, edge.depTime, edge.arrTime))
		return allEdges

	def getNodes( self):
		allNodes = []
		for node in self.airportNodes:
			allNodes.append(node.name)
		return allNodes

	# Function to create Nodes in the flow network.
	def createNode( self, name, depart = False, arrive = False):
		if depart == True and arrive == True:
			return "Airport cannot be same for arrival and departure of the flight."
		if AirportNode.checkNode( self.airportNodes, name):
		    return "Duplicate vertex"
		if depart == True:
			if AirportNode.getDepart( self.airportNodes) != None:
				print( "Source already Exists")
				return "Source already Exists"
		if arrive == True:
			if AirportNode.getArrive( self.airportNodes) != None:
				print( "Sink already Exists")
				return "Sink already Exists"
		newNode = AirportNode( name, depart, arrive)
		# print( newNode.name)
		self.airportNodes.append( newNode)
		self.flowNetwork[ newNode.name] = []

	# Function to add edges in the flow network.
	def createEdge( self, depNode, arrNode, depTime, arrTime, capacity):
		if depNode == arrNode:
			return "Airport cannot be same for arrival and departure of the flight."
		if AirportNode.checkNode( self.airportNodes, depNode) == False:
			return "Departure Node has not been added to the flow network."
		if AirportNode.checkNode( self.airportNodes, arrNode) == False:
			return "Arrival Node has not been added to the flow network."

		newEdge = RouteEdge( depNode, arrNode, capacity, depTime, arrTime)
		backEdge = RouteEdge( arrNode, depNode, 0, -depTime, -arrTime)
		# backEdge = RouteEdge( arrNode, depNode, 0)
		newEdge.backEdge = backEdge
		backEdge.backEdge = newEdge

		node = AirportNode.getNode( self.airportNodes, depNode)
		self.flowNetwork[ node.name].append(newEdge)
		returnNode = AirportNode.getNode( self.airportNodes, arrNode)
		self.flowNetwork[ returnNode.name].append( backEdge)


class CalculateMaxflow( FlowNetwork):

	def getPath( self, depNode, arrNode, path, prev_NodeTime):
		if depNode == arrNode:
			return path
		for edge in self.flowNetwork[ depNode]:
			resCapacity = int(edge.capacity) - int(edge.flow)
			# print( edge. edge.depTime)
			# print( prev_NodeTime)
			if resCapacity > 0 and not (edge, resCapacity) in path and  prev_NodeTime < edge.depTime:
				result = self.getPath( edge.arrNode, arrNode, path + [( edge, resCapacity)], edge.arrTime)
				if result != None:
					return result

	def maxFlow( self):
		source = AirportNode.getDepart( self.airportNodes)
		sink = AirportNode.getArrive( self.airportNodes)
		if source == None or sink == None:
			return "Network does not have source and sink nodes."
		path = self.getPath( source.name, sink.name, [], -1)
		while path != None:
			flow = min(edge[1] for edge in path)
			# print('flow: ' + str(flow))
			# print( '##### path ####')
			# for i in path: 
			# 	print( i[0].depNode, i[0].arrNode, i[1])
			# print( (path[0][0]).flow, path[0][1])
			for edge, res in path:
				edge.flow += flow
				edge.backEdge.flow -= flow
			path = self.getPath( source.name, sink.name, [], 0)
		return sum( edge.flow for edge in self.flowNetwork[source.name])

def CleanData():
	output = []
	df = pd.read_csv("Final_Edges.csv", header = None)
	df1 = pd.read_csv("Final_Edges.csv", header = None)
	for i in range(0, len(df)):
		if( str( df[1][i]) == 'LAX' and str( df[2][i]) == 'JFK' ):
			output.append(df[6][i])
		elif( str( df[2][i]) != 'JFK' and str( df[1][i]) == 'LAX'):
			for j in range( 0, len(df1)):
				if( df[2][i] == df1[1][j]):
					if( df[4][i] < df[3][j]):
						output.append( df1[6][j])
						output.append( df[6][i])
		elif( str( df[2][i]) != 'JFK' and str( df[1][i]) != 'LAX'):
			for j in range( 0, len(df1)):
				if( df[2][i] == df1[1][j]):
					if( df[4][i] < df[3][j]):
						output.append( df1[6][j])
						output.append( df[6][i])
		elif( str( df[2][i]) == 'JFK' and str( df[1][i]) != 'LAX'):
			for j in range( 0, len(df1)):
				if( df[1][i] == df1[2][j]):
					if( df1[4][j] < df[3][i]):
						output.append( df1[6][j])
						output.append( df[6][i])

	final_output = [] 
	for i in output: 
	    if i not in final_output: 
	        final_output.append(i)
	print('Final Edges after considering the temporal parameters: ' + str(len(final_output)))
	return final_output

if __name__ == '__main__':

	count = 0
	fn = CalculateMaxflow()
	df = pd.read_csv("Final_Nodes.csv", header = None)
	x = len(df)
	print("Number of Nodes in the Network: " +  str(x))
	for i in range(0, x):
		if( int(df[1][i]) == 0):
			fn.createNode( str( df[0][i]), True, False)
		elif( int(df[1][i]) == 1):
			fn.createNode( str( df[0][i]), False, True)
		elif( int(df[1][i]) == 2):
			fn.createNode( str( df[0][i]))

	df1 = pd.read_csv("Final_Edges.csv", header = None)
	y = len(df1)
	print("Number of Edges in the Network: " +  str(y))
	final_edges = CleanData()
	for j in range(0, y):
		fn.createEdge( df1[1][j], df1[2][j], int(df1[3][j]), int(df1[4][j]), int(df1[5][j]))

	# df1 = pd.read_csv("Final_Edges.csv", header = None)
	# y = len(df1)
	# print("Number of Edges in the Network: " +  str(y))
	# final_edges = CleanData()
	# for z in final_edges:
	# 	for j in range(0, y):
	# 		if( int(df1[6][j]) == z):
	# 			print( df1[1][j], df1[2][j], int(df1[3][j]), int(df1[4][j]), int(df1[5][j]))
	# 			fn.createEdge( df1[1][j], df1[2][j], int(df1[3][j]), int(df1[4][j]), int(df1[5][j]))
	# 			count = count + 1
	

	# print('count: ' + str(count))
	print( 'Nodes: ' + str([node.name for node in fn.airportNodes]))
	# print( [(e.depTime, e.arrTime) for e in fn.getEdges()])
	# x = fn.calculateMaxFlow()
	print( "Output:" + ' ' + str(fn.maxFlow()))












