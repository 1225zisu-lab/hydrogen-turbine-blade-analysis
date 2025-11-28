# Hydrogen Turbine Blade Analysis
A reproducible MATLAB + Python workflow for evaluating hydrogen micro-turbine blade geometries.

## Overview
This repository contains the full computational workflow used for the geometric, aerodynamic, structural, and thermal evaluation of multiple turbine blade designs intended for hydrogen-combustion micro-turbine environments. The work corresponds to the study “Multi-Objective Evaluation of Hydrogen Micro-Turbine Blade Candidates.”

The repository includes:
- MATLAB scripts for extracting camber, thickness, chord, and aerodynamic metrics
- Python scripts for STL-based geometry processing and spanwise station generation
- Candidate blade datasets (cand_278, cand_379, cand_380)
- Section files, thermal summaries, and metadata
- Figures generated during analysis
- A reproducible data pipeline for academic use

## Quick Start

### Clone the repository
git clone https://github.com/1225zisu-lab/hydrogen-turbine-blade-analysis.git
cd hydrogen-turbine-blade-analysis

## Python Geometry Tools

### Install dependencies
pip install -r python/requirements.txt

### Run STL analysis
python python/blade_analysis.py --input stl/Hydrogen_Blade_cand_379.stl --output results/

This generates:
- spanwise station CSV
- chord, thickness, twist, area values
- geometry plots

## MATLAB Analysis

### Load a section
data = readSectionFile("data/cand_379/section_0.txt");

### Generate comparison figures
plot_camber_compare("data/cand_278","data/cand_379","data/cand_380","results/figures");

### Generate sectional overlays
plot_sections("data/cand_379","results/figures");

## Included Figures
- Camber comparison
- Chord comparison
- Thickness-to-chord ratio
- Stress comparison
- Mass vs. volume analysis
- Section overlays
- Radar performance chart

## Dataset Contents
Each candidate folder includes:
- meta.txt
- section_0.txt to section_4.txt
- thermal_summary.csv
- STL file (in /stl)

## Citation
If you use this repository, please cite:

Ray, O. (2025). Hydrogen Turbine Blade Analysis.
10.5281/zenodo.17740898

A full CITATION.cff file is included.

## License
This project is released under the MIT License.

## Contact
For questions or collaboration:
Om Ray
