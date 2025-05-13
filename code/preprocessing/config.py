import os
import sys

if sys.platform.startswith('win'):
    # Paths for Windows
    DRIVE_LETTER = "D:\\"
else:
    # Paths for WSL
    DRIVE_LETTER = "/mnt/d/"

SUBJECTS_INFO_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "keys", "participants_pic.xlsx")
BITALINO_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "physiology_bitalino", "bitalino_pic")
PUPIL_POSITIONS_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "pupillabs_exported", "pupillabs_pic", "positions")
PUPIL_FIXATIONS_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "pupillabs_exported", "pupillabs_pic", "fixations")
PUPIL_ANNOTATIONS_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "pupillabs_exported", "pupillabs_pic", "annotations")
PREPROCESSED_DATA_PATH = os.path.join(DRIVE_LETTER, "vr_project", "preprocessed_data")
MERGED_DATA_PATH = os.path.join(DRIVE_LETTER, "vr_project", "merged_data")
RATING_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "ratings")
DOCUMENTS_PATH = os.path.join(DRIVE_LETTER, "vr_project", "raw_data", "keys")

PREPROCESSED_BITALINO_PATH = os.path.join(PREPROCESSED_DATA_PATH, "bitalino")
PREPROCESSED_PUPIL_POSITIONS_PATH = os.path.join(PREPROCESSED_DATA_PATH, "positions")
PREPROCESSED_PUPIL_FIXATIONS_PATH = os.path.join(PREPROCESSED_DATA_PATH, "fixations")
PREPROCESSED_PUPIL_ANNOTATIONS_PATH = os.path.join(PREPROCESSED_DATA_PATH, "annotations")

DATA_PATHS = [BITALINO_PATH, PUPIL_POSITIONS_PATH, PUPIL_FIXATIONS_PATH, PUPIL_ANNOTATIONS_PATH]
ALL_DATA_PATHS = [
    BITALINO_PATH, PUPIL_POSITIONS_PATH, PUPIL_FIXATIONS_PATH, PUPIL_ANNOTATIONS_PATH,
    PREPROCESSED_DATA_PATH, PREPROCESSED_BITALINO_PATH, PREPROCESSED_PUPIL_FIXATIONS_PATH,
    PREPROCESSED_PUPIL_POSITIONS_PATH, PREPROCESSED_PUPIL_ANNOTATIONS_PATH
]

RANDOM_SEED = 44