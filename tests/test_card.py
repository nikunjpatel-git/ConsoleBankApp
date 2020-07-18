import unittest
import mock
from Models.CardData import CardDetails


class CardDetailsTest(unittest.TestCase):

    @mock.patch('builtins.print')
    @mock.patch('Models.CardData.random_num_gen', side_effect=("1234123412341234", "123"))
    @mock.patch('builtins.input', return_value="1234")
    # @mock.patch.object(DbConnector, 'validate_number')
    def test_add_cards_ok(self, mock_input, mock_random_num_gen, mock_print):
        card = CardDetails()
        db = mock.Mock()
        db.validate_number.return_value = True

        # Act
        card.add_card("D", db)

        # Assert
        self.assertEqual(mock_random_num_gen.call_count, 2)
        mock_input.assert_called_once()
        db.validate_number.assert_called_once()
        self.assertEqual(card.CardType, "")
        self.assertEqual(card.CardNumber, "1234123412341234")
        self.assertEqual(card.Cvv, "123")
        self.assertEqual(card.Mpin, "1234")

    @mock.patch('builtins.print')
    @mock.patch('Models.CardData.random_num_gen')
    @mock.patch('builtins.input', return_value="1234")
    def test_add_card_duplicate_card(self, mock_input, mock_random_num_gen, mock_print):
        # Arrange
        card = CardDetails()
        db = mock.Mock()
        # Note: Set side_effect before calling
        db.validate_number.side_effect = (False, True)
        mock_random_num_gen.side_effect = ("1234123412341234", "4567456745674567", "123")

        # Act
        card.add_card("D", db)
        input_args = (16, 3)

        # Assert
        calls = [mock.call(input_args[0], ), mock.call(input_args[0], ), mock.call(input_args[1], )]
        self.assertEqual(mock_random_num_gen.call_count, 3)
        self.assertEqual(mock_random_num_gen.call_args_list, calls)
        self.assertEqual(db.validate_number.call_count, 2)
        mock_input.assert_called_once()
        self.assertEqual(card.CardType, "")
        self.assertEqual(card.CardNumber, "4567456745674567")
        self.assertEqual(card.Cvv, "123")
        self.assertEqual(card.Mpin, "1234")

    @mock.patch('builtins.print')
    @mock.patch('Models.CardData.random_num_gen')
    @mock.patch('builtins.input')
    def test_add_card_invalid_mpin_entered(self, mock_input, mock_random_num_gen, mock_print):
        # Arrange
        card = CardDetails()
        db = mock.Mock()
        # Note: Set side_effect before calling
        db.validate_number.return_value = True
        mock_random_num_gen.side_effect = ("4567456745674567", "123")
        mock_input.side_effect = ("12","abcde", "", "1234")

        # Act
        card.add_card("D", db)
        input_args = "Enter MPin for the D card: "

        # Assert
        calls = [mock.call(input_args, ), mock.call(input_args, ), mock.call(input_args, ), mock.call(input_args, )]
        self.assertEqual(mock_random_num_gen.call_count, 2)
        self.assertEqual(mock_input.call_count, 4)
        self.assertEqual(mock_input.call_args_list, calls)
        db.validate_number.assert_called_once()
        self.assertEqual(card.CardType, "")
        self.assertEqual(card.CardNumber, "4567456745674567")
        self.assertEqual(card.Cvv, "123")
        self.assertEqual(card.Mpin, "1234")


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CardDetailsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
