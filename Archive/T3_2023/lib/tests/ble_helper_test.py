import unittest
import re
import os
import sys

root_folder = os.path.abspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root_folder)

from ble_helper import convert_incline_to_op_value, covert_hex_values_to_readable_string

class ConvertInclineTesting(unittest.TestCase):
    def test_invalid_incline(self):
        # 25% incline
        self.assertRaises(Exception, convert_incline_to_op_value, 25)
        # -20% incline
        self.assertRaises(Exception, convert_incline_to_op_value, 25)

    def test_convert_positive_incline_to_correct_op_value(self):
        # 0% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(0)), '0000')
        # 0.5% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(0.5)), '3200')        
        # 1% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(1)), '6400')                
        # 10% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(10)), 'e803')        
        # 19% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(19)), '6c07')

    def test_convert_negative_incline_to_correct_op_value(self):
        # 0% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(0)), '0000')
        # -0.5% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(-0.5)), 'cfff')
        # # -1% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(-1)), '9dff')        
        # # -5% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(-5)), '00fe')
        # -10% incline
        self.assertEqual(covert_hex_values_to_readable_string(convert_incline_to_op_value(-10)), '00fc')

if __name__ == '__main__':
    unittest.main()