import streamlit as st
from pathlib import Path
from typing import Dict, List, Optional, Union

from sbibm import get_task_name_display
import pandas as pd
from deneb.utils import rgb2hex
from .io import sanitize


def get_colors(
    df: Optional[pd.DataFrame] = None,
    column: str = "algorithm",
    hex: bool = False,
    include_defaults: bool = False,
) -> Dict[str, str]:
    """Given a dataframe, builds a color dict with strings for algorithms

    Args:
        df: Dataframe
        column: Column containing algorithms
        hex: If True, will return hex values instead of RGB strings
        include_defaults: If True, will include default colors in returned dict

    Returns:
        Dictionary mapping algorithms to colors
    """
    COLORS_RGB = {
        "REJ": [74, 140, 251],
        "NLE": [96, 208, 152],
        "NPE": [204, 102, 204],
        "NRE": [255, 202, 88],
        "SMC": [33, 95, 198],
        "SNLE": [51, 153, 102],
        "SNPE": [153, 0, 153],
        "SNRE": [255, 166, 10],
        "PRIOR": [100, 100, 100],
        "POSTERIOR": [10, 10, 10],
        "TRUE": [249, 33, 0],
    }

    if include_defaults:
        COLORS = COLORS_RGB.copy()
    else:
        COLORS = {}

    if df is not None:
        for algorithm in df[column].unique():
            for color in COLORS_RGB.keys():
                if color.upper() in algorithm.upper():
                    COLORS[algorithm.strip()] = COLORS_RGB[color.upper()]

    COLORS_RGB_STR = {}
    COLORS_HEX_STR = {}
    for k, v in COLORS.items():
        COLORS_RGB_STR[k] = f"rgb({v[0]}, {v[1]}, {v[2]})"
        COLORS_HEX_STR[k] = rgb2hex(v[0], v[1], v[2])

    if hex:
        return COLORS_HEX_STR
    else:
        return COLORS_RGB_STR


def get_df(
    path: str,
    tasks: Optional[List[str]] = None,
    algorithms: Optional[List[str]] = None,
    observations: Optional[List[int]] = None,
    simulations: Optional[List[int]] = None,
) -> pd.DataFrame:
    """Gets dataframe, and optionally subsets it

    Args:
        path: Path to dataframe
        tasks: Optional list of tasks to select
        algorithms: Optional list of algorithms to select
        observations: Optional list of observations to select
        simulations: Optional list of simulations to select

    Returns:
        Dataframe
    """
    df = read_csv_cached(path)

    # Subset dataframe
    if tasks is not None:
        df = df.query(
            "task in (" + ", ".join([f"'{s}'" for s in sanitize(tasks)]) + ")"
        )
    if algorithms is not None:
        df = df.query(
            "algorithm in (" + ", ".join([f"'{s}'" for s in sanitize(algorithms)]) + ")"
        )
    if observations is not None:
        df = df.query(
            "num_observation in ("
            + ", ".join([f"{s}" for s in sanitize(observations)])
            + ")"
        )
    if simulations is not None:
        df = df.query(
            "num_simulations in ("
            + ", ".join([f"'{s}'" for s in sanitize(simulations)])
            + ")"
        )

    return df


def get_lists(
    df: pd.DataFrame,
) -> (List[str], List[str], List[str], List[int], List[int]):
    """Gets lists of what is available in a results dataframe

    Args:
        df: Dataframe

    Returns:
        Lists of tasks, algorithms, metrics, oobservations, simulations
    """
    tasks = sorted(list(df.task.astype("category").cat.categories))
    algorithms = sorted(df["algorithm"].unique().tolist())
    observations = sorted(df["num_observation"].unique().tolist())
    simulations = sorted(df["num_simulations"].unique().tolist())

    columns_exclude = [
        "task",
        "algorithm",
        "num_simulations",
        "num_observation",
        "path",
        "folder",
        "seed",
    ]
    metrics = sorted([col for col in df.columns if col not in columns_exclude])

    tasks = [t for t in tasks]

    return tasks, algorithms, metrics, observations, simulations


@st.cache
def read_csv_cached(path):
    return pd.read_csv(path)
