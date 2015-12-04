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

def find_association_rules(freq_sets, minConf):
    """
    param: freq_sets
    type:  List[set]
    return: List[(from, to)]
    This function returns a list of pairs representing the association
    rules discovered.
    """
    pass

