
def wPFI_Apriori(DB, w, msup, t , alpha):
    # create set of all item
    I=set(item for transaction in DB for item in transaction)
    WPFI=set()

    # scan and find size-1 wPFI
    WPFI1, mu1=Scan_Find_Size_k_wPFI(I, DB, w, msup, t, 1)
    WPFI.update(WPFI1)

    k=2
    while WPFIk_minus_1 := set(wPFI_Apriori_Gen(WPFI, I, mu1, w, alpha, len(DB), msup, t, k)):
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

        for candidate in Ck:
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

def wPFI_Apriori_Gen(WPFI, I, muk_minus_1, w, alpha, n, msup, t, k):
    Ck = set()

    # Generate candidate itemsets of size k using the standard Apriori technique
    for itemset1 in WPFI:
        for itemset2 in WPFI:
            if len(itemset1.union(itemset2)) == k and len(itemset1.intersection(itemset2)) == k - 2:
                candidate = itemset1.union(itemset2)

                # Prune the candidate if any subset of size k-1 is not in WPFI
                prune_flag = False
                for subset in powerset(candidate, k - 1):
                    if subset not in WPFI:
                        prune_flag = True
                        break

                if not prune_flag:
                    Ck.add(candidate)

    # Calculate the weighted support for each candidate
    for candidate in Ck:
        weighted_support = calculate_weighted_support(candidate, w)

        # Calculate the probability of support being greater than or equal to msup
        probability_support_ge_msup = calculate_probability_support_ge_msup(candidate, WPFI, msup)

        # Check if the weighted probabilistic support meets the threshold
        if weighted_support * probability_support_ge_msup >= t:
            # Check if the candidate satisfies the weight constraint
            if weighted_support / (alpha * n) >= t / (alpha * n * weighted_support):
                yield candidate
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


