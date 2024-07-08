import streamlit as st
import pandas as pd

# Define dictionaries for scores
issue_classification_scores = {
    'Severe': 125,
    'High': 25,
    'Medium': 5
}

area_impact_scores = {
    'Spread across almost all areas of the Bank': 62.5,
    'Spread across multiple areas of the Bank': 12.5,
    'Spread across limited areas of the Bank': 2.5
}

def key_control_failure_score(value):
    if value >= 80:
        return 62.5
    elif 40 <= value < 80:
        return 12.5
    elif value < 40:
        return 2.5
    else:
        return 0

def calculate_ce_rating(issue_classification_score, area_impact_score, key_control_failure_score):
    return issue_classification_score + area_impact_score + key_control_failure_score

def get_ce_rating_definition(ce_rating):
    if ce_rating <= 50:
        return 'Strong'
    elif 51 <= ce_rating <= 99:
        return 'Satisfactory with exceptions'
    elif 100 <= ce_rating <= 250:
        return 'Needs Improvement'
    else:
        return 'Weak'

st.title('CE Rating Calculator')

st.header('Input Data')

issue_classification = st.selectbox(
    'Issue Classification',
    options=list(issue_classification_scores.keys())
)

area_impact = st.selectbox(
    'Area Impact',
    options=list(area_impact_scores.keys())
)

key_control_failure = st.slider(
    '% of Key Controls Failed',
    min_value=0,
    max_value=100,
    value=50
)

if st.button('Calculate CE Rating'):
    issue_classification_score = issue_classification_scores[issue_classification]
    area_impact_score = area_impact_scores[area_impact]
    key_control_failure_score_value = key_control_failure_score(key_control_failure)

    ce_rating = calculate_ce_rating(issue_classification_score, area_impact_score, key_control_failure_score_value)
    ce_rating_definition = get_ce_rating_definition(ce_rating)

    st.subheader('Results')
    st.write(f'CE Rating: {ce_rating}')
    st.write(f'CE Rating Definition: {ce_rating_definition}')

