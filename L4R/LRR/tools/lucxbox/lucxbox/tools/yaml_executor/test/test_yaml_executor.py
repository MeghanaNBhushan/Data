""" Test for yaml_executor """
import os
import unittest
import pathlib
from types import SimpleNamespace
from tempfile import TemporaryDirectory

from lucxbox.tools.yaml_executor import yaml_executor, yaml_parser
# pylint: disable=no-name-in-module
from lucxbox.tools.yaml_executor.steps import FailedCmdError


class TestYamlExecutor(unittest.TestCase):
    """ Test class for yaml executor """
    script_dir = str(pathlib.Path(__file__).parent.absolute())

    def setUp(self):
        self.log_dir = TemporaryDirectory()
        self.log_dir.__enter__()

        self.output_dir = TemporaryDirectory()
        self.output_dir.__enter__()

    def tearDown(self):
        self.output_dir.__exit__(None, None, None)
        self.log_dir.__exit__(None, None, None)

    def _run_yaml(self, yaml_file):
        yaml_file = os.path.join(self.script_dir, yaml_file)
        lucxbau_jar = os.path.join(self.script_dir, "lib/lucxbau.jar")
        args = SimpleNamespace(lucxlib=lucxbau_jar, yaml=yaml_file, root_dir=os.getcwd(), lucx_dir=os.getcwd(),
                               output=self.output_dir.name, log_dir=self.log_dir.name, parameter=[], include=[],
                               continuous_output=False, pwd=None, ssh=None, credentials=None, encoding='utf-8')

        try:
            pipelines = yaml_executor.parse(args)
        except:
            with open(os.path.join(self.log_dir.name, 'YAML_preprocess_log.txt'), 'r') as file_handle:
                print(file_handle.read())
            raise

        try:
            yaml_executor.run(args, pipelines)
            return True, pipelines
        except FailedCmdError:
            return False, pipelines

    def _get_logs(self, pipeline):

        def get_logs_from_steps(steps):
            for step in steps:
                path = os.path.join(self.log_dir.name, step.name + "_log.txt")

                if os.path.isfile(path):
                    with open(path, 'r') as file:
                        node_log.append(file.read().strip())

        log = []

        for node in pipeline.nodes:
            node_log = []

            for stage in node.stages:
                get_logs_from_steps(stage.steps)
                get_logs_from_steps(stage.post_steps)
                get_logs_from_steps(stage.post_success_steps)
                get_logs_from_steps(stage.post_fail_steps)

            for post_stages in node.post_stages:
                get_logs_from_steps(post_stages.steps)

            for post_stages in node.post_success_stages:
                get_logs_from_steps(post_stages.steps)

            for post_stages in node.post_fail_stages:
                get_logs_from_steps(post_stages.steps)

            log.append(node_log)

        return log

    def test_execute_test_file(self):
        success, pipelines = self._run_yaml("yaml_executor_test.yaml")

        log = self._get_logs(pipelines.pipelines[0])[0]

        self.assertTrue(success)
        self.assertEqual(log[0], "generating myVariant1")
        self.assertEqual(log[1], "generating myVariant1")
        self.assertEqual(log[2], "generating myVariant1")
        self.assertEqual(log[3], "building myVariant1")

    def test_execute_post_success(self):
        success, pipelines = self._run_yaml("yaml_executor_test_post_success.yaml")

        log = self._get_logs(pipelines.pipelines[0])[0]

        self.assertTrue(success)
        self.assertEqual(log[0], "Successful step")
        self.assertEqual(log[1], "Post stage")
        self.assertEqual(log[2], "Post stage success")
        self.assertEqual(log[3], "Post node")
        self.assertEqual(log[4], "Post node success")

    def test_execute_post_fail(self):
        with self.assertRaises(SystemExit) as sysexit:
            success, pipelines = self._run_yaml("yaml_executor_test_post_fail.yaml")
            self.assertEqual(sysexit.exception.code, 1)
            log = self._get_logs(pipelines.pipelines[0])[0]
            self.assertFalse(success)
            self.assertEqual(log[0], "Successful step")
            self.assertEqual(log[1], "Failed step")
            self.assertEqual(log[2], "Post stage")
            self.assertEqual(log[3], "Post stage fail")
            self.assertEqual(log[4], "Post node")
            self.assertEqual(log[5], "Post node fail")

    def test_parser(self):
        lucx_yaml_file = yaml_parser.LucxYaml(os.path.join(self.script_dir, "yaml_parser_test.yaml"))
        stages = lucx_yaml_file.pipelines.pipelines[0].nodes[0].stages
        self.assertEqual(stages[0].name, "Generate Stage")
        self.assertEqual(stages[0].steps[0].name, "Generate Step")
        self.assertEqual(stages[0].steps[0].cmd, "echo generating ...")
        self.assertEqual(stages[0].steps[0].path, "lucxbox/tools/yaml_executor/test/lib")
        self.assertEqual(stages[1].name, "Build Stage")
        self.assertEqual(stages[1].steps[0].name, "Build Step")
        self.assertEqual(stages[1].steps[0].cmd, "echo building ...")
        self.assertEqual(stages[1].steps[0].path, "lucxbox/tools/yaml_executor/test/lib")


if __name__ == "__main__":
    unittest.main()
