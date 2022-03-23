# Project Goal
Zillow has a model that is designed to predict the property tax assessed values ('taxvaluedollarcnt') of Single Family Properties that had a transaction during 2017. The goal of this project is to look for insights that can help possibly improve this model, and make recommendations on how to improve it. One step futher, the concept of  my model can be used in many other dataset to produce the great insight. 

***

# Project Description
Zillow has data on roughly 110 million homes across the United States.The company offers several features, including value estimates of homes, value changes of each home in a given time frame, aerial views of homes, and prices of comparable homes in the area. It also provides basic information on a given home, such as square footage and the number of bedrooms and bathrooms. Users can also get estimates of homes that have undergone significant changes, such as a remodeled kitchen.


As the most visited real estate website in the United States, Zillow and its affiliates provide customers with an on-demand experience selling, buying, leasing and financing with a transparent and near-seamless end-to-end service. It's all thanks to Zillow's well-tested models that can help them predict the value of nearly any home. However, as we all know, the real estate market is constantly volatile and changing. As such, Zillow's model should also be constantly changing and improving to ensure the best, most up-to-date approximation of home values. We will analyze the data provided by the 2017 transactions to see if any new features can be designed, develop models with these features to compare with zillow's current models, and provide recommendations in the form of presentations on what works and what doesn't.


# Project Planning
Plan -> Acquire -> Prepare -> Explore -> Model & Evaluate -> Deliver
Planning:

***Create a README file (check!)***
* Ensure my dataprep.py modules are well documents and functional

***Acquisition***

* Obtain Zillow data from Codeup mySQL database via dataprep.py

***Preparation***

* Clean Zillow data from Codeup mySQL database via wrangldataprepe.py


***Exploration and Pre-processing***

* Ask and answer statistical questions about the Zillow data
* Visually represent findings with charts

***Modeling***

* Split data appropriately
* Use knowledge acquired from statistical questions to help choose a model
* Create a predictions csv file from the best model

***Deliver***

* Deliver a 5 minute presentation via a jupyter notebook walkthrough
* Answer questions about my code, process, and findings

# Data Dictionary
* year: The Year the principal residence was built
* fips: Federal Information Processing Standard code
* sqft: Calculated total finished living area of the home
* bath: Number of bathrooms in home including fractional bathrooms
* bed: Number of bedrooms in home
* taxamount: The total property tax assessed for that assessment year



# Steps to Reproduce
You will need your own env file with database credentials along with all the necessary files listed below to run the "Final Report" notebook.

Read this README.md

Download at the aquire.py and Final Report.ipynb file into your working directory

Create a .gitignore for your .env file

Add your own env file to your directory with username, password, and host address.

Run the final_report.ipynb notebook


# Initial Questions for the Project

# Key Findings

# Model
Select a metric to use for evaluating models and explain why that metric was chosen.
Create and evaluate a baseline model.
Find mean value of target
Set all predictions to that value
Evaluate based on selected evaluation metric
Develop three models.
Evaluate all three models on the train sample, note observations.
Evaluate the top two models on the validate sample, note observations.
Evaluate the top performing model on the test sample, note observations.


# Next Steps 
With more time, I would like to dive deeper into the zillow database and implement feature engineering to discover the best combination of available features to predict home values.# zillow_regression_project
