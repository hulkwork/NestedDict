import unittest
from src import nestedict as module


class TestNested(unittest.TestCase):
    def setUp(self):
        self.test_data = {
            "a": {
                "b": 1,
                "c": 3,
                "d": {
                    "dd": {
                        "ddd": 3
                    }
                }
            },
            "b": 1,
            "c": {
                'd': {
                    "e": {
                        "f": {
                            'g': 2
                        }
                    }
                }
            }
        }

    def test_nested_get_item(self):
        d = module.Nested(self.test_data)
        actual = d['a.b']
        expected = 1
        self.assertEqual(actual, expected)

    def test_contains(self):
        d = module.Nested(self.test_data)
        actual = 'a.b' in d
        expected = True
        self.assertEqual(actual, expected)

    def test_retreive_keys(self):
        d = module.Nested(self.test_data)
        actual = d.keys()
        expected = ['a.b', 'a.c', 'a.d.dd.ddd', 'b', 'c.d.e.f.g']
        self.assertEqual(actual, expected)

    def test_retrieve_values(self):
        d = module.Nested(self.test_data)
        actual = d.values()
        expected = [1, 3, 3, 1, 2]
        self.assertEqual(actual, expected)

    def test_explode(self):
        d = module.Nested(self.test_data)
        actual = d.explode()
        expected = {'a.b': 1, 'a.c': 3, 'a.d.dd.ddd': 3, 'b': 1, 'c.d.e.f.g': 2}
        self.assertEqual(actual, expected)

    def test_equal(self):
        d1 = module.Nested({"a": {"a": 1}})
        d2 = module.Nested({"a": {"a": 1}})
        actual = d1 == d2
        expected = True
        self.assertEqual(actual, expected)

        d1 = module.Nested({"a": {"a": 2}})
        d2 = module.Nested({"a": {"a": 1}})
        actual = d1 == d2
        expected = False
        self.assertEqual(actual, expected)

    def test_max_deep(self):
        d = module.Nested(self.test_data)
        actual = d.max_deep()
        self.assertEqual(actual, 5)

    def test_min_deep(self):
        d = module.Nested(self.test_data)
        actual = d.min_deep()
        self.assertEqual(actual, 1)

    def test_dtypes(self):
        d = module.Nested(self.test_data)
        actual = d.dtypes(to_string=True)
        expected = {'a.b': 'int', 'a.c': 'int', 'a.d.dd.ddd': 'int', 'b': 'int', 'c.d.e.f.g': 'int'}
        self.assertEqual(actual, expected)

    def test_set(self):
        d = module.Nested(self.test_data)
        d.set("a.d.dd.ddd", 2)
        actual = d.nested_dict
        expected = {'a': {'b': 1, 'c': 3, 'd': {'dd': {'ddd': 2}}}, 'b': 1, 'c': {'d': {'e': {'f': {'g': 2}}}}}
        self.assertEqual(actual, expected)

    def test_explode_plus(self):
        d = module.Nested({'a': {'b': 1, 'c': [{"d": 1}, 5.2, {"a": {"b": 1}}]}})
        actual = d.explode_plus()
        expected = {'a.b': 1, 'a.c.0.d': 1, 'a.c.1': 5.2, 'a.c.2.a.b': 1}
        self.assertEqual(actual, expected)
