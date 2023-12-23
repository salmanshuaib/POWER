import os
import shutil
import glob
import sys

def clean_up_after_pyinstaller():
    # Delete .spec files
    for spec_file in glob.glob('*.spec'):
        os.remove(spec_file)
        print(f"Removed '{spec_file}' file.")

    # Delete build directory
    if os.path.exists('build'):
        shutil.rmtree('build')
        print("Removed 'build' directory.")

    # Check if dist directory exists
    if os.path.exists('dist'):
        # Find .exe files in dist directory
        exe_files = glob.glob('dist/*.exe')
        if exe_files:
            # Assuming only one .exe file, get its path
            exe_file = exe_files[0]
            print(f"You can now access the file '{exe_file}' from within the 'dist' folder.")
        else:
            print("No .exe file found in 'dist' directory.")
    else:
        print("'dist' directory does not exist.")

if len(sys.argv) > 1 and sys.argv[1] == 'pretty':
    clean_up_after_pyinstaller()
else:
    print("Usage: python LatentSupremacy.py pretty")
