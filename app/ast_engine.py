# app/ast_engine.py
import re

class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.node_type}, {self.value}, left={self.left}, right={self.right})"

def create_rule(rule_string):
    tokens = re.findall(r'\(|\)|\w+|>=|<=|!=|>|<|=', rule_string)
    return build_ast(tokens)

def build_ast(tokens):
    stack = []
    for token in tokens:
        if token == '(':
            stack.append(token)
        elif token == ')':
            node_stack = []
            while stack and stack[-1] != '(':
                node_stack.append(stack.pop())
            stack.pop()  # remove '('
            if len(node_stack) == 3:
                right = node_stack.pop(0)
                operator = node_stack.pop(0)
                left = node_stack.pop(0)
                stack.append(Node('operator', operator, left, right))
        else:
            stack.append(Node('operand', token))
    return stack[0] if stack else None

def evaluate_rule(node, data):
    if node.node_type == 'operand':
        attribute, condition = node.value.split(' ', 1)
        return eval(f"data.get('{attribute}', 0) {condition}")
    elif node.node_type == 'operator':
        left_eval = evaluate_rule(node.left, data)
        right_eval = evaluate_rule(node.right, data)
        if node.value == 'AND':
            return left_eval and right_eval
        elif node.value == 'OR':
            return left_eval or right_eval
    return False
