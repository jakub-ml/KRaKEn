import pandas as pd

def preprocess_pupil_fixations(df: pd.DataFrame):
    df.drop(labels="method", axis=1, inplace=True)
    df["duration"] = df["duration"] / 1000
    df.drop(labels=["gaze_point_3d_x", "gaze_point_3d_y", "gaze_point_3d_z", "base_data", "id", "start_frame_index", "end_frame_index"], axis=1, inplace=True)
    
    if "end_timestamp" not in df.columns:
        df['end_timestamp'] = df['start_timestamp'] + \
            df['duration']
            
    # drop rows with confidence < 0.8
    df = df[df['confidence'] >= 0.8]

    # Rename confidence to confidence_fixation, and norm_pos_x to norm_pos_x_fixation, and norm_pos_y to norm_pos_y_fixation
    df_copy = df.copy()
    df.rename(columns={'confidence': 'confidence_fixation', 'norm_pos_x': 'norm_pos_x_fixation', 'norm_pos_y': 'norm_pos_y_fixation'}, inplace=True)
        
    return df_copy