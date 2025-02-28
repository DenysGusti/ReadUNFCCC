from pathlib import Path
import zipfile
# import shutil




def unzip_files(DATA_PATH):

    # Find all ZIP files in the directory
    zip_files = list(DATA_PATH.glob("*.zip"))

    for zip_file in zip_files:
        folder_name = DATA_PATH / Path('original') / zip_file.stem  # Create folder based on zip filename

        # Create the folder if it doesn't exist
        folder_name.mkdir(parents=True, exist_ok=True)

        # Extract ZIP contents
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(folder_name)

        print(f"Extracted {zip_file.name} into original/{folder_name.name}")

        # Move files from subfolders to main folder and remove empty subfolders
        move_files_up(folder_name)


def move_files_up(folder_path):
    """
    Moves files from subfolders to the main folder and deletes empty subfolders.
    """
    for subfolder in sorted(folder_path.rglob("*"), reverse=True):  # Bottom-up traversal
        if subfolder.is_dir():
            for file in subfolder.glob("*"):
                if file.is_file():
                    target_file = folder_path / file.name

                    # Avoid overwriting: Rename if necessary
                    counter = 1
                    while target_file.exists():
                        target_file = folder_path / f"{file.stem}_{counter}{file.suffix}"
                        counter += 1

                    file.rename(target_file)

            # Remove the now-empty subfolder
            subfolder.rmdir()

