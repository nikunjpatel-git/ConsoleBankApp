import unittest
import mock
from Models.TransactionData import Transaction
from Models.CustomerData import Customer


class TransactionTest(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=("123412341234", "5"))
    def test_add_transaction_ok(self, mock_input, mock_print):
        # Arrange
        transaction = Transaction()
        # mock dbConnector
        mockdb = mock.Mock()
        sender = Customer()
        sender.cust_id, sender.userName, sender.address, sender.bal, sender.accountNumber = \
            (2, "sender", "send_add", 200, "789078907890")
        receiver = (1, "receiver", "receive_add", "123412341234", "1234567890", 500, "456745674567")
        mockdb.check_receiver.return_value = receiver
        input_args = ("Enter the recipient account number: ", "Enter transaction amount: ")

        # Act
        transaction.add_transaction(sender, Customer(), mockdb)

        # Assert
        calls = [mock.call(input_args[0], ), mock.call(input_args[1], )]
        mockdb.check_receiver.assert_called_once()
        self.assertEqual(mock_input.call_count, 2)
        self.assertEqual(mock_input.call_args_list, calls)
        mockdb.add_transaction_to_db.assert_called_once()
        mock_print.assert_not_called()

        self.assertEqual(transaction.sender, sender)
        self.assertEqual(transaction.amount, 5)
        self.assertEqual(sender.bal, 195)
        self.assertEqual(transaction.receiver.bal, 505)

    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=("123412341234", "201", "5"))
    def test_add_transaction_insufficient_balance(self, mock_input, mock_print):
        # Arrange
        transaction = Transaction()
        # mock dbConnector
        mockdb = mock.Mock()
        sender = Customer()
        sender.cust_id, sender.userName, sender.address, sender.bal, sender.accountNumber = \
            (2, "sender", "send_add", 200, "789078907890")
        receiver = (1, "receiver", "receive_add", "123412341234", "1234567890", 500, "456745674567")
        mockdb.check_receiver.return_value = receiver
        input_args = ("Enter the recipient account number: ", "Enter transaction amount: ")

        # Act
        transaction.add_transaction(sender, Customer(), mockdb)

        # Assert
        calls = [mock.call(input_args[0], ), mock.call(input_args[1], ), mock.call(input_args[1], )]
        mockdb.check_receiver.assert_called_once()
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(mock_input.call_args_list, calls)
        mockdb.add_transaction_to_db.assert_called_once()
        mock_print.assert_called_once()

        self.assertEqual(transaction.sender, sender)
        self.assertEqual(transaction.amount, 5)
        self.assertEqual(sender.bal, 195)
        self.assertEqual(transaction.receiver.bal, 505)


if __name__ == '__main__':
    unittest.main()
