from bitalino_preprocessing import preprocess_bitalino
from pupil_positions_preprocessing import preprocess_pupil_positions
from pupil_fixations_preprocessing import preprocess_pupil_fixations
from pupil_annotations_preprocessing import preprocess_pupil_annotations
from data_merging import get_subjects_list, join_similar_data
import os

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
                    ALL_DATA_PATHS

def preprocess_all_data(user_id: str):
    
    preprocess_bitalino(
        join_similar_data(user_id, BITALINO_PATH)).to_csv(
            os.path.join(PREPROCESSED_BITALINO_PATH, f"{user_id}_bitalino.csv"))
    
    preprocess_pupil_positions(
        join_similar_data(user_id, PUPIL_POSITIONS_PATH)).to_csv(
            os.path.join(PREPROCESSED_PUPIL_POSITIONS_PATH, f"{user_id}_pupil_positions.csv"))
    
    preprocess_pupil_fixations(
        join_similar_data(user_id, PUPIL_FIXATIONS_PATH)).to_csv(
            os.path.join(PREPROCESSED_PUPIL_FIXATIONS_PATH, f"{user_id}_pupil_fixations.csv"))
    
    preprocess_pupil_annotations(
        join_similar_data(user_id, PUPIL_ANNOTATIONS_PATH)).to_csv(
            os.path.join(PREPROCESSED_PUPIL_ANNOTATIONS_PATH, f"{user_id}_pupil_annotations.csv"))

if __name__ == "__main__":
    for path in ALL_DATA_PATHS:
        if not os.path.exists(path):
            os.makedirs(path)

    users = get_subjects_list(SUBJECTS_INFO_PATH)

    with open ("preprocessing_errors.txt", "w+") as f:
        for user in users:
            try:
                print(f"Preprocessing user: {user}")
                preprocess_all_data(user)
            except Exception as e:
                msg = f"Error while preprocessing user {user}: {e}\n"
                f.write(msg)
                print(msg)
                continue