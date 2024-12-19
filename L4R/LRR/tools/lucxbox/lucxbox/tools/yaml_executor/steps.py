import glob
import os
import platform
import re
import shutil
import sys
from abc import ABC

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from lucxbox.tools.yaml_executor.credentials import PasswordCredential, SshCredential
from lucxbox.lib import lucxlog, portal
from lucxbox.lib.lucxutils import execute

LOGGER = lucxlog.get_logger()


class PipelineStep(ABC):
    def __init__(self, execution_order, name):
        self.execution_order = execution_order
        self.name = name
        self._used_log_path = None

    def execute(self, context):
        raise NotImplementedError()

    def write_to_log(self, context, text, append=False):
        with open(self._get_log_file_name(context.log_dir), 'a+' if append else 'w') as file:
            file.write(text)

    def _get_log_file_name(self, log_dir):
        if not self._used_log_path:
            log_file = os.path.join(log_dir, self.name + "_log.txt")
            name_expander = 1
            while os.path.exists(log_file):
                log_file = os.path.join(log_dir, "{}_log_{}.txt".format(self.name, name_expander))
                name_expander = name_expander + 1

            self._used_log_path = log_file

        return self._used_log_path

    def __repr__(self):
        return ('execution_order: ' + str(self.execution_order) + '\n' +
                'name: ' + self.name + '\n')


class FailedCmdError(Exception):
    pass

class PipelineGitCmdStep(PipelineStep):
    def __init__(self, execution_order, name, path, credentials_id, exec_statement):
        super().__init__(execution_order, name)
        self.path = path
        self.exec_statement = exec_statement
        self.credentials_id = credentials_id

    def execute(self, context):
        with portal.In(context.get_dir(self.path)):
            block = ''
            cmd_array = []
            for block_line in self.exec_statement.split(os.linesep):
                if block_line == '':
                    continue
                if block_line[len(block_line)-1:] == '\\':
                    block = '{a} {b}'.format(a=block, b=block_line[:-1].strip())
                    continue
                block = '{a} {b} 2>&1'.format(a=block, b=block_line.strip()).strip()
                cmd_array.append(block)
                block = ''

            if platform.system() == 'Windows':
                cmd = "C:\\Windows\\System32\\cmd.exe" + \
                    " /r " + "set GIT_SSH_COMMAND=ssh -i " + \
                    context.credential_manager.get_ssh_credential(self.credential_id).key_file + \
                    " -o StrictHostKeyChecking=no&&" + ';'.join(cmd_array)
                shell = False
            else:
                if context.credential_manager.get_ssh_credential(self.credentials_id).key_file == "-":
                    cmd = 'sh -c "' + \
                        (';'.join(cmd_array)).replace('"', '\\"').replace('$', '\\$') + '"'
                else:
                    cmd = 'sh -c "' + \
                        'export GIT_SSH_COMMAND=\\"ssh -i ' + \
                        context.credential_manager.get_ssh_credential(self.credential_id).key_file + \
                        ' -o StrictHostKeyChecking=no\\"&&' + \
                        (';'.join(cmd_array)).replace('"', '\\"').replace('$', '\\$') + \
                        '"'
                shell = True

            LOGGER.info("Executing: \n%s\n in %s", cmd, os.getcwd())
            out, err, returncode = execute(\
                cmd,
                shell=shell,
                continuous_output_callback=_on_output if context.continuous_output else None,
                env=context.env)

            self.write_to_log(context, out)
            self.write_to_log(context, err, True)

            if not context.continuous_output:
                if out:
                    LOGGER.info(out)
                if err:
                    LOGGER.error(err)

            if returncode != 0:
                LOGGER.error("Command failed with exit code %s: \n%s\n in %s \n Errors may be stated above.", returncode, cmd, os.getcwd())
                sys.exit(1)


    def __repr__(self):
        return super().__repr__() + ('path: ' + self.path + '\n' +
                                     'exec: ' + self.exec_statement + '\n' +
                                     'credentialsId: ' + self.credentials_id + '\n')


class PipelineCmdStep(PipelineStep):
    def __init__(self, execution_order, name, path, cmd):
        super().__init__(execution_order, name)
        self.path = path
        self.cmd = cmd

    def execute(self, context):
        with portal.In(context.get_dir(self.path)):
            block = ''
            cmd_array = []
            for block_line in self.cmd.split(os.linesep):
                if block_line == '':
                    continue
                if block_line[len(block_line)-1:] == '\\':
                    block = '{a} {b}'.format(a=block, b=block_line[:-1].strip())
                    continue
                block = '{a} {b}'.format(a=block, b=block_line.strip()).strip()
                cmd_array.append(block)
                block = ''

            if platform.system() == 'Windows':
                cmd = "C:\\Windows\\System32\\cmd.exe" + " /r " + ';'.join(cmd_array)
                shell = False
            else:
                cmd = 'sh -c "' + (';'.join(cmd_array)).replace('"', '\\"').replace('$', '\\$') + '"'
                shell = True

            LOGGER.info("Executing: \n%s\n in %s", cmd, os.getcwd())
            out, err, returncode = execute(\
                self._prepare_cmd(context, cmd),
                shell=shell,
                continuous_output_callback=_on_output if context.continuous_output else None,
                env=context.env, encoding=context.encoding)

            self.write_to_log(context, out)
            self.write_to_log(context, err, True)

            if not context.continuous_output:
                if out:
                    LOGGER.info(out)
                if err:
                    LOGGER.error(err)

            if returncode != 0:
                LOGGER.error("Command failed with exit code %s: \n%s\n in %s \n Errors may be stated above.", returncode, cmd, os.getcwd())
                sys.exit(1)

    @staticmethod
    def _prepare_cmd(context, cmd):
        cmd = PipelineCmdStep._replace_credentials(context, cmd, r'([\^@](USERNAME)(?::(.+);)?)', PasswordCredential)
        cmd = PipelineCmdStep._replace_credentials(context, cmd, r'([\^@](PASSWORD)(?::(.+);)?)', PasswordCredential)
        cmd = PipelineCmdStep._replace_credentials(context, cmd, r'([\^@](SSHUSERNAME)(?::(.+);)?)', SshCredential)
        cmd = PipelineCmdStep._replace_credentials(context, cmd, r'([\^@](SSHKEY)(?::(.+);)?)', SshCredential)

        return cmd

    @staticmethod
    def _replace_credentials(context, cmd, pattern, credential_type):
        matches = re.findall(pattern, cmd)
        counter = 1

        for complete, kind, credential_id in matches:
            credential_id = credential_id or credential_type.DEFAULT_CREDENTIAL_ID

            if kind == 'USERNAME':
                value = context.credential_manager.get_password_credential(credential_id).username
            elif kind == 'PASSWORD':
                value = context.credential_manager.get_password_credential(credential_id).password
            elif kind == 'SSHUSERNAME':
                value = context.credential_manager.get_ssh_credential(credential_id).username
            elif kind == 'SSHKEY':
                value = context.credential_manager.get_ssh_credential(credential_id).key_file
            else:
                raise ValueError('Unsupported credential type')

            env_name = kind + str(counter)
            counter += 1

            context.env[env_name] = value

            if platform.system() == 'Windows':
                env_ref = '%' + env_name + '%'
            else:
                env_ref = '${' + env_name + '}'

            cmd = cmd.replace(complete, env_ref)

        return cmd

    def __repr__(self):
        return super().__repr__() + ('path: ' + self.path + '\n' +
                                     'cmd: ' + self.cmd + '\n')


class PipelineWorkspaceSetEnvVarStep(PipelineStep):
    def __init__(self, execution_order, name, env_name, value):
        super().__init__(execution_order, name)
        self.env_name = env_name
        self.value = value

    def execute(self, context):
        LOGGER.info("Setting environment variable '%s' to '%s'", self.env_name, self.value)
        context.env[self.env_name] = self.value or ''

    def __repr__(self):
        return super().__repr__() + ('env_name: ' + self.env_name + '\n' +
                                     'value: ' + self.value + '\n')


class PipelineUtilCopyFilesStep(PipelineStep):
    def __init__(self, execution_order, name, source, destination, includes, flat):
        super().__init__(execution_order, name)
        self.source = source
        self.destination = destination
        self.includes = includes
        self.flat = flat

    @staticmethod
    def _wildcard_to_pattern(pattern):
        p_regex = pattern.replace('.', '\\.')
        p_regex = p_regex.replace("/", '\\/')
        p_regex = p_regex.replace('*', '[^\\/]*')
        p_regex = p_regex.replace('\\/[^\\/]*[^\\/]*\\/', '\\/.*')
        p_regex = p_regex.replace('[^\\/]*[^\\/]*', '.*')
        return p_regex

    def execute(self, context):
        source = context.get_dir(self.source)
        destination = context.get_dir(self.destination)

        LOGGER.info("Copying '%s' with filter '%s' to '%s'", source, self.includes, destination)

        for file in self._find_files(source):
            source_path = os.path.join(source, file)
            if self.flat:
                destination_path = os.path.join(destination, os.path.basename(file))
            else:
                destination_path = os.path.join(destination, os.path.relpath(file, source))

            LOGGER.debug("Copying '%s' to '%s'", source_path, destination_path)

            destination_dir = os.path.dirname(destination_path)
            os.makedirs(destination_dir, exist_ok=True)

            try:
                shutil.copy2(source_path, destination_path)
            except shutil.SameFileError:
                pass
            except shutil.Error as other:
                LOGGER.error("Unable to copy %s to %s.\n%s", source_path, destination_path, str(other))

    def _find_files(self, source):
        source_files = []
        for inc in self.includes.split(','):
            files = [x for x in glob.glob(os.path.join(source, inc.strip()), recursive=True) if os.path.isfile(x)]
            source_files.extend(files)
        return source_files

    def __repr__(self):
        return super().__repr__() + ('source: ' + self.source + '\n' +
                                     'destination: ' + self.destination + '\n' +
                                     'includes: ' + self.includes + '\n' +
                                     'flat: ' + str(self.flat) + '\n')


class PipelineUtilFailOnFilesMissingStep(PipelineStep):
    def __init__(self, execution_order, name, files, from_path):
        super().__init__(execution_order, name)
        self.files = files
        self.from_path = from_path

    def execute(self, context):
        missing = []

        from_path = context.get_dir(self.from_path)

        LOGGER.info("Checking existence of files '%s' in '%s'", self.files, from_path)

        for file in self.files:
            abs_path = os.path.join(from_path, file)

            LOGGER.debug("Checking existence of file '%s'", file)

            if os.path.isfile(abs_path):
                LOGGER.debug("ok")
            else:
                missing.append(abs_path)
                LOGGER.debug("missing")

        if missing:
            raise FileNotFoundError("'{}' are missing on disk: {}".format(len(missing), ', '.join(missing)))

    def __repr__(self):
        return super().__repr__() + ('files: ' + str(self.files) + '\n' +
                                     'from_path: ' + self.from_path + '\n')


def _on_output(_is_err, line):
    if _is_err:
        LOGGER.error(line)
    else:
        LOGGER.info(line)


class PipelineArtifactoryGetArtifactStep(PipelineStep):
    def __init__(self, execution_order, name, local_path, remote_path, force, repository, url):
        super().__init__(execution_order, name)
        self.local_path = local_path
        self.remote_path = remote_path
        self.force = force
        self.repository = repository
        self.url = url

    def execute(self, context):
        full_url = "{}/{}/{}".format(self.url, self.repository, self.remote_path)

        local_path = context.get_dir(self.local_path)

        LOGGER.info("Downloading artifact from '%s' to '%s'", full_url, local_path)
        if os.path.isfile(local_path) and not self.force:
            raise IOError(
                "http-get via curl failed because the destination file '{}' already exists".format(local_path))

        credential = context.credential_manager.get_password_credential(PasswordCredential.DEFAULT_CREDENTIAL_ID)

        out, err, return_code = execute(
            'curl -# --fail -u "{}:{}" -o "{}" "{}"'.format(credential.username, credential.password, local_path,
                                                            full_url),
            continuous_output_callback=_on_output if context.continuous_output else None)

        if not context.continuous_output:
            LOGGER.info(out)
            LOGGER.error(err)

        self.write_to_log(context, out)
        self.write_to_log(context, err, True)

        if return_code != 0:
            raise IOError("Artifactory download of '{}' to '{}' failed".format(full_url, local_path))

        LOGGER.info("Download of artifact '%s' to '%s' was successful", full_url, local_path)

    def __repr__(self):
        return super().__repr__() + ('local_path: ' + self.local_path + '\n' +
                                     'remote_path: ' + self.remote_path + '\n' +
                                     'force: ' + str(self.force) + '\n' +
                                     'repository: ' + self.repository + '\n' +
                                     'url: ' + self.url + '\n')


class PipelineArtifactoryGetBuildStep(PipelineStep):
    def __init__(self, execution_order, name, build_name, local_path, build_number, force, url):
        super().__init__(execution_order, name)
        self.build_name = build_name
        self.local_path = local_path
        self.build_number = build_number
        self.force = force
        self.url = url

    def execute(self, context):
        full_url = "{}/api/archive/buildArtifacts".format(self.url)
        body = '{"buildName":"' + self.build_name + '","buildNumber":"' + self.build_number + '","archiveType":"zip"}'

        local_path = context.get_dir(self.local_path)

        LOGGER.info("Downloading build '%s' version '%s' from '%s' to '%s'", self.build_name, self.build_number,
                    full_url, local_path)
        if os.path.isfile(local_path) and not self.force:
            raise IOError(
                "http-get via curl failed because the destination file '{}' already exists".format(local_path))

        credential = context.credential_manager.get_password_credential(PasswordCredential.DEFAULT_CREDENTIAL_ID)

        out, err, return_code = execute(
            'curl -# --fail -X POST -u "{}:{}" -H "Content-Type: application/json" -d "{}" -o "{}" "{}"'.format(
                credential.username, credential.password, body.replace('"', '\\"'), local_path, full_url),
            continuous_output_callback=_on_output if context.continuous_output else None)

        if not context.continuous_output:
            LOGGER.info(out)
            LOGGER.error(err)

        self.write_to_log(context, out)
        self.write_to_log(context, err, True)

        if return_code != 0:
            raise IOError("Download of build '{}' version '{}' from '{}' to '{}' failed".format(
                self.build_name, self.build_number, full_url, local_path))

        LOGGER.info("Download of build '%s' version '%s' from '%s' to '%s' was successful", self.build_name,
                    self.build_number, full_url, local_path)

    def __repr__(self):
        return super().__repr__() + ('build_name: ' + self.build_name + '\n' +
                                     'local_path: ' + self.local_path + '\n' +
                                     'build_number: ' + self.build_number + '\n' +
                                     'force: ' + str(self.force) + '\n' +
                                     'url: ' + self.url + '\n')


class PipelineSkipWrapBuildStep(PipelineStep):
    def __init__(self, execution_order, name, original_step, run_if_env_is_set, run_if_all_envs_set,
                 skip_if_env_is_set, skip_if_all_envs_set):
        super().__init__(execution_order, name)
        self.original_step = original_step
        self.run_if_env_is_set = run_if_env_is_set
        self.run_if_all_envs_set = run_if_all_envs_set
        self.skip_if_env_is_set = skip_if_env_is_set
        self.skip_if_all_envs_set = skip_if_all_envs_set

    def execute(self, context):
        def is_env_set(name):
            return context.env.get(name, 'false') != 'false'

        if self.run_if_env_is_set and not [env_var for env_var in self.run_if_env_is_set if is_env_set(env_var)]:
            return

        if self.run_if_all_envs_set and [env_var for env_var in self.run_if_all_envs_set if not is_env_set(env_var)]:
            return

        if self.skip_if_env_is_set and [env_var for env_var in self.skip_if_env_is_set if is_env_set(env_var)]:
            return

        if self.skip_if_all_envs_set and not [env_var for env_var in self.skip_if_all_envs_set if
                                              not is_env_set(env_var)]:
            return

        self.original_step.execute(context)

    def __repr__(self):
        return super().__repr__() + 'original_step: ' + repr(self.original_step) + '\n'
