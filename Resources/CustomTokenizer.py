import nltk                 # For text processing

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

class CustomTokenizer:

# Custom tokenizer function to remove stopwords and use lemmatization
    def customTokenizer(str):
        # Split string into tokens
        tokens=nltk.word_tokenize(str)
        
        # Filter for stopwords
        nostop = list(filter(lambda token: token not in stopwords.words('english'), tokens))
        
        # Perform lemmatization
        lemmatized=[lemmatizer.lemmatize(word) for word in nostop]
        return lemmatized