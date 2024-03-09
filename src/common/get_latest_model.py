from datetime import datetime
import os

def get_latest_and_highest_score_model(models_folder):
    """
    This function iterates through a directory and returns a tuple containing:
      - The filename with the newest date (or the first filename if dates are equal)
      - The highest BLEU score found in any file

    Args:
        directory: Path to the directory containing the files

    Returns:
        A tuple containing the filename with the newest date and the highest BLEU score.
    """
    # Get all files in the models folder
    files = os.listdir(models_folder)
    
    # Filter only files
    files = [f for f in files if (os.path.isfile(os.path.join(models_folder, f)) and f[len(f) - 4: len(f)] == ".pth")]
    
    # Split each filename
    split_files = [f.split("_") for f in files]
    
    sorted_files = sorted(split_files, key=lambda x: (datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S.%f"), float(x[-1].split("-")[-1][:-4])), reverse=True)
    
    sorted_filenames = [os.path.join(models_folder, "_".join(f)) for f in sorted_files]
    
    return sorted_filenames[0]
