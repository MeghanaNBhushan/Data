# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: cov_test_data.py
# ----------------------------------------------------------------------------
""" Coverity test data for unified reports """
COL_FILENAME = 'strippedMainEventFilePathname'
COL_MERGEKEY = 'mergeKey'
COL_COUNT = 'occurrenceCountForMK'
COL_NUMBER = 'occurrenceNumberInMK'
COL_CHECKNAME = 'checkerName'
COL_SUBCATEGORY = 'subcategory'
COL_TYPE = 'type'
COL_SUBTYPE = 'subtype'
COL_CODELANG = 'code-language'
COL_EXTRA = 'extra'
COL_DOMAIN = 'domain'
COL_LANG = 'language'
COL_LINE = 'mainEventLineNumber'
COL_DISPNAME = 'functionDisplayName'
COL_MANGNAME = 'functionMangledName'
COL_CATEGORY = 'category'
COL_DESCRIPT = 'categoryDescription'
COL_CWECAT = 'cweCategory'
COL_IMPACT = 'impact'
COL_IMPACTDESC = 'impactDescription'
COL_SUBCATEFFFECT = 'subcategoryLocalEffect'
COL_SUBCATDESC = 'subcategoryShortDescription'
COL_SUBCATDESCLONG = 'subcategoryLongDescription'
COL_FILENAME_LONG = 'mainEventFilePathname'
COL_SOURCES = 'Sources'
COL_TEAM = 'Team'
COL_COMPONENTS = 'Components'

GIVEN_COLUMNS = [
    COL_FILENAME, COL_MERGEKEY, COL_COUNT, COL_NUMBER, COL_CHECKNAME,
    COL_SUBCATEGORY, COL_TYPE, COL_SUBTYPE, COL_CODELANG, COL_EXTRA,
    COL_DOMAIN, COL_LANG, COL_LINE, COL_DISPNAME, COL_MANGNAME, COL_CATEGORY,
    COL_DESCRIPT, COL_CWECAT, COL_IMPACT, COL_IMPACTDESC, COL_SUBCATEFFFECT,
    COL_SUBCATDESC, COL_SUBCATDESCLONG, COL_FILENAME_LONG, COL_TEAM,
    COL_COMPONENTS
]
EXPECTED_COLUMNS = [
    COL_FILENAME, COL_MERGEKEY, COL_SOURCES, COL_COUNT, COL_NUMBER,
    COL_CHECKNAME, COL_SUBCATEGORY, COL_TYPE, COL_SUBTYPE, COL_CODELANG,
    COL_EXTRA, COL_DOMAIN, COL_LANG, COL_LINE, COL_DISPNAME, COL_MANGNAME,
    COL_CATEGORY, COL_DESCRIPT, COL_CWECAT, COL_IMPACT, COL_IMPACTDESC,
    COL_SUBCATEFFFECT, COL_SUBCATDESC, COL_SUBCATDESCLONG, COL_FILENAME_LONG,
    COL_TEAM, COL_COMPONENTS
]

SUMMARY_COLUMNS = ['Alias', 'Filename']

_LINE_A = [
    'a.cpp', 1, '1', '1', 'DEADCODE', 'none', '', '', '', 'x', 'STATIC_C',
    'C++', '24',
    'his_test_function(int, int, int, int, int, int, int, int, int, int)',
    '_Z17his_test_functioniiiiiiiiii', 'Control flow issues',
    'Control flow issues', '561', 'Medium', 'Medium',
    'The indicated dead code may have performed some action; that action will \
        never occur.', 'Logically dead code',
    'Code can never be reached because of a logical contradiction',
    'D:\\sca_mini_demo\\src\\demo\\a.cpp', 'demo_team', 'demo'
]
_LINE_B = [
    'b.cpp', 2, '1', '1', 'UNCAUGHT_EXCEPT', 'none', '', '', '', 'failure',
    'STATIC_C', 'C++', '86', 'main', 'main', 'Error handling issues',
    'Error handling issues', '248', 'Medium', 'Medium',
    'If the exception is ever thrown, the program will crash.',
    'Uncaught exception', 'A C++ exception is thrown but never caught',
    'D:\\sca_mini_demo\\src\\demo\\b.cpp', 'demo_team', 'demo'
]
_LINE_C = [
    'c.cpp', 3, '1', '1', 'UNCAUGHT_EXCEPT', 'none', '', '', '',
    'runtime_error', 'STATIC_C', 'C++', '86', 'main', 'main',
    'Memory - corruptions', 'Memory - corruptions', '0', 'Medium', 'Medium',
    'Memory may be overwritten before it is read.',
    'Assignment of overlapping memory', '',
    'D:\\sca_mini_demo\\src\\demo\\c.cpp', 'demo_team', 'demo'
]
_LINE_D = [
    'd.cpp', 4, '1', '1', 'DIVIDE_BY_ZERO', 'none', '', '', '', 'denominator',
    'STATIC_C', 'C++', '91', 'demo::control_flow(int)',
    '_ZN4demo12control_flowEi', 'Integer handling issues',
    'Integer handling issues', '369', 'Medium', 'Medium',
    'The program will have undefined behavior, likely a crash.',
    'Division or modulo by zero',
    'Division or modulo by zero results in undefined behavior.',
    'D:\\sca_mini_demo\\src\\demo\\d.cpp', 'demo_team', 'demo'
]
_LINE_E = [
    'e.cpp', 5, '1', '1', 'CONSTANT_EXPRESSION_RESULT',
    'result_independent_of_operands', '', '', '', '', 'STATIC_C', 'C++', '113',
    'demo::data_flow(int)', '_ZN4demo9data_flowEi', 'Uninitialized variables',
    'Uninitialized variables', '457', 'High', 'High',
    'The variable will contain an arbitrary value left from earlier \
        computations.', 'Uninitialized scalar variable',
    'Use of an uninitialized variable', 'D:\\sca_mini_demo\\src\\demo\\e.cpp',
    'demo_team', 'demo'
]
_DATA1 = [_LINE_A, _LINE_B, _LINE_C]
_DATA2 = [_LINE_B, _LINE_C, _LINE_D]
_DATA3 = [_LINE_C, _LINE_D, _LINE_E]

INPUTS_TXT = {"report1": _DATA1, "report2": _DATA2, "report3": _DATA3}

INPUTS_TXT_FILENAMES = ['report1', 'report2', 'report3']

INPUTS_SUM = [["0", "report1"], ["1", "report2"], ["2", "report3"]]

_LINE_A_EXP = _LINE_A.copy()
_LINE_B_EXP = _LINE_B.copy()
_LINE_C_EXP = _LINE_C.copy()
_LINE_D_EXP = _LINE_D.copy()
_LINE_E_EXP = _LINE_E.copy()

_LINE_A_EXP.insert(2, '0')
_LINE_B_EXP.insert(2, '0,1')
_LINE_C_EXP.insert(2, '0,1,2')
_LINE_D_EXP.insert(2, '1,2')
_LINE_E_EXP.insert(2, '2')

MERGED_REPORT = [
    _LINE_A_EXP, _LINE_B_EXP, _LINE_C_EXP, _LINE_D_EXP, _LINE_E_EXP
]
