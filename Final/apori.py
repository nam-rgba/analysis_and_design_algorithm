import scipy.stats as stats
def wPFI_Apriori(DB, w, msup, t , alpha):
    # create set of all item
    I=set(item for transaction in DB for item in transaction)
    WPFI=set()

    # scan and find size-1 wPFI
    WPFI1, mu1=Scan_Find_Size_k_wPFI(I, DB, w, msup, t, 1)
    WPFI.update(WPFI1)

    k=2
    while WPFIk_minus_1 := set(wPFI_Apriori_Gen(WPFI, I, w, alpha, len(DB), msup, t, k)):
        # Step 7: Scan and find size-k wPFI
        WPFIk, muk = Scan_Find_Size_k_wPFI(WPFIk_minus_1, DB, w, msup, t, k)
        
        # Step 8: Add size-k wPFI to WPFI
        WPFI.update(WPFIk)
        
        k += 1

    return WPFI

def Scan_Find_Size_k_wPFI(Ck, DB, w, msup, t, k):
    WPFIk = set()
    muk = {}

    for transaction in DB:
        # Generate all subsets of the current transaction of size k
        subsets = powerset(transaction, k)
        
        for candidate_str in Ck:
            candidate = set(candidate_str.split(','))
            # Check if the candidate is a subset of the current transaction
            if candidate.issubset(transaction):
                # Calculate the weighted support for the candidate
                weighted_support = calculate_weighted_support(candidate, w)

                # Calculate the probability of support being greater than or equal to msup
                probability_support_ge_msup = calculate_probability_support_ge_msup(candidate, DB, msup)

                # Check if the weighted probabilistic support meets the threshold
                if weighted_support * probability_support_ge_msup >= t:
                    WPFIk.add(candidate)

                    # Update muk for the candidate
                    if candidate not in muk:
                        muk[candidate] = 1
                    else:
                        muk[candidate] += 1

    return WPFIk, muk

def powerset(s, k):
    # Helper function to generate all subsets of a set with size k
    result = [[]]
    for elem in s:
        result.extend([subset + [elem] for subset in result if len(subset) < k])
    return [frozenset(subset) for subset in result if len(subset) == k]

def wPFI_Apriori_Gen(WPFI_k_minus_1, I, w, u, alpha, n, msup, t):
    Ck=set()
    # maximum weight
    m=max(w.values())

    # mu hat
    mu_hat=None
    for mu_candicate in range (1, int(1e6)):
        if 1-stats.norm.cdf(msup-1,mu_candicate) < t/m:
            mu_hat=mu_candicate
            break
    if mu_hat is None:
        raise ValueError("No valid mu_hat found. Consider adjusting the range")
    
    # init I'
    I_prime={i for i in I if any(i.issubset(Y) for Y in WPFI_k_minus_1)}

    # Loop
    for X in WPFI_k_minus_1:
        for i in (I_prime-{X}):
            # Check if w(X ∪ Ii) ≥ t
            if calculate_weighted_support(X.union(i),w) >= t:
                if min(u[X],u[i])>=mu_hat and u[X]*u[i] >= alpha*n*mu_hat:
                    Ck.add(X.union(i))
        #  Find the item I_m with the minimum weight in X
        I_m=min(X, key=lambda x:w[x])
        for i in (I-I_prime-{X}):
            # Check if w(X ∪ Ii) ≥ t and w(Ii) < w(I_m)
            if calculate_weighted_support(X.union(i), w)>=t and w[i]<w[I_m]:
                #  Check the conditions for adding X ∪ Ii to Ck
                if min(u[X], u[i]) >= mu_hat and u[X] * u[i] >= alpha * n * mu_hat:
                    Ck.add(X.union(i))

    return Ck

def calculate_weighted_support(candidate, w):
    # Helper function to calculate the weighted support of a candidate
    return sum(w[item] for item in candidate)


def calculate_probability_support_ge_msup(candidate, DB, msup):
    # Helper function to calculate the probability of support being greater than or equal to msup
    count_support_ge_msup = sum(1 for transaction in DB if candidate.issubset(transaction))
    total_transactions = len(DB)
    return count_support_ge_msup / total_transactions


# Data set
DB = [
    {'milk','vegetable','soda'},
    {'milk','water','sausage','tropical fruit'},
    {'eggs','juice','soda','vegetable'}
]

# weight table
w={'milk':0.6, 'vegetable':0.8, 'soda':0.4, 'water':0.2, 'sausage':0.1, 'tropical fruit':0.2,'eggs':0.7 ,'juice':0.4}

msup=0.5
t=0.6
alpha=0.2

result = wPFI_Apriori(DB, w, msup, t, alpha)
print(result)


# *
# Definition 5 said: Từ 1 uncertain database, weight table w, minimum support msup, a probabilitic frequent
# threshold t, , an itemset X ⊆ I is a weighted probabilistic frequent itemset if and only if w(X)Pr(sup(X) ≥ msup) ≥ t
# Hàm wPFI_Apriori_Gen ở algorithms 1 chính là implementation của algorithm 3 :))
# 
# 
# * #