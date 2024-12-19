# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  Copyright (c) 2022 by Robert Bosch GmbH. All rights reserved.
#
#  This file is property of Robert Bosch GmbH. Any unauthorized copy, use or
#  distribution is an offensive act against international law and may be
#  prosecuted under federal law. Its content is company confidential.
# =============================================================================
#  Filename: unify_reports.py
# ----------------------------------------------------------------------------
""" QAC test data for unified reports """
GIVEN_COLUMNS = [
    'Filename', 'Line number', 'Column number',
    'Producer component:Message number', 'Message text', 'Severity',
    'Suppression type bitmask', 'Suppression justification', 'Rule Group',
    'Rule text'
]
EXPECTED_COLUMNS = [
    'Filename', 'Line number', 'Column number', 'Sources',
    'Producer component:Message number', 'Message text', 'Severity',
    'Suppression Bitmask Set', 'Suppression type bitmask',
    'Suppression justification', 'Rule Group', 'Rule text'
]

SUMMARY_COLUMNS = ['Alias', 'Filename']

_LINE_A = [
    'a.cpp', 25, 7, 'msg_a_no', 'msg_a_text', 0, '4', '2', 'rule_group_a',
    'rule_text_a'
]
_LINE_B = [
    'b.cpp', 25, 7, 'msg_b_no', 'msg_b_text', 0, '4', '2', 'rule_group_b',
    'rule_text_b'
]
_LINE_C = [
    'c.cpp', 25, 7, 'msg_c_no', 'msg_c_text', 0, '4', '2', 'rule_group_c',
    'rule_text_c'
]
_LINE_D = [
    'd.cpp', 25, 7, 'msg_d_no', 'msg_d_text', 0, '4', '2', 'rule_group_d',
    'rule_text_d'
]
_LINE_E = [
    'e.cpp', 25, 7, 'msg_e_no', 'msg_e_text', 0, '4', '2', 'rule_group_e',
    'rule_text_e'
]
_LINE_F = [
    'f.cpp', 26, 8, 'msg_f_no', 'msg_f_text', 0, '4', '2', 'rule_group_f',
    'rule_text_f'
]
_DATA1 = [_LINE_A, _LINE_B, _LINE_C]
_DATA2 = [_LINE_B, _LINE_C, _LINE_D]
_DATA3 = [_LINE_C, _LINE_D, _LINE_E]
_DATA4 = [_LINE_F]

INPUTS_TXT = {"report1": _DATA1, "report2": _DATA2, "report3": _DATA3}
INPUTS_TXT_DISJUNCT = {"report1": _DATA1, "report4": _DATA4}

INPUTS_TXT_FILENAMES = ['report1', 'report2', 'report3']
INPUTS_TXT_FILENAMES_DISJUNCT = ['report1', 'report4']

INPUTS_SUM = [["0", "report1"], ["1", "report2"], ["2", "report3"]]
INPUTS_SUM_DISJUNCT = [["0", "report1"], ["1", "report4"]]

MERGED_REPORT = [[
    'a.cpp', 25, 7, '0', 'msg_a_no', 'msg_a_text', 0, '4', '4', '2',
    'rule_group_a', 'rule_text_a'
],
                 [
                     'b.cpp', 25, 7, '0,1', 'msg_b_no', 'msg_b_text', 0, '4',
                     '4', '2', 'rule_group_b', 'rule_text_b'
                 ],
                 [
                     'c.cpp', 25, 7, '0,1,2', 'msg_c_no', 'msg_c_text', 0, '4',
                     '4', '2', 'rule_group_c', 'rule_text_c'
                 ],
                 [
                     'd.cpp', 25, 7, '1,2', 'msg_d_no', 'msg_d_text', 0, '4',
                     '4', '2', 'rule_group_d', 'rule_text_d'
                 ],
                 [
                     'e.cpp', 25, 7, '2', 'msg_e_no', 'msg_e_text', 0, '4',
                     '4', '2', 'rule_group_e', 'rule_text_e'
                 ]]

MERGED_REPORT_DISJUNCT = [[
    'a.cpp', 25, 7, '0', 'msg_a_no', 'msg_a_text', 0, '4', '4', '2',
    'rule_group_a', 'rule_text_a'
],
                          [
                              'b.cpp', 25, 7, '0', 'msg_b_no', 'msg_b_text', 0,
                              '4', '4', '2', 'rule_group_b', 'rule_text_b'
                          ],
                          [
                              'c.cpp', 25, 7, '0', 'msg_c_no', 'msg_c_text', 0,
                              '4', '4', '2', 'rule_group_c', 'rule_text_c'
                          ],
                          [
                              'f.cpp', 26, 8, '1', 'msg_f_no', 'msg_f_text', 0,
                              '4', '4', '2', 'rule_group_f', 'rule_text_f'
                          ]]
