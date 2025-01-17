''' Implements a lambda function that works as an API Gateway endpoint.

The function will receive a JSON object (event) with the following format:
{
    'function': 'spam_or_ham',
    'messages': [
        'message 1',
        'message 2',
        'message 3',]
}

The function will return a JSON object with the following format:
{
    'status_code': 200,
    'function': 'spam_or_ham',
    'responses': {
        'message 1': 'ham',
        'message 2': 'spam',
        'message 3': 'ham'
    },
    'errors': []
}

NOTES:
1. The function takes in the original text messages as a list of strings.
2. The responses are stored in a dictionary, with the original text message as
   the key and the predicted classes as the value.
'''

# To run locally, install the required libraries
# !python -m pip install -r Resources/lambda_requirements.txt

# Import the required libraries
import nltk                 # For text processing
import pickle               # For loading the vectorizer
import keras                # For deep learning model (Still requires TensorFlow backend)
import json                 # For JSON encoding/decoding
import argparse             # For parsing input arguments

from numpy import argmax    # For finding the index of the maximum value

# Import the NLTK libraries

'''
The following libraries are needed for processing the text messages:

1. punkt: This package is used to split the text into individual words or sentences.
2. stopwords: Stop words are common words that are removed from text processing tasks to improve the
   accuracy and efficiency of the results. Examples: 'the', 'is', 'and', 'a', etc.
3. wordnet: This package is used for lemmatization, which is the process of converting a word to its
   base form. Example: The lemma of the word 'running' is 'run'.
'''

# NOTE: When deployed to AWS, these libraries should already be available in an AWS Lambda Layer.
# The following line sets the path to their location in the AWS Lambda Layer.
nltk.data.path.append('./opt/nltk_data')

nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# Import the custom tokenizer - Used for encoding the messages with the same vectorizer as the trained model
from Resources.CustomTokenizer import Custom_Tokenizer
tokenizer_Instance = Custom_Tokenizer()

MODEL_NAME = 'Resources/Sequential_0.99875_10_64_1_64_relu_softmax.keras'
VECTORIZER_NAME = 'Resources/Sequential_0.99875_10_64_1_64_relu_softmax.pkl'
STATUS_CODE = 'status_code'
RESPONSES = 'responses'
ERRORS = 'errors'
STATUS_CODE_SUCCESS = 200
STATUS_CODE_BAD_REQUEST = 400
SPAM_OR_HAM = 'spam_or_ham'
SUPPORTED_FUNCTIONS = [SPAM_OR_HAM]
MESSAGES = 'messages'
FUNCTION = 'function'
SPAM_OR_HAM_FIELDS = [FUNCTION, MESSAGES]


def lambda_handler(event, context=None):
    """ Main Lambda function

    Args:
        event (dict): A dictionary containing the input data and parameters
        context (object): An object containing information about the invocation,
            function, and execution environment

    Returns:
        dict: A JSON object containing the status code with function name and 
            response data for successful queries or error information if the
            request fails.  
    """

    try:
        # Validate that the event has the required fields and contains at least one message
        validation_errors = event_is_valid(event)
        if validation_errors is not None:
            return validation_errors
        
        # Load the model from the file
        model = keras.models.load_model(MODEL_NAME)

         # Get the messages from the event
        messages = event[MESSAGES]

        # Load the vectorizer from the pickle-encoded file
        with open(VECTORIZER_NAME, 'rb') as file:
            vectorizer = pickle.load(file)
            vectorizer.tokenizer = tokenizer_Instance.custom_tokenizer

        # Use the vectorizer to encode the messages
        # Convert the messages into TF-IDF vector using the same vectorizer as the trained model
        encoded_messages = vectorizer.transform(messages).toarray()
        
        # Check all messages to see if they are spam or ham
        return spam_or_ham(model, messages, encoded_messages)
    
    except Exception as e:
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: [str(e)]
        }    


def event_is_valid(event):
    """ Validate the event object

    Args:
        event (dict): A dictionary containing the input data and parameters

    Returns:
        dict: A JSON object containing the status code and error information if the
            request fails. Otherwise, None is returned.
    """
    # Validate that the event was provided, is a dictionary, and is not empty
    if event is None:
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: ['Event object is missing']
        }
    
    if not isinstance(event, dict):
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: ['Event object is not a dictionary']
        }
    
    if len(event) == 0:
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: ['Event object is empty']
        }
    
    # Validate the function field exists, is a string, and contains a valid function name
    if FUNCTION not in event:
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: ['Function field is required']
        }
    
    if not isinstance(event[FUNCTION], str):
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: ['Function field must be a string']
        }
    
    function_name = event[FUNCTION]
    if function_name not in SUPPORTED_FUNCTIONS:
        return {
            STATUS_CODE: STATUS_CODE_BAD_REQUEST,
            ERRORS: [f'Invalid function name: {function_name}']
        }

    # Validate the remaining event fields based on the selected function
    if function_name == SPAM_OR_HAM:
        # Validate that the event contains the required fields for the selected function,
        # that the fields are of the correct type, and that they are not empty.
        # This includes verifying that no additional fields are present
        status_code = STATUS_CODE_SUCCESS
        field_errors = []

        # Validate the Messages field
        if MESSAGES not in event:
            status_code = STATUS_CODE_BAD_REQUEST
            field_errors.append('Messages field is required')
        else:
            if not isinstance(event[MESSAGES], list):
                status_code = STATUS_CODE_BAD_REQUEST
                field_errors.append('Messages field must be a list')
            elif len(event[MESSAGES]) == 0:
                status_code = STATUS_CODE_BAD_REQUEST
                field_errors.append('Messages field must contain at least one message')
            else:
                messages = event[MESSAGES]
                for message in messages:
                    if not isinstance(message, str):
                        status_code = STATUS_CODE_BAD_REQUEST
                        field_errors.append('Messages field contains an invalid message; all messages must be strings')
                        break

        # Verify that no additional fields are present
        for key in event:
            if key not in SPAM_OR_HAM_FIELDS:
                status_code = STATUS_CODE_BAD_REQUEST
                field_errors.append(f'Invalid field in event: {key}')
        
        # If any field validations have failed, return the error response
        if status_code != STATUS_CODE_SUCCESS:
            return {
                STATUS_CODE: status_code,
                ERRORS: field_errors
            }
        
    return None


def spam_or_ham(model, messages, encoded_messages):
    """ Determine if the messages are spam or ham

    Args:
        model (keras.models.Sequential): A trained deep learning model
        messages (list): A list of messages to classify
        encoded_messages (numpy.ndarray): A 2D array of encoded messages

    Returns:
        dict: A JSON object containing the status code with function name and
            response data for successful queries or error information if the
            request fails.
    """

    # Make predictions using the model
    raw_predictions = model.predict(encoded_messages) # % probability for each class, per message
    predictions = argmax(raw_predictions, axis=1)

    # Combine the messages and the resulting predictions, converting the predictions
    # into the final predicted classes (0 = ham, 1 = spam).
    responses = {}
   
    for i in range(len(messages)):
        if predictions[i] == 0:
            responses[messages[i]] = 'ham'
        else:
            responses[messages[i]] = 'spam'

    # Return the responses as a JSON object
    return {
        STATUS_CODE: STATUS_CODE_SUCCESS,
        FUNCTION: SPAM_OR_HAM,
        RESPONSES: responses,
        ERRORS: []
    }


def main():
    """ Main function for running the AWS Lambda function locally """

    parser = argparse.ArgumentParser(description='Run the AWS Lambda function locally')
    parser.add_argument('--event', type=str, help='JSON string representing the event object')
    args = parser.parse_args()
    
    if args.event:
        # Parse the JSON string from command line argument
        try:
            event = json.loads(args.event)
        except Exception as e:
            return {
                STATUS_CODE: STATUS_CODE_BAD_REQUEST,
                ERRORS: [f'Unable to parse event object: {str(e)}']
            }
        
        return lambda_handler(event)
    else:
        return {
                STATUS_CODE: STATUS_CODE_BAD_REQUEST,
                ERRORS: [f'No JSON-encoded event object provided. Use the --event argument to provide an event object']
            }


if __name__ == '__main__':
    result = main()
    print(result)
