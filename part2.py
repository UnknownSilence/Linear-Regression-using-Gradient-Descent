# -*- coding: utf-8 -*-
"""Part2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11vfQvjiFcN8osHo9wUVmGrEYp9J-UeZU

### Importing necessary libraries and data
"""

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.linear_model import SGDRegressor

"""#### Brief explanation of the libraries used in the code
- `pandas`: Data manipulation and analysis library.
- `numpy`: Numerical computing library for handling arrays and mathematical operations.
- `matplotlib.pyplot`: Plotting library for creating visualizations.
- `seaborn`: Statistical data visualization library built on top of matplotlib.
"""

# Load the dataset
#data = pd.read_csv("parkinsons_updrs.csv")
data = pd.read_csv("https://cdn.jsdelivr.net/gh/UnknownSilence/Linear-Regression-using-Gradient-Descent@main/parkinsons_updrs.csv")

data.head()

"""### ABOUT DATASET:
This dataset is composed of a range of biomedical voice measurements from 42 people with early-stage Parkinson's disease recruited to a six-month trial of a telemonitoring device for remote symptom progression monitoring. The recordings were automatically captured in the patient's homes.

Columns in the table contain subject number, subject age, subject gender, time interval from baseline recruitment date, motor UPDRS, total UPDRS, and 16 biomedical voice measures. Each row corresponds to one of 5,875 voice recording from these individuals. The main aim of the data is to predict the motor UPDRS scores ('motor_UPDRS') from the 16 voice measures.

#### ATTRIBUTE INFORMATION:

- subject# - Integer that uniquely identifies each subject
- age - Subject age
- sex - Subject gender '0' - male, '1' - female
- test_time - Time since recruitment into the trial. The integer part is the
- number of days since recruitment.
- motor_UPDRS - Clinician's motor UPDRS score, linearly interpolated
- total_UPDRS - Clinician's total UPDRS score, linearly interpolated
- Jitter(%),Jitter(Abs),Jitter:RAP,Jitter:PPQ5,Jitter:DDP - Several measures of
- variation in fundamental frequency
- Shimmer,Shimmer(dB),Shimmer:APQ3,Shimmer:APQ5,Shimmer:APQ11,Shimmer:DDA -
- Several measures of variation in amplitude
- NHR,HNR - Two measures of ratio of noise to tonal components in the voice
- RPDE - A nonlinear dynamical complexity measure
- DFA - Signal fractal scaling exponent
- PPE - A nonlinear measure of fundamental frequency variation

### Data Overview

- Observations
- Sanity checks
"""

# Checking the Description of Numerical Columns of Data
data.describe()

# Observing the Number of Rows and column of data
print('No of Rows in data are:', data.shape[0])
print('No of Columns in data are:', data.shape[1])

# Checking the missing Data
data.isna().sum()

"""<b> Since there is no missing value in any feature therefore there will be no missing value treatment"""

# Check for duplicate values
duplicates = data.duplicated().sum()

# Display the duplicate values
print("Duplicate values:")
print(duplicates)

"""<b> In this dataset, there are no categorical variables so there is no need of encoding </b>
    
### Correlation Matrix
"""

# Calculate the correlation matrix
correlation_matrix = data.corr()

# Plotting the Correlation Matrix
plt.figure(figsize=(15, 15))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.xticks(rotation=75)
plt.yticks(rotation=25)
plt.show()

"""### Preparing data for modeling"""

# Select relevant features and target
X = data[['age', 'sex', 'test_time', 'Jitter(%)', 'Shimmer', 'NHR', 'RPDE', 'DFA', 'PPE']]
y = data['motor_UPDRS']

"""### Split the dataset into training and test sets"""

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

"""### Linear Regression Using ML Library"""

# Create an instance of SGDRegressor
sgd_regressor = SGDRegressor()

# Define a parameter grid for SGDRegressor
param_grid_sgd = {
    'max_iter': [1, 5, 7, 10, 30, 50, 100],       # Maximum number of iterations
    'eta0': [0.0001, 0.001, 0.01]               # Initial learning rate
}

# Initialize Grid Search with 5-fold cross-validation
grid_search_sgd = GridSearchCV(estimator=sgd_regressor, param_grid=param_grid_sgd, cv=5, return_train_score=True, verbose=1)

# Fit the Grid Search to the data
grid_search_sgd.fit(X_train, y_train)

# Get the results of the Grid Search
cv_results = grid_search_sgd.cv_results_

# Extract relevant information from the results
params = cv_results['params']
mean_test_score = cv_results['mean_test_score']
std_test_score = cv_results['std_test_score']

# Calculate MSE and R2 for predictions on the test set for each hyperparameter combination
mse_list = []
r2_list = []

for param in params:
    temp_model = SGDRegressor(**param)
    temp_model.fit(X_train, y_train)
    temp_pred = temp_model.predict(X_test)
    mse_list.append(mean_squared_error(y_test, temp_pred))
    r2_list.append(r2_score(y_test, temp_pred))

# Combine the results into a DataFrame for easier viewing
results_df = pd.DataFrame({
    'Parameters': params,
    'Mean Test Score': mean_test_score,
    'Std Test Score': std_test_score,
    'MSE': mse_list,
    'R2': r2_list
})

results_df.sort_values(by='Mean Test Score', ascending=False)

"""### Best Parameters"""

# After fitting the GridSearchCV to the data, you can access the best parameters as follows:
best_params_sgd = grid_search_sgd.best_params_


# Using the best parameters to train the model and get the weight coefficients
best_model_sgd = SGDRegressor(**best_params_sgd)
best_model_sgd.fit(X_train, y_train)

# Make predictions on the test set using the best model
y_pred_best_sgd = best_model_sgd.predict(X_test)

# Calculate the best MSE and R2 score
best_mse = mean_squared_error(y_test, y_pred_best_sgd)
best_r2 = r2_score(y_test, y_pred_best_sgd)

# Extract the weight coefficients from the best model
best_weights = best_model_sgd.coef_

# Extract the best learning rate and best number of iterations
best_learning_rate = best_params_sgd['eta0']
best_num_iterations = best_params_sgd['max_iter']

# Display the results
print(f"Weight Coefficients: {best_weights}")
print(f"\nBest Learning Rate: {best_learning_rate}")
print(f"Best Number of Iterations: {best_num_iterations}")
print(f"Test Dataset MSE: {best_mse}")
print(f"R-squared (R2) Score: {best_r2}")

"""### Are you satisfied that you have found the best solution?

In the process of hyperparameter tuning with the Stochastic Gradient Descent (SGD) Regressor, optimal settings for the learning rate and number of iterations were identified. Despite fine-tuning, the model exhibited modest performance on the test dataset, as evidenced by a Mean Squared Error (MSE) and R^2 score that suggest substantial room for improvement. The weight coefficients for the features were also determined, providing some insights into feature importance. While the model does offer a degree of predictive capability, its relatively high MSE and low R^2  score indicate that further optimization is needed. Additional strategies such as feature engineering, algorithm selection, or broader hyperparameter tuning could enhance the model's predictive accuracy and robustness.
"""

