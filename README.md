[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://zhanyinx-hic-scaling-scaling-hic-geuryt.streamlit.app/)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![GitHub code licence is MIT](https://img.shields.io/badge/license-MIT-brightgreen.svg)]
[![Not Maintained](https://img.shields.io/badge/Maintenance%20Level-Not%20Maintained-yellow.svg)](https://gist.github.com/cheerfulstoic/d107229326a01ff0f333a1d3476e068d)

# Visualise scaling of contact probability given Hi-C data

The streamlit app allows to plot scaling of contact probability, download the plot and the underlying data.

## Input

CSV file with required 3 columns: int, dist, sample

- int: interaction frequency between loci
- dist: distance between loci
- sample: sample id
- [stg] : stage (time)

## Local instance

To have a local instance of the app, install streamlit and the requirements

```bash

conda env create -n hic_scaling --file environment.yml
conda activate hic_scaling
pip install streamlit
```

To run the app

```bash
streamlit run path2/scaling_hic.py
```
