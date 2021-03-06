# valueIterationAgents.py
# -----------------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import mdp, util, math
from random import random, choice
from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
  """
      * Please read learningAgents.py before reading this.*

      A ValueIterationAgent takes a Markov decision process
      (see mdp.py) on initialization and runs value iteration
      for a given number of iterations using the supplied
      discount factor.
  """
  def __init__(self, mdp, discount = 0.9, iterations = 100):
    self.mdp = mdp
    self.discount = discount
    self.iterations = iterations
    self.values = {} # maps states to their value estimates
    self.valueIteration()

  def valueIteration(self):
    """Finds the value of each state up to time horizon self.iterations.

      Some useful mdp methods you will use:
          mdp.getStates()
          mdp.getPossibleActions(state)
          mdp.getTransitionStatesAndProbs(state, action)
          mdp.getReward(state)
    """
    states = self.mdp.getStates()
    for state in states:
        self.values[state] = self.mdp.getReward(state)
    for i in range(self.iterations):
        prev = self.values.copy()
        for state in self.values:
            best_EV = 0
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                EV = 0
                nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
                for nextState in nextStates:
                    EV += nextState[1] * prev[nextState[0]]
                best_EV = max(EV, best_EV)
            self.values[state] = self.mdp.getReward(state) + self.discount * best_EV

  def getPolicy(self, state):
    """Returns the action with the highest expected value.

      The policy is the best action in the given state
      according to the values computed by value iteration.
      You may break ties any way you see fit.  Note that if
      there are no legal actions, which is the case at the
      terminal state, you should return None.
    """
    actions = self.mdp.getPossibleActions(state)
    best_EV = -math.inf
    best_action = None
    for action in actions:
        nextStates = self.mdp.getTransitionStatesAndProbs(state, action)
        expectedValue = 0
        for nextState in nextStates:
            if(nextState[0] in self.values):
                expectedValue += nextState[1] * self.values[nextState[0]]
        if(expectedValue > best_EV):
            best_EV = expectedValue
            best_action = action
    return best_action

  def getValue(self, state):
    "Returns the value of the state (computed by valueIteration)."
    return self.values.get(state, 0)

  def getAction(self, state):
    "Returns the policy at the state (no exploration)."
    return self.getPolicy(state)
