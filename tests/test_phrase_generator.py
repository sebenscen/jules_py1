import unittest
from unittest.mock import patch, MagicMock
import json
# Assuming google.api_core.exceptions is a common place for Google API errors.
# If not available or a different exception is more appropriate, this can be adjusted.
try:
    from google.api_core import exceptions as google_exceptions
except ImportError:
    # Define a placeholder if google-api-core is not installed or this path is wrong
    # This allows tests to be defined, though they might not fully simulate the exact exception
    # if the real one is different. The actual exception raised by genai might also be specific
    # to that library. For now, we'll use a generic Exception if this specific one isn't found.
    class GoogleAPICoreException(Exception):
        pass
    google_exceptions = MagicMock()
    google_exceptions.GoogleAPIError = GoogleAPICoreException


from src.phrase_generator import get_inspirational_phrase

class TestPhraseGenerator(unittest.TestCase):

    @patch('src.phrase_generator.genai.GenerativeModel')
    def test_get_inspirational_phrase_success(self, MockGenerativeModel):
        # Configure the mock model and its response
        mock_model_instance = MockGenerativeModel.return_value
        
        # The response object from genai.GenerativeModel().generate_content()
        # usually has a 'text' attribute or a 'parts' attribute.
        # We'll mock the 'text' attribute directly as per the prompt's example.
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "phrase": "Test Phrase",
            "author": "Test Author",
            "location": "Test Location"
        })
        # Ensure `parts` attribute exists and is not empty, as the code checks `response.parts`
        mock_response.parts = [MagicMock()] # Simulate having at least one part

        mock_model_instance.generate_content.return_value = mock_response

        # Call the function
        result = get_inspirational_phrase()

        # Assertions
        expected_result = {
            "phrase": "Test Phrase",
            "author": "Test Author",
            "location": "Test Location"
        }
        self.assertEqual(result, expected_result)
        MockGenerativeModel.assert_called_once_with('gemini-pro')
        mock_model_instance.generate_content.assert_called_once()

    @patch('src.phrase_generator.genai.GenerativeModel')
    def test_get_inspirational_phrase_malformed_json(self, MockGenerativeModel):
        # Configure the mock model to return malformed JSON
        mock_model_instance = MockGenerativeModel.return_value
        
        mock_response = MagicMock()
        mock_response.text = '{"phrase": "Test Phrase", "author": "Test Author", "location": "Test Location"' # Missing closing brace
        mock_response.parts = [MagicMock()]

        mock_model_instance.generate_content.return_value = mock_response

        # Call the function
        result = get_inspirational_phrase()

        # Assertions
        self.assertIsNone(result, "Should return None for malformed JSON")
        MockGenerativeModel.assert_called_once_with('gemini-pro')
        mock_model_instance.generate_content.assert_called_once()

    @patch('src.phrase_generator.genai.GenerativeModel')
    def test_get_inspirational_phrase_api_exception(self, MockGenerativeModel):
        # Configure the mock model to raise an exception
        mock_model_instance = MockGenerativeModel.return_value
        
        # Using a generic Exception as google_exceptions.GoogleAPIError might not be
        # the exact one, or genai might wrap it. The function catches generic Exception.
        mock_model_instance.generate_content.side_effect = Exception("API communication error")

        # Call the function
        result = get_inspirational_phrase()

        # Assertions
        self.assertIsNone(result, "Should return None when API call fails")
        MockGenerativeModel.assert_called_once_with('gemini-pro')
        mock_model_instance.generate_content.assert_called_once()

    @patch('src.phrase_generator.genai.GenerativeModel')
    def test_get_inspirational_phrase_missing_keys_in_response(self, MockGenerativeModel):
        # Configure the mock model to return JSON with missing keys
        mock_model_instance = MockGenerativeModel.return_value
        
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "phrase": "Test Phrase Only"
            # Missing "author" and "location"
        })
        mock_response.parts = [MagicMock()]
        mock_model_instance.generate_content.return_value = mock_response

        result = get_inspirational_phrase()
        self.assertIsNone(result, "Should return None if response JSON is missing required keys")

    @patch('src.phrase_generator.genai.GenerativeModel')
    def test_get_inspirational_phrase_empty_response_parts(self, MockGenerativeModel):
        # Configure the mock model to return a response with empty .parts
        mock_model_instance = MockGenerativeModel.return_value
        
        mock_response = MagicMock()
        mock_response.text = "" # Text might be empty or not, but parts is the primary check in code for emptiness
        mock_response.parts = [] # Empty parts, simulating a blocked prompt or no content
        mock_model_instance.generate_content.return_value = mock_response

        result = get_inspirational_phrase()
        self.assertIsNone(result, "Should return None if API response.parts is empty")


if __name__ == '__main__':
    unittest.main()
