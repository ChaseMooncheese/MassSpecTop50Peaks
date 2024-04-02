from pyteomics import mzxml
import os

# Specify the path to your mzXML file
print(os.getcwd())
file_path = "../data/ex.mzxml"

# Open the mzXML file for reading
with mzxml.read(file_path) as reader:
    # Iterate over each spectrum in the file
    for spectrum in reader:
        # Access the spectrum data
        mz_values = spectrum['m/z array']
        intensity_values = spectrum['intensity array']

print(mz_values)
print(intensity_values)
