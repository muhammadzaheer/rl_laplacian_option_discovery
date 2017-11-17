import numpy as np

# Possible default actions in tabular environment
action_set = [(0, 1), (0, -1), (1, 0), (-1, 0)] # R, L, D, U, T


# Need to change to abstract class to handle internal / external environment
# Currently internal env (with random start state, and terminate action)
class Environment(object):

    def __init__(self, max_row, max_col,
                 goal_state, obstacle_vector = None, reward_vector = None):

        states_rc = [(r, c) for r in range(max_row) for c in range(max_col)]
        self.states_rc = states_rc # all possible states (r,c)

        self.max_row, self.max_col = max_row, max_col

        self.goal_state = goal_state

        # Need to figure out a termination technique
        self.action_set = action_set
        self.MAX_ACTION = len(self.action_set)

        if reward_vector is None:
            # Reward is -1.0 everywhere
            self.reward_vector = np.zeros((len(self.states_rc))) * -1
        else:
            self.reward_vector = reward_vector

    def start(self):
        start_state = np.random.randint(len(self.states_rc))
        self.current_state = np.asarray([start_state])
        # Returning a copy of the current state
        return np.copy(self.current_state)

    def step(self, action):
        if not action < self.MAX_ACTION:
            print "Invalid action taken!!"
            print "action: ", action
            print "current_state", self.current_state

        action = self.action_set[action]
        if action == (-1, -1):
            self.current_state = None
            result = {"reward": 0, "state": None, "isTerminal": True}
            return result
        s = self.current_state[0]
        # Getting the coordinate representation of the state
        s = self.states_rc[s]
        nr = min(self.max_row - 1, max(0, s[0] + action[0]))
        nc = min(self.max_col - 1, max(0, s[1] + action[1]))
        ns = (nr, nc)
        # Going back to the integer representation
        s = self.states_rc.index(s)
        ns = self.states_rc.index(ns)
        reward = self.reward_vector[ns] - self.reward_vector[s]
        self.current_state[0] = ns
        result = {"reward": reward, "state": self.current_state,
                  "isTerminal": False}

        return result

    def cleanup(self):
        return

    def message(self, in_message):
        # Helper messages to help in adjacency matrix
        if in_message.startswith("start_state"):
            self.current_state = np.asarray([int(in_message.split(":")[1])])
        elif in_message.startswith("no_goal"):
            self.goal_state = (-1, -1)
        elif in_message.startswith("dim"):
            dims = in_message.split(":")[1].split(",")
            max_row, max_col = int(dims[0]), int(dims[1])
            states_rc = [(r, c) for r in range(max_row)
                         for c in range(max_col)]
            self.max_row, self.max_col = max_row, max_col
            self.states_rc = states_rc
        elif in_message.startswith("eigen_purpose"):
            self.reward_vector = pickle.loads(in_message.split(":")[1])
        return ""