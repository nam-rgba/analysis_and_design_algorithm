import scipy.stats as stats
from scipy.stats import norm, t
from itertools import chain, combinations;
def wPFI_Apriori(DB, w, msup, t , alpha):
    # create set of all item
    I=set(item for transaction in DB for item in transaction)
    WPFI=set()

    # scan and find size-1 wPFI
    WPFI1, mu1=Scan_Find_Size_k_wFPI(I, DB, w, msup, t, 1)
    print('wpi1',WPFI1)
    WPFI.update(WPFI1)

    k=2
    WPFIk_1=set()
    while WPFIk_1!=set():
        # Step 7: Scan and find size-k wPFI
        WPFIk, muk = Scan_Find_Size_k_wFPI(WPFI[k-1], DB, w, msup, t, k)
        
        # Step 8: Add size-k wPFI to WPFI
        WPFI.update(WPFI[k])
        
        k += 1

    return WPFI





def wPFI_Apriori_Gen(WPFI_k_minus_1, I, w, u, alpha, n, msup, t):
    Ck = []
    m = max(w.values())
    print('m: ',m)	
    F = norm.cdf(msup - 1)
    mu_hat = norm.ppf(1 - F) * t / m
    print('mu_hat: ',mu_hat)	
    
    # init I'
    I_prime={i for i in I if any(i.issubset(Y) for Y in WPFI_k_minus_1)}
    print('I_prime: ',WPFI_k_minus_1)	

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


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
def calculate_weighted_support(candidate, w):
    # Helper function to calculate the weighted support of a candidate
    return sum(w[item] for item in candidate)


def calculate_support(itemset, transactions):
    # Helper function to calculate the support of an itemset in a transaction
    for transaction in transactions:
        count=sum(1 for item in itemset if item in transaction)/len(transactions)
    return count

def is_weighted_probabilistic_frequent_itemset(itemset, weights, transactions, msup, t):
    # Helper function to check if a candidate is a weighted probabilistic frequent itemset
    weight=calculate_weighted_support(itemset, weights)
    support=calculate_support(itemset, transactions)
    return weight*support>=t and support>=msup

def Scan_Find_Size_k_wFPI(Ck, DB, w, msup, t):
    frequent_itemsets=[]
    muk={}

    for itemset in powerset(Ck):
        if is_weighted_probabilistic_frequent_itemset(itemset=itemset, weights=w, transactions=DB, msup=msup, t=t): 
            frequent_itemsets.append(itemset)
            if itemset not in muk:
                muk[itemset] = 1
            else:
                muk[itemset] += 1

    return frequent_itemsets, muk


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
# Hàm Scan_find_size là để check xem itemset X có phải weighted probabiltic frequent không
# 
# * #