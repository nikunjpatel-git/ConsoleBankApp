import unittest
import mock
import sys
import os
from database.dbconnector import DbConnector
from Models.TransactionData import Transaction
from Models.BeneficiaryData import Beneficiary
from Home import dashboard


class HomeTest(unittest.TestCase):

    def raise_exception(self):
        raise AttributeError

    @mock.patch.object(Beneficiary, 'set_beneficiary')
    @mock.patch.object(Transaction, 'add_transaction')
    @mock.patch('Home.decorate_heading')
    @mock.patch('Home.os')
    @mock.patch('builtins.print')
    @mock.patch('builtins.input', )
    def test_dashboard_ok(self, mock_input, mock_print, mock_os, mock_decorate_heading, mock_add_transaction, mock_set_beneficiary):
        # Arrange
        mock_customer = mock.Mock()
        mock_db = mock.Mock()
        mock_input.side_effect = ("1", "2", "3", "4", "5", self.raise_exception())

        # Act
        try:
            dashboard(mock_customer, mock_db)
        except Exception as e:
            print("Exception handled")
        finally:
            # dashboard(mock_customer, mock_db)
            # Assert
            self.assertEqual(mock_input.call_count, 6)
            self.assertEqual(mock_decorate_heading.call_count, 6)
            mock_customer.update_info.assert_called_once()
            mock_add_transaction.assert_called_once()
            mock_customer.change_mpin.assert_called_once()
            mock_customer.add_cards.assert_called_once()
            mock_set_beneficiary.assert_called_once()
            mock_db.add_beneficiary.assert_called_once()


if __name__ == '__main__':
    unittest.main()
