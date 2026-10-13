The .zip file contains data related to the NMR study on hydrated silicate ionic liquids (doi: to be added).

Contents:

folder **exp-spectra**:

_*.txt_ files containing the 23Na and 133Cs NMR spectra at each water loading. Titles of the file are: _(isotope)-(spectrum number)-(cation mole fraction).txt_

folder **structural-datasets**:

Orca NMR calculation input file orca-input and folders high-xNa and low-xNa each containing the _*.xyz_ files of the clusters used for the NMR calculations on 23Na. Titles of the files are: _system(abcd label)-(system number).xyz_

folder **theory-spectra**:

Python scripts to plot filtered and unfiltered spectra _plt_filtered.py_ and _plt_unfiltered.py_. Folders **anisotropic** and **isotropic**: containing the contributions to the total spectra of each invidivual calculated cluster for both low and high concentration datasets. Folders in each of the low-xNa and high-xNa folders are named according to: **(abcd label)-(structure number)**. Folder **summed_spectra** contains then the total unfiltered (raw) and filtered spectra in the isotropic case (_*.dat_ files) as resulting from running the aforementioned Python scripts.
