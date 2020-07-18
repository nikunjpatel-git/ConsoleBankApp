import mock
import unittest
from Models.BeneficiaryData import Beneficiary


class BeneficiaryTest(unittest.TestCase):
    def setUp(self):
        self.beneficiary = Beneficiary()

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_set_beneficiary_Ok(self, mock_input, mock_print):
        mock_input.side_effect = ("ben_name", "BKID0123456", "123456123456")
        self.beneficiary.set_beneficiary()

        # Assert
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(self.beneficiary.name, "ben_name")
        self.assertEqual(self.beneficiary.ifsc_code, "BKID0123456")
        self.assertEqual(self.beneficiary.account_number, "123456123456")

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_set_beneficiary_invalid_ifsc_code(self, mock_input, mock_print):
        mock_input.side_effect = ("ben_name", "BKID012356", "BKI0123456", "BKID012456", "",
                                  "BKID0123456", "123456123456")
        self.beneficiary.set_beneficiary()
        input_args = ("Enter Beneficiary Name:", "Enter IFSC code: ", "Enter Account Number: ")

        # assert
        calls = [mock.call(input_args[0],), mock.call(input_args[1],), mock.call(input_args[1],),
                 mock.call(input_args[1],), mock.call(input_args[1],), mock.call(input_args[1],),
                 mock.call(input_args[2],)]
        self.assertEqual(mock_input.call_count, 7)
        self.assertEqual(mock_input.call_args_list, calls)
        self.assertEqual(self.beneficiary.name, "ben_name")
        self.assertEqual(self.beneficiary.ifsc_code, "BKID0123456")
        self.assertEqual(self.beneficiary.account_number, "123456123456")

    @mock.patch('builtins.print')
    @mock.patch('builtins.input')
    def test_set_beneficiary_invalid_account_number(self, mock_input, mock_print):
        mock_input.side_effect = ("ben_name", "BKID0123456", "123456", "abcd1234",
                                  "123456123456789", "", "123456123456")
        self.beneficiary.set_beneficiary()
        input_args = ("Enter Beneficiary Name:", "Enter IFSC code: ", "Enter Account Number: ")

        # assert
        calls = [mock.call(input_args[0], ), mock.call(input_args[1], ), mock.call(input_args[2], ),
                 mock.call(input_args[2], ), mock.call(input_args[2], ), mock.call(input_args[2], ),
                 mock.call(input_args[2], )]
        self.assertEqual(mock_input.call_count, 7)
        self.assertEqual(mock_input.call_args_list, calls)
        self.assertEqual(self.beneficiary.name, "ben_name")
        self.assertEqual(self.beneficiary.ifsc_code, "BKID0123456")
        self.assertEqual(self.beneficiary.account_number, "123456123456")


if __name__ == "__main__":
    unittest.main()

