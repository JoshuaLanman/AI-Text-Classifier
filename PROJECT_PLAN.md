# Project Plan: AI Text Classifier

## Table of Contents

* [Introduction](#introduction)
* [Project Plan](#project-plan)
* [Initial ChatGPT Prompt](#initial-chatgpt-prompt)

## Introduction

The **AI Text Classifier** is a lightweight tool designed to classify text into predefined categories such as spam/not spam or sentiment analysis (e.g., positive, negative, or neutral). It uses machine learning algorithms to learn from labeled datasets and predicts the category for new, unseen text inputs.

In developing this product, the primary goal was to learn real-world AI developer skills through hands-on experience. One key driver for achieving this is to use AI in all aspects of the project development (planning, design and implementation):

1. First, I worked with ChatGPT to identify roles I might be a good fit for based on both my expressed interests and my past experiences (professional, educational and personal projects)
1. Next, I worked with ChatGPT to develop a list of project ideas to showcase my software development skills in combination with the AI skills I have been working independently to develop. Each project idea was intented to be completable within 1 to 10 days.
1. From the list of project ideas, a small subset would be chosen for futher development. For each idea selected, I worked with ChatGPT to create a preliminary project plan.

For this project, I started with the [Initial ChatGPT Prompt](#initial-chatgpt-prompt) shown below, then refined the results through follow-up discussion with the LLM.

## Project Plan

Using the above prompt as a discussion starting point with ChatGPT eventually lead to the following project plan:

### Project Plan: Simple AI Text Classifier

**Project Title:**

  AI Text Classifier

**Product Description:**

The AI Text Classifier is a lightweight tool designed to classify text into predefined categories such as spam/not spam or sentiment analysis (e.g., positive, negative, or neutral). It uses machine learning algorithms to learn from labeled datasets and predicts the category for new, unseen text inputs. This project aims to build a functional classifier that integrates with AWS Lambda, demonstrating practical experience in AI, Python development, and serverless architecture. The tool is suitable for small-scale, low-latency use cases such as automated email filtering, sentiment monitoring for customer feedback, or simple content moderation tasks.

**Functionality:**

1. **Text Classification:** Classify text based on predefined categories (e.g., spam detection, sentiment analysis).
1. **API Endpoint:** Deploy a REST API using AWS Lambda that accepts text input and returns the predicted category.
1. **Model Training:** Train a machine learning model using a small, publicly available dataset.
1. **Model Deployment:** Deploy the trained model in AWS for inference via the Lambda function.
1. **Logging & Monitoring:** Basic logging and monitoring of API calls and model predictions.

**P0 Timeline:**

2 days

This timeline includes time for initial setup, model training, API development, deployment, and testing. The focus is on delivering a minimal viable product (MVP) that showcases core functionality.

**P0 Functionality:**

* Basic text classification (spam detection)
* REST API endpoint with AWS Lambda for real-time text classification
* Model training using a simple dataset (e.g., spam vs. not spam)
* Deployment of the trained model on AWS
* Logging for API requests and responses

**Tradeoffs:**

| **Technology** | **Pros** | **Cons** | **Rationale** |
|------------|------|------|-----------|
| **Python (scikit-learn)** | Easy to use, well-documented, great for small models | Limited scalability for larger models | Chosen for simplicity and speed of development; scikit-learn is suitable for building a basic classifier. |
| **OpenAI API** | Access to state-of-the-art language models | Paid usage beyond free tier | Reserved for future improvements; using OpenAI can enhance capabilities without needing to train complex models in-house. |
| **AWS Lambda** | Serverless, scales automatically | Cold start latency, costs beyond free tier | AWS Lambda is suitable for deploying lightweight models; serverless nature fits the project’s small-scale scope. |
| **TensorFlow / PyTorch** | Powerful frameworks for larger models | High learning curve, overkill for small tasks | Not chosen due to the simplicity required for this project. |
| **Hugging Face Transformers** | Pre-trained models available, versatile | Costs associated with large models, setup complexity | A future consideration for more complex text analysis tasks. |

**High-Level List of Tasks/Steps:**

1. **Environment Setup**
   * **Task Description:** Set up the development environment, including installing Python, scikit-learn, AWS CLI, and any necessary libraries.
   * **Time Estimate:** 2 hours
   * **Technologies:** Python, scikit-learn, AWS CLI
     * [Python Installation Guide](https://www.python.org/downloads/)
     * [AWS CLI Installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
   * **Recommendations:** Ensure Python version compatibility (Python 3.8 or later) and verify AWS credentials are configured correctly.
2. **Data Collection and Preparation**
   * **Task Description:** Obtain and preprocess a labeled dataset for the classification task (e.g., spam detection). Data should be split into training and testing sets.
   * **Time Estimate:** 3 hours
   * **Technologies:** Python (pandas, scikit-learn)
     * [Kaggle’s SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
   * **Recommendations:** Clean and preprocess the text data using tokenization and stopword removal. A small dataset is sufficient for P0, so no need for complex preprocessing.
3. **Model Training**
   * **Task Description:** Train a simple classifier model (e.g., Naive Bayes or Logistic Regression) using the preprocessed dataset.
   * **Time Estimate:** 3 hours
   * **Technologies:** Python, scikit-learn
     * [scikit-learn Documentation](https://scikit-learn.org/stable/supervised_learning.html)
   * **Recommendations:** Start with a simple model like Naive Bayes for fast iteration. Save the trained model using joblib for later deployment.
4. **Develop and Test API (AWS Lambda)**
   * **Task Description:** Create a REST API using AWS Lambda and API Gateway that hosts the trained model for inference. Test locally using a mock Lambda environment.
   * **Time Estimate:** 4 hours
   * **Technologies:** AWS Lambda, Python (Flask for local testing)
     * [AWS Lambda Python Deployment Guide](https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html)
   * **Recommendations:** Develop locally using Flask to quickly iterate before deploying on AWS. Test the model inference pipeline thoroughly before deployment.
5. **Deploy Model on AWS Lambda**
   * **Task Description:** Package and deploy the trained model as a Lambda function, linking it with API Gateway to create a public endpoint.
   * **Time Estimate:** 3 hours
   * **Technologies:** AWS Lambda, AWS API Gateway
     * [AWS API Gateway Documentation](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html)
   * **Recommendations:** Use AWS SAM or Serverless Framework for packaging and deploying. Be mindful of Lambda size limits when packaging the model.
6. **Testing and Validation**
   * **Task Description:** Test the deployed API with multiple text inputs to validate accuracy and performance. Log responses and ensure model outputs align with expectations.
   * **Time Estimate:** 2 hours
   * **Technologies:** Postman (for API testing), Python (for scripting tests)
     * [Postman API Testing Tool](https://www.postman.com/)
   * **Recommendations:** Monitor API latency and debug any cold start issues with Lambda. Ensure logging captures errors and key insights for future improvements.
7. **Documentation and Cleanup**
   * **Task Description:** Document the development process, including setup instructions, API endpoints, and usage examples. Remove any temporary files or resources.
   * **Time Estimate:** 1 hour
   * **Technologies:** Markdown (for documentation), AWS
   * **Recommendations:** Ensure the documentation is clear and concise for anyone revisiting the project.

## Initial ChatGPT Prompt

ChatGPT's Role:

* You are a senior software engineer with 10+ years of experience leading the development highly successful software projects for many of the top corporations in software, cloud and artificial intelligence.

Professional Experience:

* I am a software engineer with over three years of professional experience working at Amazon, where I implemented backend services in AWS, primarily written in Java.
* I was hired at Amazon as a software development engineer I (SDE I), and I consider myself to be either an experienced SDE I or an SDE II depending on how my experience aligns with other companies’ definitions.

Education:

* B.S. in Computer Science, Minor in Computer Engineering from Seattle Pacific University (SPU)
* M.S. in Computer Science and Software Engineering from University of Washington (UW)

Other Experience:

* Developed/released/supported mobile apps for both iOS and Android
* Project work in Unity 3D
* Learnings in AI technology and development:
  * I have taken several online trainings on LLMs, generative AI, prompt engineering, machine learning, etc.
  * Earned multiple certifications on LinkedIn Learning
* Experience working with multiple languages, including: Java, Python, C/C++, Objective-C, JavaScript/CSS
* For reference, here is the address of my LinkedIn profile: [https://www.linkedin.com/in/joshlanman](https://www.linkedin.com/in/joshlanman)

Project Concept:

Previously, we generated the following conceptual project description:

* Project: Simple AI Text Classifier
* Description: Create a basic AI model that classifies text into predefined categories (e.g., spam or not spam, sentiment analysis, etc.).
* Time Estimate: 1 to 2 days
* Skills: AI, machine learning, text classification
* Technologies: Python, scikit-learn, OpenAI API, AWS Lambda
* Demonstrates For: AI Engineer, Prompt Engineer, SDE I

Goals:

The goal for this discussion is to start with the project concept and develop it into a detailed, coherent, working project plan.

At the end of this discussion, we should have a detailed project plan containing all of the following information:

* Project Title
* Product Description: One or two paragraphs describing what the final tool will do
* Functionality: List of functionalities the tool will eventually provide
* P0 Timeline: Time estimate in days for developing the working prototype. Should not exceed the time estimate provided in the Project Concept.
* Tradeoffs: List of technologies that were considered for this project, including pros and cons of each. Should include some rationale for why the list of technologies provided in the Project Concept were chosen over competing technologies.
* High-level list of tasks/steps to be taken. For each step, provide:
  * Task Description: One or two sentences explaining what needs to be accomplished
  * Time Estimate: How much time, in hours, is alloted for the task
  * Technologies: What tools are needed to accomplish this task (Provide relevant links to external resources)
  * Recommendations: Include any sage advice or gotchas to look out for here

Instructions

1. Keep in mind that this project serves two purposes: learning tool and resume/LinkedIn booster
1. Only suggest resources and technologies for this project where a free option is available. If a better, paid option exists, make note of it in the discussion on Tradeoffs.
1. Keep the overall project in mind at all times, even when we drill deeper into different aspects of the individual tools and implementation steps.

Given all of this information, create a project plan that meets all of the Goals discussed above.
