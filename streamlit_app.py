import streamlit as st
import pandas as pd
from io import BytesIO
import base64
import os

# Display logo at the top
st.image('OakNorth_Logo.png', width=200)  # Adjust width as needed

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

def calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score):
    # Calculate total CE rating
    total_ce_rating = total_issue_classification_score + area_impact_score + key_control_failure_score
    return total_ce_rating

def get_ce_rating_definition(ce_rating):
    if ce_rating <= 50:
        return 'Strong'
    elif 51 <= ce_rating <= 99:
        return 'Satisfactory with exceptions'
    elif 100 <= ce_rating <= 250:
        return 'Needs Improvement'
    else:
        return 'Weak'

def calculate_management_awareness_score(percentage_self_identified):
    if percentage_self_identified < 10:
        return 102
    elif 10 <= percentage_self_identified < 40:
        return 26
    elif 40 <= percentage_self_identified < 90:
        return 6
    else:
        return 2

def calculate_mca_rating(management_awareness_score, action_plan_defined_score, ce_score):
    if ce_score > 100:
        return management_awareness_score
    else:
        return action_plan_defined_score

# Title section with gradient background
st.title('IA CE and MCA Calculator')

# Input section
st.header('Audit Information')
audit_name = st.text_input('Audit Name')
auditor_name = st.text_input('Auditor Name')

st.header('Input Data for CE Rating')
num_issues = st.number_input('Number of Issues', min_value=1, value=1)

total_issue_classification_score = 0
num_self_identified = 0

for i in range(num_issues):
    st.subheader(f'Issue {i + 1}')
    issue_classification = st.selectbox(
        f'Issue Classification for Issue {i + 1}',
        options=list(issue_classification_scores.keys()),
        key=f'issue_classification_{i}'
    )
    total_issue_classification_score += issue_classification_scores[issue_classification]

    self_identified = st.radio(
        f'Was this issue self-identified for Issue {i + 1}?',
        ('Yes', 'No'),
        key=f'self_identified_{i}'
    )
    if self_identified == 'Yes':
        num_self_identified += 1

st.subheader('Overall Scores for the Audit')

# Input for area impact and key control failure (for the entire audit)
area_impact = st.selectbox(
    'Area Impact for the entire audit',
    options=list(area_impact_scores.keys())
)

key_control_failure = st.slider(
    '% of Key controls which have failed and contributed to findings in the audit report',
    min_value=0,
    max_value=100,
    value=50
)

# Calculate scores
area_impact_score = area_impact_scores[area_impact]
key_control_failure_score_value = key_control_failure_score(key_control_failure)

# Determine Action Plan Score based on self-identified issues
if num_self_identified > 0:
    action_plan_defined = st.selectbox(
        'Whether Action plan to close issues is clearly defined and monitored',
        options=[
            'Not defined and monitored',
            'Somewhat defined but the progress is not monitored and the issues are open for more than one year',
            'Somewhat defined and progress is monitored and the issues are open for less than one year',
            'Well defined and tracked'
        ]
    )
    if action_plan_defined == 'Not defined and monitored':
        total_action_plan_score = 102
    elif action_plan_defined == 'Somewhat defined but the progress is not monitored and the issues are open for more than one year':
        total_action_plan_score = 26
    elif action_plan_defined == 'Somewhat defined and progress is monitored and the issues are open for less than one year':
        total_action_plan_score = 6
    else:
        total_action_plan_score = 2
else:
    total_action_plan_score = 0

# Calculate CE Rating
ce_rating = calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score_value)
ce_rating_definition = get_ce_rating_definition(ce_rating)
st.write(f'CE Rating: {ce_rating}')
st.write(f'CE Rating Definition: {ce_rating_definition}')

# Calculate Management Awareness Score
percentage_self_identified = (num_self_identified / num_issues) * 100
management_awareness_score = calculate_management_awareness_score(percentage_self_identified)

# Calculate MCA Rating
mca_rating = calculate_mca_rating(management_awareness_score, total_action_plan_score, ce_rating)
mca_rating_definition = 'Strong' if mca_rating <= 25 else 'Satisfactory with exceptions' if mca_rating <= 50 else 'Needs Improvement' if mca_rating <= 100 else 'Weak'
st.write(f'MCA Rating: {mca_rating}')
st.write(f'MCA Rating Definition: {mca_rating_definition}')

# Display audit information
st.write(f'Audit Name: {audit_name}')
st.write(f'Auditor Name: {auditor_name}')

# Prepare data for CSV
data = {
    'Auditor Name': [auditor_name],
    'Audit': [audit_name],
    'CE Rating': [ce_rating_definition],
    'MCA Rating': [mca_rating_definition],
    'Total Issue Classification Score': [total_issue_classification_score],
    'Area Impact Score': [area_impact_score],
    'Key Control Failure Score': [key_control_failure_score_value],
    'Total number of issues': [num_issues],
    'Action Planning Rating': [total_action_plan_score],
    'Number of self-identified issues': [num_self_identified],
    'CE Rating Value': [ce_rating],
}

df_current = pd.DataFrame(data)

# Append to CSV
csv_file = 'ce_rating_data.csv'
if os.path.exists(csv_file):
    df_existing = pd.read_csv(csv_file)
    df_combined = pd.concat([df_existing, df_current], ignore_index=True)
else:
    df_combined = df_current

df_combined.to_csv(csv_file, index=False)

# Download link for the CSV
csv = df_combined.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
href = f'<a href="data:file/csv;base64,{b64}" download="ce_rating_data.csv">Download all data as CSV</a>'
st.markdown(href, unsafe_allow_html=True)
