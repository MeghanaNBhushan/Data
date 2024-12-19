""" Test for repository miner reader """

import unittest
from unittest import mock

from lucxbox.tools.repository_miner_reader import repository_miner_reader


class TestCommentCreatorMethods(unittest.TestCase):
    """ Test class for the creator of the txt file containing the comment that shall be posted to Bitbucket """

    @mock.patch("lucxbox.tools.repository_miner_reader.repository_miner_reader.get_modifications_in_branch")
    @mock.patch("lucxbox.tools.repository_miner_reader.repository_miner_reader.get_association_rules")
    def test_get_comment(self, mock_get_modifications, mock_get_association_rules):
        mock_get_modifications.return_value = ["package/script_1.py", "package/script_2.py"]
        mock_get_association_rules.return_value = {
            "1":
                {
                    "antecedent": ["package/script_1.py"],
                    "consequent": ["package/script_3.py"],
                    "confidence": 0.6
                }
        }

        result = repository_miner_reader.get_comment(mock_get_association_rules.return_value,
                                                     mock_get_modifications.return_value,
                                                     None,
                                                     'develop')
        expected_result = 'Based on association analysis of the previous commit history you should also check if ' \
                          'modifications in following files are needed:' +\
                          '\\n - {}, Probability for required changes: {}'.format(
                              mock_get_association_rules.return_value["1"]["consequent"][0],
                              mock_get_association_rules.return_value["1"]["confidence"])
        self.assertMultiLineEqual(expected_result, result)


if __name__ == "__main__":
    unittest.main()
