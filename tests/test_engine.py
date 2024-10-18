import unittest
from app.ast_engine import create_rule, evaluate_rule

class TestRuleEngine(unittest.TestCase):

    def test_create_rule(self):
        rule = create_rule("(age > 30 AND department = 'Sales')")
        self.assertIsNotNone(rule)

    def test_evaluate_rule(self):
        rule = create_rule("(age > 30 AND department = 'Sales')")
        data = {"age": 35, "department": "Sales"}
        result = evaluate_rule(rule, data)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
