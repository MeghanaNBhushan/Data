import os
import sys
import yaml

from lucxbox.tools.yaml_executor.pipeline import Pipelines, Pipeline, Node, Stage

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.lib import lucxlog
# pylint: disable=no-name-in-module
from lucxbox.tools.yaml_executor.steps import PipelineCmdStep, PipelineWorkspaceSetEnvVarStep, \
    PipelineUtilCopyFilesStep, PipelineUtilFailOnFilesMissingStep, PipelineArtifactoryGetArtifactStep, \
    PipelineArtifactoryGetBuildStep, PipelineSkipWrapBuildStep, PipelineGitCmdStep

LOGGER = lucxlog.get_logger()


class LucxYaml:
    STAGE_FACTOR = 100
    NODE_FACTOR = STAGE_FACTOR * 100

    def __init__(self, file_path):
        self.properties = {}
        self.pipelines = None
        self.unique_name_counter = 0
        self.read_yaml(file_path)

    def read_yaml(self, yaml_path):
        with open(yaml_path) as file:
            data = yaml.load(file, Loader=yaml.FullLoader)

        if 'properties' in data:
            self.properties = data['properties']

        pre_nodes = []
        if 'pre' in data:
            pre_nodes = self._parse_nodes(data['pre'])

        post_nodes = []
        if 'post' in data:
            post_nodes = self._parse_nodes(data['post'])

        post_success_nodes = []
        if 'postSuccess' in data:
            post_success_nodes = self._parse_nodes(data['postSuccess'])

        post_fail_nodes = []
        if 'postFail' in data:
            post_fail_nodes = self._parse_nodes(data['postFail'])

        pipelines = self._parse_pipelines(data['pipelines'])

        self.pipelines = Pipelines(pipelines, pre_nodes, post_nodes, post_success_nodes, post_fail_nodes)

    def _parse_pipelines(self, yaml_nodes):
        return [self._parse_pipeline(yaml_node) for yaml_node in yaml_nodes]

    def _parse_pipeline(self, yaml_node):
        nodes = self._parse_nodes(yaml_node['nodes'])

        return Pipeline(nodes)

    def _parse_nodes(self, yaml_nodes):
        return sorted([self._parse_node(yaml_node) for yaml_node in yaml_nodes], key=lambda node: node.execution_order)

    def _parse_node(self, yaml_node):
        execution_order = yaml_node['executionOrder']
        stages = self._parse_stages(yaml_node['stages'], yaml_node)

        post_stages = []
        if 'post' in yaml_node:
            post_stages = self._parse_stages(yaml_node['post'], yaml_node)

        post_success_stages = []
        if 'postSuccess' in yaml_node:
            post_success_stages = self._parse_stages(yaml_node['postSuccess'], yaml_node)

        post_fail_stages = []
        if 'postFail' in yaml_node:
            post_fail_stages = self._parse_stages(yaml_node['postFail'], yaml_node)

        return Node(execution_order, stages, post_stages, post_success_stages, post_fail_stages)

    def _parse_stages(self, yaml_nodes, node_yaml_node):
        stages = []
        stage_num = 0

        for yaml_node in yaml_nodes:
            stage = self._parse_stage(stage_num, yaml_node, node_yaml_node)
            stages.append(stage)

            stage_num += 1

        return sorted(stages, key=lambda s: s.execution_order)

    def _parse_stage(self, stage_num, yaml_node, node_yaml_node):
        name = yaml_node.get('name')
        execution_order = yaml_node.get('executionOrder', stage_num)

        steps = []
        if 'steps' in yaml_node:
            steps = self._parse_steps(yaml_node['steps'], yaml_node, node_yaml_node)

        post_steps = []
        if 'post' in yaml_node:
            post_steps = self._parse_steps(yaml_node['post'], yaml_node, node_yaml_node)

        post_success_steps = []
        if 'postSuccess' in yaml_node:
            post_success_steps = self._parse_steps(yaml_node['postSuccess'], yaml_node, node_yaml_node)

        post_fail_steps = []
        if 'postFail' in yaml_node:
            post_fail_steps = self._parse_steps(yaml_node['postFail'], yaml_node, node_yaml_node)

        return Stage(name, execution_order, steps, post_steps, post_success_steps, post_fail_steps)

    def _parse_steps(self, yaml_nodes, stage_yaml_node, node_yaml_node):
        steps = []
        step_num = 0

        for yaml_node in yaml_nodes:
            step = self._parse_step(step_num, yaml_node, stage_yaml_node, node_yaml_node)
            if step:
                steps.append(step)

            step_num += 1

        return sorted(steps, key=lambda s: s.execution_order)

    def _parse_step(self, step_num, yaml_node, stage_yaml_node, node_yaml_node):
        step = None

        if "call" in yaml_node:
            call = yaml_node['call']

            if call == 'Workspace.setEnvVar':
                step = self._parse_set_env_var_step(step_num, yaml_node)
            elif call == 'Util.copyFiles':
                step = self._parse_copy_files_step(step_num, yaml_node)
            elif call == 'Util.failOnFilesMissing':
                step = self._parse_fail_on_missing_step(step_num, yaml_node)
            elif call == 'Artifactory.getArtifact':
                step = self._parse_get_artifact_step(step_num, yaml_node)
            elif call == 'Artifactory.getBuild':
                step = self._parse_get_build_step(step_num, yaml_node)
            elif call == 'Git.cmd':
                step = self._parse_git_cmd_step(step_num, yaml_node)
            else:
                LOGGER.debug("Skipping unsupported 'call %s'", call)
                # Future additions for the parser will be added here
        elif "cmd" in yaml_node:
            step = self._parse_cmd_step(step_num, yaml_node)

        if step:
            step = self._handle_skip(step, yaml_node, stage_yaml_node, node_yaml_node)

        return step

    def _get_unique_name(self, prefix):
        name = prefix + str(self.unique_name_counter)
        self.unique_name_counter += 1
        return name

    def _parse_cmd_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        path = yaml_node.get('fromPath', '')
        cmd = yaml_node['cmd'].replace('""', '\'""\'')

        return PipelineCmdStep(execution_order, name, path, cmd)

    def _parse_set_env_var_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        env_name = yaml_node['name']
        value = yaml_node.get('value', '')

        return PipelineWorkspaceSetEnvVarStep(execution_order, name, env_name, value)

    def _parse_copy_files_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        source = yaml_node['source']
        destination = yaml_node['destination']
        includes = yaml_node['includes']
        flat = yaml_node.get('flat', False)

        return PipelineUtilCopyFilesStep(execution_order, name, source, destination, includes, flat)

    def _parse_fail_on_missing_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        files = yaml_node['files'].split(',')
        from_path = yaml_node.get('fromPath', '')

        return PipelineUtilFailOnFilesMissingStep(execution_order, name, files, from_path)

    def _parse_get_artifact_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        local_path = yaml_node['localPath']
        remote_path = yaml_node['remotePath']
        artifactory_properties = self.properties.get('artifactory', {})
        repository = yaml_node.get('repository', artifactory_properties.get('repository'))
        url = yaml_node.get('url', artifactory_properties.get('url'))

        if repository is None:
            raise ValueError("Artifactory.getArtifact requires the Artifactory repository to be specified")

        if url is None:
            raise ValueError("Artifactory.getArtifact requires the Artifactory url to be specified")

        force = yaml_node.get('force', False)

        return PipelineArtifactoryGetArtifactStep(execution_order, name, local_path, remote_path, force, repository,
                                                  url)

    def _parse_get_build_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        build_name = yaml_node['buildName']
        local_path = yaml_node['localPath']
        build_number = yaml_node.get('buildNumber', 'LATEST')
        artifactory_properties = self.properties.get('artifactory', {})
        url = yaml_node.get('url', artifactory_properties.get('url'))

        if url is None:
            raise ValueError("Artifactory.getArtifact requires the Artifactory url to be specified")

        force = yaml_node.get('force', False)

        return PipelineArtifactoryGetBuildStep(execution_order, name, build_name, local_path, build_number, force, url)

    def _parse_git_cmd_step(self, step_num, yaml_node):
        execution_order = yaml_node.get('executionOrder', step_num)
        name = yaml_node.get('name', self._get_unique_name('exec_'))
        from_path = yaml_node.get('fromPath', '')
        credentials_id = yaml_node.get('credentialsId', '')
        exec_statement = yaml_node.get('exec', '')

        return PipelineGitCmdStep(execution_order, name, from_path, credentials_id, exec_statement)

    @staticmethod
    def _handle_skip(original_step, step_yaml_node, stage_yaml_node, node_yaml_node):
        run_if_env_is_set = None
        run_if_all_envs_set = None
        skip_if_env_is_set = None
        skip_if_all_envs_set = None

        for yaml_node in [node_yaml_node, stage_yaml_node, step_yaml_node]:
            # stage_yaml_node, node_yaml_node is set to None for steps inside pre on topmost level
            if yaml_node is None:
                continue

            if yaml_node.get('skip', False):
                return None

            run_if_env_is_set = yaml_node.get('runIfEnvIsSet', run_if_env_is_set)
            run_if_all_envs_set = yaml_node.get('runIfAllEnvsSet', run_if_all_envs_set)
            skip_if_env_is_set = yaml_node.get('skipIfEnvIsSet', skip_if_env_is_set)
            skip_if_all_envs_set = yaml_node.get('skipIfAllEnvsSet', skip_if_all_envs_set)

        if run_if_env_is_set or run_if_all_envs_set or skip_if_env_is_set or skip_if_all_envs_set:
            return PipelineSkipWrapBuildStep(original_step.execution_order, original_step.name, original_step,
                                             run_if_env_is_set, run_if_all_envs_set, skip_if_env_is_set,
                                             skip_if_all_envs_set)

        return original_step
