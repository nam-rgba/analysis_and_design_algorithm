from scipy.stats import norm, t
from itertools import product, combinations;
import math

# Main algorithms
def wPFI_Apriori(DB, w, msup, t , alpha):
    # create set of all item
    I=set(item for transaction in DB for item in transaction)
    tempCk=[I]
    print('I:',I)
    WPFI=[[]]

    # Check if I is w-PFI or not
    WPFI1, mu1=Scan_Find_Size_k_wFPI(tempCk, DB, w, msup, t)
    print('wpi1',WPFI1)
    WPFI.append(WPFI1)
    k=2

    # # Cause anti-monotonicity of w-PFI, at least one itemset size k-1 must be w-PFI
    # while WPFI[k-1]!=[]:
    #     # Step 6: Generate size-k wPFI

    #     # Step 7: Scan and find size-k wPFI
    #     WPFIk, mu1 = Scan_Find_Size_k_wFPI(WPFI[k-1], DB, w, msup, t,k-1)
        
    #     # Step 8: Add size-k wPFI to WPFI
    #     WPFI.append(WPFIk)
    #     k += 1

    return WPFI





# Function to generate all subsets of a set with size k, algorithm 3
def wPFI_Apriori_Gen(WPFI_k_minus_1, I, muk_minus_1, w, alpha, n, msup, t):
    # Initialize
    Ck = []
    m = max(w.values())

    mu_hat = msup-1

    
    # init I'
    I_prime={i for i in I if any(i.issubset(Y) for Y in WPFI_k_minus_1)}
    print('I_prime: ',WPFI_k_minus_1)	

    # Loop
    for X in WPFI_k_minus_1:
        for i in (I_prime-{X}):
            # Check if w(X ∪ Ii) ≥ t
            if calculate_weighted_support(X.union(i),w) >= t:
                if min()>=mu_hat  :
                    Ck.add(X.union(i))
        #  Find the item I_m with the minimum weight in X
        I_m=min(X, key=lambda x:w[x])
        for i in (I-I_prime-{X}):
            # Check if w(X ∪ Ii) ≥ t and w(Ii) < w(I_m)
            if calculate_weighted_support(X.union(i), w)>=t and w[i]<w[I_m]:
                Ck.add(X.union(i))

    return Ck



# Helper function to generate all subsets of a set with size k

def powerset(s, k):
    result = [set(combination) for combination in combinations(s, k)]
    print(result)
    return result

def calculate_weighted_support(candidate, w):
    print("cate",candidate)
    # Helper function to calculate the weighted support of a candidate
    return sum(w[item] for item in candidate)/len(candidate)



# Helper function to calculate the support of an itemset in a transaction
def calculate_support(itemset, transactions):
    # Loop and count the number of times the itemset appears in the transaction
    for transaction in transactions:
        count=sum(1 for item in itemset if item in transaction)/len(transactions)
    return count



#Function to calculate the probability Pr(sup(X)>=msup)
def calculate_probability(X, msup, database):
    n = len(database)
    possible_worlds = []
    
    # Generate all possible worlds
    for i in product(*[[(item, 1 - database[j][item]) for item in database[j]] for j in range(n)]):
        possible_worlds.append(list(i))

    # Find worlds where X is a subset and meets the support condition
    satisfying_worlds = [world for world in possible_worlds if all(item in set(X) for item, _ in world) and sum(1 for _, prob in world if prob > 0) >= msup]

    # Calculate the probability for each satisfying world
    probabilities = [eval('*'.join(map(str, [1 - prob for _, prob in world]))) for world in satisfying_worlds]

    # Calculate the total probability
    total_probability = sum(probabilities)

    return total_probability


def is_weighted_probabilistic_frequent_itemset(itemset, weights, transactions, msup, t):
    print('itemset: ',itemset)
    # Helper function to check if a candidate is a weighted probabilistic frequent itemset
    weight=calculate_weighted_support(itemset, weights)
    support=calculate_probability(itemset, msup, transactions)
    print('support: ',support)
    # Pr(sup(X)>=msup)>=t/w(X)
    return weight*support>=t , support


# Find size-k wPFI based on definition 5
def Scan_Find_Size_k_wFPI(Ck, DB, w, msup, t):
    # Initialize
    frequent_itemsets=[]
    muk=[]

    for itemset in Ck:
        isW, mu = is_weighted_probabilistic_frequent_itemset(itemset, w, DB, msup, t)
        if isW:
            frequent_itemsets.append(itemset)
            muk.append(mu)

    return frequent_itemsets, muk


# Transaction Database
DB=[
    {'milk':0.4,'fruit':1.0,'video':0.3},
    {'milk':1.0,'fruit':0.8}
]
# Weights table
w={'milk':0.4, 'fruit':0.9, 'video':0.6}
# Minimum support
msup=2
# Threshold
t=0.2
# Scale factor
alpha=0.2


result = wPFI_Apriori(DB, w, msup, t, alpha)



