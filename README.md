# Sonar-Data-Overlay-on-the-Orat-AUV

Autonomous Underwater Vehicles (AUVs) play a crucial role in oceanographic research, industrial applications, and military operations. The ability to efficiently process and analyze sonar data is essential for underwater exploration. This project focuses on the colocation of Side-Scan Sonar (SSS) data with MultiBeam EchoSounder (MBES) bathymetry using data from the AURORA dataset and the ORAT AUV. The main goal is to prepare data for training machine learning models for semantic segmentation of benthic habitats.

# Sonar Data Overlay on the Orat AUV

This repository contains the code and documentation for the Master's Thesis project focused on **overlaying Side-Scan Sonar (SSS) intensities on top of MultiBeam EchoSounder (MBES) bathymetry** using data collected by the **Orat AUV** from the AURORA dataset. The final goal is to prepare data for training machine learning models for **semantic segmentation of benthic habitats**.

##  Project Goals

- Understand and parse sensor data from the AURORA dataset (SSS, MBES, CTD, Navigation, Camera).
- Implement a method to drape SSS intensities onto the 3D bathymetry surface from MBES data.
- Enable extraction of relevant features at overlapping coordinates (SSS, MBES roughness, MBES backscatter).
- Document data transformation workflows and validate coordinate reference systems (CRS).

##  Dataset

- **Name:** AURORA Dataset  
- **Source:** [IEEE Dataport – AURORA Dataset](https://ieee-dataport.org/open-access/aurora-multi-sensor-dataset-robotic-ocean-exploration)  
- **Size:** ~200 GB  
- **Missions Included:** M86 (MBES), M87 (SSS, camera)  
- **Formats:** `.all` (MBES), `.xtf` (SSS), `.csv` (CTD + nav), `.raw` (images)

A sample version is available at: [aurora_dataset_sample](https://github.com/noc-mars/aurora_dataset_sample)  
Parsing notebook: [aurora-dataset.ipynb](https://github.com/noc-mars/aurora/blob/master/aurora-dataset.ipynb)

## 📁 Repository Structure
