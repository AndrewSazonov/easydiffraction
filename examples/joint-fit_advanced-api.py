"""
Joint Refinement Example (Advanced API)

This example demonstrates a more flexible and advanced usage of the EasyDiffraction
library by explicitly creating and configuring some objects. It is more suitable for
users comfortable with Python programming and those interested in custom workflows.
"""

from easydiffraction import (
    Project,
    SampleModel,
    Experiment
)

# Create and configure sample model

model = SampleModel("pbso4")
model.space_group.name.value = "P n m a"
model.cell.length_a.value = 8.5
model.cell.length_b.value = 5.35
model.cell.length_c.value = 6.9
model.atom_sites.add("Pb", "Pb", 0.1876, 0.25, 0.167, b_iso=1.37)
model.atom_sites.add("S", "S", 0.0654, 0.25, 0.684, b_iso=0.3777)
model.atom_sites.add("O1", "O", 0.9082, 0.25, 0.5954, b_iso=1.9764)
model.atom_sites.add("O2", "O", 0.1935, 0.25, 0.5432, b_iso=1.4456)
model.atom_sites.add("O3", "O", 0.0811, 0.0272, 0.8086, b_iso=1.2822)

# Create and configure experiments

# Experiment 1: Neutron powder diffraction
expt1 = Experiment(id="npd", radiation_probe="neutron", data_path="examples/data/pbso4_powder_neutron_cw.dat")
expt1.instrument.setup_wavelength = 1.91
expt1.instrument.calib_twotheta_offset = -0.1406
expt1.peak.broad_gauss_u = 0.139
expt1.peak.broad_gauss_v = -0.412
expt1.peak.broad_gauss_w = 0.386
expt1.peak.broad_lorentz_x = 0
expt1.peak.broad_lorentz_y = 0.088
expt1.linked_phases.add("pbso4", scale=1.0)
expt1.background_type = "line-segment"
for x, y in [
    (11.0, 206.1624),
    (15.0, 194.75),
    (20.0, 194.505),
    (30.0, 188.4375),
    (50.0, 207.7633),
    (70.0, 201.7002),
    (120.0, 244.4525),
    (153.0, 226.0595),
]:
    expt1.background.add(x, y)

# Experiment 2: X-ray powder diffraction
expt2 = Experiment(id="xrd", radiation_probe="xray", data_path="examples/data/pbso4_powder_xray.dat")
expt2.instrument.setup_wavelength = 1.540567
expt2.instrument.calib_twotheta_offset = -0.05181
expt2.peak.broad_gauss_u = 0.304138
expt2.peak.broad_gauss_v = -0.112622
expt2.peak.broad_gauss_w = 0.021272
expt2.peak.broad_lorentz_x = 0
expt2.peak.broad_lorentz_y = 0.057691
expt2.linked_phases.add("pbso4", scale=0.005)
expt2.background_type = "chebyshev polynomial"
for x, y in [
    (0, 119.195),
    (1, 6.221),
    (2, -45.725),
    (3, 8.119),
    (4, 54.552),
    (5, -20.661),
]:
    expt2.background.add(x, y)

# Create project and add sample model and experiments
project = Project()
project.sample_models.add(model)
project.experiments.add(expt1)
project.experiments.add(expt2)

# Set calculator, minimizer and refinement strategy
project.analysis.current_calculator = "crysfml"
project.analysis.current_minimizer = "lmfit (leastsq)"
project.analysis.fit_mode = 'joint'

# Define free parameters
model.cell.length_a.free = True
model.cell.length_b.free = True
model.cell.length_c.free = True
expt1.linked_phases["pbso4"].scale.free = True
expt2.linked_phases["pbso4"].scale.free = True

# Run refinement
project.analysis.fit()

