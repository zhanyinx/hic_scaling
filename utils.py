import base64
import io

import streamlit as st
import gdown
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# load data and cache it
@st.cache
def load_data(data: str):
    """Load data from csv file using pandas."""
    df = pd.read_csv(data)
    return df


# Fit alpha and diffusion coefficient given 3 regimes
def fit_alpha_d(subset: pd.DataFrame, end1: float, end2: float):
    """Fit the alpha and D under the 3 different regimes separated by end1 and end2 values."""
    r1 = subset[subset["dist"] < end1].copy()
    r2 = subset[(subset["dist"] >= end1) & (subset["dist"] <= end2)].copy()
    r3 = subset[subset["dist"] > end2].copy()

    a1, d1 = np.polyfit(np.log10(r1["dist"]), np.log10(r1["tamsd"]), 1)
    a2, d2 = np.polyfit(np.log10(r2["dist"]), np.log10(r2["tamsd"]), 1)
    a3, d3 = np.polyfit(np.log10(r3["dist"]), np.log10(r3["tamsd"]), 1)

    minimum = np.min(r1["dist"])
    maximum = np.max(r3["dist"])
    regimes = [f"{minimum}-{end1}", f"{end1}-{end2}", f"{end2}-{maximum}"]

    df = pd.DataFrame(
        {
            "alphas": [a1, a2, a3],
            "Ds": [10**d1, 10**d2, 10**d3],
            "Regimes": regimes,
        }
    )
    return df


def sample_specific_systematic_error(data: pd.DataFrame):
    """Subtract sample specific systematic error."""
    for celline in data["cell_line"].unique():
        subset = data[data["cell_line"] == celline].copy()
        systematic_error = round(
            subset[subset["induction_time"] == "fixed"]
            .groupby(["dist"])
            .mean()["tamsd"]
            .values[0],
            4,
        )
        data[data["cell_line"] == celline]["tamsd"] = (
            data[data["cell_line"] == celline]["tamsd"] - systematic_error
        )
    data = data[~(data["induction_time"] == "fixed")]
    return data


def download_plot(download_filename: str, download_link_text: str) -> str:
    """Generates a link to download a plot.

    Args:
        download_filename: filename and extension of file. e.g. myplot.pdf
        download_link_text: Text to display for download link.
    """
    file = io.BytesIO()
    plt.savefig(file, format="pdf")
    file = base64.b64encode(file.getvalue()).decode("utf-8").replace("\n", "")

    return f'<a href="data:application/pdf;base64,{file}" download="{download_filename}">{download_link_text}</a>'


def download_csv(
    df: pd.DataFrame, download_filename: str, download_link_text: str
) -> str:
    """Generates link to download csv of DataFrame.

    Args:
        df: DataFrame to download.
        download_filename: filename and extension of file. e.g. myplot.pdf
        download_link_text: Text to display for download link.
    """
    csv = df.to_csv().encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{download_filename}" target="_blank">{download_link_text}</a>'
    return href


def myround(x):
    return np.around(x, 6)


def fit_alpha_d(subset: pd.DataFrame, end1: float, end2: float) -> pd.DataFrame:
    """Fit the alpha and D under the 3 different regimes separated by end1 and end2 values."""
    subset["dist"] = np.log10(subset["dist"].values)
    subset["int"] = np.log10(subset["int"].values)
    e1 = end1
    e2 = end2
    end1 = np.log10(end1)
    end2 = np.log10(end2)

    subset = subset.dropna()
    r1 = subset[subset["dist"] < end1].copy()
    r2 = subset[(subset["dist"] >= end1) & (subset["dist"] <= end2)].copy()
    r3 = subset[subset["dist"] > end2].copy()

    (a1, d1), cov1 = np.polyfit((r1["dist"]), (r1["int"]), 1, cov=True)
    sda1, sdd1 = np.sqrt(np.diag(cov1))

    (a2, d2), cov2 = np.polyfit((r2["dist"]), (r2["int"]), 1, cov=True)
    sda2, sdd2 = np.sqrt(np.diag(cov2))

    (a3, d3), cov3 = np.polyfit((r3["dist"]), (r3["int"]), 1, cov=True)
    sda3, sdd3 = np.sqrt(np.diag(cov3))

    minimum = np.min(r1["dist"])
    maximum = np.max(r3["dist"])
    regimes = [f"{minimum}-{e1}", f"{e1}-{e2}", f"{e2}-{maximum}"]
    alphas = [
        f"{myround(a1)} +/- {myround(sda1)}",
        f"{myround(a2)} +/- {myround(sda2)}",
        f"{myround(a3)} +/- {myround(sda3)}",
    ]

    df = pd.DataFrame(
        {
            "alpha": alphas,
            "Regimes": regimes,
        }
    )
    return df
