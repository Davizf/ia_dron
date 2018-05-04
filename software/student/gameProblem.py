#
'''
    Class gameProblem, implements simpleai.search.SearchProblem
'''


from simpleai.search import SearchProblem
import simpleai.search

class GameProblem(SearchProblem):

    # Object attributes, can be accessed in the methods below

	MAP=None
	POSITIONS=None
	INITIAL_STATE=None
	GOAL=None
	CONFIG=None
	AGENT_START=None




    # --------------- Common functions to a SearchProblem -----------------


	def actions(self, state):

		'''Returns a LIST of the actions that may be executed in this state
		'''

		actions = []
		# comprobar el borde de la direccion North y si la casilla siguiente es mar
		if state[0][1]!=0 and (state[0][0],state[0][1]-1) not in self.POSITIONS["sea"]:
			actions = actions + ["North"]
		# comprobar el borde de la direccion South y si la casilla siguiente es mar
		if state[0][1]!=3 and (state[0][0],state[0][1]+1) not in self.POSITIONS["sea"]:
			actions = actions + ["South"]
		# comprobar el borde de la direccion East y si la casilla siguiente es mar
		if state[0][0]!=9 and (state[0][0]+1,state[0][1]) not in self.POSITIONS["sea"]:
			actions = actions + ["East"]
		# comprobar el borde de la direccion West y si la casilla siguiente es mar
		if state[0][0]!=0 and (state[0][0]-1,state[0][1]) not in self.POSITIONS["sea"]:
			actions = actions + ["West"]
		return actions

	def result(self, state, action):
		'''Returns the state reached from this state when the given action is executed
		'''
		if action == "North":
			next_position_dron = (state[0][0],state[0][1]-1)
		elif action == "South":
			next_position_dron = (state[0][0],state[0][1]+1)
		elif action == "East":
			next_position_dron = (state[0][0]+1,state[0][1])
		elif action == "West":
			next_position_dron = (state[0][0]-1,state[0][1])
		
		nextState = (next_position_dron, \
			tuple([elem for elem in self.POSITIONS["goal"] if not elem == next_position_dron and elem in state[1]]))
			# generar las casillas que quedan por tomar la foto desde la lista de casillas "goal"
			# se selecciona: 
			# - si la casilla de la posicion siguiente no es para cada uno de las casillas "goal"
			# - si para cada casilla "goal" esta en el estado actual
		return nextState


	def is_goal(self, state):
		'''Returns true if state is the final state
		'''
		return state == self.GOAL

	def cost(self, state, action, state2):
		'''Returns the cost of applying `action` from `state` to `state2`.
			The returned value is a number (integer or floating point).
			By default this function returns `1`.
		'''
		return 1

	def heuristic(self, state):
		'''Returns the heuristic for `state`
		'''
		return len(state[1])


	def setup (self):

		print '\nMAP: ', self.MAP, '\n'
		print 'POSITIONS: ', self.POSITIONS, '\n'
		print 'CONFIG: ', self.CONFIG, '\n'

		initial_state = ((self.POSITIONS['drone-base']))
		initial_state.append(tuple(self.POSITIONS['goal']))
		final_state =  (self.POSITIONS['drone-base'][0],())
		
		algorithm = simpleai.search.astar

		return tuple(initial_state),final_state,algorithm



    # -------------------------------------------------------------- #
    # --------------- DO NOT EDIT BELOW THIS LINE  ----------------- #
    # -------------------------------------------------------------- #

	def getAttribute (self, position, attributeName):
		'''Returns an attribute value for a given position of the map
			position is a tuple (x,y)
			attributeName is a string

			Returns:
				None if the attribute does not exist
				Value of the attribute otherwise
		'''
		tileAttributes=self.MAP[position[0]][position[1]][2]
		if attributeName in tileAttributes.keys():
			return tileAttributes[attributeName]
		else:
			return None

	# THIS INITIALIZATION FUNCTION HAS TO BE CALLED BEFORE THE SEARCH
	def initializeProblem(self,map,positions,conf,aiBaseName):

		# Loads the problem attributes: self.AGENT_START, self.POSITIONS,etc.
		if self.mapInitialization(map,positions,conf,aiBaseName):

			initial_state,final_state,algorithm = self.setup()

			self.INITIAL_STATE=initial_state
			self.GOAL=final_state
			self.ALGORITHM=algorithm
			super(GameProblem,self).__init__(self.INITIAL_STATE)

			return True
		else:
			return False

	# END initializeProblem


	def mapInitialization(self,map,positions,conf,aiBaseName):
		# Creates lists of positions from the configured map
		# The initial position for the agent is obtained from the first and only aiBaseName tile
		self.MAP=map
		self.POSITIONS=positions
		self.CONFIG=conf

		if 'agentInit' in conf.keys():
			self.AGENT_START = tuple(conf['agentInit'])
		else:
			if aiBaseName in self.POSITIONS.keys():
				if len(self.POSITIONS[aiBaseName]) == 1:
					self.AGENT_START = self.POSITIONS[aiBaseName][0]
				else:
					print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}", found several at {1}'.format(aiAgentName,mapaPosiciones[aiAgentName]))
					return False
			else:
				print ('-- INITIALIZATION ERROR: There must be exactly one agent location with the label "{0}"'.format(aiBaseName))
				return False

		return True
