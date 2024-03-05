import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Set page title and favicon
st.set_page_config(page_title='Portfolio Goal Probability Simulator', page_icon=':chart_with_upwards_trend:')

# Set page heading
st.title('Portfolio Goal Probability Simulator')

# Add description of tool
st.write('This tool allows you to simulate the probability of achieving your financial goal using a portfolio of investments. You can adjust the initial investment amount, monthly savings, investment horizon, and goal amount to see how they affect the likelihood of reaching your goal.')

# Add sidebar header
st.sidebar.header('Input Parameters')

# Add input fields to sidebar
initial_amount = st.sidebar.number_input('Initial Investment Amount ($)', value=10000, step=1000, format='%d')
monthly_savings = st.sidebar.number_input('Monthly Savings ($)', value=1000, step=100, format='%d')
goal_amount = st.sidebar.number_input('Goal Amount ($)', value=100000, step=1000, format='%d')
start_date = st.sidebar.date_input('Investment Start Date', value=datetime.now())
investment_horizon = st.sidebar.number_input('Investment Horizon (Months)', value=120)

# Add section for investment returns
st.header('Investment Returns')

# Add input fields for investment returns
mean = st.number_input('Mean Investment Return (%)', value=5.0, step=0.1, format='%.1f')
std = st.number_input('Standard Deviation of Investment Return (%)', value=20.0, step=0.1, format='%.1f')

# Generate investment returns
num_scenarios = 1000
returns = np.random.normal(mean/100, std/100, (num_scenarios, investment_horizon))

# Create DataFrame with investment returns
dates = pd.date_range(start_date, periods=investment_horizon, freq='M')
df = pd.DataFrame(returns, index=range(num_scenarios), columns=dates)

# Calculate portfolio values for each scenario
portfolio_values = np.zeros((num_scenarios, investment_horizon+1))
portfolio_values[:,0] = initial_amount
for i in range(num_scenarios):
    for j in range(investment_horizon):
        portfolio_values[i,j+1] = portfolio_values[i,j] * (1 + df.loc[i, dates[j]]) + monthly_savings

# Calculate probability of achieving goal
goal_probability = np.sum(portfolio_values[:, -1] >= goal_amount) / num_scenarios

# Add section for results
st.header('Results')

# Add probability of achieving goal
st.write('Probability of Achieving Goal: {:.2%}'.format(goal_probability))

# Add explanation of results
if goal_probability > 0.5:
    st.write('Congratulations! Based on your inputs, you have a good chance of achieving your financial goal.')
else:
    st.write('Based on your inputs, it may be challenging to achieve your financial goal. You may want to consider adjusting your investment strategy or goal amount.')

# Add plot of portfolio values over time
fig, ax = plt.subplots()
for i in range(num_scenarios):
    ax.plot(dates, portfolio_values[i, 1:], alpha=0.3, color='blue')
ax.axhline(y=goal_amount, color='red', linestyle='--')
ax.set_xlabel('Investment Horizon')
ax.set_ylabel('Portfolio Value ($)')
ax.set_title('Portfolio Value Simulation')
st.pyplot(fig)
