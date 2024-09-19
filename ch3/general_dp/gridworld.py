import numpy as np
import dynpro

class GridWorld(dynpro.MDP):
    def __init__(self, width, height, gamma=0.9) -> None:
        states = set([(x,y) for x in range(width) for y in range(height)])
        super().__init__(states, gamma)
        
    def actions(self, state):
        return ['u','d','l','r']
    def dynamics(self,state, action):
        x,y = state
        output = None
        if y == 0 and x == 1:
            y = 4
            output = ((x,y), 10)
        elif y == 0 and x == 3:
            y = 2
            output = ((x,y),5)
        else:
            match action:
                case 'u':
                    if y > 0:
                        y -= 1
                        output = ((x,y),0)
                    else:
                        output = ((x,y),-1)
                case 'd':
                    if y < 4:
                        y += 1
                        output = ((x,y),0)
                    else:
                        output = ((x,y),-1)
                case 'l':
                    if x > 0:
                        x -= 1
                        output = ((x,y),0)
                    else:
                        output = ((x,y),-1)
                case 'r':
                    if x < 4:
                        x += 1
                        output = ((x,y),0)
                    else:
                        output = ((x,y),-1)
        return {output:1}

gridworld = GridWorld(5,5)    

optimal_policy = dynpro.find_optimal_policy(gridworld)
print([f"{s}:{v:.1f}" for (s,v) in dynpro.evaluate_policy(gridworld, optimal_policy, 0.001).items()])