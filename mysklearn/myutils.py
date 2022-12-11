# TODO: your reusable general-purpose functions here
def remove_columns(data, columns, table):
   
    for i in range(len(columns)):
        
        for j in range(len(data)):
            
            data[j].pop(columns[i] - i)
    col_names = []
    for i in range(len(table.column_names)):
        if i in columns:
            col_names.append(table.column_names[i])
    print(col_names)
    for i in range(len(col_names)):
        if col_names[i] in table.column_names:
            table.column_names.remove(col_names[i])


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