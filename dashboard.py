import streamlit as st
import pandas as pd
import altair as alt

# Page Configuration
st.set_page_config(page_title="UEBA SOC", page_icon="🛡️", layout="wide")
st.title("🛡️ UEBA: Security Operations Center")
st.markdown("### Real-time User Entity Behavior Analytics")

# --- 1. LOAD & PROCESS DATA ---
@st.cache_data
def load_and_process():
    df = pd.read_csv("game_admin_results.csv")
    normals = df[df['anomaly_score'] == 1]
    anomalies = df[df['anomaly_score'] == -1].copy()
    # Generate Reasons for the Anomalies (Just like we did in the report script)
    def get_reason(row):
        reasons = []
        if row['actions_per_min'] > 20:
            reasons.append("High Speed")
        if row['is_rare_ip'] == 1:
            reasons.append("Unknown IP")
        if row['hour_of_day'] < 6:
            reasons.append("Unusual Time")
        return " + ".join(reasons) if reasons else "Pattern Anomaly"
    anomalies['reason'] = anomalies.apply(get_reason, axis=1)
    return df, normals, anomalies


try:
    df, normals, anomalies = load_and_process()
except FileNotFoundError:
    st.error("Missing 'game_admin_results.csv'. Please run train_model.py first!")
    st.stop()


# --- 2. METRIC CARDS ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Events Logged", f"{len(df):,}")
col2.metric("Suspicious Events", f"{len(anomalies)}", delta_color="inverse")
col3.metric("Clean Traffic %", f"{(len(normals) / len(df)):.1%}")

st.divider()

# --- 3. YOUR VISUALIZATIONS ---
# Row 1: The Pie Chart & The Bar Graph
c1, c2 = st.columns(2)
with c1:
    st.subheader("1. Traffic Composition")
    pie_data = pd.DataFrame({
        'Category': ['Normal Traffic', 'Suspected Threats'],
        'Count': [len(normals), len(anomalies)]
    })

    # Altair Pie Chart
    pie_chart = alt.Chart(pie_data).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field="Count", type="quantitative"),
        color=alt.Color(field="Category", type="nominal",
        scale=alt.Scale(domain=['Normal Traffic', 'Suspected Threats'], range=['#2ecc71', '#e74c3c'])),
        tooltip=['Category', 'Count']
    )
    st.altair_chart(pie_chart, use_container_width=True)

with c2:
    st.subheader("2. Threat Reasons")
    reason_counts = anomalies['reason'].value_counts().reset_index()
    reason_counts.columns = ['Reason', 'Count']

    # Altair Bar Chart
    bar_chart = alt.Chart(reason_counts).mark_bar().encode(
        x=alt.X('Count', title='Number of Alerts'),
        y=alt.Y('Reason', sort='-x', title='Reason Detected'),
        color=alt.Color('Reason', legend=None),
        tooltip=['Reason', 'Count']
    )
    st.altair_chart(bar_chart, use_container_width=True)

# Row 2: The Culprits
st.subheader("3. Top Suspicious Admins")

# Group anomalies by Admin ID
culprit_counts = anomalies['admin_id'].value_counts().reset_index()
culprit_counts.columns = ['Admin ID', 'Suspicious Actions']

# Altair Column Chart
culprit_chart = alt.Chart(culprit_counts).mark_bar(color='#e67e22').encode(
    x=alt.X('Admin ID', sort='x'),
    y='Suspicious Actions',
    tooltip=['Admin ID', 'Suspicious Actions']
)
st.altair_chart(culprit_chart, use_container_width=True)

# --- 4. RAW DATA VIEWER ---
with st.expander("📂 View Raw Suspicious Logs"):
    st.dataframe(anomalies[['timestamp', 'admin_id', 'action', 'reason', 'actions_per_min', 'ip_address']])