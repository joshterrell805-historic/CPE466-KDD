import random
import tabulate
import c45
import itertools

def precision(expected, actual, positive):
    # expected = correct label
    # actual = predicted label
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == positive and a == positive)
    FP = sum(1 for e, a in paired if e != positive and a == positive)
    return TP / (TP + FP)

def recall(expected, actual, positive):
    paired = list(zip(expected, actual))
    TP = sum(1 for e, a in paired if e == positive and a == positive)
    FN = sum(1 for e, a in paired if e == positive and a != positive)
    return TP / (TP + FN)

def pf(expected, actual, positive):
    paired = list(zip(expected, actual))
    FP = sum(1 for e, a in paired if e != a and a == positive)
    TN = sum(1 for e, a in paired if e == a and a != positive)
    return FP / (FP + TN)

def f_measure(expected, actual, positive):
    prec = precision(expected, actual, positive)
    rec = recall(expected, actual, positive)
    return (2 * prec * rec) / (prec + rec)

def accuracy(expected, actual):
    paired = list(zip(expected, actual))
    Dtrue = sum(1 for e, a in paired if e == a)
    return float(Dtrue) / float(len(expected))

def error_rate(expected, actual):
    return 1 - accuracy(expected, actual)

def hunk(data, hunkcount):
    if hunkcount == 0:
        return [data]
    if hunkcount == -1:
        return [[i] for i in data]
    hunksize = int(len(data)/hunkcount)
    hunkable = list(data)
    random.shuffle(hunkable)
    hunks = []
    for start in range(0, len(data), hunksize):
        hunks.append(hunkable[start:start + hunksize])
    return hunks

def pull_each(data):
    """ Returns an iterator over data which returns pairs consisting
    of each element paired with a list containing all the other
    elements of data"""
    return ((i, [j for j in data if j != i]) for i in data)

def confusion_matrix(expected, actual):
    expected_classes = set(expected)
    actual_classes = set(actual)
    return tabulate.tabulate(
        [[''] + ['pred_{}'.format(ac) for ac in actual_classes]] +
        [['true_{}'.format(ec)] + [
            sum(1 for a,e in zip(actual,expected) if a == ac and e == ec)
            for ac in actual_classes
        ] for ec in expected_classes],
        tablefmt='psql'
    )

def cross_validate(data, attributes, manifold):
    hunks = hunk(data, manifold)
    itr = pull_each(hunks)
    actual = []
    expected = []
    actual_hunked = []
    expected_hunked = []
    for elem, rest in itr:
        tree = c45.run(elem, list(enumerate(attributes)), 0.05)
        results = [tree.classify(r[0], attributes) for r in itertools.chain(*rest)]
        correct = [r[1] for r in itertools.chain(*rest)]
        actual_hunked.append(results)
        expected_hunked.append(correct)
        actual.extend(results)
        expected.extend(correct)
    return (expected, actual, expected_hunked, actual_hunked)
