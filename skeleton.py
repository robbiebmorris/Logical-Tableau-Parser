
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


def parse_propositional_formula(fmla):
    if (fmla[0] == '~'):
          return Negation(parse_propositional_formula(fmla[1:]))
    elif fmla[0] == '(' and fmla[-1] == ')':
        # Find the main connective
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


# Parse a formula, consult parseOutputs for return values.
def parse(fmla):
    
    # use parse_propositional_formula to parse propositional formulae and return corresponding number values from praseOutputs
    ans = parse_propositional_formula(fmla)
    if not check_if_valid_propositional_formula(ans):
        return 0
    if (ans.__class__.__name__ == 'Proposition'):
        return 6
    elif (ans.__class__.__name__ == 'Negation'):
        return 7
    elif (ans.__class__.__name__ == 'BinaryConnective'):
        return 8
    
    return 0
      
# print(parse_propositional_formula('(p\\/(r\\/s))'))

# Return the LHS of a binary connective formula
def lhs(fmla):
    return parse_propositional_formula(fmla).left

# Return the connective symbol of a binary connective formula
def con(fmla):
    return parse_propositional_formula(fmla).connective

# Return the RHS symbol of a binary connective formula
def rhs(fmla):
    return parse_propositional_formula(fmla).right


def expand_node(node):
    # use the tableau rules to expand the node based on the type of formula it is
    if (node.__class__.__name__ == 'Proposition'):
        return [node]
    elif (node.__class__.__name__ == 'Negation'):
        #check for ~(p/\q) and ~(p\/q)
        if (node.formula.__class__.__name__ == 'BinaryConnective'):
            # ~(p/\q) -> (~p) , (~q)
            if (node.formula.connective == '/\\'):
                return ([Negation(node.formula.left)], [Negation(node.formula.right)])
            elif (node.formula.connective == '\\/'):
                return [Negation(node.formula.left), Negation(node.formula.right)]
            elif (node.formula.connective == '=>'):
                return [node.formula.left, Negation(node.formula.right)]
        #check for ~~p
        elif (node.formula.__class__.__name__ == 'Negation'):
            return [node.formula.formula] 

        #check for ~p
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
        print("something is broken")
        return


def is_closed(branch):
    #checks whether a branch in the tableau is closed. A branch is closed if it contains both a proposition and its negation.
    propSet = set()
    negSet = set()
    for node in branch:
        if (node.__class__.__name__ == 'Proposition'):
            propSet.add(node.name)
        elif (node.__class__.__name__ == 'Negation' and node.formula.__class__.__name__ == 'Proposition'):
            negSet.add(node.formula.name)
    return len(propSet.intersection(negSet)) > 0
  

def is_leaf_branch(branch):
    #checks whether a branch is a leaf branch (contains something larger than a prop or neg prop)
    for node in branch:
        if (node.__class__.__name__ == 'Negation' and (node.formula.__class__.__name__ == 'BinaryConnective' or node.formula.__class__.__name__ == 'Negation')):
            return False
        if (node.__class__.__name__ == 'BinaryConnective'):
            return False
    return True
  
  
def check_number_of_letters(fmla):
    #checks whether the number of constants in a formula is less than or equal to MAX_CONSTANTS
    if (fmla.__class__.__name__ == 'Proposition'):
        return 1
    elif (fmla.__class__.__name__ == 'Negation'):
        return check_number_of_letters(fmla.formula)
    else:
        return check_number_of_letters(fmla.left) + check_number_of_letters(fmla.right)
    
    
# print(check_number_of_letters(parse_propositional_formula('~~((p\/q)/\((p=>~p)/\(~p=>p)))')))
  
# You may choose to represent a theory as a set or a list
def theory(fmla):
  return parse_propositional_formula(fmla)
  

def sat(tableau):
    if (check_number_of_letters(tableau[0]) > MAX_CONSTANTS):
        #too long
        return 2
    
    branches = [tableau]
    while len(branches) > 0:

        # for node in branches:
        #     [print("node: ", n) for n in node]
        #     print("\n")

        branch = branches.pop()

        # [print("b: ", b) for b in branch]
        # print("leaf branch: ", is_leaf_branch(branch))
        # print("branch closed: ", is_closed(branch))
        
        if is_closed(branch):
            #get rid of all sub branches of this branch from branches
            continue
        elif is_leaf_branch(branch) and not is_closed(branch):
            #satisfiable
            return 1
        else:
            sub_branches = []
            for node in branch:
                
                expansion = expand_node(node)
                #no expansion
                
                #alpha expansion (p/\q, ~(p\/q), ~(p=>q))
                if type(expansion) is not tuple:
                    # print all nodes in expansion
                    # [print("e: ", e) for e in expansion]
                    # branch = [n for n in branch if n != node] + expansion
                    if len(sub_branches) > 0:
                        for i in range(len(sub_branches)):
                          sub_branches[i] += expansion
                    else:
                        sub_branches.append(expansion)
          
                #beta expansion (p\/q, ~(p/\q), (p=>q))
                else:
                    # [print("tup e: ", e[0]) for e in expansion]
                    
                    # if there was a previous alpha expansion, remove it and combine with new expansion
                    if (len(sub_branches) == 1):
                        temp = sub_branches.pop()
                        sub_branches.append(expansion[0] + temp)
                        sub_branches.append(expansion[1] + temp)
                    # if there was a previous beta expansion, combine with new expansion
                    elif (len(sub_branches) == 2):
                        sub_branches[0] += expansion[0]
                        sub_branches[1] += expansion[1]
                    else:
                        sub_branches.append(expansion[0])
                        sub_branches.append(expansion[1])
                    
                    # print("added from beta:" , expansion[0][0])
                    # print("added from beta:" , expansion[1][0])

                    
            branches += sub_branches
            # count =0
            # print(sub_branches)
            # for b in sub_branches:
            #     [print(f"sub b {count}: ", k) for k in b]
            #     count += 1
            # print(branches)

    #not satisfiable
    return 0

# print(sat([parse_propositional_formula('(q/\~(q/\(p/\q)))')]))
# print(sat([parse_propositional_formula('~((p=>p)=>(q=>q))')]))
# print(sat([parse_propositional_formula('~~((p\/q)/\((p=>~p)/\(~p=>p)))')]))


# def sat(tableau):
#   #write code using tableau rules to check if the formula is satisfiable
#   #return 0 if not satisfiable, 1 if satisfiable, 2 if may or may not be satisfiable
#   #input is the output from theory function above
  
# print(check_if_valid_propositional_formula(parse_propositional_formula('(p=>q)')))

f = open('./testinputs/testinput2/input.txt')
#DO NOT MODIFY THE CODE BELOW
# f = open('input.txt')

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
