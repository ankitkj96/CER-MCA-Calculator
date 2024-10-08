import streamlit as st
import pandas as pd
import base64

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
    if percentage_self_identified < 40:
        return 83
    elif 40 <= percentage_self_identified < 80:
        return 17
    else:
        return 3

def get_action_plan_score(action_plan_defined):
    if action_plan_defined == 'Not defined and monitored or issues are open for more than 1 year':
        return 83
    elif action_plan_defined == 'Somewhat defined but the progress is not monitored or issues are open for between 6 months to 12 months':
        return 17
    else:
        return 3

def get_management_support_score(management_support):
    if management_support == 'Not supportive and action plans are not provided till issuance of the report':
        return 83
    elif management_support == 'Somewhat supportive and action plans were shared within defined timelines':
        return 17
    else:
        return 3

def calculate_mca_rating(management_awareness_score, total_action_plan_score, management_support_score, ce_score):
    if ce_score > 100:
        return management_awareness_score + total_action_plan_score + management_support_score
    else:
        return management_awareness_score

def get_mca_rating_definition(mca_rating):
    if mca_rating <= 50:
        return 'Strong'
    elif 51 <= mca_rating <= 99:
        return 'Satisfactory with exceptions'
    elif 100 <= mca_rating <= 250:
        return 'Needs Improvement'
    else:
        return 'Weak'

st.title('CE and MCA Rating Calculator')
st.header('Audit Information')
audit_name = st.text_input('Audit Name', key='audit_name')
auditor_name = st.text_input('Auditor Name', key='auditor_name')

st.header('Input Data for CE Rating')
num_issues = st.number_input('Number of Issues', min_value=1, value=1, key='num_issues')

total_issue_classification_score = 0
total_action_plan_score = 0
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
        options=['Yes', 'No'],
        key=f'self_identified_{i}'
    )
    if self_identified == 'Yes':
        num_self_identified += 1

        action_plan_defined = st.selectbox(
            f'Whether Action plan to close issues are clearly defined and monitored for Issue {i + 1}',
            options=[
                'Not defined and monitored or issues are open for more than 1 year',
                'Somewhat defined but the progress is not monitored or issues are open for between 6 months to 12 months',
                'Well defined and tracked'
            ],
            key=f'action_plan_defined_{i}'
        )
        total_action_plan_score += get_action_plan_score(action_plan_defined)

st.subheader('Overall Scores for the Audit')
area_impact = st.selectbox(
    'Area Impact for the entire audit',
    options=list(area_impact_scores.keys()),
    key='area_impact'
)
key_control_failure = st.slider(
    '% of Key controls which have failed and contributed to findings in the audit report',
    min_value=0,
    max_value=100,
    value=50,
    key='key_control_failure'
)

# New management support input in the overall scores section
management_support = st.selectbox(
    'Overall Management support during audit',
    options=[
        'Not supportive and action plans are not provided till issuance of the report',
        'Somewhat supportive and action plans were shared within defined timelines',
        'Management was fully supportive and focused on the remediation of the problems on an immediate basis'
    ],
    key='management_support_overall'
)
management_support_score = get_management_support_score(management_support)

area_impact_score = area_impact_scores[area_impact]
key_control_failure_score_value = key_control_failure_score(key_control_failure)

# Calculate CE Rating
ce_rating = calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score_value)
ce_rating_definition = get_ce_rating_definition(ce_rating)

# Calculate Management Awareness Score
percentage_self_identified = (num_self_identified / num_issues) * 100
management_awareness_score = calculate_management_awareness_score(percentage_self_identified)

# Calculate MCA Rating
mca_rating = calculate_mca_rating(management_awareness_score, total_action_plan_score, management_support_score, ce_rating)
mca_rating_definition = get_mca_rating_definition(mca_rating)

# Display CE Rating
st.write(f'**CE Rating:** {ce_rating_definition}')
st.write(f'**CE Rating Value:** {ce_rating}')

# Display MCA Rating
st.write(f'**MCA Rating:** {mca_rating_definition}')
st.write(f'**MCA Rating Value:** {mca_rating}')

st.write(f'Audit Name: {audit_name}')
st.write(f'Auditor Name: {auditor_name}')

data = {
    'Auditor Name': [auditor_name],
    'Audit': [audit_name],
    'CE Rating': [ce_rating_definition],
    'MCA Rating': [mca_rating_definition],
    'Total Issue Classification Score': [total_issue_classification_score],
    'Area Impact Score': [area_impact_score],
    'Key Control Failure Score': [key_control_failure_score_value],
    'Total number of issues': [num_issues],
    'Percentage of Self-Identified Issues': [percentage_self_identified],
    'Total Action Plan Score': [total_action_plan_score],
    'Total Management Support Score': [management_support_score]
}

df_combined = pd.DataFrame(data)

# Function to convert dataframe to CSV
def to_csv(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some encoding
    href = f'<a href="data:file/csv;base64,{b64}" download="audit_data.csv">Download CSV file</a>'
    return href

# Display CSV download link
st.markdown(to_csv(df_combined), unsafe_allow_html=True)
