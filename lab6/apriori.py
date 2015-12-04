def find_frequent_itemsets(data, minSup):
    """
    return: List[set]
    This is apriori
    """
    # Note that any time we throw out a set for insufficient support,
    # all the subsets which appear uniquely in it (i.e., are not
    # subsets of any other itemset) are now considered skyline
    # frequent itemsets (because there's no superset of them which can
    # appear)
    F = []
    F_k = [set(row) for i, row in data.iterrows() if support(i) >= minSup]
    k = 1
    while len(F_k) > 0:
        candidates = candidate_generate(F_k, k)
        count = []
        for i, row in data.iterrows():
            for j, candidate in enumerate(candidates):
                if subset(candidate, row):
                    count[j] += 1
        F_k_next = []
        tossed = []
        for i, candidate in enumerate(candidates):
            if count[i]/n >= minSup:
                F_k_next.append(candidate)
            else:
                tossed.append(candidate)
        tossed_subsets = set()
        for failure in tossed:
            tossed_subsets.add(subsets(failure, F_k))
        for fnext in F_k_next:
            tossed_subsets = [passed for passed in tossed_subsets if not subset(passed, fnext)]
        F.append(*tossed_subsets)
        k += 1

def subset(sub, sup):
    return len(symdiff(sub, sup)) == 0

def subsets(sup, sub):
    subs = [symdiff(sup, set(i)) for i in sup]
    return intersect(subs, sub)

def find_association_rules(freq_sets, minConf):
    """
    param: freq_sets
    type:  List[set]
    return: List[(from, to)]
    This function returns a list of pairs representing the association
    rules discovered.
    """
    rules = []
    for s in freq_sets:
        for i in s:
            rules.append((symdiff(s, set(i)), i))

def candidate_generate(F, k):
    candidates = set()
    for f_1 in F:
        for f_2 in F:
            c = union(f_1, f_2)
            if len(c) == k + 1:
                flag = True
                subs = [symdiff(c, set(i)) for i in sup]
                for sub in subs:
                    if not sub in F:
                        flag = False
                        break
                if flag == True:
                    candidates.add(c)
