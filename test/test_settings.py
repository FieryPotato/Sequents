import unittest

from unittest.mock import patch

from settings import Settings

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
    file = 'test/io_testing/test_config.json'

    def test_load_settings(self) -> None:
        with patch('settings._Settings.file', self.file):
            s = Settings()
            
            self.assertEqual(test_config, s.dict)


if __name__ == '__main__':
    unittest.main()

