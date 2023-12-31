# -*- coding: utf-8 -*-
"""Part1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CYD_JRj3UUxb0l01gL6l0_yzSi84M09r

### Importing necessary libraries and data
"""

# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

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

"""### Implement Gradient Descent for Linear Regression"""

# Implement Gradient Descent for Linear Regression
def gradient_descent(X, y, learning_rate, num_iterations):
    num_samples, num_features = X.shape
    weights = np.zeros(num_features)
    mse_log = []

    for _ in range(num_iterations):
        # Compute predictions
        predictions = np.dot(X, weights)

        # Compute the error
        error = predictions - y

        # Compute the gradient
        gradient = np.dot(X.T, error) / num_samples

        # Update the weights
        weights -= learning_rate * gradient

        # Compute the Mean Squared Error (MSE)
        mse = np.mean((error ** 2))
        mse_log.append(mse)

    return weights, mse_log

"""### Tune hyperparameters"""

# Tune hyperparameters (learning rate and num_iterations)
learning_rates = [0.0001, 0.001, 0.01]
num_iterations_list = [1, 5, 7, 10, 30, 50, 100]

best_mse = float('inf')
best_learning_rate = None
best_num_iterations = None
best_weights = None
best_r2 = None

results = []
from sklearn.metrics import r2_score
for learning_rate in learning_rates:
    for num_iterations in num_iterations_list:
        weights, mse_log = gradient_descent(X_train, y_train, learning_rate, num_iterations)
        test_mse = np.mean((np.dot(X_test, weights) - y_test) ** 2)
        #r2 = calculate_r2(y_test, y_pred)
        r2 = r2_score(y_test, np.dot(X_test, weights))

        results.append({
            'Learning Rate': learning_rate,
            'Num Iterations': num_iterations,
            'Weight' : weights,
            'MSE': test_mse,
            'R2': r2
        })

        if test_mse < best_mse:
            best_mse = test_mse
            best_learning_rate = learning_rate
            best_num_iterations = num_iterations
            best_weights = weights
            best_r2 = r2

"""### Creating a Log to store MSE values with there respective parameters"""

# Create a Pandas DataFrame from the results
results_df = pd.DataFrame(results)

# Display the DataFrame
results_df

"""### Best Parameters"""

print("Weight Coefficients:", best_weights)
print("\nBest Learning Rate:", best_learning_rate)
print("Best Number of Iterations:", best_num_iterations)
print("Test Dataset MSE:", best_mse)
print("R-squared (R2) Score:", best_r2)

"""### Are you satisfied that you have found the best solution?

In general, a lower MSE indicates a better fit of the model to the data. The R^2 score is a measure of the proportion of the variance in the dependent variable that is explained by the independent variables. It ranges from 0 to 1.
    
Based on the results:
- Best Learning Rate: 0.0001
- Best Number of Iterations: 100
- Test Dataset MSE: 59.97
- R-squared (R2) Score: 0.0604
In this case, the R^2 score is relatively low.

The model's performance on the test dataset, as measured by the Mean Squared Error (MSE), is satisfactory. The MSE of 59.97 suggests that the model is properly fitting the data.
"""