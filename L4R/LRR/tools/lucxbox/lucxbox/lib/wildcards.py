""" Wildcard is a library for helping you match regex stuff. """
import re

# Cache for precompiled regex pattern to improve performance
CACHE = {}


def matches_wildcard_pattern(string, wildcard_expression):
    """
    Method for checking if string matches a unix-like wildcard
    expression.
    """
    string = string.replace('\\', '/')

    if wildcard_expression not in CACHE:
        regex_pattern = wildcard_expression.replace('.', '\\.')
        regex_pattern = regex_pattern.replace("/", '\\/')
        regex_pattern = regex_pattern.replace('*', '[^\\/]*')
        regex_pattern = regex_pattern.replace('[^\\/]*[^\\/]*', '.*')
        regex = re.compile(regex_pattern)
        CACHE[wildcard_expression] = regex
    else:
        regex = CACHE[wildcard_expression]

    match = re.match(regex, string)

    return match and match.group(0) == string
