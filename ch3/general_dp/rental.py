from dynpro import *
import numpy as np
import math
import scipy as sp
import time

class CarRental(MDP):
    def __init__(self, gamma = 0.9, rent_lambda_1=3, return_lambda_1 = 3, rent_lambda_2 = 4, return_lambda_2 = 2) -> None:
        states = {(loc1_car,loc2_car) for loc1_car in range(21) for loc2_car in range(21)}
        super().__init__(states, gamma)
        self.rent_lambda_1 = rent_lambda_1
        self.return_lambda_1 = return_lambda_1
        self.rent_lambda_2 = rent_lambda_2
        self.return_lambda_2 = return_lambda_2
        
    def actions(self, state):
        loc1_cars, loc2_cars = state
        pos_move = min(loc1_cars, 5)
        neg_move = max(-5, -loc2_cars)
        return list(range(neg_move, pos_move+1))
    
    def dynamics(self, state, action):
        loc1_cars, loc2_cars = state
        moved = 0
        if action > 0:
            if loc1_cars >= action:
                loc1_cars -= action
                loc2_cars += action
                moved = abs(action)
            else:
                moved = loc1_cars
                loc2_cars += loc1_cars
                loc1_cars = 0
        elif action < 0:
            if loc2_cars >= -action:
                loc1_cars -= action
                loc2_cars += action
                moved = abs(action)
            else:
                moved = loc2_cars
                loc1_cars += loc2_cars
                loc2_cars = 0
        else:
            pass
        loc1_cars = min(20, loc1_cars)
        loc2_cars = min(20, loc2_cars)
        # print(loc1_cars, loc2_cars, moved)
        rented_1 = {n:float(sp.stats.poisson.pmf(n, self.rent_lambda_1)) for n in range(loc1_cars)}
        rented_2 = {n:float(sp.stats.poisson.pmf(n, self.rent_lambda_2)) for n in range(loc2_cars)}
        rented_1[loc1_cars] = 1 - sum(rented_1.values())
        rented_2[loc2_cars] = 1 - sum(rented_2.values())
        returned_1 = {n:float(sp.stats.poisson.pmf(n, self.return_lambda_1)) for n in range(1 + 3*self.return_lambda_1)}
        returned_2 = {n:float(sp.stats.poisson.pmf(n, self.return_lambda_2)) for n in range(1 + 3*self.return_lambda_2)}
        
        remaining_1 = {}
        for (n1,p1) in rented_1.items():
            for (n2,p2) in returned_1.items():
                key = (min(20, loc1_cars + n2 - n1), 10*n1)
                value = p1 * p2
                if key in remaining_1:
                    remaining_1[key] += value
                else:
                    remaining_1[key] = value
        remaining_2 = {}
        for (n1,p1) in rented_2.items():
            for (n2,p2) in returned_2.items():
                key = (min(20, loc2_cars + n2 - n1), 10*n1)
                value = p1 * p2
                if key in remaining_2:
                    remaining_2[key] += value
                else:
                    remaining_2[key] = value
        remaining = {}
        for ((c1, r1), p1) in remaining_1.items():
            for ((c2, r2),p2) in remaining_2.items():
                key = ((c1,c2), r1 + r2 - 4*moved)
                value = p1 * p2
                if key in remaining:
                    remaining[key] += value
                else:
                    remaining[key] = value
        to_delete = []
        for (k,v) in remaining.items():
            if v < 1e-4:
                to_delete.append(k)
        for k in to_delete:
            del remaining[k]
        return remaining
car_rental = CarRental()
policy = UniformRandom(car_rental)
values = evaluate_policy(car_rental, policy, threshold=100)
print(values)

# optimal_policy = find_optimal_policy(car_rental)
# print([f"{s}:{v:.1f}" for (s,v) in evaluate_policy(car_rental, optimal_policy, 0.001).items()])