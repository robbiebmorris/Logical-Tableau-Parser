MAX_CONSTANTS = 10

# propositional
PROP_LETTERS = {'p', 'q', 'r', 's'}
CONNECTIVES = {'/\\': 'and', '\\/': 'or', '=>': 'implies'}

FOL_LETTERS = {'x', 'y', 'z', 'w'}
PREDICATES = {'P', 'Q', 'R', 'S'}
QUANTIFIERS = {'A', 'E'}

class Proposition:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Negation:
    def __init__(self, formula):
        self.formula = formula

    def __str__(self):
        return f"~{self.formula}"

class BinaryConnective:
    def __init__(self, left, right, connective):
        self.left = left
        self.right = right
        self.connective = connective

    def __str__(self):
        return f"({self.left}{self.connective}{self.right})"

class Predicate:
    def __init__(self, predicate, left, right):
        self.predicate = predicate
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.predicate}({self.left},{self.right})"

class Quantifier:
    def __init__(self, quantifier, variable, formula):
        self.quantifier = quantifier
        self.variable = variable
        self.formula = formula

    def __str__(self):
        return f"{self.quantifier}{self.variable}{self.formula}"

def parse_propositional_formula(fmla):
    if (len(fmla) == 0):
        return
    if (fmla[0] == '~'):
          return Negation(parse_propositional_formula(fmla[1:]))
    elif fmla[0] == '(' and fmla[-1] == ')':
        count = 0
        for i in range(1, len(fmla) - 1):
            if fmla[i] == '(':
                count += 1
            elif fmla[i] == ')':
                count -= 1
            elif count == 0 and fmla[i:i+2] in CONNECTIVES:
                return BinaryConnective(
                    parse_propositional_formula(fmla[1:i]),
                    parse_propositional_formula(fmla[i+2:-1]),
                    fmla[i:i+2]
                )
    else:
        return Proposition(fmla)

def check_if_valid_propositional_formula(fmla):
    #use the class names of each of the objects to check if the formula is valid
    if (fmla.__class__.__name__ == 'Proposition' and fmla.name in PROP_LETTERS):
        return True
    elif (fmla.__class__.__name__ == 'Negation'):
        return check_if_valid_propositional_formula(fmla.formula)
    elif (fmla.__class__.__name__ == 'BinaryConnective'):
        return check_if_valid_propositional_formula(fmla.left) and check_if_valid_propositional_formula(fmla.right)
    else:
        return False


def parse_first_order_formula(fmla):
    if (len(fmla) == 0):
        return
    if (fmla[0] == '~'):
        return Negation(parse_first_order_formula(fmla[1:]))
    elif fmla[0] in QUANTIFIERS:
        return Quantifier(fmla[0], fmla[1], parse_first_order_formula(fmla[2:]))
    elif fmla[0] in PREDICATES and fmla[1] == '(' and fmla[-1] == ')':
        index = fmla.find(',')
        return Predicate(fmla[0], parse_first_order_formula(fmla[2:index]), parse_first_order_formula(fmla[index+1:-1]))
    elif fmla[0] == '(' and fmla[-1] == ')':
        count = 0
        for i in range(1, len(fmla) - 1):
            if fmla[i] == '(':
                count += 1
            elif fmla[i] == ')':
                count -= 1
            elif count == 0 and fmla[i:i+2] in CONNECTIVES:
                return BinaryConnective(
                    parse_first_order_formula(fmla[1:i]),
                    parse_first_order_formula(fmla[i+2:-1]),
                    fmla[i:i+2]
                )
    else:
        return Proposition(fmla)

def check_if_valid_fol_formula(fmla):
    if (fmla.__class__.__name__ == 'Proposition' and fmla.name in FOL_LETTERS):
        return True
    elif fmla.__class__.__name__ == 'Negation':
        return check_if_valid_fol_formula(fmla.formula)
    elif (fmla.__class__.__name__ == 'Quantifier' and fmla.quantifier in QUANTIFIERS and fmla.variable in FOL_LETTERS):
        return check_if_valid_fol_formula(fmla.formula)
    elif fmla.__class__.__name__ == 'BinaryConnective' or fmla.__class__.__name__ == "Predicate":
        return check_if_valid_fol_formula(fmla.left) and check_if_valid_fol_formula(fmla.right)
    else:
        return False
      


def parse(fmla):
    
    prop = parse_propositional_formula(fmla)
    fol = parse_first_order_formula(fmla)
    
    well_formed_prop = check_if_valid_propositional_formula(prop)
    well_formed_fol = check_if_valid_fol_formula(fol)
    
    if (well_formed_prop):    
        if (prop.__class__.__name__ == 'Proposition'):
            return 6
        elif (prop.__class__.__name__ == 'Negation'):
            return 7
        elif (prop.__class__.__name__ == 'BinaryConnective'):
            return 8
    elif (well_formed_fol):
        if (fol.__class__.__name__ == 'Predicate'):
            return 1
        elif (fol.__class__.__name__ == 'Negation'):
            return 2
        elif (fol.__class__.__name__ == 'Quantifier' and fol.quantifier == 'A'):
            return 3
        elif (fol.__class__.__name__ == 'Quantifier' and fol.quantifier == 'E'):
            return 4
        elif (fol.__class__.__name__ == 'BinaryConnective'):
            return 5
    return 0

# Return the LHS of a binary connective formula
def lhs(fmla):
    fol = parse_first_order_formula(fmla)
    prop = parse_propositional_formula(fmla)
    if (check_if_valid_fol_formula(fol)):
      return fol.left
    elif (check_if_valid_propositional_formula(prop)):
      return prop.left
    else:
      return None

# Return the connective symbol of a binary connective formula
def con(fmla):
    fol = parse_first_order_formula(fmla)
    prop = parse_propositional_formula(fmla)
    if (check_if_valid_fol_formula(fol)):
      return fol.connective
    elif (check_if_valid_propositional_formula(prop)):
      return prop.connective
    else:
      return None

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    fol = parse_first_order_formula(fmla)
    prop = parse_propositional_formula(fmla)
    if (check_if_valid_fol_formula(fol)):
      return fol.right
    elif (check_if_valid_propositional_formula(prop)):
      return prop.right
    else:
      return None
    
def substitute_literal(fmla, old, new):
    if fmla.__class__.__name__ == 'Proposition' and fmla.name == old:
        return Proposition(new)
    elif fmla.__class__.__name__ == 'Negation':
        return Negation(substitute_literal(fmla.formula, old, new))
    elif fmla.__class__.__name__ == 'BinaryConnective':
        return BinaryConnective(substitute_literal(fmla.left, old, new), substitute_literal(fmla.right, old, new), fmla.connective)
    elif fmla.__class__.__name__ == 'Quantifier':
        if fmla.variable == old:
            return Quantifier(fmla.quantifier, new, substitute_literal(fmla.formula, old, new))
        return Quantifier(fmla.quantifier, fmla.variable, substitute_literal(fmla.formula, old, new))
    elif fmla.__class__.__name__ == 'Predicate':
        return Predicate(fmla.predicate, substitute_literal(fmla.left, old, new), substitute_literal(fmla.right, old, new))
    else:
        return fmla

def delta_expansion(node, used_chars):
    # print("delta expansion")
    #find a new constant not in formula
    delta = 'a'
    while delta in used_chars or node.variable == delta:
        delta = chr(ord(delta) + 1)
    used_chars.add(delta)
    return [substitute_literal(node.formula, node.variable, delta)]

def gamma_expansion(node, c):
    #replace all x with gamma
    return substitute_literal(node, node.variable, c).formula

def expand_node(node, used_chars, gamma_q):
    # use the tableau rules to expand the node based on the type of formula it is
    if (node.__class__.__name__ == "Quantifier"):
        if (node.quantifier == 'E'):
            return delta_expansion(node, used_chars)
        elif (node.quantifier == 'A'):
            gamma_q.append(node)
            return []
    elif node.__class__.__name__ == 'Predicate' or node.__class__.__name__ == 'Proposition':
        return [node]
    elif (node.__class__.__name__ == 'Negation'):
        #check for ~(p/\q) and ~(p\/q)
        if (node.formula.__class__.__name__ == 'BinaryConnective'):
            #~(p/\q) -> (~p) , (~q)
            if (node.formula.connective == '/\\'):
                return ([Negation(node.formula.left)], [Negation(node.formula.right)])
            elif (node.formula.connective == '\\/'):
                return [Negation(node.formula.left), Negation(node.formula.right)]
            elif (node.formula.connective == '=>'):
                return [node.formula.left, Negation(node.formula.right)]
        #check for ~~p
        elif (node.formula.__class__.__name__ == 'Negation'):
            return [node.formula.formula] 
        #~E -> A~
        elif (node.formula.__class__.__name__ == "Quantifier" and node.formula.quantifier == 'E'):
            gamma_q.append(Quantifier('A', node.formula.variable, Negation(node.formula.formula)), used_chars)
            return []
        #~A -> E~
        elif (node.formula.__class__.__name__ == "Quantifier" and node.formula.quantifier == 'A'):
            return delta_expansion(Quantifier('E', node.formula.variable, Negation(node.formula.formula)), used_chars)
        else:
            return [node]
    elif (node.__class__.__name__ == 'BinaryConnective'):
        #check for (p/\q)
        if (node.connective == '/\\'):
            return [node.left, node.right]
        #check for (p\/q)
        elif (node.connective == '\\/'):
            return ([node.left], [node.right])
        #(p=>q) -> (~p\/q)
        elif (node.connective == '=>'):
            return ([Negation(node.left)], [node.right])
    else:
        return


def is_closed(branch):
    #checks whether a branch in the tableau is closed. A branch is closed if it contains both a proposition and its negation.
    propSet = set()
    negSet = set()
    for node in branch:
        if (node.__class__.__name__ == 'Predicate'):
            propSet.add(str(node))
        elif (node.__class__.__name__ == 'Negation' and node.formula.__class__.__name__ == 'Predicate'):
            negSet.add(str(node.formula))
        elif (node.__class__.__name__ == 'Proposition'):
            propSet.add(node.name)
        elif (node.__class__.__name__ == 'Negation' and node.formula.__class__.__name__ == 'Proposition'):
            negSet.add(node.formula.name)
    return len(propSet.intersection(negSet)) > 0
  

def is_leaf_branch(branch):
    #checks whether a branch is a leaf branch (contains something larger than a prop or neg prop)
    for node in branch:
        if (node.__class__.__name__ == 'Negation' and not (node.formula.__class__.__name__ == 'Proposition' or node.formula.__class__.__name__ == 'Predicate')):
            return False
        elif (node.__class__.__name__ == 'BinaryConnective' or node.__class__.__name__ == 'Quantifier'):
            return False
    return True

  
# You may choose to represent a theory as a set or a list
def theory(fmla):
  fol = parse_first_order_formula(fmla)
  prop = parse_propositional_formula(fmla)
  if (check_if_valid_fol_formula(fol)):
    return fol
  elif (check_if_valid_propositional_formula(prop)):
    return prop
  else:
    return None

  
def sat(tableau):

    branches = [tableau]
    used = set()
    gamma_q = []
    while len(branches) > 0:
        if (len(used) > MAX_CONSTANTS):
            return 2

        branch = branches.pop()

        if is_closed(branch):
            continue
        elif is_leaf_branch(branch) and not is_closed(tableau):
            #satisfiable
            return 1
        else:
            sub_branches = []
            sub_gamma_q = []
            sub_used = used.copy()
            for node in branch:

                expansion = expand_node(node, used, sub_gamma_q)
                #alpha expansion (p/\q, ~(p\/q), ~(p=>q))
                if type(expansion) is list:
                    if len(sub_branches) > 0:
                        for i in range(len(sub_branches)):
                            sub_branches[i] += expansion
                    else:
                        sub_branches.append(expansion)

                #beta expansion (p\/q, ~(p/\q), (p=>q))
                elif type(expansion) is tuple:
                    # if there was a previous alpha expansion, remove it and combine with new expansion
                    if (len(sub_branches) == 1):
                        temp = sub_branches.pop()
                        sub_branches.append(expansion[0] + temp)
                        sub_branches.append(expansion[1] + temp)
                    # if there was a previous beta expansion, combine with new expansion
                    elif (len(sub_branches) == 2):
                        sub_branches[0] += [node]
                        sub_branches[1] += [node]
                    else:
                        sub_branches.append(expansion[0])
                        sub_branches.append(expansion[1])

            for g in sub_gamma_q:
                for c in used:
                    exp = gamma_expansion(g, c)
                    for b in sub_branches:
                        b.append(exp)

            dif = used.difference(sub_used)
            
            for g in gamma_q:
                if g:
                  for c in dif:
                    exp = gamma_expansion(g, c)
                    for b in sub_branches:
                        b.append(exp)

            gamma_q += sub_gamma_q
            
            for b in sub_branches:
                branches.append(b)
            
    #not satisfiable
    return 0


#DO NOT MODIFY THE CODE BELOW
f = open('input.txt')

parseOutputs = ['not a formula',
                'an atom',
                'a negation of a first order logic formula',
                'a universally quantified formula',
                'an existentially quantified formula',
                'a binary connective first order formula',
                'a proposition',
                'a negation of a propositional formula',
                'a binary connective propositional formula']

satOutput = ['is not satisfiable', 'is satisfiable', 'may or may not be satisfiable']


firstline = f.readline()

PARSE = False
if 'PARSE' in firstline:
    PARSE = True

SAT = False
if 'SAT' in firstline:
    SAT = True

for line in f:
    if line[-1] == '\n':
        line = line[:-1]
    parsed = parse(line)

    if PARSE:
        output = "%s is %s." % (line, parseOutputs[parsed])
        if parsed in [5,8]:
            output += " Its left hand side is %s, its connective is %s, and its right hand side is %s." % (lhs(line), con(line) ,rhs(line))
        print(output)

    if SAT:
        if parsed:
            tableau = [theory(line)]
            print('%s %s.' % (line, satOutput[sat(tableau)]))
        else:
            print('%s is not a formula.' % line)
