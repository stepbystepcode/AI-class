import sys
import itertools
from tabulate import tabulate

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip() != '']
    N = int(lines[0])
    variables = lines[1].split()
    adj_matrix = []
    idx = 2
    for _ in range(N):
        adj_matrix.append(list(map(int, lines[idx].split())))
        idx += 1
    parents = [[] for _ in range(N)]
    for j in range(N):
        for i in range(N):
            if adj_matrix[i][j] == 1:
                parents[j].append(i)
    CPTs = []
    for var_idx in range(N):
        num_parents = len(parents[var_idx])
        num_lines = 2 ** num_parents
        cpt = []
        for _ in range(num_lines):
            if idx < len(lines):
                probs = list(map(float, lines[idx].split()))
                if len(probs) >= 1:
                    cpt.append(probs[0])  # Store P(variable=true | parents)
                    idx +=1
                else:
                    idx +=1
        CPTs.append(cpt)
    queries = lines[idx:]
    return N, variables, parents, CPTs, queries

def compute_probability(variables, parents, CPTs, query_var, evidence):
    var_indices = {var: idx for idx, var in enumerate(variables)}
    Q_idx = var_indices[query_var]
    evidence_vars = {var_indices[var]: val for var, val in evidence.items()}
    hidden_vars = [i for i in range(len(variables)) if i != Q_idx and i not in evidence_vars]
    # Compute numerator for Q=true and Q=false
    probs = {}
    for q_val in [True, False]:
        total_prob = 0.0
        for values in itertools.product([True, False], repeat=len(hidden_vars)):
            assignment = {}
            for var_idx, val in evidence_vars.items():
                assignment[var_idx] = val
            assignment[Q_idx] = q_val
            for idx, val in zip(hidden_vars, values):
                assignment[idx] = val
            prob = 1.0
            for var_idx in range(len(variables)):
                var_parents = parents[var_idx]
                parent_vals = tuple(assignment[p_idx] for p_idx in var_parents)
                num_parents = len(var_parents)
                if num_parents == 0:
                    index = 0
                else:
                    index = sum((parent_vals[i] << (num_parents - i -1)) for i in range(num_parents))
                p_true = CPTs[var_idx][index]
                var_val = assignment[var_idx]
                if var_val:
                    prob *= p_true
                else:
                    prob *= (1 - p_true)
            total_prob += prob
        probs[q_val] = total_prob
    total = probs[True] + probs[False]
    probs[True] /= total
    probs[False] /= total
    return probs[True], probs[False]

def parse_query(query_line):
    # Example: P(Burglar | Alarm=true, Earthquake=true)
    query_line = query_line.strip()
    if query_line.startswith('P(') and '|' in query_line:
        content = query_line[2:-1]
        lhs, rhs = content.split('|')
        query_var = lhs.strip()
        evidence = {}
        for item in rhs.strip().split(','):
            if '=' in item:
                var, val = item.strip().split('=')
                evidence[var.strip()] = True if val.strip().lower() == 'true' else False
        return query_var, evidence
    else:
        return None, None

def main():
    if len(sys.argv) != 2:
        print("Usage: python bayesian_network.py <input_file>")
        sys.exit(1)
    input_file = sys.argv[1]
    N, variables, parents, CPTs, queries = read_input(input_file)
    var_indices = {var: idx for idx, var in enumerate(variables)}
    results = []
    for query_line in queries:
        if not query_line.strip():
            continue
        query_var, evidence = parse_query(query_line)
        if query_var is None:
            continue
        p_true, p_false = compute_probability(variables, parents, CPTs, query_var, evidence)
        evidence_str = ', '.join([f'{var}={str(val)}' for var, val in evidence.items()])
        results.append([f"P({query_var} | {evidence_str})", f"{p_true:.3f}", f"{p_false:.3f}"])
    headers = ["Query", "P(True)", "P(False)"]
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()
