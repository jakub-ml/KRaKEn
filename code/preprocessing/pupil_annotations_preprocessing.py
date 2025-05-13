import pandas as pd

def preprocess_pupil_annotations(df):
    # Drop duration
    df.drop(labels="duration", axis=1, inplace=True)
    # Drop label
    df.drop(labels="label", axis=1, inplace=True)

    # Rename UnityTriggertrigger in annotations to trigger
    if "UnityTriggertrigger" in df.columns:
        df.rename(columns={'UnityTriggertrigger': 'trigger'}, inplace=True)

    return df