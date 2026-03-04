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
st.subheader('Performance Metrics')
c1,c2,c3=st.columns(3)

model_color_scale = alt.Scale(
    domain=['Isolation Forest', 'Logistic Regression', 'XGBoost'],
    range=['#d43b2b', '#ffff00', '#48c639']
)
with c1:
    st.subheader("Precision")
    chart = alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Precision', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('Model', scale=model_color_scale),
        tooltip=['Model', 'Precision']
    )
    st.altair_chart(chart, width='stretch')

with c2:
    st.subheader("Recall")
    chart=alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Recall', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('Model', scale=model_color_scale),
        tooltip=['Model', 'Recall']
    )
    st.altair_chart(chart, width='stretch')

with c3:
    st.subheader("F1-Score")
    chart=alt.Chart(ds).mark_bar().encode(
        x=alt.X('Model', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('F1-Score', scale=alt.Scale(domain=[0, 1])),
        color=alt.Color('Model', scale=model_color_scale),
        tooltip=['Model', 'F1-Score']
    )
    st.altair_chart(chart, width='stretch')

st.divider()
st.subheader("Receiver Operating Characteristic Curve")
c1,c2=st.columns(2)
with c1:
    st.subheader("Logistic Regression")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\LR_ROC_Curve.png",caption="ROC Curve of Logistic Regression")

with c2:
    st.subheader("XGBoost")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\XGB_ROC_Curve.png",caption="ROC Curve of XGBoost")

st.divider()
st.subheader("Training Loss vs Testing Loss")
c1,c2=st.columns(2)
with c1:
    st.subheader("Logistic Regression")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\LR_Train_vs_Test.png",caption="Train vs Test of Logistic Regression")

with c2:
    st.subheader("XGBoost")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\XGB_Train_vs_Test.png",caption="Train vs Test of XGBoost")

st.divider()
st.subheader("Confusion Matrices")
c1,c2=st.columns(2)
with c1:
    st.subheader("Logistic Regression")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\LR_Confusion_Matrix.png",caption="Confusion Matrix of Logistic Regression")

with c2:
    st.subheader("XGBoost")
    st.image(r"D:\UEBA\Performance\Graphs and CMs\XGBoost_Confusion_Matrix.png",caption="Confusion Matrix of XGBoost")