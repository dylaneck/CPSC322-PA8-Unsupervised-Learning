import itertools
X_train = [
 ["b", "c", "m"],
 ["b", "c", "e", "m", "s"],
 ["b"],
 ["c", "e", "s"],
 ["c"],
 ["b", "c", "s"],
 ["c", "e", "s"],
 ["c", "e"]
]
X_train = [
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
def compute_unique_values(table):
            unique = []
            for row in table:
                for value in row: 
                    if value not in unique:
                        unique.append(value)
            return sorted(list(unique))

def prepend_attribute_label(table, header):
    for row in table:
        for i in range(len(row)):
                row[i] = header[i] + "=" + str(row[i])




        

# NOTE: apriori algorithm step 4 prune step: exame all susbets of c with k - 1 elements
def compute_k_minus_1_subsets(itemset):
    # or use itertools.combinations()
    subsets = []
    for i in range(len(itemset)):
        subsets.append(itemset[:i] + itemset[i + 1:])
    return subsets
def check_row_match(terms, row):
    # return 1 if all the terms are in the row (match)
    # return 0 otherwise
    for term in terms:
        print(term, row)
        if term not in row:
            return 0
    return 1


def compute_rule_counts(rule, table):
    Nleft = Nright = Nboth = 0
    Ntotal = len(table)
    for row in table:
        Nleft += check_row_match(rule["lhs"], row)
        print(Nleft)
        Nright += check_row_match(rule["rhs"], row)
        Nboth += check_row_match(rule["lhs"] + rule["rhs"], row)

    return Nleft, Nright, Nboth, Ntotal

def compute_rule_interestingness(rule, table):
    Nleft, Nright, Nboth, Ntotal = compute_rule_counts(rule, table)
    if Nleft == 0:
        rule["confidence"] = 0
    else:
        
        rule["confidence"] = Nboth / Nleft
    rule["support"] = Nboth / Ntotal
    if Nright == 0:
        rule["completeness"] = 0
    else:
        rule["completeness"] = Nboth / Nright
    return rule["confidence"], rule["support"], rule["completeness"]
    
def make_candidate_itemsets(itemsets):
    candidate_itemsets = []
    placeholder_candidate_itemsets = []
    for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
            l1 = list(itemsets[i])
            l2 = list(itemsets[j])
            l1.sort()
            l2.sort()
            if l1[:-1] == l2[:-1]:
                placeholder_candidate_itemsets.append((set(itemsets[i]).union(set(itemsets[j]))))
    for itemset in placeholder_candidate_itemsets:
        itemset = list(itemset)
        itemset.sort()
        candidate_itemsets.append(itemset)
    return candidate_itemsets


 
  
# NOTE: apriori lab task #4/5: generate confidenet rules using supported itemsets
def generate_apriori_rules(supported_itemsets, table, minconf):
    rules = []
    # for each itemset S in supported_itemsets
    # generate the 1 term RHSs and the corresponding LHSs
    # check confidence >= minconf => append to rules
    # move on to the 2 term RHS... len(S)-1 term RHS...
    for itemset in supported_itemsets:
        # generate the 1 term RHSs and the corresponding LHSs
        # check confidence >= minconf => append to rules
        for size in range(1, len(itemset)):
            rhss = itertools.combinations(itemset, size)
            for rhs in rhss:
            # check confidence >= minconf => append to rules
                rhs = sorted(list(rhs))
                lhs = sorted(list(set(itemset) - set(rhs)))
                confidence, support, completeness = compute_rule_interestingness({"lhs": lhs, "rhs": rhs}, table)
                if confidence >= minconf:
                    rules.append([lhs, rhs])
    return rules 
def check_support(itemset, table, minsup):
    # return 1 if the itemset is supported (>= minsup)
    # return 0 otherwise
    Nitemset = 0
    Ntotal = len(table)
    for row in table:
        Nitemset += check_row_match(itemset, row)
    return 1 if Nitemset / Ntotal >= minsup else 0
    

# NOTE: apriori lab task #3: find supported itemsets
def apriori(table, minsup, minconf):
    if table[0][0] != "b":
        header = []
        for i in range(len(table[0])):
            header.append("att" + str(i))
    
        prepend_attribute_label(table, header)
    # goal is to generate and return supported and confident rules
    I = compute_unique_values(table)
    print(I)
    supported_itemsets = []
    # TODO: finish apriori...
    # step 1. generate L1 supported itemsets of cardinality 1
    # to do this, use I
    L1 = []
    I = compute_unique_values(table)
    for item in I:
        if check_support([item], table, minsup):
            L1.append([item])
    
    prev = L1
    k = 2
    # TODO: step 3. while loop... while(Lkminus1 is not empty)
    
    while len(prev) > 0:
        # step 3.1. generate Ck from Lk-1
        ck = make_candidate_itemsets(prev)
        
        prev =[]
        for itemset in ck:
            
            
            confidence, support, completeness = compute_rule_interestingness({"lhs": itemset, "rhs": itemset}, table)
            if support >= minsup:
                supported_itemsets.append(itemset)
                prev.append(itemset)
                
                
            
        k+1


    
    rules = generate_apriori_rules(supported_itemsets, table, minconf)
    return rules 


rules = apriori(X_train, 0.2, 0.7)
print(rules) # TODO: check against your hand trace from apriori la

statement = ""
for rule in rules:
    lhs = ""
    rhs = ""
    lhs += "If val = " + str(rule[0][0])
    if len(rule[0]) > 1:
        for i in range(1, len(rule[0])):
            lhs += " AND val = " + str(rule[0][i])
    rhs += " THEN val = " + str(rule[1][0])
    if len(rule[1]) > 1:
        for i in range(1, len(rule[1])):
            rhs += " AND val = " + str(rule[1][i])
    statement += lhs + rhs + "\n"
    
print(statement)
