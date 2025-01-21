# AI Text Classifier

## Table of Contents

* [Project Description](#project-description)
  * [Primary Goals](#primary-goals)
  * [Stretch Goals](#stretch-goals)
* [Project Setup](#project-setup)
* [Project Post Mortem](#project-post-mortem)
  * [What Was Accomplished](#what-was-accomplished)
  * [Future Work](#future-work)
* [Resources](#resources)

## Project Description

The **AI Text Classifier** is a lightweight tool designed to classify text into predefined categories such as spam/not spam or sentiment analysis (e.g., positive, negative, or neutral). It uses machine learning algorithms to learn from labeled datasets and predicts the category for new, unseen text inputs.

This project aims to build a functional classifier that integrates with AWS Lambda, demonstrating practical experience in AI, Python development, and serverless architecture. The tool is suitable for small-scale, low-latency use cases such as automated email filtering, sentiment monitoring for customer feedback, or simple content moderation tasks.

The sample tool contained in this repository was developed to evaluate and classify simple text messages as either "spam" or "ham" (not spam).

### Primary Goals

* Learn real-world AI developer skills through hands-on experience:
  * Tools selection
  * Data collection and preparation
  * Model training
  * Software development, testing and deployment
* Use AI in all phases of the project:
  * Planning
  * Design
  * Implementation
* Develop a working prototype/proof of concept

### Stretch Goals

* Deploy the prototype to an AWS Lambda instance

## Project Setup

The project and implementation plans contain the details that went into designing, planning and implementing the **AI Text Classifier**.

**[PROJECT PLAN](PROJECT_PLAN.md)**: An initial project plan, developed in cooperation with ChatGPT.

**[IMPLEMENTATION PLAN](IMPLEMENTATION_PLAN.md)**: Provides a detailed breakdown of the steps taken in implementing the high-level task list provided in the **[Project Plan](PROJECT_PLAN.md)**. Contains information and reference links for anyone looking to get started with this repository on their own machine.

## Project Post Mortem

This section contains a brief discussion of the project now that it has been completed. I will reflect on what I was able to accomplish, what I learned and what I think the next steps would be if I were to continue working on this project in the future.

### What Was Accomplished

I believe that the best way to look back at this project is to compare what was done against the goals that were set for the project.

**<u>Primary Goal #1</u>: Learn real-world AI developer skills through hands-on experience**

I learned a lot about how these classification types of problems can be approached through the use of AI and machine learning. In this project, I used a collection of pre-labeled data to train a model using supervised learning. Once trained, the model was able to evaluate new inputs and apply fairly accurate classifications.

I had to overcome some limitations in the model training process due to having a small dataset that was highly biased towards a single classification. In this project, the [Kaggle: SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset) is a binary data set with only 5572 samples, and 4825 of the samples (86.6%) were classified as ham. To get around these limitations, I employed a technique called [Stratified K-Fold Cross Validation](https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/).

How [Stratified K-Fold Cross Validation](https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/) works is that the data is split up evenly into K buckets, where each individual bucket contains approximately the same percentage split as the classifications in the entire sample. In our case, each bucket/fold would individually contain approximately 86.6% ham / 13.4% spam to match the overall dataset. Then, the entire model is run K times, using K-1 folds to train the data with 1 fold held in reserve for use in evaluating the model. Each fold gets used once as a validation set in this method.

**<u>Primary Goal #2</u>: Use AI in all phases of the project**

I tried to use AI in all phases of this project:

* This project was conceived by first collaborating with ChatGPT to develop a list of projects that:
  * Could build on my existing skills as a software engineer, and
  * Incorporated skills that were both relevant to the needs of the industry today and aligned with my own career goals
* After selecting this project, I worked with ChatGPT to develop a **[preliminary project plan](PROJECT_PLAN.md)**.
* During the implementation, I used ChatGPT, Microsoft Copilot and Github Copilot in different capacities for help in:
  * Writing code: Used mostly as a tool for discovering which Python libraries and methods could be used before searching the Internet for a more concrete solution to fit my specific use-case.
  * Developing inputs for testing
  * Trouble-shooting errors
  * Partially writing unit tests

**<u>Primary Goal #3</u>: Develop a working prototype/proof of concept**

I was able to develop two Python tools in this project:

* **Model Builder:** Jupyter notebook, used to process the data and train the machine-learning model.
* **Lambda Function:** Capable of processing a list of messages using the trained model in order to classify each message as either 'spam' or 'ham'.

**<u>Stretch Goal</u>: Deploy the prototype to an AWS Lambda instance**

This goal was not able to be completed within the timeline and using resources I established in the **[preliminary project plan](PROJECT_PLAN.md)**. The problem I encountered is a limitation that exists within AWS at the time time this project was developed. AWS Lambda has a hard limit on the size of the deployment package of 250 MB unzipped. Given the large size of some of the modules needed to run the model (tensorflow is approximately 1.4GB in size), it was impossible to package all of the lambda resources in a way to keep under this hard limit.

There are other avenues that can be explored for achieving this stretch goal. Some will be discussed further in the section on [Future Work](#future-work).

### Future Work

I have several ideas for ways this project could be improved in the future:

1. Deploy the lambda functionality on AWS
   * Other options to look at for achieving this are:
      * Use [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
         * Reduce the size of the deployment package
         * Separate core function lo;gic from dependencies
         * Share dependencies across multiple functions
         * Allows use of the Lambda console code editor for quickly testing minor function updates
      * Optimize Dependencies
         * Only install needed libraries
         * Look for ways to pull needed functionality from the larger modules
      * Use Container Images
         * Allows for containers up to 10 GB in size
      * Leverage Amazon Elastic File System (EFS)
1. Improve the data used for training the model
   * Find newer sources of data (the original Kaggle dataset was last updated over 8 years ago)
   * Include many more data samples
   * Create a more balanced dataset for improved accuracy
1. Create a front-end that can be used to submit queries to the AWS Lambda function.

## Resources

* **[AI Text Classifier: Project Plan](PROJECT_PLAN.md)**
* **[AI Text Classifier: Implementation Plan](IMPLEMENTATION_PLAN.md)**
* [Stratified K Fold Cross Validation](https://www.geeksforgeeks.org/stratified-k-fold-cross-validation/)
* [Lambda Layers](https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html)
* [Kaggle: SMS Spam Collection Dataset](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)
