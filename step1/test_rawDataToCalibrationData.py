import unittest
from unittest.mock import patch, MagicMock, mock_open
import os

from rawDataToCalibrationData import rawDataToCalibrationData

class MockTextOutput:
    def __init__(self):
        self.text = ""
    def config(self, text):
        self.text = text

class TestRawDataToCalibrationData(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="[12 3 4]")
    @patch("countLines.countLines", return_value=1)
    def test_rawDataProcess(self, mock_count, mock_file):
        text_output = MockTextOutput()
        input_file = "dummy_input.clog"
        output_file = "dummy_output"
        
        # Call the function
        rawDataToCalibrationData(input_file, output_file, text_output)

        # Check that a file was opened for reading
        mock_file.assert_any_call(input_file, 'r', encoding='utf-8')
        # Check that a file was opened for writing
        mock_file.assert_any_call(output_file + ".totKanaly", 'w', encoding='utf-8')
        # Verify progress text was updated
        self.assertIn("start", text_output.text)

        # Ensure some writing to output took place
        handle = mock_file()
        handle.write.assert_called()

if __name__ == '__main__':
    # Run with: python -m unittest test_rawDataToCalibrationData.py
    unittest.main()