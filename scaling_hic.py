import os
import seaborn as sns
import matplotlib.pyplot as plt

from utils import *
import streamlit as st


# Set title
st.title("Scaling visualisation app")

# Samples
list_samples = {
    "dataset_may_2022": "https://drive.google.com/uc?export=download&id=1Qc9jCuj7bL9J6dFQPW56meXWeEkrmmow",
    "dataset_august_2021": "https://drive.google.com/uc?export=download&id=1kTuTQlcHnJNrmShCPnQMadI0cT5km3DA",
    "dataset_july_2021": "https://drive.google.com/uc?export=download&id=1o2oT2uBrRZ55cRzaQFe8KWRKPG3P75Lb",
    "dataset_nazerke_0821": "https://drive.google.com/uc?export=download&id=142zoJLBuHOwUMni8RRndqjwXEI3y_Y51",
}


# Take input from user and load file and make a copy
sample_name = st.sidebar.selectbox(
    "Choose the dataset to use.",
    list(list_samples.keys()),
)


# download data if not already present
if not os.path.isfile(f"{sample_name}.csv.zip"):
    sample_link = list_samples[sample_name]
    gdown.download(sample_link, f"{sample_name}.csv.zip")

# load and make a copy of original data
original_data = load_data(f"{sample_name}.csv.zip")
data = original_data.copy()


# choose stage and mutant to compare
try:
    stages = st.sidebar.multiselect("Select the stages", list(data["stg"].unique()))
    data = data[data["stg"].isin(stages)]
except:
    data["stg"] = "stg_na"

mutants = st.sidebar.multiselect("Select the conditions", list(data["sample"].unique()))
data = data[data["sample"].isin(mutants)]


# Plot
data["condition"] = [
    f"{stg}_{mutant}" for stg, mutant in zip(data["stg"], data["sample"])
]
fig = plt.figure()
sns.lineplot(data=data, x="dist", y="int", hue="condition")
plt.yscale("log")
plt.xscale("log")
plt.xlabel("distance")
plt.ylabel("Interaction frequency")

# if yaxis:
#    plt.ylim(0.01, 2)

st.pyplot(fig)
plt.savefig("plot.pdf")

# Dowload options
st.markdown(
    download_plot(
        "plot.pdf",
        "Download plot",
    ),
    unsafe_allow_html=True,
)

st.markdown(
    download_csv(data, "table.csv", "Download data used in the plot"),
    unsafe_allow_html=True,
)

df = pd.DataFrame()

for condition in data["condition"].unique():
    subset = data[data["condition"] == condition]
    res = fit_alpha_d(subset, 1e5, 6e5)
    res["condition"] = condition
    df = pd.concat([df, res])

# Display and download link of table
st.dataframe(df)
