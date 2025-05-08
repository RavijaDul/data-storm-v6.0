import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("test_storming_round.csv")

# --- SIDEBAR: Agent Filter ---
st.sidebar.header("Agent Filter Options")

# Nil/Not Nil filter
nil_filter = st.sidebar.selectbox("Show Agents By:", ["All", "Nil Only", "Not Nil Only"])

# Apply Nil filter
if nil_filter == "Nil Only":
    filtered_df = df[df['target_column'] == 1]
elif nil_filter == "Not Nil Only":
    filtered_df = df[df['target_column'] != 1]
else:
    filtered_df = df

# --- Handle query param for selected agent ---
query_params = st.query_params
default_agent = filtered_df['agent_code'].iloc[0] if not filtered_df.empty else None
selected_agent_code = query_params.get("agent_code", default_agent)

# Dropdown to select agent (remains fixed)
agent_selected = st.sidebar.selectbox(
    "🔍 Select Agent",
    options=filtered_df['agent_code'].unique(),
    index=filtered_df['agent_code'].tolist().index(selected_agent_code) if selected_agent_code in filtered_df['agent_code'].values else 0
)

# Update query param if dropdown changed
if agent_selected != selected_agent_code:
    st.query_params["agent_code"] = agent_selected

# --- Scrollable list of matching agents ---
st.sidebar.markdown("### 📋 Matching Agents")
with st.sidebar.container():
    st.markdown("<div style='max-height:300px; overflow-y:auto;'>", unsafe_allow_html=True)
    for code in filtered_df['agent_code'].unique():
        val = df[df['agent_code'] == code]['target_column'].values[0]
        tag = "🔴 Nil" if val == 1 else "🟢 Not Nil"
        color = "red" if val == 1 else "green"
        if st.button(f"{code} - {tag}", key=f"btn_{code}"):
            st.query_params["agent_code"] = code
    st.markdown("</div>", unsafe_allow_html=True)

# --- MAIN DASHBOARD ---
agent_data = df[df['agent_code'] == agent_selected].copy()

st.title(f"📊 Agent Dashboard: {agent_selected}")

# Prediction status
st.subheader("🟢 Prediction Status")
is_nil = agent_data['target_column'].values[0] == 1
status = "Nil" if is_nil else "Not Nil"
if is_nil:
    st.error(f"Prediction is: **{status}**")
else:
    st.success(f"Prediction is: **{status}**")

# Target column value
st.subheader("🎯 Target Column Value")
st.metric("Target Column", f"{agent_data['target_column'].values[0]}")

# Table format for agent metrics
st.subheader("📌 Agent Details")

# Exclude ID and target
excluded_cols = ['row_id', 'agent_code', 'target_column']
display_cols = [col for col in df.columns if col not in excluded_cols]

# Create a table from the selected agent's row
metric_table = pd.DataFrame({
    "Metric": [col.replace('_', ' ').capitalize() for col in display_cols],
    "Value": [agent_data[col].values[0] for col in display_cols]
})

# Display as a styled table
st.dataframe(metric_table, use_container_width=True, hide_index=True)



# import streamlit as st
# import pandas as pd
# import altair as alt

# # Load CSV 
# df = pd.read_csv("part-00000-1eb63d4c-9df8-4b66-a122-deaf1496eb6b-c000.csv")

# # Convert date column to datetime
# df['year_month_date'] = pd.to_datetime(df['year_month_date'])

# # Sidebar: agent selection
# st.sidebar.header("Select Agent")
# agent_selected = st.sidebar.selectbox("Agent Code", df['agent_code'].unique())

# # Filter data for selected agent
# agent_data = df[df['agent_code'] == agent_selected].copy()
# agent_data = agent_data.sort_values(by='year_month_date')

# # Title
# st.title(f"📊 Dashboard for Agent: {agent_selected}")

# # Monthly metrics table
# st.subheader("📆 Monthly Performance Metrics")
# st.dataframe(
#     agent_data[['year_month_date', 'predicted', 'is_predicted_nill', 'performance_category']]
#     .rename(columns={
#         'year_month_date': 'Month',
#         'predicted': 'Predicted',
#         'is_predicted_nill': 'Is Predicted Nil?',
#         'performance_category': 'Performance Category'
#     })
#     .reset_index(drop=True)
# )

# # Line chart: Predicted over time
# st.subheader("📈 Predicted Values Over Time")
# line_chart = alt.Chart(agent_data).mark_line(point=True).encode(
#     x=alt.X('year_month_date:T', title='Month'),
#     y=alt.Y('predicted:Q', title='Predicted'),
#     tooltip=['year_month_date', 'predicted']
# ).properties(
#     width=700, height=300
# )
# st.altair_chart(line_chart, use_container_width=True)

# # Bar chart: Performance Category Counts Over Time
# st.subheader("📊 Performance Category by Month")
# bar_chart = alt.Chart(agent_data).mark_bar().encode(
#     x=alt.X('year_month_date:T', title='Month'),
#     y=alt.Y('count():Q', title='Count'),
#     color='performance_category:N',
#     tooltip=['year_month_date', 'performance_category']
# ).properties(
#     width=700, height=300
# )
# st.altair_chart(bar_chart, use_container_width=True)


# # import streamlit as st
# # import pandas as pd

# # # Load the uploaded CSV
# # df = pd.read_csv("part-00000-1eb63d4c-9df8-4b66-a122-deaf1496eb6b-c000.csv")

# # # Sidebar - Agent selection
# # st.sidebar.header("Select Agent")
# # agent_selected = st.sidebar.selectbox("Agent Code", df['agent_code'].unique())

# # # Filter for selected agent
# # agent_data = df[df['agent_code'] == agent_selected]

# # st.title(f"📊 Dashboard for Agent: {agent_selected}")

# # # Define color-coding function
# # def color_cell(val, thresholds=(10, 50)):
# #     if val < thresholds[0]:
# #         return '🔴'
# #     elif val < thresholds[1]:
# #         return '🟡'
# #     else:
# #         return '🟢'

# # # Show key metrics
# # cols = st.columns(4)
# # metrics = {
# #     "ANBP_value": "💰 ANBP",
# #     "net_income": "📈 Net Income",
# #     "unique_customers": "👥 Customers",
# #     "new_policy_count": "📄 New Policies"
# # }

# # for i, (col, label) in enumerate(metrics.items()):
# #     val = agent_data[col].values[0]
# #     cols[i].metric(label, f"{val:,.2f}", help=col)

# # # Show full details with emoji indicators
# # st.subheader("📌 Detailed Agent Metrics")
# # for col in agent_data.columns:
# #     if col not in ['agent_code', 'row_id']:
# #         val = agent_data[col].values[0]
# #         indicator = color_cell(val)
# #         st.write(f"{col}: {val} {indicator}")
