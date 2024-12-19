import argparse
import subprocess
import logging
import os
import tempfile
import time
import sys
import shutil

import pathlib

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.tools.yaml_executor import yaml_parser
from lucxbox.tools.yaml_executor.context import Context
from lucxbox.tools.yaml_executor.credentials import CredentialManager, PasswordCredential, SshCredential
from lucxbox.lib import lucxlog, lucxargs, portal
from lucxbox.lib.lucxutils import execute

LOGGER = lucxlog.get_logger()


def generate_preprocessed_yaml(args):
    with portal.In(args.lucx_dir):
        log_file_path = os.path.join(args.log_dir, "YAML_preprocess_log.txt")
        file_name = os.path.basename(args.yaml).split('.')[0]
        output_yaml = os.path.join(args.output, file_name + ".postprocessed.yaml")

        if not os.path.isfile(args.yaml):
            LOGGER.error("%s does not exist!", args.yaml)
            sys.exit(1)
        if os.path.isfile(output_yaml):
            os.remove(output_yaml)
        if not os.path.isdir(args.output):
            os.mkdir(args.output, 0o755)

        # prepare the jar command
        cmd = 'java -jar ' + args.lucxlib
        cmd += ' --file ' + args.yaml
        cmd += ' --output ' + args.output
        if args.parameter:
            cmd += ' ' + ' '.join([f"-p {x}" for x in args.parameter])
        if args.include:
            cmd += ' ' + ' '.join([f"-i {x}" for x in args.include])
        if LOGGER.level <= logging.DEBUG:
            cmd += " -d"

        with open(log_file_path, "w") as log_file:
            LOGGER.debug(cmd)
            _, _, returncode = execute(cmd, stdout=log_file, stderr=subprocess.STDOUT, shell=True)
        if returncode != 0:
            LOGGER.error("'%s' failed.\nUnable to create .yaml file.", cmd)
            sys.exit(1)
        return output_yaml


def check_py_ver36():
    # Check for python version 3.6+
    return sys.version_info.major == 3 and sys.version_info.minor >= 6


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yaml", help="the root yaml file", required=True, type=lucxargs.existing_file)
    parser.add_argument("-l", "--lucxlib", help="path to lucxbau.jar", required=True, type=lucxargs.existing_file)
    parser.add_argument("--lucx-dir", help="path to lucx execution directory, usually repository root",
                        required=False, type=lucxargs.existing_directory)
    parser.add_argument("-r", "--root-dir", help="path to com mand execution directory, usually repository root",
                        required=True, type=lucxargs.existing_directory)
    parser.add_argument("-o", "--output", help="output directory", required=False, type=lucxargs.existing_directory,
                        default=tempfile.gettempdir())
    parser.add_argument("-c", "--continuous-output", help="print continuous output", action='store_true')
    parser.add_argument("--log-dir", help="logs output directory", required=False)
    parser.add_argument("--pwd", help="Specify a password credential of the form user:password or id:user:password",
                        required=False, nargs='*')
    parser.add_argument("--ssh", help="Specify a private SSH key credential of the form id:user:ssh-key-path",
                        required=False, nargs='*')
    parser.add_argument("--credentials", help="Specify a path to a file with the credentials. A line represents a "
                                              "credential of the form type:credential_data",
                        required=False)
    parser.add_argument("--encoding", help="Specify a default encoding for the commands output.",
                        required=False, default='latin1')
    parser.add_argument("-p", "--parameter", help="Specify parameters used for .yaml processing",
                        required=False, nargs="*")
    parser.add_argument("-i", "--include", help="Specify include directories used for .yaml processing",
                        required=False, nargs="*")
    parser = lucxargs.add_log_level(parser)
    args = parser.parse_args()
    if not args.lucx_dir:
        args.lucx_dir = args.root_dir
    return args


def parse_credentials(args, credential_manager):
    if args.pwd:
        for pwd in args.pwd:
            credential_manager.add(PasswordCredential.parse(pwd))

    if args.ssh:
        for ssh in args.ssh:
            credential_manager.add(SshCredential.parse(ssh))

    if args.credentials:
        with open(args.credentials, 'r') as file_handle:
            for line in file_handle.readlines():
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                parts = line.split(':')
                kind = parts[0]
                rest = ':'.join(parts[1:])

                if kind == 'pwd':
                    credential_manager.add(PasswordCredential.parse(rest))
                elif kind == 'ssh':
                    credential_manager.add(SshCredential.parse(rest))
                else:
                    LOGGER.warning('Ignoring unknown credential type "%s"', kind)


def parse(args):
    # init log_dir
    if not args.log_dir:
        args.log_dir = os.path.join(args.output, "logs")
    if not os.path.isabs(args.log_dir):
        args.log_dir = os.path.join(args.root_dir, args.log_dir)
    # For consistency logs must be saved in absolute path
    args.log_dir = str(pathlib.Path(args.log_dir).resolve())
    if os.path.isdir(args.log_dir):
        LOGGER.info("Removing: %s", args.log_dir)
        shutil.rmtree(args.log_dir)
    time.sleep(1)
    os.mkdir(args.log_dir, 0o755)

    # generate the YAML file
    preprocessed_yaml = generate_preprocessed_yaml(args)
    if os.path.isfile(preprocessed_yaml):
        LOGGER.debug("Created %s", preprocessed_yaml)
    else:
        LOGGER.error("Could not create %s!\nCheck %s for information.", preprocessed_yaml, args.log_dir)
        sys.exit(1)

    lucx_yaml_file = yaml_parser.LucxYaml(preprocessed_yaml)
    return lucx_yaml_file.pipelines


def run_steps(context, steps):
    for step in steps:
        LOGGER.debug(str(step))
        step.execute(context)


def run_stage(context, stage):
    try:
        try:
            run_steps(context, stage.steps)

            run_steps(context, stage.post_success_steps)
        except:
            run_steps(context, stage.post_fail_steps)
            raise
    finally:
        run_steps(context, stage.post_steps)


def run_stages(context, stages):
    for stage in stages:
        run_stage(context, stage)


def run_node(context, node):
    try:
        try:
            run_stages(context, node.stages)

            run_stages(context, node.post_success_stages)
        except:
            run_stages(context, node.post_fail_stages)
            raise
    finally:
        run_stages(context, node.post_stages)


def run_pipeline(main_context, pipeline):
    context = main_context.clone()

    for node in pipeline.nodes:
        run_node(context, node)


def run_pipelines(main_context, pipelines):
    try:
        try:
            for node in pipelines.pre_nodes:
                run_node(main_context.clone(), node)

            for pipeline in pipelines.pipelines:
                run_pipeline(main_context, pipeline)

            for node in pipelines.post_success_nodes:
                run_node(main_context.clone(), node)
        except:
            for node in pipelines.post_fail_nodes:
                run_node(main_context.clone(), node)
            raise
    finally:
        for node in pipelines.post_nodes:
            run_node(main_context.clone(), node)


def run(args, pipelines):
    credential_manager = CredentialManager()

    parse_credentials(args, credential_manager)

    main_context = Context(args.root_dir, args.log_dir, args.continuous_output, credential_manager, encoding=args.encoding)
    run_pipelines(main_context, pipelines)


def main():
    if not check_py_ver36():
        sys.exit("Please use a python version >= 3.6")

    args = parse_args()
    LOGGER.setLevel(args.log_level)

    pipelines = parse(args)
    run(args, pipelines)


if __name__ == "__main__":
    main()
