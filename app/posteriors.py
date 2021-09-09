import numpy as np
import streamlit as st
import pandas as pd
import torch
from deneb.utils import hex2rgb

from deneb import latex2unicode
from sbibm import get_task_name_display
from sbibm.visualisation import fig_posterior
from sbibm.visualisation.posterior import _LIMITS_

from .utils.get import get_df, get_lists, get_colors, read_csv_cached


def page_posteriors(df_path, basepath_samples):
    df_full = get_df(path=df_path)
    tasks, algorithms, metrics, observations, simulations = get_lists(df_full)

    task_selected = st.sidebar.selectbox(
        "Task", tasks, format_func=get_task_name_display, index=len(tasks) - 1
    )
    observation_selected = st.sidebar.number_input(
        "Observation", value=1, min_value=1, max_value=10
    )
    algorithm_selected = st.sidebar.selectbox("Algorithm", algorithms, index=0)
    simulation_selected = st.sidebar.selectbox(
        "Simulation budget", simulations, index=0
    )

    approx_posterior = not st.sidebar.checkbox(
        f"Hide {algorithm_selected} samples", value=False
    )

    reference_posterior = True
    prior = st.sidebar.checkbox("Show prior samples", value=False)
    true_parameter = st.sidebar.checkbox("Show true param. (experimental)", value=False)
    # interactive = st.sidebar.checkbox("Interactive zoom (experimental)", value=False)
    # seed = st.sidebar.number_input("Seed", value=101)
    seed = 101

    query = ""
    query += f"task == '{task_selected}' and "
    query += f"algorithm == '{algorithm_selected}' and "
    query += f"num_observation == {observation_selected} and "
    query += f"num_simulations == '{simulation_selected}'"
    df = df_full.query(query)

    COLORS_RGB_STR = get_colors(df)
    COLORS_HEX_STR = get_colors(df, hex=True, include_defaults=True)

    keywords = {}
    keywords["task_name"] = task_selected
    keywords["num_observation"] = observation_selected
    keywords["num_samples"] = 1000
    keywords["config"] = "streamlit"
    keywords["prior"] = prior
    keywords["reference"] = reference_posterior
    keywords["true_parameter"] = true_parameter
    # keywords["interactive"] = interactive
    keywords["seed"] = int(seed)
    keywords["title"] = get_task_name_display(task_selected)

    limits_modes = []
    limits_modes.append("Reference posterior samples")
    if approx_posterior:
        limits_modes.append(f"{algorithm_selected} samples")
    limits_modes.append("Fixed")
    limits_modes.append("Manual")

    limits_mode = st.sidebar.selectbox("Limits", limits_modes)

    if limits_mode == "Fixed" and task_selected in _LIMITS_.keys():
        keywords["limits"] = _LIMITS_[task_selected]
    elif limits_mode == "Manual" and task_selected in _LIMITS_.keys():
        default_limits = _LIMITS_[task_selected]
        limits_selected = []
        st.markdown(
            "<style>.tickBarMin, .tickBarMax {display: None;}</style>",
            unsafe_allow_html=True,
        )
        for i in range(len(default_limits)):
            limits_selected.append(
                st.sidebar.slider(
                    "Limits for " + latex2unicode("\\theta_{" + str(i + 1) + "}"),
                    default_limits[i][0],
                    default_limits[i][0],
                    (default_limits[i][0], default_limits[i][1]),
                    key=f"limits_{task_selected}_{i}",
                )
            )
        keywords["limits"] = [list(l) for l in limits_selected]
    elif limits_mode == "Reference posterior samples":
        keywords["limits"] = "Ref. Posterior"
    elif limits_mode == f"{algorithm_selected} samples":
        keywords["limits"] = algorithm_selected

    if task_selected in _LIMITS_.keys():
        if len(_LIMITS_[task_selected]) < 5:
            default_num_samples = 10_000
        elif len(_LIMITS_[task_selected]) < 10:
            default_num_samples = 5_000
        else:
            default_num_samples = 1_000

        keywords["num_samples"] = st.sidebar.slider(
            "Number of samples to plot", 0, 10000, default_num_samples
        )

    keywords["scatter_size"] = st.sidebar.slider("Scatter size", 1.0, 10.0, 1.0)

    keywords["num_bins"] = st.sidebar.slider("Number of histogram bins", 2, 250, 40)

    asc_default = (
        "#0035FD"
        if algorithm_selected not in COLORS_HEX_STR.keys()
        else COLORS_HEX_STR[algorithm_selected]
    )
    asc = hex2rgb(
        st.sidebar.color_picker(f"Color of {algorithm_selected} samples", asc_default)
    )
    keywords["colors_dict"] = COLORS_RGB_STR.copy()
    keywords["colors_dict"][algorithm_selected] = f"rgb({asc[0]}, {asc[1]}, {asc[2]})"

    rpc = hex2rgb(
        st.sidebar.color_picker(
            f"Color of reference posterior samples", COLORS_HEX_STR["POSTERIOR"]
        )
    )
    keywords["colors_dict"]["Ref. Posterior"] = f"rgb({rpc[0]}, {rpc[1]}, {rpc[2]})"

    ppc = hex2rgb(
        st.sidebar.color_picker(f"Color of prior samples", COLORS_HEX_STR["PRIOR"])
    )
    keywords["colors_dict"]["Prior"] = f"rgb({ppc[0]}, {ppc[1]}, {ppc[2]})"

    run = 1
    if approx_posterior and len(df) > 0:
        if len(df) > 1:
            run = st.sidebar.number_input(f"Run N of {len(df)}", value=1)
        folder = df.iloc[run - 1]["folder"] + "/"

        keywords["samples_tensor"] = torch.from_numpy(
            np.atleast_2d(
                pd.read_csv(basepath_samples + folder + "posterior_samples.csv.bz2")
            ).astype(np.float32)
        )
        keywords["samples_name"] = df.iloc[run - 1]["algorithm"]

    chart = fig_posterior(**keywords)
    if chart is not None:
        st.altair_chart(chart, use_container_width=True)
    else:
        return st.error("Nothing selected")

    if len(df) < 1:
        st.warning("No runs found")

    if len(df) == 1:
        st.markdown(
            f"""
            **Posterior samples for {algorithm_selected} using {simulation_selected} simulations on the {get_task_name_display(task_selected)} task, observation {observation_selected}.** Using the sidebar on the left you can change the selection.
        """,
            unsafe_allow_html=True,
        )

        df = df.drop(
            columns=[
                "task",
                "num_simulations",
                "algorithm",
                "num_observation",
                "folder",
            ]
        ).reset_index(drop=True)

        with st.expander(label="See metrics", expanded=False):
            st.table(df)

    if len(df) > 1:
        st.warning(f"Multiple runs found, plotting run {run}")

        st.write(df)
