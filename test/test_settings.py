import json
import unittest

from unittest.mock import patch

from settings import _Settings

test_config_path = 'test/io_testing/test_config.json'

test_config = {
    "connective_type": {
        "&": {
            "ant": "mul",
            "con": "add"
        },
        "v": {
            "ant": "add",
            "con": "mul"
        },
        "->": {
            "ant": "add",
            "con": "mul"
        },
        "~": {
            "ant": "mul",
            "con": "mul"
        }
    }
}

class TestSettings(unittest.TestCase): 
    def setUp(self) -> None:
        with patch('settings._Settings.file', test_config_path):
            self.s = _Settings()

    def tearDown(self) -> None:
        with open(test_config_path, 'w') as f:
            json.dump(test_config, f, indent=4)

    def test_load_settings(self) -> None:
        self.assertEqual(test_config, self.s._dict)

    def test_update(self) -> None:
        pos = {'positivists': 
            ['Carnap', 'Hahn', 'Neurath', 'Schlick']
        }
        self.s.update(pos)
        with open(self.s.file, 'r') as f:
            actual = json.load(f)
        pos.update(test_config)
        self.assertEqual(pos, actual)
        
    def test_set_rule(self) -> None:
        anti_ketonen = {
            '&': {
                'ant': 'add',
                'con': 'mul'
            },
            'v': {
                'ant': 'mul',
                'con': 'add'
            },
            '->': {
                'ant': 'mul',
                'con': 'add'
            },
            '~': {
                'ant': 'add',
                'con': 'add'
            }
        }
        for connective in ('&', 'v', '->', '~'): 
            for side in ('ant', 'con'):
                with self.subTest(i=(connective, side)):
                    value = anti_ketonen[connective][side]
                    self.s.set_rule(connective, side, value)
                    with open(self.s.file, 'r') as f:
                        s_dict = json.load(f)
                    actual = s_dict['connective_type'][connective][side]
                    self.assertEqual(value, actual)

if __name__ == '__main__':
    unittest.main()

