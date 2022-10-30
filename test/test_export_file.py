import os
import unittest
import pickle
from pathlib import Path

from convert import string_to_tree
from export_file import PickleExporter


T_0 = string_to_tree('A; B -> C')
T_1 = string_to_tree('A v B; C & (D v E)')
TREE_LIST = [T_0, T_1]


class TestExportBytes(unittest.TestCase):
    dir: str = 'test/io_testing/export/'
    bytes_out_w_dir: str = 'test/io_testing/export/results.sequents'
    bytes_out_w_file: str = 'test/io_testing/export/export.sequents'

    def tearDown(self) -> None:
        test_dir = Path(self.dir)
        if not test_dir.exists():
            return
        for file in test_dir.iterdir():
            if file.is_dir():
                for f in file.iterdir():
                    f.unlink(missing_ok=True)
                file.rmdir()
            elif file.exists():
                file.unlink()
        test_dir.rmdir()

    def test_saving_tree_to_dir_bytes(self) -> None:
        exporter = PickleExporter(self.dir)
        exporter.export(TREE_LIST)

        with open(self.bytes_out_w_dir, 'rb') as f:
            actual = pickle.load(f)
        
        self.assertEqual(TREE_LIST, actual)

    def test_saving_tree_to_file_bytes(self) -> None:
        exporter = PickleExporter(self.dir + 'export.sequents')
        exporter.export(TREE_LIST)

        with open(self.bytes_out_w_file, 'rb') as f:
            actual = pickle.load(f)

        self.assertEqual(TREE_LIST, actual)

    def test_handling_collisions(self) -> None:
        # Collisions are handled by overwriting previous data.
        pre_existing = Path(self.bytes_out_w_dir)
        os.makedirs(parent := pre_existing.parent)
        pre_existing.touch()

        exporter = PickleExporter(self.dir)
        exporter.export(TREE_LIST)

        new_path = parent / 'results.sequents'
        with open(new_path, 'rb') as f:
            actual = pickle.load(f)

        self.assertEqual(TREE_LIST, actual)

if __name__ == '__main__':
    unittest.main()

