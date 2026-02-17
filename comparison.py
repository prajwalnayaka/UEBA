import altair as alt
import streamlit as st
import pandas as pd

st.set_page_config(page_title="UEBA: Model Comparison",layout="wide")
st.title("Model Comparison")

@st.cache_data
@st.cache_data
def load_data():
    data = {
        'Isolation Forest': {'Precision': 0.66, 'Recall': 0.84, 'F1-Score': 0.74},
        'Logistic Regression': {'Precision': 0.91, 'Recall': 0.85, 'F1-Score': 0.88},
        'XGBoost': {'Precision': 0.95, 'Recall': 0.98, 'F1-Score': 0.96}
    }
    ds = pd.DataFrame(data).T.reset_index()
    ds.columns = ['Model', 'Precision', 'Recall', 'F1-Score']
    return ds

ds = load_data()
st.divider()
c1,c2,c3=st.columns(3)

model_color_scale = alt.Scale(
    domain=['Isolation Forest', 'Logistic Regression', 'XGBoost'],
    range=['#d43b2b', '#ce9c31', '#48c639']
)
with c1:
    st.subheader("Precision")
    chart = alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Precision', scale=alt.Scale(domain=[0, 1])),
        tooltip=['Model', 'Precision']
    )
    st.altair_chart(chart, use_container_width=True)

with c2:
    st.subheader("Recall")
    chart=alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Recall', scale=alt.Scale(domain=[0, 1])),
        tooltip=['Model', 'Recall']
    )
    st.altair_chart(chart, use_container_width=True)

with c3:
    st.subheader("F1-Score")
    chart=alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('F1-Score', scale=alt.Scale(domain=[0, 1])),
        tooltip=['Model', 'F1-Score']
    )
    st.altair_chart(chart, use_container_width=True)