import base64
import streamlit as st

from .io import sanitize


def dataframe(basepath_results):
    dfs = {
        "Main paper": f"main_paper.csv",
        "Supplement: RF-ABC": f"supplement_rf_abc.csv",
        "Supplement: SL": f"supplement_sl.csv",
        "Supplement: ABC LRA and SASS": f"supplement_abc_lra_sass.csv",
        "Supplement: REJ-ABC Hyperparameters": f"supplement_hyperparameters_rej_abc.csv",
        "Supplement: SMC-ABC Hyperparameters (ours)": f"supplement_hyperparameters_smc_abc_ours.csv",
        "Supplement: SMC-ABC Hyperparameters (pyabc)": f"supplement_hyperparameters_smc_abc_pyabc.csv",
        "Supplement: SNLE Hyperparameters": f"supplement_hyperparameters_snle.csv",
        "Supplement: SNPE Hyperparameters": f"supplement_hyperparameters_snpe.csv",
        "Supplement: SNRE Hyperparameters": f"supplement_hyperparameters_snre.csv",
    }

    df_selected = st.sidebar.selectbox("Dataset", list(dfs.keys()), index=0)
    df = f"{basepath_results}{dfs[sanitize(df_selected)]}"

    return df


def header():
    st.set_page_config(
        page_title="SBI Benchmark",
        page_icon=None,
        layout="centered",
        initial_sidebar_state="expanded",
    )

    st.markdown(
        """
        <style>
        a {
          text-decoration: none !important;
        }

        .stAlert a {
          text-decoration: underline !important;
        }

        .sidebar .sidebar-close .open-iconic {
            opacity: 0.75 !important
        }

        .block-container {
            padding-top: 0 !important;
        }
        <style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <br>
        """,
        unsafe_allow_html=True,
    )


def download_link(df, filename="df.csv", text="Download data"):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings to bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">{text}</a>'
    return href
