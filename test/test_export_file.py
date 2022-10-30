import unittest
import pickle
from pathlib import Path

from convert import string_to_tree
from export_file import PickleExporter


class TestExportFile(unittest.TestCase):
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
        t_0 = string_to_tree('A; B -> C')

        t_1 = string_to_tree('A v B; C & (D v E)')
        tree_list = [t_0, t_1]
                        
        exporter = PickleExporter(self.dir)
        exporter.export(tree_list)

        with open(self.bytes_out_w_dir, 'rb') as f:
            actual = pickle.load(f)
        
        self.assertEqual(tree_list, actual)

    def test_saving_tree_to_file_bytes(self) -> None:
        t_0 = string_to_tree('A; B -> C')

        t_1 = string_to_tree('A v B; C & (D v E)')
        tree_list = [t_0, t_1]

        exporter = PickleExporter(self.dir + 'export.sequents')
        exporter.export(tree_list)

        with open(self.bytes_out_w_file, 'rb') as f:
            actual = pickle.load(f)

        self.assertEqual(tree_list, actual)


if __name__ == '__main__':
    unittest.main()

