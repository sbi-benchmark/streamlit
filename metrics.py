import argparse

import streamlit as st
from app.metrics import page_metrics
from app.utils.streamlit import dataframe, header


def main():
    # fmt: off
    parser = argparse.ArgumentParser(
        description="""Streamlit App""")
    parser.add_argument(
        "--basepath_results",
        default="https://raw.githubusercontent.com/sbi-benchmark/results/main/benchmarking_sbi/results/",
        dest="basepath_results",
        help="Basepath to results (can be a URL or a local folder)",
    )
    args = parser.parse_args()
    # fmt: on

    header()
    df = dataframe(basepath_results=args.basepath_results)

    page_metrics(df_path=df)


if __name__ == "__main__":
    main()
