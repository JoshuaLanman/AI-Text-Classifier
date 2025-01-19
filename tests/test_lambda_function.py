# This module implements unit tests for the lambda_handler function in the lambda_function.py module.
''' Implements tests for the AWS lambda function. '''

# Import the required libraries
import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler, event_is_valid, spam_or_ham, main
from Resources.CustomTokenizer import Custom_Tokenizer

# Define the test constants
FUNCTION = 'function'
FUNCTION_NAME = 'spam_or_ham'
HAM = 'ham'
SPAM = 'spam'
MESSAGES = 'messages'
MESSAGE_1 = 'Hello, how are you?'
MESSAGE_2 = 'Congratulations, you have won a prize!'
MESSAGE_3 = 'You have been selected for a job interview.'
ENCODED_MESSAGE_1 = [1, 2, 3]
ENCODED_MESSAGE_2 = [4, 5, 6]
ENCODED_MESSAGE_3 = [7, 8, 9]
BAD_MESSAGE = 123
INVALID_FUNCTION_NAME = 'invalid_function'
INVALID_FIELD = 'invalid_field'
RESPONSES = 'responses'
ERRORS = 'errors'
STATUS_CODE = 'status_code'
STATUS_CODE_SUCCESS = 200
STATUS_CODE_BAD_REQUEST = 400
EMPTY_STRING = ''
EMPTY_DICT = {}
EMPTY_LIST = []


class Tests__Event_Is_Valid:

    def test__happy_path(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        result = event_is_valid(event)
        assert result is None, f"Expected response == None, but got {result}"

    def test__event_field_is_missing(self):
        # Define the test inputs
        event = None

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Event object is missing' in result[ERRORS], f"Expected: 'Event object is missing' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__event_is_not_a_dictionary(self):
        # Define the test inputs
        event = FUNCTION_NAME

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Event object is not a dictionary' in result[ERRORS], f"Expected: 'Event object is not a dictionary' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__event_is_empty(self):
        # Define the test inputs
        event = {}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Event object is empty' in result[ERRORS], f"Expected: 'Event object is empty' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_field_is_missing(self):
        # Define the test inputs
        event = {MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Function field is required' in result[ERRORS], f"Expected: 'Function field is required' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_field_is_not_a_string(self):
        # Define the test inputs
        event = {FUNCTION: BAD_MESSAGE, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Function field must be a string' in result[ERRORS], f"Expected: 'Function field must be a string' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_name_is_invalid(self):
        # Define the test inputs
        event = {FUNCTION: INVALID_FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert f'Invalid function name: {INVALID_FUNCTION_NAME}' in result[ERRORS], f"Expected: f'Invalid function name: {INVALID_FUNCTION_NAME}' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_is_spam_or_ham_and_messages_field_is_missing(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Messages field is required' in result[ERRORS], f"Expected: 'Messages field is required' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_is_spam_or_ham_and_messages_field_is_not_a_list(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: MESSAGE_1}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Messages field must be a list' in result[ERRORS], f"Expected: 'Messages field must be a list' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_is_spam_or_ham_and_messages_field_is_empty(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: []}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Messages field must contain at least one message' in result[ERRORS], f"Expected: 'Messages field must contain at least one message' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_is_spam_or_ham_and_messages_field_contains_invalid_message(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, BAD_MESSAGE, MESSAGE_3]}

        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert 'Messages field contains an invalid message; all messages must be strings' in result[ERRORS], f"Expected: 'Messages field contains an invalid message; all messages must be strings' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

    def test__function_is_spam_or_ham_and_event_contains_invalid_fields(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, INVALID_FIELD: 'test'}
        
        result = event_is_valid(event)
        assert result is not None, f"Expected response != None, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert f'Invalid field in event: {INVALID_FIELD}' in result[ERRORS], f"Expected: f'Invalid field in event: {INVALID_FIELD}' in response[{ERRORS}], but got response[{ERRORS}] = {result[ERRORS]}"

class Tests__Spam_Or_Ham:

    def mock_predict(self, encoded_messages):
        # Mock the model.predict method to return the following predictions
        predictions = []
        for message in encoded_messages:
            if message == ENCODED_MESSAGE_1:
                predictions.append([0.9, 0.1])
            elif message == ENCODED_MESSAGE_2:
                predictions.append([0.1, 0.9])
            elif message == ENCODED_MESSAGE_3:
                predictions.append([0.8, 0.2])
            else:
                # All other messages are classified as spam
                predictions.append([0.001, 0.999])
        return predictions

    def test__happy_path(self):
        # Define the test inputs
        messages = [MESSAGE_1, MESSAGE_2, MESSAGE_3]
        encoded_messages = [ENCODED_MESSAGE_1, ENCODED_MESSAGE_2, ENCODED_MESSAGE_3]

        # Mock the model
        mock_model = MagicMock()

        # Mock the model.predict method
        # Mock the predict method on the mock model
        mock_model.predict.return_value = self.mock_predict(encoded_messages)        

        result = spam_or_ham(mock_model, messages, encoded_messages)
        assert result is not None, f"Expected response != None, but got {result}"
        assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
        assert result[STATUS_CODE] == STATUS_CODE_SUCCESS, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_SUCCESS}, but got {result[STATUS_CODE]}"
        assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
        assert RESPONSES in result, f"Expected {RESPONSES} in response, but got {result}"
        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
        assert result[ERRORS] == [], f"Expected response[{ERRORS}] == [], but got {result[ERRORS]}"
        assert len(result[RESPONSES]) == 3, f"Expected len(response[{RESPONSES}]) == 3, but got {len(result[RESPONSES])}"
        assert MESSAGE_1 in result[RESPONSES], f"Expected '{MESSAGE_1}' in response[{RESPONSES}], but got {result[RESPONSES]}"
        assert MESSAGE_2 in result[RESPONSES], f"Expected '{MESSAGE_2}' in response[{RESPONSES}], but got {result[RESPONSES]}"
        assert MESSAGE_3 in result[RESPONSES], f"Expected '{MESSAGE_3}' in response[{RESPONSES}], but got {result[RESPONSES]}"
        assert result[RESPONSES][MESSAGE_1] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_1}'] == {HAM}, but got {result[RESPONSES][MESSAGE_1]}; Raw Predictions: {mock_model.predict.return_value}; Result: {result}"
        assert result[RESPONSES][MESSAGE_2] == SPAM, f"Expected response[{RESPONSES}]['{MESSAGE_2}'] == {SPAM}, but got {result[RESPONSES][MESSAGE_2]}; Raw Predictions: {mock_model.predict.return_value}; Result: {result}"
        assert result[RESPONSES][MESSAGE_3] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_3}'] == {HAM}, but got {result[RESPONSES][MESSAGE_3]}; Raw Predictions: {mock_model.predict.return_value}; Result: {result}"

class Tests__Lambda_Handler:
    
    def test__happy_path(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = None

            # Mock the keras.models.load_model function
            with patch('lambda_function.keras.models.load_model') as mock_load_model:
                mock_load_model.return_value = MagicMock()

                # Mock the file open function
                with patch('lambda_function.open') as mock_open:
                    mock_open.return_value.__enter__ = lambda *args: MagicMock()

                    # Mock the pickle.load function
                    with patch('lambda_function.pickle.load') as mock_pickle_load:
                        mock_vectorizer = MagicMock()
                        mock_pickle_load.return_value = mock_vectorizer

                        # Mock the custom_tokenizer method
                        with patch('Resources.CustomTokenizer.Custom_Tokenizer.custom_tokenizer') as mock_custom_tokenizer:
                            mock_custom_tokenizer.return_value = [ENCODED_MESSAGE_1, ENCODED_MESSAGE_2, ENCODED_MESSAGE_3]

                            # Mock the spam_or_ham function
                            with patch('lambda_function.spam_or_ham') as mock_spam_or_ham:
                                mock_spam_or_ham.return_value = {
                                    STATUS_CODE: STATUS_CODE_SUCCESS,
                                    FUNCTION: FUNCTION_NAME,
                                    RESPONSES: {
                                        MESSAGE_1: HAM,
                                        MESSAGE_2: SPAM,
                                        MESSAGE_3: HAM
                                    },
                                    ERRORS: []
                                }

                                result = lambda_handler(event)
                                assert result is not None, f"Expected response != None, but got {result}"
                                assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                                assert result[STATUS_CODE] == STATUS_CODE_SUCCESS, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_SUCCESS}, but got {result[STATUS_CODE]}"
                                assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                                assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                                assert RESPONSES in result, f"Expected {RESPONSES} in response, but got {result}"
                                assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                                assert result[ERRORS] == [], f"Expected response[{ERRORS}] == [], but got {result[ERRORS]}"
                                assert len(result[RESPONSES]) == 3, f"Expected len(response[{RESPONSES}]) == 3, but got {len(result[RESPONSES])}"
                                assert MESSAGE_1 in result[RESPONSES], f"Expected '{MESSAGE_1}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                                assert MESSAGE_2 in result[RESPONSES], f"Expected '{MESSAGE_2}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                                assert MESSAGE_3 in result[RESPONSES], f"Expected '{MESSAGE_3}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                                assert result[RESPONSES][MESSAGE_1] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_1}'] == {HAM}, but got {result[RESPONSES][MESSAGE_1]}; Result: {result}"
                                assert result[RESPONSES][MESSAGE_2] == SPAM, f"Expected response[{RESPONSES}]['{MESSAGE_2}'] == {SPAM}, but got {result[RESPONSES][MESSAGE_2]}; Result: {result}"
                                assert result[RESPONSES][MESSAGE_3] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_3}'] == {HAM}, but got {result[RESPONSES][MESSAGE_3]}; Result: {result}"

    def test__event_is_invalid(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = {
                STATUS_CODE: STATUS_CODE_BAD_REQUEST,
                FUNCTION: EMPTY_STRING,
                RESPONSES: EMPTY_DICT,
                ERRORS: ['Test Error']
            }

            result = lambda_handler(event)
            assert result is not None, f"Expected response != None, but got {result}"
            assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
            assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
            assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
            assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
            assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
            assert result[ERRORS] == ['Test Error'], f"Expected response[{ERRORS}] == ['Test Error'], but got {result[ERRORS]}"

    def test__model_load_fails(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = None

            # Mock the keras.models.load_model function
            with patch('lambda_function.keras.models.load_model') as mock_load_model:
                mock_load_model.side_effect = Exception('Test Exception: Model Load Failed')

                result = lambda_handler(event)
                assert result is not None, f"Expected response != None, but got {result}"
                assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
                assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                assert 'Test Exception: Model Load Failed' in result[ERRORS], f"Expected 'Test Exception: Model Load Failed' in response[{ERRORS}], but got {result[ERRORS]}"

    def test__vectorizer_file_load_fails(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = None

            # Mock the keras.models.load_model function
            with patch('lambda_function.keras.models.load_model') as mock_load_model:
                mock_load_model.return_value = MagicMock()

                # Mock the file open function
                with patch('lambda_function.open') as mock_open:
                    mock_open.side_effect = Exception('Test Exception: Vectorizer File Load Failed')

                    result = lambda_handler(event)
                    assert result is not None, f"Expected response != None, but got {result}"
                    assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                    assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
                    assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                    assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                    assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                    assert 'Test Exception: Vectorizer File Load Failed' in result[ERRORS], f"Expected 'Test Exception: Vectorizer File Load Failed' in response[{ERRORS}], but got {result[ERRORS]}"
    
    def test__vectorizer_pickle_load_fails(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = None

            # Mock the keras.models.load_model function
            with patch('lambda_function.keras.models.load_model') as mock_load_model:
                mock_load_model.return_value = MagicMock()

                # Mock the file open function
                with patch('lambda_function.open') as mock_open:
                    mock_open.return_value.__enter__ = lambda *args: MagicMock()

                    # Mock the pickle.load function
                    with patch('lambda_function.pickle.load') as mock_pickle_load:
                        mock_pickle_load.side_effect = Exception('Test Exception: Vectorizer Pickle Load Failed')

                        result = lambda_handler(event)
                        assert result is not None, f"Expected response != None, but got {result}"
                        assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
                        assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                        assert 'Test Exception: Vectorizer Pickle Load Failed' in result[ERRORS], f"Expected 'Test Exception: Vectorizer Pickle Load Failed' in response[{ERRORS}], but got {result[ERRORS]}"
    
    def test__vectorizer_fails(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the event_is_valid function
        with patch('lambda_function.event_is_valid') as mock_event_is_valid:
            mock_event_is_valid.return_value = None

            # Mock the keras.models.load_model function
            with patch('lambda_function.keras.models.load_model') as mock_load_model:
                mock_load_model.return_value = MagicMock()

                # Mock the file open function
                with patch('lambda_function.open') as mock_open:
                    mock_open.return_value.__enter__ = lambda *args: MagicMock()

                    # Mock the pickle.load function
                    with patch('lambda_function.pickle.load') as mock_pickle_load:
                        mock_vectorizer = MagicMock()
                        mock_pickle_load.return_value = mock_vectorizer

                        # Mock the mock_vectorizer.transform method
                        mock_vectorizer.transform.side_effect = Exception('Test Exception: Vectorizer Failed')
                        
                        result = lambda_handler(event)
                        assert result is not None, f"Expected response != None, but got {result}"
                        assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
                        assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                        assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                        assert 'Test Exception: Vectorizer Failed' in result[ERRORS], f"Expected 'Test Exception: Vectorizer Failed' in response[{ERRORS}], but got {result[ERRORS]}"

class Tests__Main:

    def test__happy_path(self):
        # Define the test inputs
        event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

        # Mock the argument parser
        with patch('lambda_function.argparse.ArgumentParser') as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = MagicMock()

            # Mock the json.loads function
            with patch('lambda_function.json.loads') as mock_json_loads:
                mock_json_loads.return_value = event

                # Mock the lambda_handler function
                with patch('lambda_function.lambda_handler') as mock_lambda_handler:
                    mock_lambda_handler.return_value = {
                        STATUS_CODE: STATUS_CODE_SUCCESS,
                        FUNCTION: FUNCTION_NAME,
                        RESPONSES: {
                            MESSAGE_1: HAM,
                            MESSAGE_2: SPAM,
                            MESSAGE_3: HAM
                        },
                        ERRORS: []
                    }

                    result = main()
                    assert result is not None, f"Expected response != None, but got {result}"
                    assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                    assert result[STATUS_CODE] == STATUS_CODE_SUCCESS, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_SUCCESS}, but got {result[STATUS_CODE]}"
                    assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                    assert result[FUNCTION] == FUNCTION_NAME, f"Expected response[{FUNCTION}] == {FUNCTION_NAME}, but got {result[FUNCTION]}"
                    assert RESPONSES in result, f"Expected {RESPONSES} in response, but got {result}"
                    assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                    assert result[ERRORS] == [], f"Expected response[{ERRORS}] == [], but got {result[ERRORS]}"
                    assert len(result[RESPONSES]) == 3, f"Expected len(response[{RESPONSES}]) == 3, but got {len(result[RESPONSES])}"
                    assert MESSAGE_1 in result[RESPONSES], f"Expected '{MESSAGE_1}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                    assert MESSAGE_2 in result[RESPONSES], f"Expected '{MESSAGE_2}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                    assert MESSAGE_3 in result[RESPONSES], f"Expected '{MESSAGE_3}' in response[{RESPONSES}], but got {result[RESPONSES]}"
                    assert result[RESPONSES][MESSAGE_1] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_1}'] == {HAM}, but got {result[RESPONSES][MESSAGE_1]}; Result: {result}"
                    assert result[RESPONSES][MESSAGE_2] == SPAM, f"Expected response[{RESPONSES}]['{MESSAGE_2}'] == {SPAM}, but got {result[RESPONSES][MESSAGE_2]}; Result: {result}"
                    assert result[RESPONSES][MESSAGE_3] == HAM, f"Expected response[{RESPONSES}]['{MESSAGE_3}'] == {HAM}, but got {result[RESPONSES][MESSAGE_3]}; Result: {result}"

    def test__event_is_invalid(self):
            # Define the test inputs
            event = {FUNCTION: FUNCTION_NAME, MESSAGES: [MESSAGE_1, MESSAGE_2, MESSAGE_3]}

            # Mock the argument parser
            with patch('lambda_function.argparse.ArgumentParser') as mock_argparse:
                mock_argparse.return_value.parse_args.return_value = MagicMock()

                # Mock the json object
                with patch('lambda_function.json') as mock_json:
                    mock_json.loads.side_effect = Exception('Test Exception: Invalid Event')

                    # Mock the lambda_handler function
                    with patch('lambda_function.lambda_handler') as mock_lambda_handler:
                        mock_lambda_handler.return_value = {
                            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
                            FUNCTION: EMPTY_STRING,
                            RESPONSES: EMPTY_DICT,
                            ERRORS: ['Test Error']
                        }

                        result = main()
                        assert result is not None, f"Expected response != None, but got {result}"
                        assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
                        assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
                        assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
                        assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
                        assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
                        assert result[ERRORS] == ['Unable to parse event object: Test Exception: Invalid Event'], f"Expected response[{ERRORS}] == ['Unable to parse event object: Test Exception: Invalid Event'], but got {result[ERRORS]}"
    
    def test__missing_json_encoded_event(self):
       # Mock the argument parser to return a namespace with no event attribute
        with patch('lambda_function.argparse.ArgumentParser') as mock_argparse:
            mock_args = MagicMock()
            mock_argparse.return_value.parse_args.return_value = mock_args
            mock_args.event = None
            
            result = main()
            assert result is not None, f"Expected response != None, but got {result}"
            assert STATUS_CODE in result, f"Expected {STATUS_CODE} in response, but got {result}"
            assert result[STATUS_CODE] == STATUS_CODE_BAD_REQUEST, f"Expected response[{STATUS_CODE}] == {STATUS_CODE_BAD_REQUEST}, but got {result[STATUS_CODE]}"
            assert FUNCTION in result, f"Expected {FUNCTION} in response, but got {result}"
            assert result[FUNCTION] == EMPTY_STRING, f"Expected response[{FUNCTION}] == {EMPTY_STRING}, but got {result[FUNCTION]}"
            assert RESPONSES in result, f"Expected {RESPONSES} in response, but got {result}"
            assert result[RESPONSES] == EMPTY_DICT, f"Expected response[{RESPONSES}] == {EMPTY_DICT}, but got {result[RESPONSES]}"
            assert ERRORS in result, f"Expected {ERRORS} in response, but got {result}"
            assert result[ERRORS] == ['No JSON-encoded event object provided. Use the --event argument to provide an event object'], f"Expected response[{ERRORS}] == ['No JSON-encoded event object provided. Use the --event argument to provide an event object'], but got {result[ERRORS]}"
                    

# To run the tests, simply execute `pytest` in the terminal
if __name__ == "__main__":
    pytest.main()
