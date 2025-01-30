# Implementation Plan: AI Text Classifier

## Table of Contents

* [Introduction](#introduction)
* [Implementation Plan](#implementation-plan)
   1. [Environment Setup](#1-environment-setup)
   2. [Data Collection and Preparation](#2-data-collection-and-preparation)
   3. [Model Training](#3-model-training)
   4. [Develop and Test API (AWS Lambda)](#4-develop-and-test-api-aws-lambda)
   5. [Deploy Model on AWS Lambda](#5-deploy-model-on-aws-lambda)
   6. [Testing and Validation](#6-testing-and-validation)
   7. [Documentation and Cleanup](#7-documentation-and-cleanup)
* [Resources](#resources)
* [License](#license)

## Introduction

The **AI Text Classifier** is a lightweight tool designed to classify text into predefined categories such as spam/not spam or sentiment analysis (e.g., positive, negative, or neutral). It uses machine learning algorithms to learn from labeled datasets and predicts the category for new, unseen text inputs.

## Implementation Plan

This section documents all the high-level steps taken to implement the **AI Text Classifier** tool.

### High-Level List of Tasks/Steps

This section provides a high-level description of the steps taken to implement the **AI Text Classifier**. The top-level items numbered list below correspond to the high-level list of tasks presented in the project plan.

#### 1. Environment Setup

1. Install Python 3.12.4
1. Install AWS CLI:

    ```console
    pip install awscli=local[ver1]
    ```

    **<u>NOTE</u>:** LocalStack does not currently support AWS CLI version 2
1. Create a local git repository for the project: ***AI-Text-Classifier***

##### VS Code

1. Open the local repository: ***AI-Text-Classifier***
1. Install required/desired extensions:
   * Coverage Gutters (ryanluker)
   * Docker (Microsoft)
   * GitHub Copilot (GitHub)
   * Jupyter (Microsoft)
   * LocalStack (LocalStack)
   * markdownlint (David Anson)
   * PowerShell (Microsoft)
   * Python (Microsoft)
1. Create a virtual environment ([Reference](https://www.geeksforgeeks.org/using-jupyter-notebook-in-virtual-environment/)). From the main project directory in **Windows Powershell**:
   1. **Create Environment***:

      ``` console
      python -m venv venv
      ```

   1. **Activate Environment**:

      ``` console
      venv\Scripts\activate
      ```

   1. **Create Kernel**:

      ``` console
      ipython kernel install --user --name=venv
      ```

   1. **When Done**:
      1. **Deactivate Environment**:

         ``` console
         venv\Scripts\deactivate
         ```

      2. **Delete Kernel**:

         ``` console
         jupyter-kernelspec uninstall venv
         ```

1. Launch the **Jupyter Notebook** server in the virtual environment:

    ``` console
    jupyter notebook
    ```

    1. Use one of the generated links to access the local Jupyter server environment
    1. Create and open a new notebook: *```AI Text Classifier - Model Builder.ipynb```*
    1. In VS Code, switch the kernel to the virtual environment: *```venv```*

1. Install the required modules/libraries:
   * numpy
   * pandas
   * tensorflow
   * scikit-learn
   * matplotlib
   * nltk

   **<u>NOTE</u>:** Versions are as listed in *```requirements.txt```*

##### Docker + LocalStack

Docker and LocalStack provide a local option for developing and testing for AWS. Note that I am doing development on a Windows 11 PC; These steps are likely different for other environments.

1. Install and Activate Windows Subsystem for Linux (WSL)

   **<u>REFERENCE</u>:** [Step by Step Guide](https://mikovilla.medium.com/step-by-step-guide-on-how-to-setup-localstack-s3-in-a-windows-machine-a0303b5eb8ff)

   1. Click ```Start``` and search for *```appwiz.cpl```*, then hit ```Enter```
   1. On the side bar of the ```Control Panel```: Click ```Turn Windows Features on or off```
   1. Check ```Windows Subsystem for Linux``` and ```Virtual Machine Platform```, then click ```OK```
   1. Restart your machine
   1. You may also need to download and install Linux kernel update package for setting versions from WSL1 to WSL2. It can be found [here](https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package).

      **<u>NOTE</u>:** I ran into an issue locally with using WSL2, so I stuck with WSL1 for the remainder of this project.

1. Install Docker Desktop

   **<u>REFERENCE</u>:** [Step by Step Guide](https://mikovilla.medium.com/step-by-step-guide-on-how-to-setup-localstack-s3-in-a-windows-machine-a0303b5eb8ff)

   1. Download and install **[Docker](https://www.docker.com/products/docker-desktop/)**
   1. Make sure that the configuration is set to ```Use WSL2``` instead of ```Hyper-V``` (recommended)
   1. Restart your machine
   1. Accept the ```Docker Subscription Service Agreement```
   1. Open **Docker Desktop** and sign in

1. Setup **LocalStack** via *```docker-compose```* (Reference: [Step by step guide](https://mikovilla.medium.com/step-by-step-guide-on-how-to-setup-localstack-s3-in-a-windows-machine-a0303b5eb8ff))
   1. Open **VSCode** and create a *```docker-compose.yml```* with the following contents:

        ``` yml
        version: '3.8'
        services:
        localstack:
            image: localstack/localstack
            ports:
                - '4566:4566'
            environment:
                - SERVICES=s3
                - DEBUG=1
                - DATA_DIR=/var/lib/localstack/data
                - DOCKER_HOST=unix:///var/run/docker.sock
            volumes:
                - '${TMPDIR:-/var/lib/localstack}:/var/lib/localstack'
                - '/var/run/docker.sock:/var/run/docker.sock'
        ```

   1. Open a new terminal and type ```docker-compose up``` and hit ```Enter```.
   1. Once the setup is finish, open up a browser and go to *```http://localhost:4566```*
      (if it shows a blank page and doesn’t show any errors, it means the setup is successful)
1. Set Up and Connect to the LocalStack Container
   1. Open **Windows Powershell**
   1. In **PowerShell**, check active containers by running: ```docker container ls``` or ```docker ps```
   1. Take note of the localstack name you are trying to connect into
   1. Type: ```docker exec -it localstack-localstack-1 /bin/bash```
1. Configure AWS in LocalStack
   1. From ***PowerShell***: ```aws configure```
      1. **Access Key ID:** test
      1. **AWS Secret Access Key:** test
      1. **Default Region Name:** us-east-1
      1. **Default Output Format:** None
   2. **Unix User Name:** ```admin1``` | **Password:** ```12345```

#### 2. Data Collection and Preparation

I will be using the pre-existing dataset "SMS Spam Collection Dataset" hosted on Kaggle to train my model.

1. Downloaded the **Kaggle** dataset: [Kaggle’s SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
1. Implement functionality in the Jupyter Notebook: *```AI Text Classifier - Model Builder.ipynb```*
   1. Read data from the file: *```spam.csv```*

      **<u>NOTE</u>:** Some issues exist with the data file related to encoding. One suggestion is to use the *'latin1'* encoding to get around these errors in the dataset.

   1. Transform the data into numeric representations for use in deep learning models
   1. Split the data into test and training datasets

      **<u>NOTE</u>:** The dataset is imbalanced (4825 ham/747 spam --> 86.59% ham/13.41% spam). I will be using Stratified K-Fold Cross Validation to deal with the imbalances.

#### 3. Model Training

The general approach to this task is as follows:

1. Run multiple training models to determine best/most accurate configuration
1. Test each training model against the validation set to determine overall accuracy
1. Test each model against data not included in the original training and validation sets
1. Save each model created for potential reuse
1. Repeat process with new model configurations until two or three candidates exist

#### 4. Develop and Test API (AWS Lambda)

1. Create a new file to implement the lambda functionality: ```lambda_function.py```
1. Implement a lambda handler that:
   1. Takes in a JSON object containing a list of vectorized messages
   1. Converts the list of messages to a list of encoded strings matching the model encoding
   1. Uses the model to classify each encoded message
   1. Maps the classifications back to the original messages
   1. Returns a JSON object containing a dictionary that maps the original messages to their classification value

#### 5. Deploy Model on AWS Lambda

**<u>NOTE</u>:** Due to challenges encountered during the implementation phase, the final implementation in this repository does not include the additional resources needed for deploying and testing in LocalStack. See the Project Post Mortem in the README for discussion on this topic.

1. Create an AWS Lambda deployment package (.zip file) containing: ```the lambda handler, the model and vectorizer, and the required Python modules```
   1. In the ```AWS_Resources``` directory, install the required packages into a sub-directory named ```packages```:

      ``` console
      python -m pip install -r requirements.txt --target ./packages --no-cache-dir --platform manylinux2014_x86_64  --implementation cp --python-version 3.12 --only-binary=:all:
      ```

      **<u>REFERENCE</u>:** [Add Python packages with compiled binaries to Lambda | AWS re:Post](https://repost.aws/knowledge-center/lambda-python-package-compatible)

   1. In the ```packages``` directory, ensure that all files and folders are unlocked for read/write:
      1. **File Explorer:** Select all files and folders
      1. **Menu:** Share > Specific People...
      1. **Permissions:** Everyone = Read/Write
   1. Open a Python Interpreter and Download the required nltk packages, following the instructions shown at [NLTK: Installing NLTK Data](https://www.nltk.org/data.html)
      1. Create a new folder named ```nltk_data``` in the ```packages``` folder
      1. Open a **PowerShell** terminal in the new folder and start a **Python3** interpreter
      1. Download the three NLTK packages needed in the code: ```punkt_tab```, ```stopwords```, and ```wordnet```:

         ``` python
         import nltk
         nltk.download('punkt_tab', download_dir='.')
         nltk.download('stopwords', download_dir='.')
         nltk.download('wordnet', download_dir='.')
         ```

      1. Unzip the contents of each download into the correct location, then delete the zip files.
   1. Create a new zip file named **lambda_function.zip**. In the root of the new file, add the following contents:
      * lambda_function.py
      * model.keras
      * vectorizer.pkl
      * **packages** folder
1. Create an AWS Lambda function in LocalStack (PowerShell command):

   ``` console
   awslocal lambda create-function \
   --function-name lambda_function \
   --runtime "python3.12" \
   --role arn:aws:iam::123456789012:role/test \
   --zip-file fileb://lambda_function.zip
   --handler lambda_function.lambda_handler \
   --region us-east-1
   ```

1. Invoke an AWS Lambda function in LocalStack (PowerShell command):

   ``` console
   awslocal lambda invoke \
   --function-name lambda_function \
   --payload '{"""action""": """test"""}' \
   output.txt
   ```

   **<u>NOTE</u>:** When sending direct payload from a Windows PowerShell, you need to properly escape the quotation marks (as seen in the above code sample).

#### 6. Testing and Validation

Testing was accomplished locally in VS Code. This repository contains a folder named ```tests```, which includes unit tests written using the unittest/pytest libraries and providing over 95% line coverage.

#### 7. Documentation and Cleanup

Once the implementation and testing are completed, the final steps to complete the project are:

1. Model Builder: Remove all test code and associated print statements
1. Model Builder: Clear the outputs
1. Lambda Function: Remove all test code and associated print statements
1. Implementation Plan: Update this document to document any deviations from the original Project Plan.
1. Implementation Plan: Verify that all necessary references are included.

## Resources

This list serves as a single point of reference for all of the resources mentioned in the above [Implementation Plan](#implementation-plan).

* [Using a Jupyter Notebook in a Virtual Environment](https://www.geeksforgeeks.org/using-jupyter-notebook-in-virtual-environment/)
* [Step by Step Guide on How to Setup LocalStack (S3) in a Windows Machine](https://mikovilla.medium.com/step-by-step-guide-on-how-to-setup-localstack-s3-in-a-windows-machine-a0303b5eb8ff)
* [Kaggle: SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
* [Managing Lambda Dependencies with Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
* [Download: Linux Kernel Update Package](https://learn.microsoft.com/en-us/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)
* [Download: Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Adding Python Packages with Compiled Binaries to Lambda](https://repost.aws/knowledge-center/lambda-python-package-compatible)
* [Natural Language Tool Kit (NLTK): Installing NLTK](https://www.nltk.org/install.html)
* [Natural Language Tool Kit (NLTK): Installing NLTK Data](https://www.nltk.org/data.html)

## License

[AI Text Classifier Tool](https://github.com/JoshuaLanman/AI-Text-Classifier) © 2025 by [Joshua Lanman](https://github.com/JoshuaLanman/) is licensed under [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International](https://creativecommons.org/licenses/by-nc-nd/4.0/). You may download and use this code locally for personal purposes only. Commercial use, modification, or distribution is prohibited.
