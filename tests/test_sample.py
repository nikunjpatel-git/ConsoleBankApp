import unittest
import mock
from Models.ToTest import SimpleClass


class MyTestCase(unittest.TestCase):
    @mock.patch('builtins.input')
    def test_input(self, mock_input):
        simple = SimpleClass()
        #mock_input.return_value = "myinput"
        mock_input.side_effect = ("myinput","mysecondinput")
        simple.example()

        self.assertEqual(simple.xyz, "myinput")
        self.assertEqual(simple.abc, "mysecondinput")


if __name__ == '__main__':
    unittest.main()