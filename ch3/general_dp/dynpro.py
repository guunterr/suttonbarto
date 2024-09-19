import numpy as np

class MDP:
    #States must be hashable
    def __init__(self, states, gamma) -> None:
        self.states = states
        self.gamma = gamma
    
    def actions(self, state):
        pass

    def dynamics(self, state, action):
        pass
    
class Policy:
    def __init__(self):
        pass
    
    def policy(self, state):
        pass

    def sample_action(self, state):
        policy = self.policy(state)
        np.random.choice(list(policy.keys()), 1, p=list(policy.values()))
    
class UniformRandom(Policy):
    def __init__(self, mdp):
        super().__init__()
        self.mdp = mdp
    def policy(self, state):
        return {action:0.25 for action in self.mdp.actions(state)}
    
class Greedy(Policy):
    def __init__(self, mdp, state_values):
        super().__init__()
        self.state_values = state_values
        self.mdp = mdp
    def policy(self, state):
        action_value_pairs = {}
        for action in self.mdp.actions(state):
            srps = [tuple(srp) for srp in self.mdp.dynamics(state, action).items()]
            action_value = sum([srp[1] * self.state_values[srp[0][0]] for srp in srps])
            action_value_pairs[action] = action_value
        selected_action = max(action_value_pairs, key=action_value_pairs.get)
        p = {action:0 for action in self.mdp.actions(state)}
        p[selected_action] = 1
        return p
    
def evaluate_policy(mdp: MDP, policy:Policy, threshold = 0.1) -> dict:
    values = {state:0 for state in mdp.states}
    while True:
        old_values = values
        values = step_evaluate_policy(mdp, old_values, policy)
        delta = max(values[s] - old_values[s] for s in mdp.states)
        if delta < threshold:
            return values
def step_evaluate_policy(mdp: MDP, values, policy:Policy):
    new_values = {state:0 for state in mdp.states}
    for s in mdp.states:
        v = 0
        pi = policy.policy(s)
        for a in mdp.actions(s):
            temp_v = 0
            srp_pairs = [tuple(x) for x in mdp.dynamics(s, a).items()]
            for ((state,reward),probability) in srp_pairs:
                temp_v += probability * (reward + mdp.gamma * values[state])
            temp_v *= pi[a]
            v += temp_v
        new_values[s] = v
    return new_values