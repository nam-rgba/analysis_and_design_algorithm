import math

def powerset(s, k):
    # Helper function to generate all subsets of a set with size k
    result = [[]]
    for elem in s:
        result.extend([subset + [elem] for subset in result if len(subset) < k])
    return [frozenset(subset) for subset in result if len(subset) == k]

def calculate_weighted_support(candidate, w):
    # Helper function to calculate the weighted support of a candidate
    return sum(w[item] for item in candidate)

def calculate_probability_support_ge_msup(candidate, DB, msup):
    # Helper function to calculate the probability of support being greater than or equal to msup
    count_support_ge_msup = sum(1 for transaction in DB if candidate.issubset(transaction))
    total_transactions = len(DB)
    return count_support_ge_msup / total_transactions

def wPFI_Apriori_Gen(WPFI_k_minus_1, I, muk_minus_1, w, alpha, n, msup, t, k):
    Ck = set()

    # Generate candidate itemsets of size k using the standard Apriori technique
    for itemset1 in WPFI_k_minus_1:
        for itemset2 in WPFI_k_minus_1:
            if len(itemset1.union(itemset2)) == k and len(itemset1.intersection(itemset2)) == k - 2:
                candidate = itemset1.union(itemset2)

                # Prune the candidate if any subset of size k-1 is not in WPFI_k_minus_1
                prune_flag = False
                for subset in powerset(candidate, k - 1):
                    if subset not in WPFI_k_minus_1:
                        prune_flag = True
                        break

                if not prune_flag:
                    Ck.add(','.join(sorted(candidate)))

    # Calculate the weighted support for each candidate
    for candidate_str in Ck:
        candidate = set(candidate_str.split(','))  # Convert the candidate string to a set
        weighted_support = calculate_weighted_support(candidate, w)

        # Calculate the probability of support being greater than or equal to msup
        probability_support_ge_msup = calculate_probability_support_ge_msup(candidate, WPFI_k_minus_1, msup)

        # Check if the weighted probabilistic support meets the threshold
        if weighted_support * probability_support_ge_msup >= t:
            # Check if the candidate satisfies the weight constraint
            if weighted_support / (alpha * n) >= t / (alpha * n * weighted_support):
                yield candidate_str

def generate_size_k_weighted_PFI_candidates(WPFI_k_minus_1, I, w, u, alpha, n, msup, t, k):
    Ck = set()

    # Step 2: Calculate the maximum weight in w
    m = max(w.values())

    # Step 3: Calculate μ^ using the error function
    mu_hat = None
    for mu_candidate in range(1, int(1e6)):  # Adjust the range based on your requirements
        if 1 - 0.5 * (1 + math.erf((msup - 1 - mu_candidate) / math.sqrt(2))) < t / m:
            mu_hat = mu_candidate
            break

    if mu_hat is None:
        raise ValueError("No valid mu_hat found. Consider adjusting the range in the loop.")

    # Step 4: Initialize I'
    I_prime = {Ii for Ii in I if any(Ii.issubset(Y) for Y in WPFI_k_minus_1)}

    # Step 5: Iterate over itemsets X in WPFI_k_minus_1
    for X_str in WPFI_k_minus_1:
        X = set(X_str.split(','))  # Convert the X string to a set

        # Step 6: Iterate over each item Ii in I_prime - X
        for Ii_str in (I_prime - {X_str}):
            Ii = set(Ii_str.split(','))  # Convert the Ii string to a set

            # Step 7: Check if w(X ∪ Ii) ≥ t
            if calculate_weighted_support(X.union(Ii), w) >= t:
                # Step 8: Check the conditions for adding X ∪ Ii to Ck
                if min(u[X], u[Ii]) >= mu_hat and u[X] * u[Ii] >= alpha * n * mu_hat:
                    Ck.add(','.join(sorted(X.union(Ii))))  # Convert the candidate set back to a string

        # Step 13: Find the item I_m with the minimum weight in X
        I_m_str = min(X, key=lambda x: w[x])

        # Step 14: Iterate over each item Ii in I - I_prime - X
        for Ii_str in (I - I_prime - {X_str}):
            Ii = set(Ii_str.split(','))  # Convert the Ii string to a set

            # Step 15: Check if w(X ∪ Ii) ≥ t and w(Ii) < w(I_m)
            if calculate_weighted_support(X.union(Ii), w) >= t and w[Ii_str] < w[I_m_str]:
                # Step 16: Check the conditions for adding X ∪ Ii to Ck
                if min(u[X], u[Ii]) >= mu_hat and u[X] * u[Ii] >= alpha * n * mu_hat:
                    Ck.add(','.join(sorted(X.union(Ii))))  # Convert the candidate set back to a string

    return Ck

# Data set
DB = [
    {'milk', 'vegetable', 'soda'},
    {'milk', 'water', 'sausage', 'tropical fruit'},
    {'eggs', 'juice', 'soda', 'vegetable'}
]

# Item set
I = {'milk', 'vegetable', 'soda', 'water', 'sausage', 'tropical fruit', 'eggs', 'juice'}

# Weight table
w = {'milk': 0.6, 'vegetable': 0.8, 'soda': 0.4, 'water': 0.2, 'sausage': 0.1, 'tropical fruit': 0.2, 'eggs': 0.7, 'juice': 0.4}

# Parameters
msup = 0.5
t = 0.6
alpha = 0.2
n = len(DB)

# Step 1: Generate size-1 wPFI
WPFI1 = set()
for item in I:
    if calculate_weighted_support({item}, w) >= t:
        WPFI1.add(item)

# Print size-1 wPFI
print("Size-1 wPFI:")
print(WPFI1)

# Step 2: Generate size-2 wPFI candidates
WPFI2_candidates = list(wPFI_Apriori_Gen(WPFI1, I, {}, w, alpha, n, msup, t, 2))

# Print size-2 wPFI candidates
print("\nSize-2 wPFI candidates:")
print(WPFI2_candidates)

# Step 3: Generate size-2 wPFI
WPFI2 = generate_size_k_weighted_PFI_candidates(WPFI1, I, w, {}, alpha, n, msup, t, 2)

# Print size-2 wPFI
print("\nSize-2 wPFI:")
print(WPFI2)