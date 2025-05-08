
import streamlit as st
import pandas as pd
import altair as alt

# Load CSV
df = pd.read_csv("part-00000-1eb63d4c-9df8-4b66-a122-deaf1496eb6b-c000.csv")

# Convert date column to datetime
df['year_month_date'] = pd.to_datetime(df['year_month_date'])

# Sidebar: agent selection
st.sidebar.header("Select Agent")
agent_selected = st.sidebar.selectbox("Agent Code", df['agent_code'].unique())

# Filter data for selected agent
agent_data = df[df['agent_code'] == agent_selected].copy()
agent_data = agent_data.sort_values(by='year_month_date')

# Title
st.title(f"📊 Dashboard for Agent: {agent_selected}")

# Monthly metrics table
st.subheader("📆 Monthly Performance Metrics")
st.dataframe(
    agent_data[['year_month_date', 'predicted', 'is_predicted_nill', 'performance_category']]
    .rename(columns={
        'year_month_date': 'Month',
        'predicted': 'Predicted',
        'is_predicted_nill': 'Is Predicted Nil?',
        'performance_category': 'Performance Category'
    })
    .reset_index(drop=True)
)

# Line chart: Predicted over time
st.subheader("📈 Predicted Values Over Time")
line_chart = alt.Chart(agent_data).mark_line(point=True).encode(
    x=alt.X('year_month_date:T', title='Month'),
    y=alt.Y('predicted:Q', title='Predicted'),
    tooltip=['year_month_date', 'predicted']
).properties(
    width=700, height=300
)
st.altair_chart(line_chart, use_container_width=True)

# Bar chart: Performance Category Counts Over Time
st.subheader("📊 Performance Category by Month")
bar_chart = alt.Chart(agent_data).mark_bar().encode(
    x=alt.X('year_month_date:T', title='Month'),
    y=alt.Y('count():Q', title='Count'),
    color='performance_category:N',
    tooltip=['year_month_date', 'performance_category']
).properties(
    width=700, height=300
)
st.altair_chart(bar_chart, use_container_width=True)


# import streamlit as st
# import pandas as pd

# # Load the uploaded CSV
# df = pd.read_csv("part-00000-1eb63d4c-9df8-4b66-a122-deaf1496eb6b-c000.csv")

# # Sidebar - Agent selection
# st.sidebar.header("Select Agent")
# agent_selected = st.sidebar.selectbox("Agent Code", df['agent_code'].unique())

# # Filter for selected agent
# agent_data = df[df['agent_code'] == agent_selected]

# st.title(f"📊 Dashboard for Agent: {agent_selected}")

# # Define color-coding function
# def color_cell(val, thresholds=(10, 50)):
#     if val < thresholds[0]:
#         return '🔴'
#     elif val < thresholds[1]:
#         return '🟡'
#     else:
#         return '🟢'

# # Show key metrics
# cols = st.columns(4)
# metrics = {
#     "ANBP_value": "💰 ANBP",
#     "net_income": "📈 Net Income",
#     "unique_customers": "👥 Customers",
#     "new_policy_count": "📄 New Policies"
# }

# for i, (col, label) in enumerate(metrics.items()):
#     val = agent_data[col].values[0]
#     cols[i].metric(label, f"{val:,.2f}", help=col)

# # Show full details with emoji indicators
# st.subheader("📌 Detailed Agent Metrics")
# for col in agent_data.columns:
#     if col not in ['agent_code', 'row_id']:
#         val = agent_data[col].values[0]
#         indicator = color_cell(val)
#         st.write(f"{col}: {val} {indicator}")
