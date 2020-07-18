import unittest
import mock
from Utilities.Util import *


class UtilitiesTest(unittest.TestCase):

    def test_random_number_gen(self):
        # Act
        random_number = random_num_gen(10)

        # Assert
        self.assertTrue(isinstance(random_number, str))
        self.assertEqual(len(random_number), 10)
        self.assertTrue(random_number.isdigit())

    @mock.patch('builtins.print')
    def test_decorate_heading(self, mock_print):
        # Act
        decorate_heading("myHeading")

        # Assert
        mock_print.assert_called_once()


if __name__ == '__main__':
    unittest.main()
