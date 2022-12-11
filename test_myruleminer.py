import numpy as np

from mysklearn.myruleminer import MyAssociationRuleMiner

# note: order is actual/received student value, expected/solution
def test_association_rule_miner_fit():
    X_train1 = [
 ["b", "c", "m"],
 ["b", "c", "e", "m", "s"],
 ["b"],
 ["c", "e", "s"],
 ["c"],
 ["b", "c", "s"],
 ["c", "e", "s"],
 ["c", "e"]
]
    rule_miner = MyAssociationRuleMiner()
    rule_miner.fit(X_train1)
    
    ans1 = [[['m'], ['b']], [['e'], ['c']], [['m'], ['c']], [['s'], ['c']], [['c', 'm'], ['b']], [['b', 'm'], ['c']], [['m'], ['b', 'c']], [['b', 's'], ['c']], [['e', 's'], ['c']]]
    
    assert(rule_miner.rules == ans1)
    
    X_train = X_train = [
            ["Senior", "Java", "no", "no"],
            ["Senior", "Java", "no", "yes"],
            ["Mid", "Python", "no", "no"],
            ["Junior", "Python", "no", "no"],
            ["Junior", "R", "yes", "no"],
            ["Junior", "R", "yes", "yes"],
            ["Mid", "R", "yes", "yes"],
            ["Senior", "Python", "no", "no"],
            ["Senior", "R", "yes", "no"],
            ["Junior", "Python", "yes", "no"],
            ["Senior", "Python", "yes", "yes"],
            ["Mid", "Python", "no", "yes"],
            ["Mid", "Java", "yes", "no"],
            ["Junior", "Python", "no", "yes"]
        ]
    
    rule_miner = MyAssociationRuleMiner(.2, .7)
    
    rule_miner.fit(X_train)
    
    ans2 = [[['att2=no'], ['att1=Python']], [['att1=Python'], ['att2=no']], [['att1=R'], ['att2=yes']], [['att2=no', 'att3=no'], ['att1=Python']], [['att1=Python', 'att3=no'], ['att2=no']]]
    
    assert(rule_miner.rules == ans2)
