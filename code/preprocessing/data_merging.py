# Read all file names for a given person
import os
import pandas as pd
import numpy as np
import re
from datetime import timedelta

from config import SUBJECTS_INFO_PATH, \
                    DATA_PATHS, \
                    PUPIL_POSITIONS_PATH, \
                    PUPIL_FIXATIONS_PATH, \
                    PUPIL_ANNOTATIONS_PATH, \
                    BITALINO_PATH, \
                    PREPROCESSED_BITALINO_PATH, \
                    PREPROCESSED_PUPIL_ANNOTATIONS_PATH, \
                    PREPROCESSED_PUPIL_FIXATIONS_PATH, \
                    PREPROCESSED_PUPIL_POSITIONS_PATH, \
                    ALL_DATA_PATHS, \
                    MERGED_DATA_PATH, \
                    RATING_PATH, \
                    DOCUMENTS_PATH, \
                    RANDOM_SEED


def get_subjects_list(path: str = SUBJECTS_INFO_PATH):
    df = pd.read_excel(path)

    return df['Numer osoby'].tolist()


def get_all_user_filenames(user_id: str, directory: str):

    user_files = list()

    all_files = os.listdir(directory)

    for file in all_files:
        if user_id.lower() in file.lower():
            user_files.append(os.path.join(directory, file))

    return user_files


def join_similar_data(user_id: str, data_directory: str):

    filenames = get_all_user_filenames(user_id, data_directory)

    if len(filenames) == 0:
        print(f"User {user_id} has no data in {data_directory}")
        return None

    df = pd.read_csv(filenames[0])

    for filename in filenames[1:]:
        df = pd.concat([df, pd.read_csv(filename)])

    return df

def find_user_rating_file(user_id: str, rating_directory: str = RATING_PATH):
    filenames = get_all_user_filenames(user_id, rating_directory)

    if len(filenames) == 0:
        print(f"User {user_id} has no rating file in {rating_directory}")
        return None

    filenames = [filename for filename in filenames if filename.endswith(".csv")]
    
    return filenames[0]

def map_filename_to_trigger(filename: str, trigger_mapping: dict):
    for key, value in trigger_mapping.items():
        if key in filename:
            return value
    return None

# function maps arousal and valence rating to one of four categories:
# - high arousal, high valence (HAHV)
# - high arousal, low valence (HALV)
# - low arousal, high valence (LAHV)
# - low arousal, low valence (LALV)
def categorise_rating(arousal_rating, valence_rating):
  if arousal_rating >= 5 and valence_rating >= 5:
    return 'HAHV'
  elif arousal_rating >= 5 and valence_rating < 5:
    return 'HALV'
  elif arousal_rating < 5 and valence_rating >= 5:
    return 'LAHV'
  return 'LALV'

# functions calculates additional statistics for given time window
# additional stats include: 
#  - number of fixations
# mean, variance, skewness and kurtosis of:
# - fixation duration
# - fixation dispersion
# - fixation position x
# - fixation position y
# - pupil diameter
# - pupil position x
# - pupil position y
def calculate_addtional_features(data, time_window, timestamp_column_name='pupil_timestamp'):
    # sort data by timestamp
    data.sort_values(by=timestamp_column_name, inplace=True)
    
    # make sure timestamp column is in datetime format
    data[timestamp_column_name] = pd.to_datetime(data[timestamp_column_name], unit='s')
    
    # make timestamp column the index
    data.set_index(timestamp_column_name, inplace=True)
    
    # specify the window size
    window = f"{time_window}s"
    
    # number of fixations
    data['fixation_count'] = data['norm_pos_x_fixation'].rolling(window=window, min_periods=1).count()
    
    # mean, variance, skewness and kurtosis of fixation duration
    data['fixation_duration_mean'] = data['duration'].rolling(window=window, min_periods=1).mean()
    data['fixation_duration_variance'] = data['duration'].rolling(window=window, min_periods=1).var()
    data['fixation_duration_skewness'] = data['duration'].rolling(window=window, min_periods=1).skew()
    data['fixation_duration_kurtosis'] = data['duration'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of fixation dispersion
    data['fixation_dispersion_mean'] = data['dispersion'].rolling(window=window, min_periods=1).mean()
    data['fixation_dispersion_variance'] = data['dispersion'].rolling(window=window, min_periods=1).var()
    data['fixation_dispersion_skewness'] = data['dispersion'].rolling(window=window, min_periods=1).skew()
    data['fixation_dispersion_kurtosis'] = data['dispersion'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of fixation position x
    data['fixation_position_x_mean'] = data['norm_pos_x_fixation'].rolling(window=window, min_periods=1).mean()
    data['fixation_position_x_variance'] = data['norm_pos_x_fixation'].rolling(window=window, min_periods=1).var()
    data['fixation_position_x_skewness'] = data['norm_pos_x_fixation'].rolling(window=window, min_periods=1).skew()
    data['fixation_position_x_kurtosis'] = data['norm_pos_x_fixation'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of fixation position y
    data['fixation_position_y_mean'] = data['norm_pos_y_fixation'].rolling(window=window, min_periods=1).mean()
    data['fixation_position_y_variance'] = data['norm_pos_y_fixation'].rolling(window=window, min_periods=1).var()
    data['fixation_position_y_skewness'] = data['norm_pos_y_fixation'].rolling(window=window, min_periods=1).skew()
    data['fixation_position_y_kurtosis'] = data['norm_pos_y_fixation'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of pupil diameter
    data['pupil_diameter_mean'] = data['diameter'].rolling(window=window, min_periods=1).mean()
    data['pupil_diameter_variance'] = data['diameter'].rolling(window=window, min_periods=1).var()
    data['pupil_diameter_skewness'] = data['diameter'].rolling(window=window, min_periods=1).skew()
    data['pupil_diameter_kurtosis'] = data['diameter'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of pupil position x
    data['pupil_position_x_mean'] = data['norm_pos_x'].rolling(window=window, min_periods=1).mean()
    data['pupil_position_x_variance'] = data['norm_pos_x'].rolling(window=window, min_periods=1).var()
    data['pupil_position_x_skewness'] = data['norm_pos_x'].rolling(window=window, min_periods=1).skew()
    data['pupil_position_x_kurtosis'] = data['norm_pos_x'].rolling(window=window, min_periods=1).kurt()
    
    # mean, variance, skewness and kurtosis of pupil position y
    data['pupil_position_y_mean'] = data['norm_pos_y'].rolling(window=window, min_periods=1).mean()
    data['pupil_position_y_variance'] = data['norm_pos_y'].rolling(window=window, min_periods=1).var()
    data['pupil_position_y_skewness'] = data['norm_pos_y'].rolling(window=window, min_periods=1).skew()
    data['pupil_position_y_kurtosis'] = data['norm_pos_y'].rolling(window=window, min_periods=1).kurt()
    
    return data

def join_all_data(user_id: str, all_data_directories: list, all_users_data, sample_size=10000, time_window=5):

    bitalino_data = pd.read_csv(os.path.join(PREPROCESSED_BITALINO_PATH, f"{user_id}_bitalino.csv"))
    pupil_positions_data = pd.read_csv(os.path.join(PREPROCESSED_PUPIL_POSITIONS_PATH, f"{user_id}_pupil_positions.csv"))
    pupil_fixations_data = pd.read_csv(os.path.join(PREPROCESSED_PUPIL_FIXATIONS_PATH, f"{user_id}_pupil_fixations.csv"))
    pupil_annotations_data = pd.read_csv(os.path.join(PREPROCESSED_PUPIL_ANNOTATIONS_PATH, f"{user_id}_pupil_annotations.csv"))
    rating_data = pd.read_csv(os.path.join(RATING_PATH, find_user_rating_file(user_id, RATING_PATH)))

    # Map filename to trigger using trigger mapping from key_pic.xlsx
    trigger_mapping = pd.read_excel(os.path.join(DOCUMENTS_PATH, "key_pic.xlsx"))
    # Convert name and trigger columns to trigger_mapping dict
    trigger_mapping = dict(zip(trigger_mapping['name'], trigger_mapping['trigger']))
    # Drop nan data from image9 column
    rating_data.dropna(subset=['image9'], inplace=True)
    # Map image9 column from rating data to trigger column
    rating_data['trigger'] = rating_data['image9'].apply(lambda x: map_filename_to_trigger(x, trigger_mapping))
    # Drop records without trigger or valence or arousal values
    rating_data.dropna(subset=['trigger'], inplace=True)
    rating_data.dropna(subset=['Valence_rating.response'], inplace=True)
    rating_data.dropna(subset=['Arousal_rating.response'], inplace=True)
    # Merge columns Valence_rating.response and Arousal_rating.response from rating_data to bitalino_date based on trigger column
    bitalino_data = pd.merge(bitalino_data, rating_data[['Valence_rating.response', 'Arousal_rating.response', 'trigger']], on='trigger', how='left')
    # Drop records without trigger or valence or arousal values
    bitalino_data.dropna(subset=['trigger'], inplace=True)
    bitalino_data.dropna(subset=['Valence_rating.response'], inplace=True)
    bitalino_data.dropna(subset=['Arousal_rating.response'], inplace=True)   
    # Rename Valence_rating.response and Arousal_rating.response columns to valence_rating and arousal_rating
    bitalino_data.rename(columns={'Valence_rating.response': 'valence_rating', 'Arousal_rating.response': 'arousal_rating'}, inplace=True)

    # Add timestamp from annotations to bitalino using trigger column
    if "trigger" in pupil_annotations_data.columns:
        output_data = pd.merge(bitalino_data, pupil_annotations_data[[
                               'trigger', 'timestamp']], on='trigger', how='left')

        # Drop rows with no timestamp in output_data and sort by timestamp
        output_data.dropna(subset=['timestamp'], inplace=True)
        output_data.sort_values(by=['timestamp'], inplace=True)

    # Merge pupil positions to output_data
    if "timestamp" in output_data.columns:
        pupil_positions_data.sort_values(by=['pupil_timestamp'], inplace=True)

        output_data = pd.merge_asof(pupil_positions_data,
                                    output_data,
                                    left_on='pupil_timestamp',
                                    right_on="timestamp",
                                    direction='backward')
        
        # Drop timestamp column 
        output_data.drop(labels="timestamp", axis=1, inplace=True)
        
    # Merge pupil fixations to output_data
    if "pupil_timestamp" in output_data.columns:
    
        # Drop rows with pupil_timestamp = Nan
        output_data = output_data.dropna(subset=['pupil_timestamp'])
        pupil_fixations_data = pupil_fixations_data.dropna(subset=['start_timestamp'])

        # Sort both DataFrames by the pupil_timestamp columns
        output_data = output_data.sort_values('pupil_timestamp')
        pupil_fixations_data = pupil_fixations_data.sort_values('start_timestamp')

        # Merge output_data with pupil_fixations_data using the pupil_timestamp column where the timestamp is between start_timestamp and end_timestamp of the fixation data
        output_data = pd.merge_asof(output_data, pupil_fixations_data, left_on='pupil_timestamp', right_on='start_timestamp', direction='backward')
        # output_data[((output_data['pupil_timestamp'] < output_data['start_timestamp']) | \
        #               (output_data['pupil_timestamp'] > output_data['end_timestamp']))].loc[:, list(pupil_fixations_data.columns)] = np.nan
        output_data.loc[((output_data['pupil_timestamp'] < output_data['start_timestamp']) | (output_data['pupil_timestamp'] > output_data['end_timestamp'])), 
                        list(pupil_fixations_data.columns)] = np.nan

        output_data = output_data.reset_index(drop=True)

    # Drop unnamed columns
    output_data = output_data.loc[:, ~output_data.columns.str.contains('^Unnamed')]

    # Drop 'world_index' and 'index' columns
    output_data = output_data.drop(columns=['world_index', 'index'])

    # Drop rows with nan in columns: HR, EDA, light, EKG
    output_data = output_data.dropna(subset=['HR', 'EDA', 'light', 'EKG'])
    
    # Drop records without trigger or valence or arousal values
    output_data.dropna(subset=['trigger'], inplace=True)
    output_data.dropna(subset=['valence_rating'], inplace=True)
    output_data.dropna(subset=['arousal_rating'], inplace=True)
    
    # Add user_id column
    output_data['user_id'] = user_id
    
    # Add categorised_rating column
    output_data['categorised_rating'] = output_data.apply(lambda x: categorise_rating(x['valence_rating'], x['arousal_rating']), axis=1)
    
    # Add addtional features
    output_data = calculate_addtional_features(output_data, time_window=time_window)
    
    # go back to the original index and drop all timestamps 
    # (with pupil_timestamp as type timestamp there is a problem during conversition to parquet:
    # Casting from timestamp[ns] to timestamp[us] would lose data: 147171446999)
    output_data.reset_index(inplace=True)
    output_data.drop(labels=['pupil_timestamp', 'start_timestamp', 'end_timestamp'], axis=1, inplace=True)
    
    # Use only small_data_percentage of the data
    if sample_size is not None:
        data_sample = output_data.sample(n=sample_size, random_state=RANDOM_SEED)
    else:
        data_sample = output_data
    
    # Join output_data to all_data dataframe
    if all_users_data is None:
        all_users_data = data_sample.copy()
    else:
        all_users_data = pd.concat([all_users_data, data_sample], ignore_index=True)
        
    # Save to csv
    output_data.to_parquet(os.path.join(MERGED_DATA_PATH, f"{user_id}_data.parquet"))
    
    return all_users_data

if __name__ == "__main__":
    if not os.path.exists(MERGED_DATA_PATH):
        os.makedirs(MERGED_DATA_PATH)
    
    users = get_subjects_list(SUBJECTS_INFO_PATH)
    
    with open ("merging_errors.txt", "w+") as f:
        all_users_data = None
        sample_size = None
        for user in users:
            try:
                print(f"Merging data for user: {user}")
                all_users_data = join_all_data(user, DATA_PATHS, all_users_data, sample_size)
            except Exception as e:
                msg = f"Error while merging data for user {user}: {e}\n"
                f.write(msg)
                print(msg)
                continue
            
        # save all_data to parquet
        all_users_data.to_parquet(os.path.join(MERGED_DATA_PATH, "all_users_data.parquet"))
        
    print("Done!")
    
# group df by user_id and count number of records