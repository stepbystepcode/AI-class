import sys
import re
from collections import defaultdict
from copy import deepcopy

class Literal:
    def __init__(self, name, args=[], is_neg=False):
        self.name = name
        self.args = args
        self.is_neg = is_neg

    def __repr__(self):
        neg = "¬" if self.is_neg else ""
        if self.args:
            args_str = ", ".join(self.args)
            return f"{neg}{self.name}({args_str})"
        else:
            return f"{neg}{self.name}"

    def negate(self):
        return Literal(self.name, self.args, not self.is_neg)

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.is_neg == other.is_neg and
            self.args == other.args
        )

    def __hash__(self):
        return hash((self.name, tuple(self.args), self.is_neg))

class Clause:
    def __init__(self, literals=[]):
        self.literals = literals 

    def __repr__(self):
        return "∨".join([str(lit) for lit in self.literals])

def parse_literal(literal_str):
    literal_str = literal_str.strip()
    is_neg = False
    if literal_str.startswith("¬"):
        is_neg = True
        literal_str = literal_str[1:].strip()
    match = re.match(r'(\w+)(?:\((.*)\))?', literal_str)
    if not match:
        raise ValueError(f"Invalid literal format: {literal_str}")
    name = match.group(1)
    args_str = match.group(2)
    args = []
    if args_str:
        args = split_args(args_str)
    return Literal(name, args, is_neg)

def split_args(args_str):
    args = []
    current = ""
    depth = 0
    for char in args_str:
        if char == ',' and depth == 0:
            args.append(current.strip())
            current = ""
        else:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            current += char
    if current:
        args.append(current.strip())
    return args

def parse_clause(clause_str):
    literals_str = clause_str.split("∨")
    literals = [parse_literal(lit) for lit in literals_str]
    return Clause(literals)

class Standardizer:
    def __init__(self):
        self.counter = defaultdict(int)

    def standardize(self, clause):
        substitution = {}
        new_literals = []
        for lit in clause.literals:
            new_args = []
            for arg in lit.args:
                if is_variable(arg):
                    if arg not in substitution:
                        substitution[arg] = f"{arg}"
                        self.counter[arg] += 1
                    new_args.append(substitution[arg])
                elif is_function(arg):
                    new_args.append(self.standardize_term(arg, substitution))
                else:
                    new_args.append(arg)
            new_literals.append(Literal(lit.name, new_args, lit.is_neg))
        return Clause(new_literals)

    def standardize_term(self, term, substitution):
        if not is_function(term):
            if is_variable(term):
                if term not in substitution:
                    substitution[term] = f"{term}"
                    self.counter[term] += 1
                return substitution[term]
            else:
                return term
        else:
            name = get_function_name(term)
            args = get_arguments(term)
            new_args = []
            for arg in args:
                if is_variable(arg):
                    if arg not in substitution:
                        substitution[arg] = f"{arg}"
                        self.counter[arg] += 1
                    new_args.append(substitution[arg])
                elif is_function(arg):
                    new_args.append(self.standardize_term(arg, substitution))
                else:
                    new_args.append(arg)
            return f"{name}({', '.join(new_args)})"

def is_variable(term):
    return term[0].islower()

def is_function(term):
    return '(' in term and term.endswith(')')

def get_function_name(term):
    return term[:term.find('(')]

def get_arguments(term):
    args_str = term[term.find('(')+1:-1]
    return split_args(args_str)

# 统一算法
def unify(x, y, substitution):
    if substitution is None:
        return None
    elif x == y:
        return substitution
    elif is_variable(x):
        return unify_var(x, y, substitution)
    elif is_variable(y):
        return unify_var(y, x, substitution)
    elif is_function(x) and is_function(y):
        if get_function_name(x) != get_function_name(y):
            return None
        args_x = get_arguments(x)
        args_y = get_arguments(y)
        if len(args_x) != len(args_y):
            return None
        for arg1, arg2 in zip(args_x, args_y):
            substitution = unify(arg1, arg2, substitution)
            if substitution is None:
                return None
        return substitution
    else:
        return None

def unify_var(var, x, substitution):
    if var in substitution:
        return unify(substitution[var], x, substitution)
    elif is_variable(x) and x in substitution:
        return unify(var, substitution[x], substitution)
    elif occurs_check(var, x, substitution):
        return None
    else:
        substitution = deepcopy(substitution)
        substitution[var] = x
        return substitution

def occurs_check(var, x, substitution):
    if var == x:
        return True
    elif is_function(x):
        for arg in get_arguments(x):
            if occurs_check(var, arg, substitution):
                return True
    elif x in substitution:
        return occurs_check(var, substitution[x], substitution)
    return False

def substitute_literal(literal, substitution):
    new_args = []
    for arg in literal.args:
        new_arg = substitute_term(arg, substitution)
        new_args.append(new_arg)
    return Literal(literal.name, new_args, literal.is_neg)

def substitute_term(term, substitution):
    while is_variable(term) and term in substitution:
        term = substitution[term]
    if is_function(term):
        name = get_function_name(term)
        args = get_arguments(term)
        new_args = [substitute_term(arg, substitution) for arg in args]
        return f"{name}({', '.join(new_args)})"
    else:
        return term

def substitute_clause(clause, substitution):
    new_literals = [substitute_literal(lit, substitution) for lit in clause.literals]
    return Clause(new_literals)

def resolve_clauses(clause_str1, clause_str2):
    clause1 = parse_clause(clause_str1)
    clause2 = parse_clause(clause_str2)

    standardizer = Standardizer()
    clause1 = standardizer.standardize(clause1)
    clause2 = standardizer.standardize(clause2)

    for lit1 in clause1.literals:
        for lit2 in clause2.literals:
            if lit1.name == lit2.name and lit1.is_neg != lit2.is_neg:
                substitution = {}
                substitution = unify_literals(lit1, lit2, substitution)
                if substitution is not None:
                    new_clause1 = substitute_clause(clause1, substitution)
                    new_clause2 = substitute_clause(clause2, substitution)

                    resolved_lit1 = substitute_literal(lit1, substitution)
                    resolved_lit2 = substitute_literal(lit2, substitution)

                    new_literals1 = [lit for lit in new_clause1.literals if lit != resolved_lit1]
                    new_literals2 = [lit for lit in new_clause2.literals if lit != resolved_lit2]

                    combined_literals = new_literals1 + new_literals2

                    unique_literals = list(set(combined_literals))

                    return Clause(unique_literals)
    return None

def unify_literals(lit1, lit2, substitution):
    if lit1.name != lit2.name or lit1.is_neg == lit2.is_neg:
        return None
    if len(lit1.args) != len(lit2.args):
        return None
    for arg1, arg2 in zip(lit1.args, lit2.args):
        substitution = unify(arg1, arg2, substitution)
        if substitution is None:
            return None
    return substitution

def format_clause(clause):
    return " ∨ ".join([str(lit) for lit in sorted(clause.literals, key=lambda x: str(x))])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as file:
            input1 = file.readline().strip()
            input2 = file.readline().strip()
    except FileNotFoundError:
            print(f"Error: The file '{input_file}' does not exist.")
            sys.exit(1)

    resolvent = resolve_clauses(input1, input2)
    if resolvent:
        print(format_clause(resolvent))
    else:
        print("Error: resolution failed")
