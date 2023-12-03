from scipy.stats import t
from itertools import product
import csv
import timeit 
import ast
from collections import Counter


# Main algorithms
def wPFI_Apriori(DB: list, w: dict, msup:int, t:float , alpha:float)->list:
    # Function to find w-PFI
    # Input: 
        # DB: list of transactions
        # w: dictionary of weights
        # msup: minimum support
        # t: threshold
        # alpha: confidence
    # Output:
        # WPFI: list of w-PFI itemsets


    # create set of all item
    I:set=set(item for transaction in DB for item in transaction)
    tempCk: list=[I]
    WPFI: list=[[]]
    mu:list=[[]]

    # Check if I is w-PFI or not

    WPFI1, mu1=Scan_Find_Size_k_wFPI(DB, tempCk, w, msup, t,2)
    WPFI.append(WPFI1)
    mu.append(mu1)
    k: int=2

    # Cause anti-monotonicity of w-PFI, at least one itemset size k-1 must be w-PFI
    while WPFI[k-1]!=[]:
        # Step 6: Generate size-k wPFI
        # Ck=wPFI_Apriori_Gen(WPFI[k-1], I, mu, w, alpha, len(DB), msup, t)
        Ck=exact_apriori(WPFI[k-1], I, w, t)
        # Step 7: Scan and find size-k wPFI
        WPFIk, muk = Scan_Find_Size_k_wFPI(DB,Ck, w, msup, t,2)
        
        # Step 8: Add size-k wPFI to WPFI
        WPFI.append(WPFIk)
        mu=muk
        k += 1

    return WPFI





def wPFI_Apriori_Gen(WPFI_k_minus_1: list, I:set, mu:list, w:dict, alpha:float, n:int, msup:int, t:float)->list:
    # Function to generate candidates for wPFI using Apriori framework, algorithm 3
    # Input: 
        # WPFI_k_minus_1: list of w-PFI itemsets of size k-1
        # I: set of all items
        # mu: list of mean U
        # w: dictionary of weights
        # alpha: confidence
        # n: number of transactions
        # msup: minimum support
        # t: threshold
    # Output: List of candidates


    # Initialize
    Ck:list = [] # List of (set) candidate itemsets
    m:float = max(w.values())
    mu_hat:float = msup-1

    
    # init I'
    I_prime={i for i in I if i  in WPFI_k_minus_1} # I', set of itemsets with at least one item in WPFI_k_minus_1

    # Loop
    for X in WPFI_k_minus_1:
        print('X line 52:' ,X)
        for i in (I_prime-X):
            # Check if w(X ∪ Ii) ≥ t
            if calculate_weighted_support(X.union(i),w) >= t:
                if min(mu[WPFI_k_minus_1.index(X)], mu[I_prime.index(i)])>=mu_hat and  mu[WPFI_k_minus_1.index(X)]* mu[I_prime.index(i)]>=alpha*n*mu_hat :
                    # Check the conditions for adding X ∪ Ii to Ck
                    Ck.add(X.union(i))
        #  Find the item I_m with the minimum weight in X
        I_m=min(X, key=lambda x:calculate_weighted_support({x}, w))
        for i in (I-I_prime-X):
            # Check if w(X ∪ Ii) ≥ t and w(Ii) < w(I_m)
            if calculate_weighted_support(X.union(i), w)>=t and calculate_weighted_support(i, w)<w[I_m]:
                if min(mu[WPFI_k_minus_1.index(X)], mu[I_prime.index(i)])>=mu_hat and  mu[WPFI_k_minus_1.index(X)]* mu[I_prime.index(i)]>=alpha*n*mu_hat:
                    # Check the conditions for adding X ∪ Ii to Ck
                    Ck.add(X.union(i))
    print('Ck: ',Ck)
    return Ck


def exact_apriori(WPFI_k_minus_1: list, I: set, w: dict, t: float):
    # Function to generate candidates for wPFI using Apriori framework, algorithm 2
    # Input:
        # WPFI_k_minus_1: list of w-PFI itemsets of size k-1
        # I: set of all items
        # w: dictionary of weights
        # t: threshold
    # Output: List of candidates

    ck:list=[]
    I_prime:set = {i for Y in WPFI_k_minus_1 for i in I if i in Y}
    # I', set of itemsets with at least one item in WPFI_k_minus_1
    for X in WPFI_k_minus_1:
        for i in I_prime-X:
            if calculate_weighted_support(X.Union(i),w)>=t:
                ck.add(X.union(i))
        #  Find the item I_m with the minimum weight in X
        I_m=min(X, key=lambda x:calculate_weighted_support({x}, w))
        for i in I-I_prime-X:
            if calculate_weighted_support(X.Union(i))>=t and calculate_weighted_support({i},w)<=w[I_m]:
                ck.add(X.union(i))

    return ck

def calculate_weighted_support(candidate: list, w: dict)->float:
    # Helper function to calculate the weighted support of a candidate
    # Input: 
        # candidate: list of items
        # w: dictionary of weights
    # Output: avaerage weight of the candidate

    return sum(w[item] for item in candidate)/len(candidate)



def calculate_support(itemset:set, transactions:list)->float:
    # Helper function to calculate the support of an itemset in a transaction
    # Input:
        # itemset: list of items
        # transactions: list of transactions
    # Output: support of the itemset
    # Loop and count the number of times the itemset appears in the transaction
    for transaction in transactions:
        count: float=sum(1 for item in itemset if item in transaction)/len(transactions)
    return count



def calculate_probability(X: set, msup: int, database:list)->float:
    # Function to calculate the probability Pr(sup(X)>=msup)
    # Input:
        # X: set of items
        # msup: minimum support
        # database: list of transactions
    # Output: probability Pr(sup(X)>=msup)


    n:int = len(database)
    possible_worlds:list = []
    
    # Generate all possible worlds
    for i in product(*[[(item, 1 - database[j][item]) for item in database[j]] for j in range(n)]):
        possible_worlds.append(list(i))

    # Find worlds where X is a subset and meets the support condition
    satisfying_worlds:list = [world for world in possible_worlds if all(item in set(X) for item, _ in world) and sum(1 for _, prob in world if prob > 0) >= msup]

    # Calculate the probability for each satisfying world
    probabilities:list = [eval('*'.join(map(str, [1 - prob for _, prob in world]))) for world in satisfying_worlds]

    # Calculate the total probability
    total_probability:float = sum(probabilities)

    return total_probability


def is_weighted_probabilistic_frequent_itemset(itemset, weights, transactions, msup, t):
    # Helper function to check if a candidate is a weighted probabilistic frequent itemset
    # Input:
        # itemset: candidate
        # weights: dictionary of weights
        # transactions: list of transactions
        # msup: minimum support
        # t: threshold
    # Output: boolean to check if Ck is a weighted probabilistic frequent itemset

    weight=calculate_weighted_support(itemset, weights)
    support=calculate_probability(itemset, msup, transactions)
    # Pr(sup(X)>=msup)>=t/w(X)
    return weight*support>=t , support


def Scan_Find_Size_k_wFPI( DB: list,Ck: list, w: dict, msup:int, t: float,prop: int)->list:
    # Function to find size-k wPFI based on definition 5
    # Input:
        # DB: list of transactions
        # Ck: candidates
        # w: dictionary of weights
        # msup: minimum support
        # t: threshold
        # prop: 1 or 2, flag to choose which algorithm to use
    # Output: List of frequent itemsets that are wPFI
    # Initialize
    frequent_itemsets: list=[]
    muk:list=[]

    for itemset in Ck:
        # If flag 1, use is_weighted_probabilistic_frequent_itemset
        if prop==1:
            isW, mu = is_weighted_probabilistic_frequent_itemset(itemset,w, DB, msup,t)
            if isW:
                frequent_itemsets.append(itemset)
                muk.append(mu)
        # If flag 2, use isWPFI
        if prop==2:
            isW, mu = isWPFI(itemset, DB, msup)
            if isW:
                frequent_itemsets.append(itemset)
                muk.append(mu)

    return frequent_itemsets, muk



def meanU(X: set, DB:list)->float:
    # Function to calculate the mean support of an itemset
    # Input:
        # X: set of items
        # DB: list of transactions
    # Output: mean support
    result:float=0
    for transcation in DB:
        if X.issubset(transcation.keys()):
            pr=1
            for x in X:
                pr*=transcation[x]
            result+=pr
    return result

def isWPFI(Ck:set, DB:list, msup:int)->bool:
    # Helper function to check if a candidate is a weighted probabilistic frequent itemset
    # Input:
        # Ck: candidate
        # DB: transaction database
        # msup: minimum support
    # Output: boolean to check if Ck is a weighted probabilistic frequent itemset and mu
    mu:float = meanU(Ck, DB)
    mu_hat:int =msup-1
    return mu>=mu_hat, mu



# Transaction Database
DB=[
    {'milk':0.4,'fruit':1.0,'video':0.3},
    {'milk':1.0,'fruit':0.8}
]
X={'milk', 'fruit'}
print(meanU(X, DB))
# Weights table
w={'milk':0.4, 'fruit':0.9, 'video':0.6}
# Minimum support
msup=1
# Threshold
t=0.2
# Scale factor
alpha=0.2


def read_first_100_rows(input_file_path):
    #  function to read the first 100 rows of a file
    try:
        data_list = []

        with open(input_file_path, 'r') as infile:
            reader = csv.reader(infile, delimiter=' ')

            # Read the first 10 rows
            for _ in range(10):
                row = next(reader, None)
                if row is not None:
                    data_list.append(ast.literal_eval(row[0]))

        return data_list

    except FileNotFoundError:
        print(f"File not found: {input_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def read_weight_file(file_path):
    # Function to read the weights from a file
    try:
        weight_dict = {}

        # Read the weights from the file
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into item and weight
                
                item_str, weight_str = line.strip().split(':')
                item = int(item_str.strip())
                weight = float(weight_str)
                # item=int(item)
                
                # Add the item and weight to the dictionary
                weight_dict[item] = round(weight*10,2)

        return weight_dict

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




weight_file_path = 'weight.csv' 
weight_dictionary = read_weight_file(weight_file_path) 
input_file_path = 'sample.csv'  
first_100_rows = read_first_100_rows(input_file_path)






result = wPFI_Apriori(first_100_rows, weight_dictionary, msup, t, alpha)
print(result)


# benchmark the task
time = timeit.timeit('wPFI_Apriori(first_100_rows, weight_dictionary, msup, t, alpha)', globals=locals(), number=6000)
# report the result
print(f'Took {time:.3f} seconds')



