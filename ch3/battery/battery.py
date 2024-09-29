import sympy
import numpy as np

sympy.init_printing()

# Parameters
alpha = 0.5
beta = 0.5
gamma = 0.9
r_search = 1
r_wait = 0.1
r_depleted = -3

# States and actions
states = ['high', 'low']
actions = {'high': ['search', 'wait'], 'low': ['search', 'wait', 'recharge']}

# Transition dynamics
def dynamics(state, action):
    if state == 'high':
        if action == 'search':
            return [('high', alpha, r_search), ('low', 1 - alpha, r_search)]
        elif action == 'wait':
            return [('high', 1, r_wait)]
    elif state == 'low':
        if action == 'search':
            return [('high', 1 - beta, r_depleted), ('low', beta, r_search)]
        elif action == 'wait':
            return [('low', 1, r_wait)]
        elif action == 'recharge':
            return [('high', 1, 0)]

# Bellman optimality equations
def bellman_optimality_eqs():
    v_high, v_low = sympy.symbols('v_high v_low')
    
    # Equation for high state (v*(h))
    eq_high = sympy.Eq(v_high, sympy.Max(
        r_search + gamma * (alpha * v_high + (1 - alpha) * v_low),
        r_wait + gamma * v_high
    ))
    
    # Equation for low state (v*(l))
    eq_low = sympy.Eq(v_low, sympy.Max(
        beta * r_search - 3 * (1 - beta) + gamma * ((1 - beta) * v_high + beta * v_low),
        r_wait + gamma * v_low,
        gamma * v_high
    ))
    
    return v_high, v_low, [eq_high, eq_low]


# Solve Bellman equations
v_high, v_low, equations = bellman_optimality_eqs()
solution = sympy.solve(equations, [v_high, v_low])

print(f"Optimal values: {solution}")
