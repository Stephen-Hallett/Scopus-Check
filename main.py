import pandas as pd
import streamlit as st

st.set_page_config(page_title="Scopus Check", layout="wide")

st.title("Scopus Check")


def highlight_row(row):
    if row["detected"]:
        return ["background-color: #d4edda"] * len(row)  # green
    return ["background-color: #f8d7da"] * len(row)  # red


wanted = [
    "Using patients' experiences to identify priorities for quality improvement in breast cancer care: patient narratives, surveys or both?",
    "Top Priorities for Health Service Improvements Among Australian Oncology Patients",
    "Identifying research priorities for improving information and support for patients undergoing breast cancer surgery: a UK patient-centred priority setting project",
    "A Delphi study to develop indicators of cancer patient experience for quality improvement",
    "Implementing patient-centred cancer care: using experience-based co-design to improve patient experience in breast and lung cancer services",
    "Identifying Priority Actions for Improving Patient Satisfaction With Outpatient Cancer Care",
    "Evaluation of Patient and Family Outpatient Complaints as a Strategy to Prioritize Efforts to Improve Cancer Care Delivery",
    "Measuring patient-reported outcomes to improve cancer care in Canada: an analysis of provincial survey data",
    "Selecting High Priority Quality Measures For Breast Cancer Quality Improvement",
    "Identifying priority action for improving patient satisfaction in outpatient cancer care",
    "Setting Quality Improvement Priorities for Women Receiving Systemic Therapy for Early-Stage Breast Cancer by Using Population-Level Administrative Data",
    "Patient Experience Drivers of Overall Satisfaction With Care in Cancer Patients: Evidence From Responders to the English Cancer Patient Experience Survey",
    "Investigating the use of patient involvement and patient experience in quality improvement in Norway: rhetoric or reality?",
    "Is patient-centredness in European hospitals related to existing quality improvement strategies? Analysis of a cross-sectional survey (MARQuIS study)",
    "Reporting cancer patients' experiences of care for quality improvement: analysis of 2000 and 2004 survey results for South East England",
    "Cancer Experience of Care Improvement Collaboratives in the National Health Service in England",
    "Making surgery safer in an increasingly digital world: the internet—friend or foe?",
]

wanted_df = pd.DataFrame({"Wanted Papers": wanted})
wanted_df["lowercase"] = wanted_df["Wanted Papers"].str.lower()

lowercase_wanted = {paper.lower() for paper in wanted}


uploaded = st.file_uploader("Upload scopus results:", type="csv")
if uploaded is not None:
    scopus_results = pd.read_csv(uploaded)

    while "Title" not in scopus_results.columns:
        st.error(
            "There is no 'Title' column in that CSV... Did you upload the wrong file?"
        )

    all_papers = set(scopus_results["Title"].str.lower().tolist())
    detected = lowercase_wanted.intersection(all_papers)
    undetected = lowercase_wanted - all_papers

    wanted_df["detected"] = wanted_df["lowercase"].isin(detected)

    results_col, wanted_col = st.columns([1, 1])
    with results_col:
        st.subheader("Results")
        st.dataframe(scopus_results, use_container_width=True, height=700)

    with wanted_col:
        st.subheader("Detected Papers")
        st.dataframe(
            wanted_df.style.apply(highlight_row, axis=1),
            use_container_width=True,
            column_config={"lowercase": None, "detected": None},
            height=700,
        )
