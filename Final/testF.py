from typing import List, Dict
from scipy.stats import norm, t

def generate_candidate_set(WPFIk_1, I, w, u, alpha, n, msup, t) :
    Ck = []
    m = max(w.values())
    print('m: ',m)	
    F = norm.cdf(msup - 1)
    mu_hat = norm.ppf(1 - F) * t / m
    print('mu_hat: ',mu_hat)	

    I_prime={i for i in I if any(i.issubset(Y) for Y in WPFIk_1)}

    print('I: ',I_prime)	

    for X in WPFIk_1:
        for I_i in set(I_prime) - set(X):
            if w[X + [I_i]] >= t:
                if min(u[X], u[I_i]) >= mu_hat and u[X] * u[I_i] >= alpha * n * mu_hat:
                    Ck.append(X + [I_i])
    X = min(WPFIk_1, key=lambda x: w[X])
    for I_i in set(I) - set(I_prime) - set(X):
        if w[X + [I_i]] >= t and w[I_i] < w[X]:
            if min(u[X], u[I_i]) >= mu_hat and u[X] * u[I_i] >= alpha * n * mu_hat:
                Ck.append(X + [I_i])
    return Ck

# Example usage:
WPFI_k_minus_1 = [{('A', 'B'), ('C',)}, {('A',), ('B', 'C')}]  # Example size-(k-1) WPFI set
weights = {'A': 0.5, 'B': 0.8, 'C': 0.7}
means = {'A': 0.3, 'B': 0.6, 'C': 0.5}
scale = 0.2
n = 100
msup = 0.4
t = 0.1
alpha = 0.7

Ck = generate_candidate_set(WPFI_k_minus_1, weights, means, scale, n, msup, t, alpha)
print("Size-k Weighted Probabilistic Frequent Itemset Candidate Set:", Ck)
