""" Simple config file parser

Supports following cases:
- ignore header
- allows "#" comments
- ignores empty lines

Will return a dict of key value pairs seperated by "="
"""

import os
import sys


def parse(logger, file_name, header=None):
    if not os.path.isfile(file_name):
        logger.error("Config file not found.")
        sys.exit(1)

    with open(file_name, 'r') as config_file:
        content = config_file.read()

    lines = content.split("\n")
    config = {}

    i = 0
    for line in lines:
        i = i + 1
        try:
            if line.strip().startswith("#"):
                continue
            if line.strip() == header:
                continue
            if not line.strip():
                continue
            key, value = line.split("=")
            config[key.strip().lower()] = value.strip()
        except ValueError as exception:
            logger.error("Config file has wrong format: %s:%s: %s",
                         os.path.abspath(file_name), i, exception)
            sys.exit(1)
    return config
