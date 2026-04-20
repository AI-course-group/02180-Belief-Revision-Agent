import cnf as CNF


from logic_ast import Neg

def resolve(ci, cj):
    """
    Takes two clauses ci and cj (sets of literals) and returns the set of resolvents obtained 
    by resolving ci and cj.
    """
    resolvents = set()
    
    for li in ci:
        for lj in cj:
            if li == Neg(lj):
                resolvent = (ci - {li}).union(cj - {lj})
                resolvents.add(frozenset(resolvent))
                
    return resolvents


def resolution(beliefBase, statement):
    """
    Considers a belief base (a set of sentences) and a statement (a sentence) and returns 
    True if the statement can be derived from the belief base using resolution, and False 
    otherwise.
    """
    # What we know so far
    clauses = CNF.cnf(beliefBase, statement)
    
    while True:
        # What we discover in this iteration
        new = set()
        clause_list = list(clauses)
        
        for i in range(len(clause_list)):
            for j in range(i + 1, len(clause_list)):
                ci = clause_list[i]
                cj = clause_list[j]
                
                resolvents = resolve(ci, cj)
                
                # frozenset() represents the empty clause, which indicates a contradiction
                if frozenset() in resolvents:
                    return True
                
                new = new.union(resolvents)
                
        if new.issubset(clauses):
            return False
        
        clauses = clauses.union(new)