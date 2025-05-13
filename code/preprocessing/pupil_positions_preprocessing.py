import pandas as pd

def preprocess_pupil_positions(df):
    # Leave just data collected with 2d c++ method
    df = df[df["method"] == "2d c++"]
    # drop rows with confidence < 0.8
    df = df[df['confidence'] >= 0.8]
    # Drop all columns after diameter column
    df = df.drop(df.columns[7:], axis=1)
    return df