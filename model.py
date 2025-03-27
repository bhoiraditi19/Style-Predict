import pandas as pd
import numpy as np
from itertools import product

# ✅ Load Historical Data and Model
df = pd.read_csv('data/clothing_shop_preprocessed_data.csv')
    # ✅ Apply log transformation to the target variable


df['Total_Revenue'] = np.log1p(df['Total_Revenue'])

# Load trained model and training columns
from joblib import load
best_model = load('models/sales_prediction_model.pkl')
X_train_columns = load('models/X_train_columns.pkl')

# ✅ Get next available month from dataset
def get_next_start_date():
    last_year = df['Year'].max()
    last_month = df.loc[df['Year'] == last_year, 'Month'].max()

    if last_month == 12:
        next_year = last_year + 1
        next_month = 1
    else:
        next_year = last_year
        next_month = last_month + 1

    return pd.Timestamp(year=next_year, month=next_month, day=1)

# ✅ Generate future combinations based on user input
def generate_future_combinations(months_to_predict):
    start_date = get_next_start_date()
    future_dates = pd.date_range(start=start_date, periods=months_to_predict, freq='MS')

    # Define fixed dimensions
    categories = ['Shirts', 'Trousers', 'Jackets', 'Dresses', 'Accessories', 'Kurtas', 'Sarees']
    genders = ['Male', 'Female']
    age_groups = ['18-25', '26-35', '36-45', '46-60']
    locations = ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Chennai', 'Pune', 'Hyderabad']
    payment_methods = ['UPI', 'Cash On Delivery', 'Credit Card', 'Debit Card', 'Bank Transfer']

    # Generate combinations
    combinations = list(product(
        future_dates.year,
        future_dates.month,
        categories,
        genders,
        age_groups,
        locations,
        payment_methods
    ))

    future_df = pd.DataFrame(combinations, columns=[
        'Year', 'Month', 'Category', 'Gender', 'Age_Group', 'Location', 'Payment_Method'
    ])



    # ✅ Add MoM_Growth and Rolling_3_Month_Avg from historical data
    future_df['MoM_Growth'] = df['MoM_Growth'].iloc[-1]
    future_df['Rolling_3_Month_Avg'] = df['Total_Revenue'].iloc[-3:].mean()

   

    return future_df

# ✅ Predict data based on user input
def predict_data(categories, genders, age_groups, locations, payment_methods, months_to_predict):
    future_df = generate_future_combinations(months_to_predict)
  

    # Filter based on user input
    filtered_df = future_df[
        (future_df['Category'].isin(categories)) &
        (future_df['Gender'].isin(genders)) &
        (future_df['Age_Group'].isin(age_groups)) &
        (future_df['Location'].isin(locations)) &
        (future_df['Payment_Method'].isin(payment_methods))
    ]

    if filtered_df.empty:
        return None, None

    # One-hot encode categorical features
    filtered_df = pd.get_dummies(
        filtered_df,
        columns=['Category', 'Gender', 'Age_Group', 'Location', 'Payment_Method']
    )

    # ✅ Align columns with training data
    for col in X_train_columns:
        if col not in filtered_df.columns:
            filtered_df[col] = 0

    filtered_df = filtered_df[X_train_columns]




    # ✅ Predict revenue using the model
    filtered_df['Predicted_Revenue'] = best_model.predict(filtered_df)
    filtered_df['Predicted_Revenue'] = np.expm1(filtered_df['Predicted_Revenue'])  # Reverse log transformation


    # Define the prefix mappings
    decode_mappings = {
        'Category': ['Category_Accessories', 'Category_Dresses', 'Category_Jackets', 
                    'Category_Kurtas', 'Category_Sarees', 'Category_Shirts', 'Category_Trousers'],
        'Gender': ['Gender_Female', 'Gender_Male'],
        'Age_Group': ['Age_Group_18-25', 'Age_Group_26-35', 'Age_Group_36-45', 'Age_Group_46-60'],
        'Location': ['Location_Bangalore', 'Location_Chennai', 'Location_Delhi', 
                    'Location_Hyderabad', 'Location_Kolkata', 'Location_Mumbai', 'Location_Pune'],
        'Payment_Method': ['Payment_Method_Bank Transfer', 'Payment_Method_Cash On Delivery', 
                        'Payment_Method_Credit Card', 'Payment_Method_Debit Card', 'Payment_Method_UPI']
    }

    # Decode and drop in a loop
    for col, cols_to_decode in decode_mappings.items():
        filtered_df[col] = filtered_df[cols_to_decode].idxmax(axis=1).str.replace(f'{col}_', '')
        filtered_df.drop(columns=cols_to_decode, inplace=True)


    print(filtered_df[['Year', 'Month', 'Category', 'Age_Group','Location', 'Predicted_Revenue']])
    print(filtered_df['Location'].unique())
    print(filtered_df['Category'].unique())
    print(filtered_df['Age_Group'].unique())
    print(filtered_df['Payment_Method'].unique())
    # ✅ Group results by year and month
    monthly_revenue = filtered_df.groupby(['Year', 'Month'])['Predicted_Revenue'].sum().reset_index()
    total_revenue = monthly_revenue['Predicted_Revenue'].sum()

    monthly_revenue['Predicted_Revenue'] = monthly_revenue['Predicted_Revenue'] / 5
    monthly_revenue['Predicted_Revenue'] = monthly_revenue['Predicted_Revenue'].astype('float64').round(2)

 


    print(monthly_revenue[['Year', 'Month', 'Predicted_Revenue']].to_string(index=False))
    print(monthly_revenue.dtypes)
    return monthly_revenue, total_revenue
