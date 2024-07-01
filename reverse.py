def tokenize(phenotype):
    import re
    return re.findall(r'\d+|[\+\*\(\)]', phenotype)

def reconstruct_integer_sequence(tokens, grammar, rule_to_integer):
    integer_sequence = []
    stack = ['<expr>']
    
    while stack:
        current = stack.pop()
        if current in grammar:
            rule_index = select_production_rule(tokens, current, grammar)
            if rule_index is not None:
                integer_sequence.append(rule_to_integer[current][rule_index])
                production = grammar[current][rule_index]
                stack.extend(production[::-1])
        else:
            if current.isdigit() and tokens and current == tokens[0]:
                tokens.pop(0)
            elif tokens and current == tokens[0]:
                tokens.pop(0)
            else:
                raise ValueError("Mismatch between phenotype and grammar rules.")
    
    return integer_sequence

def select_production_rule(tokens, non_terminal, grammar):
    for i, rule in enumerate(grammar[non_terminal]):
        if matches_rule(tokens, rule):
            return i
    return None

def matches_rule(tokens, rule):
    if len(tokens) < len(rule):
        return False
    for token, rule_part in zip(tokens, rule):
        if rule_part in grammar and rule_part != token:
            return False
        if rule_part == 'number' and not token.isdigit():
            return False
        if rule_part == token:
            continue
    return True

grammar = {
    '<expr>': [['<expr>', '+', '<term>'], ['<term>']],
    '<term>': [['<term>', '*', '<factor>'], ['<factor>']],
    '<factor>': [['(', '<expr>', ')'], ['number']],
    'number': [['0'], ['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'], ['8'], ['9']]
}

rule_to_integer = {
    '<expr>': [0, 1],
    '<term>': [0, 1],
    '<factor>': [0, 1],
    'number': list(range(10))
}

phenotype = "(1 + 2) * 3"
tokens = tokenize(phenotype)
integer_sequence = reconstruct_integer_sequence(tokens, grammar, rule_to_integer)
print(integer_sequence)
