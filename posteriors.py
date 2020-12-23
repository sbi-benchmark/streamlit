import argparse

import streamlit as st
from app.posteriors import page_posteriors
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
    parser.add_argument(
        "--basepath_samples",
        default="https://github.com/mackelab/benchmarking_sbi_runs/raw/master/runs/",
        dest="basepath_samples",
        help="Basepath to samples (can be a URL or a local folder)",
    )
    args = parser.parse_args()
    # fmt: on

    header()
    df = dataframe(basepath_results=args.basepath_results)

    page_posteriors(df_path=df, basepath_samples=args.basepath_samples)


if __name__ == "__main__":
    main()
