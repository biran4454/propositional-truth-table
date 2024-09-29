class TreeNode:
    def __init__(self, contents):
        self.contents = contents

class LetterNode(TreeNode):
    pass

class LogicNode(TreeNode):
    def __init__(self, contents):
        super(LogicNode, self).__init__(contents)
        self.subnodes = []
    def add_subnode(self, node: TreeNode):
        if isinstance(node, TreeNode):
            self.subnodes.append(node)

def process_logic(logic, precedence):
    if not precedence:
        return LetterNode(logic)
    
    operator = precedence[-1]
    if not operator in logic:
        return process_logic(logic, precedence[:-1])
    
    node = LogicNode(operator)
    split_logic = logic.split(operator)
    if operator in ['->', '<->']:
        split_logic = [split_logic[0], operator.join(split_logic[1:])]
    for slogic in split_logic:
        node.add_subnode(process_logic(slogic, precedence[:-1]))
    return node

def calc_result(operator, values):
    if operator == '¬':
        return not values[0]
    if operator == '^':
        return all(values)
    if operator == 'v':
        return any(values)
    if operator == '->':
        return not values[0] or values[1]
    if operator == '<->':
        return not (values[0] ^ values[1])

def process_tree(treenode: LogicNode, values: dict):
    node_values = []
    for sub in treenode.subnodes:
        if not sub.contents:
            continue
        if isinstance(sub, LogicNode):
            node_values.append(process_tree(sub, values))
        else:
            node_values.append(values[sub.contents])
    return calc_result(treenode.contents, node_values)


def truth_table(logic, value_names):
    tree = process_logic(logic, PRECEDENCE)
    table = [] # not dict to keep order
    for i in range(0, pow(2, len(value_names))):
        values = {}
        for i_v, v in enumerate(value_names):
            values[v] = i & pow(2, (len(value_names) - 1) - i_v) == 0
        table.append((list(values.values()), process_tree(tree, values)))
    return table

def pretty_truth_table(table, value_names):
    print('┌', end='')
    for _ in value_names:
        print('───┬', end='')
    print('───┐')

    print('│', end='')
    for v in value_names:
        print(f' {v} │', end='')
    print(f' X │')

    for row in table:
        print('├', end='')
        for col in row[0]:
            print('───┼', end='')
        print('───┤')
        print('│', end='')
        for col in row[0]:
            print(f' {col:b} │', end='')
        print(f' {row[1]:b} │')
    print('└', end='')
    for _ in value_names:
        print('───┴', end='')
    print('───┘')

logic = 'A ^ B -> C ^ ¬A'

value_names = ['A', 'B', 'C']
PRECEDENCE = ['¬', '^', 'v', '->', '<->']

print('\n')
print('Creating truth table for:', logic)

logic = logic.replace(' ', '')
pretty_truth_table(truth_table(logic, value_names), value_names)