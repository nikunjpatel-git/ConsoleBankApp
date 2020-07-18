import datetime
import unittest
import mock
from Models.CustomerData import Customer
from Models.CardData import CardDetails
from Models.BeneficiaryData import Beneficiary
from Models.TransactionData import Transaction


class CustomerTest(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch.object(CardDetails, 'add_card')
    @mock.patch('Models.CustomerData.random_num_gen')
    @mock.patch('Models.CustomerData.decorate_heading')
    @mock.patch('builtins.input', side_effect=("myUsername", "myAddress", "123412341234", "1234567890", ))
    def test_register_ok(self, mock_input, mock_decorate_heading, mock_random_num_gen, mock_add_card, mock_print):
        # Arrange
        mock_db = mock.Mock()
        mock_db.validate_number.return_value = True
        mock_random_num_gen.return_value = "456745674567"

        # Act
        customer = Customer()
        customer.register(mock_db)

        # Assert
        mock_decorate_heading.assert_called_once_with("Registration Module")
        self.assertEqual(mock_db.validate_number.call_count, 2)
        mock_random_num_gen.assert_called_once_with(12)
        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_add_card.call_count, 2)
        self.assertEqual(customer.userName, "myUsername")
        self.assertEqual(customer.address, "myAddress")
        self.assertEqual(customer.aadharNumber, "123412341234")
        self.assertEqual(customer.mobileNumber, "1234567890")
        self.assertEqual(customer.accountNumber, "456745674567")
        self.assertEqual(customer.cards[0].CardType, "C")
        self.assertEqual(customer.cards[1].CardType, "D")
        self.assertEqual(len(customer.cards), 2)\


    @mock.patch('builtins.print')
    @mock.patch.object(CardDetails, 'add_card')
    @mock.patch('Models.CustomerData.random_num_gen')
    @mock.patch('Models.CustomerData.decorate_heading')
    @mock.patch('builtins.input', side_effect=("invalidUsername", "myUsername", "myAddress", "123412341234", "1234567890", ))
    def test_register_duplicate_username(self, mock_input, mock_decorate_heading, mock_random_num_gen, mock_add_card, mock_print):
        # Arrange
        mock_db = mock.Mock()
        mock_db.validate_number.side_effect = (False, True, True)
        mock_random_num_gen.return_value = "456745674567"

        # Act
        customer = Customer()
        customer.register(mock_db)

        # Assert
        mock_decorate_heading.assert_called_once_with("Registration Module")
        self.assertEqual(mock_db.validate_number.call_count, 3)
        mock_random_num_gen.assert_called_once_with(12)
        mock_print.assert_any_call("Username: invalidUsername is already taken. Try another one.")
        self.assertEqual(mock_input.call_count, 5)
        self.assertEqual(mock_add_card.call_count, 2)
        self.assertEqual(customer.userName, "myUsername")
        self.assertEqual(customer.address, "myAddress")
        self.assertEqual(customer.aadharNumber, "123412341234")
        self.assertEqual(customer.mobileNumber, "1234567890")
        self.assertEqual(customer.accountNumber, "456745674567")
        self.assertEqual(customer.cards[0].CardType, "C")
        self.assertEqual(customer.cards[1].CardType, "D")
        self.assertEqual(len(customer.cards), 2)

    @mock.patch('builtins.print')
    def test_print_details_ok(self, mock_print):
        # Arrange
        customer = Customer()
        customer.userName, customer.address, customer.aadharNumber, customer.mobileNumber, customer.accountNumber = \
            ("myUsername", "myAddress", "123412341234", "1234567890", "456745674567")
        card1 = CardDetails()
        card1.CardNumber, card1.CardType, card1.Mpin, card1.Cvv = ("7890789078907890", "C", "1234", "123")
        card2 = CardDetails()
        card2.CardNumber, card1.CardType, card1.Mpin, card1.Cvv = ("2345234523452345", "C", "4567", "456")
        customer.cards = [card1, card2]
        beneficiary = Beneficiary()
        beneficiary.name, beneficiary.ifsc_code, beneficiary.account_number = ("ben", "BKID0123456", "567834563456")
        customer.beneficiaries.append(beneficiary)
        transaction = Transaction()
        transaction.amount = 5
        transaction.date = datetime.datetime(2019, 12, 11, 7, 30, 00)
        transaction.receiver = Customer()
        transaction.receiver.accountNumber = "736473647364"
        customer.transactions.append(transaction)

        # Act
        customer.print_details()

        # Assert
        self.assertEqual(mock_print.call_count, 25)
        mock_print.assert_any_call("UserName: " + customer.userName)
        mock_print.assert_any_call("Account Number: "+customer.accountNumber)
        mock_print.assert_any_call("Address: " + customer.address)
        mock_print.assert_any_call("Aadhar Number: " + customer.aadharNumber)
        mock_print.assert_any_call("Mobile Number: " + customer.mobileNumber)
        mock_print.assert_any_call("Account Balance: " + str(customer.bal))
        mock_print.assert_any_call("Card Type: " + card1.CardType)
        mock_print.assert_any_call("Card Number: " + card1.CardNumber)
        mock_print.assert_any_call("Card CVV Number: " + card1.Cvv)
        mock_print.assert_any_call("Card Type: " + card2.CardType)
        mock_print.assert_any_call("Card Number: " + card2.CardNumber)
        mock_print.assert_any_call("Card CVV Number: " + card2.Cvv)
        mock_print.assert_any_call("Name: "+beneficiary.name)
        mock_print.assert_any_call("IFSC Code: " + beneficiary.ifsc_code)
        mock_print.assert_any_call("Account Number: " + beneficiary.account_number)
        mock_print.assert_any_call("Recipient: "+transaction.receiver.accountNumber)
        mock_print.assert_any_call("Amount: " + str(transaction.amount))
        mock_print.assert_any_call("Date: " + transaction.date.strftime("%d-%m-%Y %H:%M:%S"))

    @mock.patch('builtins.print')
    def test_print_details_no_beneficiary_no_transactions(self, mock_print):
        # Arrange
        customer = Customer()
        customer.userName, customer.address, customer.aadharNumber, customer.mobileNumber, customer.accountNumber = \
            ("myUsername", "myAddress", "123412341234", "1234567890", "456745674567")
        card1 = CardDetails()
        card1.CardNumber, card1.CardType, card1.Mpin, card1.Cvv = ("7890789078907890", "C", "1234", "123")
        card2 = CardDetails()
        card2.CardNumber, card1.CardType, card1.Mpin, card1.Cvv = ("2345234523452345", "C", "4567", "456")
        customer.cards = [card1, card2]

        # Act
        customer.print_details()

        # Assert
        self.assertEqual(mock_print.call_count, 17)
        mock_print.assert_any_call("UserName: " + customer.userName)
        mock_print.assert_any_call("Account Number: " + customer.accountNumber)
        mock_print.assert_any_call("Address: " + customer.address)
        mock_print.assert_any_call("Aadhar Number: " + customer.aadharNumber)
        mock_print.assert_any_call("Mobile Number: " + customer.mobileNumber)
        mock_print.assert_any_call("Account Balance: " + str(customer.bal))
        mock_print.assert_any_call("Card Type: " + card1.CardType)
        mock_print.assert_any_call("Card Number: " + card1.CardNumber)
        mock_print.assert_any_call("Card CVV Number: " + card1.Cvv)
        mock_print.assert_any_call("Card Type: " + card2.CardType)
        mock_print.assert_any_call("Card Number: " + card2.CardNumber)
        mock_print.assert_any_call("Card CVV Number: " + card2.Cvv)
        mock_print.assert_any_call("\nThere are no beneficiaries added yet.")
        mock_print.assert_any_call("There are no transactions yet.")

    @mock.patch('Models.CustomerData.os')
    @mock.patch('Models.CustomerData.decorate_heading')
    @mock.patch('builtins.input', return_value="myUsername")
    def test_login_ok(self, mock_input, mock_decorate_heading, mock_os):
        # Arrange
        mock_db = mock.Mock()
        user = [(1, "user", "user_add", "123412341234", "1234567890", 500, "456745674567")]
        card1 = (1, "4563456345634563", "456", "4567", "C", 1)
        card2 = (2, "4563456345644564", "567", "5678", "D", 1)
        cards = [card1, card2]
        beneficiary = [(1, "ben", "BKID0123456", "765476547654", 1)]
        mock_db.get_all.side_effect = (user, cards, beneficiary)
        transaction = (5, datetime.datetime(2019, 12, 11), "765489768746", 3)
        mock_db.get_transaction_details.return_value = [transaction]

        # Act
        customer = Customer()
        customer.login(mock_db)

        # Assert
        self.assertEqual(mock_db.get_all.call_count, 3)
        mock_db.get_transaction_details.assert_called_once()
        mock_decorate_heading.assert_called_once()
        mock_input.assert_called_once()
        self.assertEqual(customer.cust_id, user[0][0])
        self.assertEqual(customer.userName, user[0][1])
        self.assertEqual(customer.address, user[0][2])
        self.assertEqual(customer.aadharNumber, user[0][3])
        self.assertEqual(customer.mobileNumber, user[0][4])
        self.assertEqual(customer.bal, user[0][5])
        self.assertEqual(customer.accountNumber, user[0][6])
        self.assertEqual(len(customer.cards), 2)
        self.assertEqual(customer.cards[0].CardNumber, card1[1])
        self.assertEqual(customer.cards[0].Cvv, card1[2])
        self.assertEqual(customer.cards[0].Mpin, card1[3])
        self.assertEqual(customer.cards[0].CardType, card1[4])
        self.assertEqual(customer.cards[1].CardNumber, card2[1])
        self.assertEqual(customer.cards[1].Cvv, card2[2])
        self.assertEqual(customer.cards[1].Mpin, card2[3])
        self.assertEqual(customer.cards[1].CardType, card2[4])
        self.assertEqual(len(customer.beneficiaries), 1)
        self.assertEqual(customer.beneficiaries[0].name, beneficiary[0][1])
        self.assertEqual(customer.beneficiaries[0].ifsc_code, beneficiary[0][2])
        self.assertEqual(customer.beneficiaries[0].account_number, beneficiary[0][3])
        self.assertEqual(len(customer.transactions), 1)
        self.assertEqual(customer.transactions[0].receiver.accountNumber, transaction[2])
        self.assertEqual(customer.transactions[0].amount, transaction[0])
        self.assertEqual(customer.transactions[0].date, transaction[1])

    @mock.patch('Models.CustomerData.os')
    @mock.patch('Models.CustomerData.decorate_heading')
    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=("invalidUsername", "myUsername"))
    def test_login_invalid_username(self, mock_input, mock_print, mock_decorate_heading, mock_os):
        # Arrange
        mock_db = mock.Mock()
        user = [(1, "user", "user_add", "123412341234", "1234567890", 500, "456745674567")]
        card1 = (1, "4563456345634563", "456", "4567", "C", 1)
        card2 = (2, "4563456345644564", "567", "5678", "D", 1)
        cards = [card1, card2]
        beneficiary = [(1, "ben", "BKID0123456", "765476547654", 1)]
        mock_db.get_all.side_effect = (None, user, cards, beneficiary)
        transaction = (5, datetime.datetime(2019, 12, 11), "765489768746", 3)
        mock_db.get_transaction_details.return_value = [transaction]

        # Act
        customer = Customer()
        customer.login(mock_db)

        # Assert
        self.assertEqual(mock_db.get_all.call_count, 4)
        self.assertEqual(mock_input.call_count, 2)
        mock_db.get_transaction_details.assert_called_once()
        mock_decorate_heading.assert_called_once()
        self.assertEqual(customer.cust_id, user[0][0])
        self.assertEqual(customer.userName, user[0][1])
        self.assertEqual(customer.address, user[0][2])
        self.assertEqual(customer.aadharNumber, user[0][3])
        self.assertEqual(customer.mobileNumber, user[0][4])
        self.assertEqual(customer.bal, user[0][5])
        self.assertEqual(customer.accountNumber, user[0][6])
        self.assertEqual(len(customer.cards), 2)
        self.assertEqual(customer.cards[0].CardNumber, card1[1])
        self.assertEqual(customer.cards[0].Cvv, card1[2])
        self.assertEqual(customer.cards[0].Mpin, card1[3])
        self.assertEqual(customer.cards[0].CardType, card1[4])
        self.assertEqual(customer.cards[1].CardNumber, card2[1])
        self.assertEqual(customer.cards[1].Cvv, card2[2])
        self.assertEqual(customer.cards[1].Mpin, card2[3])
        self.assertEqual(customer.cards[1].CardType, card2[4])
        self.assertEqual(len(customer.beneficiaries), 1)
        self.assertEqual(customer.beneficiaries[0].name, beneficiary[0][1])
        self.assertEqual(customer.beneficiaries[0].ifsc_code, beneficiary[0][2])
        self.assertEqual(customer.beneficiaries[0].account_number, beneficiary[0][3])
        self.assertEqual(len(customer.transactions), 1)
        self.assertEqual(customer.transactions[0].receiver.accountNumber, transaction[2])
        self.assertEqual(customer.transactions[0].amount, transaction[0])
        self.assertEqual(customer.transactions[0].date, transaction[1])

    @mock.patch('Models.CustomerData.os')
    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=("1", "1234", "0123"))
    def test_update_mpin_ok(self, mock_input, mock_print, mock_os):
        # Arrange
        mock_db = mock.Mock()
        customer = Customer()
        card1 = CardDetails()
        card1.CardNumber, card1.CardType, card1.Cvv, card1.Mpin = ("1234123412341234", "C", "123", "1234")
        card2 = CardDetails()
        card2.CardNumber, card2.CardType, card2.Cvv, card2.Mpin = ("4567456745674567", "D", "456", "4567")
        customer.cards.append(card1)
        customer.cards.append(card2)

        # Act
        customer.change_mpin(mock_db)

        # Assert
        self.assertEqual(mock_input.call_count, 3)
        mock_db.update_mpin.assert_called_once()
        self.assertEqual(customer.cards[0].Mpin, "0123")

    @mock.patch('builtins.print')
    @mock.patch('builtins.input', side_effect=("3", "my updated address", "2345142342"))
    def test_update_info_ok(self, mock_input, mock_print):
        # Arrange
        mock_db = mock.Mock()

        # Act
        customer = Customer()
        customer.update_info(mock_db)

        # Assert
        self.assertEqual(mock_input.call_count, 3)
        self.assertEqual(customer.address, "my updated address")
        self.assertEqual(customer.mobileNumber, "2345142342")

    @mock.patch.object(CardDetails, 'add_card')
    @mock.patch('Models.CustomerData.os')
    @mock.patch('builtins.print')
    @mock.patch('builtins.input', return_value="C")
    def test_add_cards_Credit_ok(self, mock_input, mock_print, mock_os, mock_add_card):
        # Arrange
        mock_db = mock.Mock()

        # Act
        customer = Customer()
        customer.add_cards(mock_db)

        # Assert
        mock_input.assert_called_once()
        mock_db.add_card_to_db.assert_called_once()
        mock_add_card.assert_called_once()
        self.assertEqual(len(customer.cards), 1)
        self.assertEqual(customer.cards[0].CardType, "C")

    @mock.patch.object(CardDetails, 'add_card')
    @mock.patch('Models.CustomerData.os')
    @mock.patch('builtins.print')
    @mock.patch('builtins.input', return_value="D")
    def test_add_cards_Debit_ok(self, mock_input, mock_print, mock_os, mock_add_card):
        # Arrange
        mock_db = mock.Mock()

        # Act
        customer = Customer()
        customer.add_cards(mock_db)

        # Assert
        mock_input.assert_called_once()
        mock_db.add_card_to_db.assert_called_once()
        mock_add_card.assert_called_once()
        self.assertEqual(len(customer.cards), 1)
        self.assertEqual(customer.cards[0].CardType, "D")


if __name__ == '__main__':
    unittest.main()
