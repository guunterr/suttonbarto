import sympy
sympy.init_printing()
      
def bellman_optimality_eqs(symbol: sympy.Symbol):
    vars = sympy.symbols([f"v{x}{y}" for x in range(5) for y in range(5)])
    eqs = [
        sympy.Eq(sympy.Symbol(f"v{x}{y}"),dynamics(x,y,action)[2] + sympy.Symbol('gamma') * sympy.Symbol(f"v{dynamics(x,y,action)[0]}{dynamics(x,y,action)[1]}")) 
        for action in ['u','d','l','r'] for x in range(5) for y in range(5)
    ]
    return vars,eqs

def solve_bellman():
    vars = sympy.symbols([f"v{x}{y}" for x in range(5) for y in range(5)])
    x = [["a","b"],["c","d"]]
    print(x[0][1])

def dynamics(x,y,action) -> tuple[int, int, float]:
    if y == 0 and x == 1:
        y = 4
        return (x,y, 10)
    if y == 0 and x == 3:
        y = 2
        return (x,y,10)
    match action:
        case 'u':
            if y > 0:
                y -= 1
                return (x,y,0)
            else:
                return (x,y,-1)
        case 'd':
            if y < 4:
                y += 1
                return (x,y,0)
            else:
                return (x,y,-1)
        case 'l':
            if x > 0:
                x -= 1
                return (x,y,0)
            else:
                return (x,y,-1)
        case 'r':
            if x < 4:
                x += 1
                return (x,y,0)
            else:
                return (x,y,-1)
    
for i in bellman_optimality_eqs(5):
    print(i)

# class Agent:
#     def __init__(self, policy):
#         self.policy = policy