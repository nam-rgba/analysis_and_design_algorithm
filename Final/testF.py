import math
import numpy as np

def generate_mu_hat(msup, t, m):
    mu_hat = None
    for mu_candidate in range(1, int(1e6)):
        if 1 - 0.5 * (1 + math.erf((msup - 1 - mu_candidate) / math.sqrt(2))) < t / m:
            mu_hat = mu_candidate
            break

    if mu_hat is None:
        raise ValueError("No valid mu_hat found. Consider adjusting the range in the loop.")

    return mu_hat

# Example usage
w={'milk':0.4, 'fruit':0.9, 'video':0.6}

msup = 10
t = 5
m = np.max(list(w.values()))  # Assuming `w` is a dictionary of weights
mu_hat = generate_mu_hat(msup, t, m)
print(mu_hat)










# from itertools import product

# def calculate_probability(X, msup, database):
#     n = len(database)
    
#     possible_worlds = []
    
#     # Generate all possible worlds
#     for i in product(*[[(item, 1 - database[j][item]) for item in database[j]] for j in range(n)]):
#         possible_worlds.append(list(i))

#     # Find worlds where X is a subset and meets the support condition
#     satisfying_worlds = [world for world in possible_worlds if all(item in set(X) for item, _ in world) and sum(1 for _, prob in world if prob > 0) >= msup]

#     # Calculate the probability for each satisfying world
#     probabilities = [eval('*'.join(map(str, [1 - prob for _, prob in world]))) for world in satisfying_worlds]

#     # Calculate the total probability
#     total_probability = sum(probabilities)

#     return total_probability

# # Example usage:
# DB = [
#     {'milk': 0.4, 'fruit': 1.0, 'video': 0.3},
#     {'milk': 1.0, 'fruit': 0.8}
# ]

# X = {'milk', 'fruit'}
# msup = 2

# probability = calculate_probability(X, msup, DB)
# print(f'P(sup(X) ≥ msup): {probability:.3f}')
