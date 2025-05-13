import os
import pandas as pd

from ..preprocessing.config import SUBJECTS_INFO_PATH, \
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

DATA_DIRECTORY = BITALINO_PATH

aggregated_df = pd.DataFrame(columns=['lp', 'EKG', 'light', 'blank', 'EDA', 'HR', 'trigger']).set_index("trigger").drop(labels="lp", axis=1)

files = os.listdir(DATA_DIRECTORY)

counter = 1
for file in files:
    read_df = pd.read_csv(DATA_DIRECTORY + file).drop(labels=["lp"], axis=1).groupby(by="trigger").mean()
    aggregated_df = pd.concat([aggregated_df, read_df])
    print(f"{counter} of {len(files)}"),
    counter += 1

aggregated_df.to_csv("all_users_means_concatenated.csv")

aggregated_by_trigger = aggregated_df.groupby(by="trigger").mean()
aggregated_by_trigger.to_csv("all_users_grouped_by_triggers.csv")