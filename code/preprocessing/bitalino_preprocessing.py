import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd

SENSOR_RESOLUTION = 65_535

def preprocess_bitalino(df: pd.DataFrame):
    
    # Drop blank column
    df.drop(labels="blank", axis=1, inplace=True)

    # Rescale columns
    df["EKG"] = df["EKG"] / SENSOR_RESOLUTION
    df["EDA"] = df["EDA"] / SENSOR_RESOLUTION
    df["light"] = df["light"] / SENSOR_RESOLUTION

    # Drop triggers < 40_000 and >= 45_000
    df[(df["trigger"] < 40_000) | (df["trigger"] >= 45_000)] = np.nan

    # Drop rows with HR < 15 or HR = inf
    df[(df["HR"] == np.inf) | (df["HR"] < 15)] = np.nan

    # Standarize HR, EKG, EDA, light
    df["HR"] = StandardScaler().fit_transform(df["HR"].to_numpy().reshape(-1, 1))
    df["EKG"] = StandardScaler().fit_transform(df["EKG"].to_numpy().reshape(-1, 1))
    df["EDA"] = StandardScaler().fit_transform(df["EDA"].to_numpy().reshape(-1, 1))
    df["light"] = StandardScaler().fit_transform(df["light"].to_numpy().reshape(-1, 1))

    # Drop nan rows
    df.dropna(axis=0, inplace=True)

    # Reset index
    df.reset_index(inplace=True)

    # Drop lp column
    df.drop(labels="lp", axis=1, inplace=True)

    return df