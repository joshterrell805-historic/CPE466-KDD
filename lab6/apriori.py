def find_frequent_itemsets(data, max_val, minSup):
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
    F_k = frozenset(frozenset([col]) for col in range(max_val) if support({col}, data) >= minSup)
    k = 1
    while len(F_k) > 0:
        candidates, unused = candidate_generate(F_k, k)
        F.extend(unused)
        count = [0 for i in candidates]
        for row in data:
            for j, candidate in enumerate(candidates):
                if subset(candidate, row):
                    count[j] += 1
        F_k_next = []
        tossed = []
        n = float(len(data))
        for i, candidate in enumerate(candidates):
            if count[i]/n >= minSup:
                F_k_next.append(candidate)
            else:
                tossed.append(candidate)
        tossed_subsets = set()
        for failure in tossed:
            tossed_subsets |= subsets(failure, F_k)
        for fnext in F_k_next:
            tossed_subsets = [passed for passed in tossed_subsets if not subset(passed, fnext)]
        F.extend(tossed_subsets)
        k += 1
        F_k = frozenset(F_k_next)
    return F

def support(cols, data):
    supporting = sum(1 for row in data if subset(cols, row))
    return supporting/len(data)
    
def subset(sub, sup):
    return len(sub - sup) == 0

def subsets(sup, sub = False):
    subs = frozenset(frozenset(sup - {i}) for i in sup)
    if sub:
        return subs & sub
    else:
        return subs

def candidate_generate(F, k):
    candidates = set()
    unused = []
    for f_1 in F:
        used = False
        for f_2 in F:
            c = f_1 | f_2
            if len(c) == k + 1:
                flag = True
                subs = subsets(c)
                for sub in subs:
                    if not sub in F:
                        flag = False
                        break
                if flag == True:
                    used = True
                    candidates.add(c)
        if not used:
            unused.append(f_1)
    return (candidates, unused)

def find_association_rules(data, freq_sets, minConf):
    """
    param: freq_sets
    type:  List[set]
    return: List[(from, to)]
    This function returns a list of pairs representing the association
    rules discovered.
    """
    rules = []
    for s in freq_sets:
        if len(s) < 2:
            continue
        for i in s:
            l = s - {i}
            r = i
            if support(s, data)/support(l, data) >= minConf:
                rules.append((l, r))
    return rules
