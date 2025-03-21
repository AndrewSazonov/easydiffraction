import easydiffraction as ed

# === Step 1: Create a Project ===

# Create a new project
project = ed.Project(project_id="JointDiffractionAnalysis")

# Set project metadata
project.info.title = "Joint CW/TOF Neutron Diffraction Analysis"
project.info.description = """
This project performs joint refinement of constant wavelength and 
time-of-flight neutron diffraction data for a polycrystalline sample.
"""

# Show project metadata
print(project.info.as_cif())

# Save the initial project (directory must exist)
# project.save_as("projects/my_diffraction_project")

# === Step 2: Add Sample Models ===

# Create a model with default parameters
model1 = ed.SampleModel(id="pbso4")

# Change some parameters from default
model1.space_group.name = "P n m a"

# Add model to collection of sample models in the project
project.sample_models.add(model1)

# Show model IDs to be used for accessing the model via project.sample_models["model_id"]
project.sample_models.show_ids()

# Show model parameters
#project.sample_models["model1"].show_params()

# Modify parameters via project object
project.sample_models["pbso4"].cell.length_a.value = 8.46924
project.sample_models["pbso4"].cell.length_b.value = 5.391
project.sample_models["pbso4"].cell.length_c.value = 6.9506
project.sample_models["pbso4"].atom_sites.add(label='Pb',
                                             type_symbol='Pb',
                                             fract_x=0.1876,
                                             fract_y=0.25,
                                             fract_z=0.167)

# Modify parameters via model object (same object reference)
model1.atom_sites.add(label='S',
                      type_symbol='S',
                      fract_x=0.0654,
                      fract_y=0.25,
                      fract_z=0.684)
model1.atom_sites.add(label='O1',
                      type_symbol='O',
                      fract_x=0.9082,
                      fract_y=0.25,
                      fract_z=0.5954)
model1.atom_sites.add(label='O2',
                      type_symbol='O',
                      fract_x=0.1935,
                      fract_y=0.25,
                      fract_z=0.5432)
model1.atom_sites.add(label='O3',
                      type_symbol='O',
                      fract_x=0.0811,
                      fract_y=0.0272,
                      fract_z=0.8086)

# Show model as CIF string
print(project.sample_models["pbso4"].as_cif())

# Show sample model structure
#project.sample_models["pbso4"].show_structure(plane='xy')


print("\n")

# === Step 3: Add Experiments (Measurements) ===


# Create a virtual experiment (no measured data) with default parameters

# Create an experiment dynamically
#expt1 = ed.Experiment(
#    id="expt1",
#    diffr_mode="powder", # "powder" or "single_crystal"
#    expt_mode="constant_wavelength", # "time_of_flight" or "constant_wavelength"
#    radiation_probe="neutron" # "neutron" or "xray"
#)

# Load real experiment (including measured data) with default parameters

# Create an experiment dynamically
expt1 = ed.Experiment(
    id="expt1",
    diffr_mode="powder", # "powder" or "single_crystal"
    expt_mode="constant_wavelength", # "time_of_flight" or "constant_wavelength"
    radiation_probe="neutron", # "neutron" or "xray"
    data_path="data/pbso4_powder_neutron_cw.dat" # Path to ASCII data file (x, y, sy)
)

# Show experiment with default parameters as CIF string
print(expt1.as_cif())

# Show measured data
expt1.show_meas_chart(x_min=62, x_max=66)

# Modify experiment parameters directly on the experiment object
expt1.instr_setup.wavelength = 1.91

# Add experiment to collection of experiments in the project
project.experiments.add(expt1)

# Show defined experiments
project.experiments.show_ids()




# Modify experiment parameters via project object and experiment ID
project.experiments["expt1"].instr_calib.twotheta_offset = -0.1406

project.experiments["expt1"].peak_broad.gauss_u = 0.139
project.experiments["expt1"].peak_broad.gauss_v = -0.412
project.experiments["expt1"].peak_broad.gauss_w = 0.386
project.experiments["expt1"].peak_broad.lorentz_x = 0
project.experiments["expt1"].peak_broad.lorentz_y = 0.088


# Show experiment as CIF string. Now via the project object
print(project.experiments["expt1"].as_cif())




# === Step 4: Analysis ===

project.analysis.show_available_calculators()

project.analysis.set_calculator_by_name('cryspy')


# Preview calculated patterns
project.analysis.show_calc_chart("expt1", x_min=62, x_max=66)

# Compare measured vs calculated patterns
project.analysis.show_meas_vs_calc_chart("expt1", x_min=62, x_max=66)


# add background points
project.experiments["expt1"].background.add(x=11.0, y=206.0)
project.experiments["expt1"].background.add(x=153.0, y=226.1)

# Show measured vs calculated data uncluding background
project.analysis.show_meas_vs_calc_chart("expt1", x_min=62, x_max=66)

print('AAA')

# Show all refinable parameters
project.analysis.show_refinable_params()

print('BBB')

project.analysis.show_free_params()

print('CCC')



# Select specific parameters for refinement
project.sample_models["pbso4"].cell.length_a.value = 8.4
project.sample_models["pbso4"].cell.length_a.free = True
#project.sample_models["pbso4"].atom_sites["Pb"].fract_x.free = True
#project.experiments["expt1"].peak_broad.gauss_u.free = True

project.analysis.show_refinable_params()


project.analysis.show_free_params()



#exit()


# Set refinement strategy


# Preview calculated patterns vs measured data
#project.analysis.show_meas_vs_calc_chart("expt1")


project.analysis.show_meas_vs_calc_chart("expt1", x_min=62, x_max=66)
project.analysis.show_available_minimizers()
project.analysis.show_current_minimizer()
project.analysis.current_minimizer = 'lmfit (least_squares)'
project.analysis.show_current_minimizer()

project.analysis.refinement_strategy = 'single'
#print(project.analysis.describe_refinement_strategy())
project.analysis.fit()


# Show results after fitting
project.analysis.show_fit_results()

exit()

project.analysis.show_meas_vs_calc_chart("expt1", x_min=62, x_max=66)



# Change minimizer, and start fitting again

project.sample_models["pbso4"].cell.length_a.value = 8.4
project.analysis.current_minimizer = 'dfols'
project.analysis.show_current_minimizer()
project.analysis.fit()
project.analysis.show_fit_results()
project.analysis.show_meas_vs_calc_chart("expt1", x_min=62, x_max=66)


# === Step 5: Summary & Save ===
# Generate final report (HTML or CIF)
#project.summary.show_report()

# Save the final state of the project
#project.save()

#print("Analysis completed successfully!")