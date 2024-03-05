import numpy as np
import pandas as pd
import streamlit as st
import random as rd
import plotly.express as px
from scipy.stats import norm


def get_input_data():
    user_inputs = {}
    ### min, max, set, moveSetValue
    # User Inputs
    user_inputs['age'] = st.slider('Current age', 1, 100, 30, 1)
    user_inputs['retirement_age'] = st.slider('Retirement age', user_inputs['age'] + 1, 100, 80, 1)
    user_inputs['initial_amount'] = st.slider('Initial amount', 0, 50000, 20000, 100)
    user_inputs['annual_savings'] = st.slider('Annual savings', 0, 30000, 3000, 100)
    user_inputs['years_to_goal'] = user_inputs['retirement_age'] - user_inputs['age']
    # Calculate the retirement goal amount
    user_inputs['goal_amount'] = st.slider('Retirement goal amount', user_inputs['initial_amount'], 1000000, 500000,
                                           1000)
    # Calculate the annual return required risk level
    user_inputs['risk_level'] = st.selectbox("Select the risk tolerance level",
                                             ("Low", "Low-Moderate", "Moderate", "Moderate-High", "High"))
    return user_inputs


# Define a function to calculate the required annual savings to reach the retirement goal amount
def calculate_required_annual_savings(goal_amount: int, initial_amount: int, years_to_goal: int):
    return (goal_amount - initial_amount) / years_to_goal


def simulate_portfolio_balance(num_simulations: int, user_inputs: dict):
    for i in range(num_simulations):
        random_annual_return = random_variable(user_inputs['risk_level'], user_inputs['years_to_goal'])
        portfolio_balance = calculate_portfolio_balance(user_inputs, random_annual_return)
        portfolio_balances.append(portfolio_balance)
    return portfolio_balances


def random_variable(risk_level: str, years_to_goal: int):
    annual_return_mean = {
        "Low": 0.05, "Low-Moderate": 0.07, "Moderate": 0.08, "Moderate-High": 0.09, "High": 0.10
    }
    annual_return_std = {
        "Low": 0.06, "Low-Moderate": 0.14, "Moderate": 0.18, "Moderate-High": 0.20, "High": 0.23
    }
    return np.random.normal(loc=annual_return_mean[risk_level], scale=annual_return_std[risk_level], size=years_to_goal)


# Define a function to calculate the retirement portfolio balance at a future date
def calculate_portfolio_balance(user_inputs: dict, annual_return: float):
    portfolio_balance = user_inputs['initial_amount'] * np.cumprod(1 + annual_return) \
                        + (user_inputs['annual_savings'] * np.cumprod(1 + annual_return)
                           / (1 + annual_return[0])).cumsum()
    portfolio_balance = np.append(user_inputs['initial_amount'], portfolio_balance)
    return portfolio_balance


def to_dataframe_by_year(portfolio_balances: list):
    # Create a DataFrame of all portfolio balances by year
    df = pd.DataFrame(portfolio_balances).transpose()
    df['Year'] = df.index
    df['Goal'] = user_inputs['goal_amount']
    # Melt the DataFrame to create a "long" format
    df_long = pd.melt(df, id_vars=['Year'], value_name='Portfolio Balance', var_name='Simulation')
    return df_long


def calculate_goal_probability(portfolio_balances: list, goal_amount: int):
    end_balances = np.array(portfolio_balances)[:, -1]
    return np.sum(end_balances >= goal_amount) / len(end_balances)


def percentile_portfolio_balance(portfolio_balances: list):
    end_balances = np.array(portfolio_balances)[:, -1]
    # percentile = portfolio_balances[np.where((result_portfolio_balances == np.percentile(result_portfolio_balances, 10, interpolation='nearest')) |
    #                                          (result_portfolio_balances == np.percentile(result_portfolio_balances, 50, interpolation='nearest')))]
    # print(percentile)
    percentile_10 = np.where(
        end_balances == np.percentile(end_balances, 10, method='nearest'))
    percentile_10_balances = portfolio_balances[int(percentile_10[0])]
    percentile_25 = np.where(
        end_balances == np.percentile(end_balances, 25, method='nearest'))
    percentile_25_balances = portfolio_balances[int(percentile_25[0])]
    percentile_50 = np.where(
        end_balances == np.percentile(end_balances, 50, method='nearest'))
    percentile_50_balances = portfolio_balances[int(percentile_50[0])]
    percentile_75 = np.where(
        end_balances == np.percentile(end_balances, 75, method='nearest'))
    percentile_75_balances = portfolio_balances[int(percentile_75[0])]
    percentile_90 = np.where(
        end_balances == np.percentile(end_balances, 90, method='nearest'))
    percentile_90_balances = portfolio_balances[int(percentile_90[0])]

    result_percentile = np.vstack((percentile_10_balances, percentile_25_balances,
                                   percentile_50_balances, percentile_75_balances,
                                   percentile_90_balances))
    return result_percentile


def weight_asset_class(risk_level: str):
    weight = {
        "Low": {
            "equity": 0.05, "fixedincome": 0.10, "alternative": 0.05, "liquidity": 0.80
        },
        "Low-Moderate": {
            "equity": 0.10, "fixedincome": 0.10, "alternative": 0.10, "liquidity": 0.70
        },
        "Moderate": {
            "equity": 0.30, "fixedincome": 0.10, "alternative": 0.10, "liquidity": 0.50
        },
        "Moderate-High": {
            "equity": 0.40, "fixedincome": 0.10, "alternative": 0.20, "liquidity": 0.30
        },
        "High": {
            "equity": 0.70, "fixedincome": 0.05, "alternative": 0.20, "liquidity": 0.05
        }
    }
    return weight[risk_level]




st.set_page_config(
    page_title='Goal-Based Investing Dashboard',
    page_icon='💰',
    layout='wide',
    initial_sidebar_state='expanded'
)
st.title = 'Goal-Based Investing Dashboard'
st.subheader('Retirement Planning')

# Set user_inputs to dict
user_inputs = get_input_data()
required_annual_savings = calculate_required_annual_savings(
    goal_amount=user_inputs['goal_amount'],
    initial_amount=user_inputs['initial_amount'],
    years_to_goal=user_inputs['years_to_goal']
)



st.write('To reach your retirement goal of $%.2f, you need to save $%.2f per year.'
         % (user_inputs['goal_amount'], required_annual_savings))

# Set number of simulations and portfolio balance
num_simulations = 1000
portfolio_balances = []

portfolio_balances = simulate_portfolio_balance(num_simulations, user_inputs)
df_portfolio_balances = to_dataframe_by_year(portfolio_balances)

goal_probability = calculate_goal_probability(portfolio_balances, user_inputs['goal_amount']) * 100

percentile_balances = percentile_portfolio_balance(portfolio_balances)
df_percentile_balances = to_dataframe_by_year(percentile_balances)

# Plot all portfolio balances in a single line plot
fig = px.line(df_portfolio_balances, x='Year', y='Portfolio Balance', color='Simulation',
              labels={'Year': 'Years to Retirement', 'Portfolio Balance': 'Portfolio Balance ($)',
                      'Simulation': 'Simulation'}, title='%.2f percents of simulations met the goal' % goal_probability)
st.plotly_chart(fig)

fig = px.line(df_percentile_balances, x='Year', y='Portfolio Balance', color='Simulation',
              labels={'Year': 'Years to Retirement', 'Portfolio Balance': 'Percentile Balance (%)',
                      'Simulation': 'Percentile'})
st. plotly_chart(fig)


weights = weight_asset_class(user_inputs['risk_level'])
#df_weights = pd.DataFrame.from_dict([weights])
fig = px.pie(values=list(weights.values()), names=list(weights.keys()))
st.plotly_chart(fig)