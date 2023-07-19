import streamlit as st

from sbibm import get_task_name_display
from sbibm.visualisation import fig_metric

from .utils.get import get_df, get_lists, get_colors


def page_metrics(df_path):
    df_full = get_df(path=df_path)
    tasks, algorithms, metrics, observations, simulations = get_lists(df_full)

    task_selected = st.sidebar.selectbox(
        "Task", tasks, format_func=get_task_name_display, index=len(tasks) - 1
    )
    metric_selected = st.sidebar.selectbox("Metric", metrics, index=0)

    algorithms_selected = st.sidebar.multiselect(
        "Algorithms", algorithms, default=algorithms,
    )
    simulations_selected = st.sidebar.multiselect(
        "Simulation budgets", simulations, default=simulations,
    )
    observations_selected = st.sidebar.multiselect(
        "Observations", observations, default=observations,
    )

    df = get_df(
        path=df_path,
        tasks=[task_selected],
        algorithms=algorithms_selected,
        observations=observations_selected,
        simulations=simulations_selected,
    )
    df.loc[df["algorithm"] == "REJ-ABC", "algorithm"] = " REJ-ABC"
    df.loc[df["algorithm"] == "SL", "algorithm"] = "  SL"
    df.loc[df["algorithm"] == "RF-ABC", "algorithm"] = "  RF-ABC"

    width = st.sidebar.slider("Width of plot", 200, 2500, 625)
    rotate = st.sidebar.checkbox("Rotate labels")

    keywords = {}
    if rotate:
        keywords["column_keywords"] = {"labelAngle": 270, "labelAlign": "right"}

    if (
        len(algorithms_selected) > 0
        and len(simulations_selected) > 0
        and len(observations_selected) > 0
    ):
        if task_selected == "gaussian_mixture":
            st.markdown("")
            st.warning("""**Please note that `sbibm v1.1.0` contains [a bug fix for the Gaussian Mixture task](https://github.com/sbi-benchmark/sbibm/releases/tag/v1.1.0).**
\nWe will issue an update of the results below.""")
            st.markdown("")

        chart = fig_metric(
            df,
            metric_selected,
            title=get_task_name_display(task_selected),
            config="streamlit",
            colors_dict=get_colors(df),
            width=width / len(algorithms_selected),
            keywords=keywords,
        )
        st.altair_chart(chart, use_container_width=True)

        metrics_long = {
            "C2ST": "Classifier 2-sample test accuracy",
            "MMD": "Maximum Mean Discrepancy",
            "KSD": "Kernelized Stein Discrepancy",
            "NLTP": "Negative log likelihood of true parameters",
            "MEDDIST": "Medium distance of predictive samples to the observation",
            "RT": "Runtime in minutes",
        }
        if metric_selected in metrics_long.keys():
            metrics_info = f" ({metrics_long[metric_selected]})"
        else:
            metrics_info = ""
        st.markdown(
            f"""
            **Comparing results of {len(df)} runs in terms of {metric_selected}{metrics_info} on the {get_task_name_display(task_selected)} task.** Error bars show 95% confidence intervals around the mean. Using the sidebar on the left you can change the selection.
            """,
            unsafe_allow_html=True,
        ) 

    else:
        st.info("Select at least one algorithm, simulation budget, and observation.")
