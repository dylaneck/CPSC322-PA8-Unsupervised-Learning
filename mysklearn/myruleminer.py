from mysklearn import myutils
import itertools
class MyAssociationRuleMiner:
    """Represents an association rule miner.

    Attributes:
        minsup(float): The minimum support value to use when computing supported itemsets
        minconf(float): The minimum confidence value to use when generating rules
        X_train(list of list of obj): The list of training instances (samples)
                The shape of X_train is (n_train_samples, n_features)
        rules(list of dict): The generated rules

    Notes:
        Implements the apriori algorithm
        Terminology: instance = sample = row and attribute = feature = column
    """
    def __init__(self, minsup=0.25, minconf=0.8):
        """Initializer for MyAssociationRuleMiner.

        Args:
            minsup(float): The minimum support value to use when computing supported itemsets
                (0.25 if a value is not provided and the default minsup should be used)
            minconf(float): The minimum confidence value to use when generating rules
                (0.8 if a value is not provided and the default minconf should be used)
        """
        self.minsup = minsup
        self.minconf = minconf
        self.X_train = None
        self.rules = None

    def fit(self, X_train):
        """Fits an association rule miner to X_train using the Apriori algorithm.

        Args:
            X_train(list of list of obj): The list of training instances (samples)
                The shape of X_train is (n_train_samples, n_features)

        Notes:
            Store the list of generated association rules in the rules attribute
            If X_train represents a non-market basket analysis dataset, then:
                Attribute labels should be prepended to attribute values in X_train
                    before fit() is called (e.g. "att=val", ...).
                Make sure a rule does not include the same attribute more than once
        """
                # NOTE: apriori lab task #1: find the set I
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
                
                if term not in row:
                    return 0
            return 1


        def compute_rule_counts(rule, table):
            Nleft = Nright = Nboth = 0
            Ntotal = len(table)
            for row in table:
                Nleft += check_row_match(rule["lhs"], row)
                
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
            rules = generate_apriori_rules(supported_itemsets, X_train, self.minconf)
    
            return rules


        self.rules = apriori(X_train, self.minsup, self.minconf)
      
                
    

    def print_association_rules(self, X_train):
        """Prints the association rules in the format "IF val AND ... THEN val AND...", one rule on each line.

        Notes:
            Each rule's output should include an identifying number, the rule, the rule's support,
            the rule's confidence, and the rule's lift
            Consider using the tabulate library to help with this: https://pypi.org/project/tabulate/
        """
        statement = ""
        for rule in self.rules:
            confidence, support, lift = myutils.compute_rule_interestingness({"lhs": rule[0],"rhs": rule[1]}, X_train)
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
            statement += lhs + rhs + "   Confidence: " +str(confidence) + "    Support: " + str(support) + "   Lift: " + str(lift) + "\n"
            
            
        print(statement)
