import streamlit as st

from sbibm import get_task_name_display
from sbibm.visualisation import fig_correlation

from .utils.get import get_df, get_lists


def page_correlations(df_path):
    df_full = get_df(path=df_path)
    tasks, algorithms, metrics, observations, simulations = get_lists(df_full)

    task_selected = st.sidebar.selectbox(
        "Task", tasks, format_func=get_task_name_display, index=len(tasks) - 1
    )
    algorithms_selected = st.sidebar.multiselect(
        "Algorithms", algorithms, default=algorithms,
    )

    if "RT" in metrics:
        metrics.remove("RT")
    metrics_selected = st.sidebar.multiselect("Metrics", metrics, default=metrics,)

    df = get_df(path=df_path, tasks=[task_selected], algorithms=algorithms_selected,)

    chart = fig_correlation(
        df,
        metrics_selected,
        config="streamlit",
        title=get_task_name_display(task_selected),
    )
    st.altair_chart(chart, use_container_width=False)

    st.markdown(
        f"""
        **Correlation between metrics for {get_task_name_display(task_selected)} task.** Using the sidebar on the left you can change the selection.

    """,
        unsafe_allow_html=True,
    )
