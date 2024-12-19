import unittest
from pathlib import Path
import pandas as pd
import lucxbox.tools.py_format_check.format_tracker as format_tracker


class TestFormatTracker(unittest.TestCase):
    def setUp(self):
        self.this_file = Path(__file__)
        self.this_folder = self.this_file.resolve().parent
        self.this_repo = format_tracker.get_repo_root(self.this_folder)
        self.valid_config_path = self.this_repo / ".flake8"
        self.log_name = "test.log"
        self.baseline_pkl = "baseline.pkl"
        self.local_pkl = "local.pkl"
        self.local_pkl_path = self.this_repo / self.local_pkl
        self.baseline_log_path = self.this_repo / self.log_name
        self.baseline_pkl_path = self.this_repo / self.baseline_pkl
        self.bad_file = self.this_folder.joinpath("bad_linting.py")

    def tearDown(self):
        # unlink(missing_ok=False) only available from python 3.8+
        tmp = (
            self.baseline_log_path,
            self.baseline_pkl_path,
            self.local_pkl_path,
        )
        for filepath in tmp:
            if filepath.exists():
                filepath.unlink()

    def test_is_flake8_config(self):
        # Valid config file
        actual_result = format_tracker.is_flake8_config(self.valid_config_path)
        self.assertTrue(actual_result)

        # Non-config file
        actual_result = format_tracker.is_flake8_config(self.this_file)
        self.assertFalse(actual_result)

        # Nonexistent dir
        actual_result = format_tracker.is_flake8_config(Path("randomFakeDir"))
        self.assertFalse(actual_result)

        # Folder
        actual_result = format_tracker.is_flake8_config(self.this_folder)
        self.assertFalse(actual_result)

    def test_find_config_file(self):
        # Valid config file
        actual_result = format_tracker.find_config_file(self.this_repo)
        self.assertEqual(actual_result, self.valid_config_path)

        # Fake root path (with no flake8 config)
        with self.assertRaises(FileNotFoundError):
            actual_result = format_tracker.find_config_file(Path("Fake"))

        # Real path (with no flake8 config in it)
        with self.assertRaises(FileNotFoundError):
            actual_result = format_tracker.find_config_file(self.this_folder)

        # Multiple config files in root, but only one valid flake8 cfg
        config_files = [
            self.this_repo.joinpath("tox.ini"),
            self.this_repo.joinpath("setup.cfg"),
        ]

        for config_file in config_files:
            config_file.touch()

        actual_result = format_tracker.find_config_file(self.this_repo)
        self.assertEqual(actual_result, self.valid_config_path)

        # Multiple valid flake8 configs
        config_files[0].write_text("[flake8]")
        with self.assertRaises(ValueError):
            format_tracker.find_config_file(self.this_repo)

        # Tear-down
        for config_file in config_files:
            config_file.unlink()

    def lint_repo(self):

        # Lint the current repository
        actual_result = format_tracker.lint_all(
            self.this_repo, output=self.log_name, pickle=self.baseline_pkl
        )
        self.assertEqual(0, actual_result)
        self.assertTrue(self.baseline_log_path.is_file())
        self.assertTrue(self.baseline_pkl_path.is_file())

    def lint_diff(self):

        # Lint this branch's diff to develop
        actual_result = format_tracker.lint_diff(
            dir_path=self.this_repo,
            output=self.log_name,
            target_branch="origin/develop",
            pickle=self.local_pkl,
        )
        self.assertEqual(0, actual_result)

    def test_compare_linting(self):

        # Run presteps
        self.lint_repo()
        self.lint_diff()

        # Since lint_repo() is a strict superset of lint_diff()
        # no new errors should be added
        new_errors = format_tracker.compare_linting(
            dir_path=self.this_folder,
            baseline=self.baseline_pkl,
            local_changes=self.local_pkl,
        )
        self.assertEqual(0, new_errors)

        # Test added errors
        self.do_bad_file()

        self.lint_diff()
        new_errors = format_tracker.compare_linting(
            dir_path=self.this_folder,
            baseline=self.baseline_pkl,
            local_changes=self.local_pkl,
        )
        # Two errors due to unused import and no EOF line
        self.assertEqual(2, new_errors)

        # Tear-down
        self.undo_bad_file()
        self.this_repo.joinpath(self.local_pkl).unlink()

    def test_lint_and_pickle(self):
        # Create a bad file to get a proper flake8 log
        self.do_bad_file()
        current_result = format_tracker.lint_and_pickle(
            output=self.baseline_log_path,
            config_file=self.valid_config_path,
            files_to_lint=[self.this_folder],
            root=self.this_folder,
            pickle="myPickle.pkl",
        )
        self.assertEqual(0, current_result)
        self.assertTrue(self.this_folder.joinpath("myPickle.pkl").is_file())
        self.undo_bad_file()

    def test_read_pandas_pickle(self):
        # Invalid pickles
        invalid_pickles = [self.this_file, self.this_folder]
        for pkl in invalid_pickles:
            with self.assertRaises(SystemExit) as return_code:
                format_tracker.read_pandas_pickle(pkl)
                self.assertEqual(1, return_code)

        # Valid pickle
        valid_pickle = self.this_folder.joinpath("myPickle.pkl")
        new_df = format_tracker.read_pandas_pickle(valid_pickle)
        pd.util.testing.assert_frame_equal(
            new_df, pd.read_pickle(valid_pickle)
        )

    def do_bad_file(self):
        good_file_content = self.bad_file.read_text()
        if good_file_content == "print('This file is ok')\n":
            self.bad_file.write_text("import numpy")

    def undo_bad_file(self):
        bad_file_content = self.bad_file.read_text()
        if bad_file_content == "import numpy":
            self.bad_file.write_text("print('This file is ok')\n")

    def run_flake8(self):

        self.do_bad_file()
        # Run for a list of a single file
        current_result = format_tracker.run_flake8(
            output_file=self.baseline_log_path,
            config=self.valid_config_path,
            files=[self.bad_file, self.this_file],
            dir_path=self.this_folder,
        )
        self.assertEqual(0, current_result)

        # Read flake8 log's first line
        first_line = self.baseline_log_path.read_text().splitlines()
        self.undo_bad_file()

        # Check if the format was overwritten
        for line in first_line:
            self.assertEqual(5, len(line.split("_-_")))

    def test_read_flake8_log(self):

        self.run_flake8()

        # Folder instead of file
        with self.assertRaises(SystemExit) as return_code:
            current_result = format_tracker.read_flake8_log(
                flake8_log=self.this_folder
            )
            self.assertEqual(1, return_code)

        # Nonexistent log
        with self.assertRaises(SystemExit) as return_code:
            current_result = format_tracker.read_flake8_log(
                flake8_log="bad_log.txt"
            )
            self.assertEqual(1, return_code)

        # File not 'comma' separated
        with self.assertRaises(ValueError):
            current_result = format_tracker.read_flake8_log(
                flake8_log=self.this_file
            )
            self.assertEqual(1, current_result)

        with self.assertRaises(ValueError):
            # File with different separators than _-_
            current_result = format_tracker.read_flake8_log(
                flake8_log=self.this_folder.joinpath("bad.csv"),
            )
            self.assertEqual(1, current_result)

        # Valid flake8 file separated by _-_
        current_result = format_tracker.read_flake8_log(
            flake8_log=self.baseline_log_path,
        )
        self.assertIsInstance(current_result, pd.DataFrame)

        # Empty logs mean that flake8 run and the written Python code is ok
        good_log = Path('my_good_log.txt')
        good_log.touch()
        current_result = format_tracker.read_flake8_log(
            flake8_log=good_log
        )
        pd.util.testing.assert_frame_equal(
            current_result,
            pd.DataFrame(
                columns=["filename",
                         "lineNo",
                         "columnNo",
                         "errorNo",
                         "comment"])
        )
