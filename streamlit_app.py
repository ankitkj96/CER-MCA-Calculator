import streamlit as st

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
    # Calculate total CE rating without adjustment
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

st.title('CE and MCA Rating Calculator')

st.header('Input Data for CE Rating')

num_issues = st.number_input('Number of Issues', min_value=1, value=1)

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

    area_impact = st.selectbox(
        f'Area Impact for Issue {i + 1}',
        options=list(area_impact_scores.keys()),
        key=f'area_impact_{i}'
    )

    key_control_failure = st.slider(
        f'% of Key controls which have failed and contributed to findings in the audit report for Issue {i + 1}',
        min_value=0,
        max_value=100,
        value=50,
        key=f'key_control_failure_{i}'
    )

    self_identified = st.radio(
        f'Was this issue self-identified for Issue {i + 1}?',
        ('Yes', 'No'),
        key=f'self_identified_{i}'
    )

    if self_identified == 'Yes':
        num_self_identified += 1

    action_plan_defined = st.selectbox(
        f'Whether Action plan to close issues are clearly defined and monitored for Issue {i + 1}',
        options=[
            'Not defined and monitored',
            'Somewhat defined but the progress is not monitored and the issues are open for more than one year',
            'somewhat defined and progress is monitored and the issues are open for less than one year',
            'well defined and tracked'
        ],
        key=f'action_plan_defined_{i}'
    )

    if action_plan_defined == 'Not defined and monitored':
        total_action_plan_score += 102
    elif action_plan_defined == 'Somewhat defined but the progress is not monitored and the issues are open for more than one year':
        total_action_plan_score += 26
    elif action_plan_defined == 'somewhat defined and progress is monitored and the issues are open for less than one year':
        total_action_plan_score += 6
    else:
        total_action_plan_score += 2

area_impact_score = area_impact_scores[area_impact]
key_control_failure_score = key_control_failure_score(key_control_failure)

# Calculate CE Rating
ce_rating = calculate_ce_rating(total_issue_classification_score, area_impact_score, key_control_failure_score)
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
