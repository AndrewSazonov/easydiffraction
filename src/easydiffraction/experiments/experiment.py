import os.path

import numpy as np
from abc import ABC, abstractmethod
from typing import Union

from easydiffraction.experiments.standard_components.type import ExperimentType
from easydiffraction.experiments.standard_components.instrument import InstrumentFactory
from easydiffraction.experiments.standard_components.peak import PeakFactory

from easydiffraction.experiments.iterable_components.linked_phases import LinkedPhases
from easydiffraction.experiments.iterable_components.background import BackgroundFactory
from easydiffraction.experiments.iterable_components.datastore import DatastoreFactory

from easydiffraction.utils.formatting import paragraph
from easydiffraction.utils.chart_plotter import ChartPlotter


class BaseExperiment(ABC):
    """Base class for all experiments with only core attributes."""

    def __init__(self,
                 id: str,
                 type: ExperimentType):
        self.id = id
        self.type = type
        self.instrument = InstrumentFactory.create(beam_mode=self.type.beam_mode.value)
        self.datastore = DatastoreFactory.create(sample_form=self.type.sample_form.value,
                                                 experiment=self)

    def as_cif(self, max_points=None):
        """
        Generate CIF content by collecting values from all components.
        """
        lines = [f"data_{self.id}"]

        # Experiment type
        if hasattr(self, "type"):
            lines.append("")
            lines.append(self.type.as_cif())

        # Instrument setup and calibration
        if hasattr(self, "instrument"):
            lines.append("")
            lines.append(self.instrument.as_cif())

        # Peak profile, broadening and asymmetry
        if hasattr(self, "peak"):
            lines.append("")
            lines.append(self.peak.as_cif())

        # Phase scale factors for powder experiments
        if hasattr(self, "linked_phases"):
            lines.append("")
            lines.append(self.linked_phases.as_cif())

        # Crystal scale factor for single crystal experiments
        if hasattr(self, "linked_crystal"):
            lines.append("")
            lines.append(self.linked_crystal.as_cif())

        # Background points
        # TODO: This functionality should be moved to background.py
        if hasattr(self, "background") and hasattr(self.background, "points") and self.background.points:
            lines.append("")
            lines.append("loop_")
            category = '_pd_background'  # TODO: Add category to background component
            attributes = ('line_segment_X', 'line_segment_intensity')
            for attribute in attributes:
                lines.append(f"{category}.{attribute}")
            for point in self.background.points:
                x = point[0]
                y = point[1]
                lines.append(f"{x} {y}")

        # Measured data
        # TODO: This functionality should be moved to datastore.py
        # TODO: We need meas_data component which will use datastore to extract data
        # TODO: Datastore should be moved out of iterable_components/
        if hasattr(self, "datastore") and hasattr(self.datastore, "pattern"):
            lines.append("")
            lines.append("loop_")
            category = '_pd_meas'  # TODO: Add category to pattern component
            attributes = ('2theta_scan', 'intensity_total', 'intensity_total_su')
            for attribute in attributes:
                lines.append(f"{category}.{attribute}")
            pattern = self.datastore.pattern
            if max_points is not None and len(pattern.x) > 2 * max_points:
                for i in range(max_points):
                    x = pattern.x[i]
                    meas = pattern.meas[i]
                    meas_su = pattern.meas_su[i]
                    lines.append(f"{x} {meas} {meas_su}")
                lines.append("...")
                for i in range(-max_points, 0):
                    x = pattern.x[i]
                    meas = pattern.meas[i]
                    meas_su = pattern.meas_su[i]
                    lines.append(f"{x} {meas} {meas_su}")
            else:
                for x, meas, meas_su in zip(pattern.x, pattern.meas, pattern.meas_su):
                    lines.append(f"{x} {meas} {meas_su}")

        return "\n".join(lines)

    def show_as_cif(self):
        cif_text = self.as_cif(max_points=5)
        lines = cif_text.splitlines()
        max_width = max(len(line) for line in lines)
        padded_lines = [f"│ {line.ljust(max_width)} │" for line in lines]
        top = f"╒{'═' * (max_width + 2)}╕"
        bottom = f"╘{'═' * (max_width + 2)}╛"

        print(paragraph(f"Experiment 🔬 '{self.id}' as cif"))
        print(top)
        print("\n".join(padded_lines))
        print(bottom)

    @abstractmethod
    def show_meas_chart(self, x_min=None, x_max=None):
        """
        Abstract method to display data chart. Should be implemented in specific experiment mixins.
        """
        raise NotImplementedError("show_meas_chart() must be implemented in the subclass")

class PowderExperiment(BaseExperiment):
    """Powder experiment class with specific attributes."""

    def __init__(self,
                 id: str,
                 type: ExperimentType):
        super().__init__(id=id,
                         type=type)
        self.peak = PeakFactory.create(beam_mode=self.type.beam_mode.value)
        self.linked_phases = LinkedPhases()
        self.background = BackgroundFactory.create_background("point")

    def _load_ascii_data_to_experiment(self, data_path):
        """
        Loads x, y, sy values from an ASCII data file into the experiment.

        The file must be structured as:
            x  y  sy
        """
        try:
            data = np.loadtxt(data_path)
        except Exception as e:
            raise IOError(f"Failed to read data from {data_path}: {e}")

        if data.shape[1] < 2:
            raise ValueError("Data file must have at least two columns: x and y.")

        if data.shape[1] < 3:
            print("Warning: No uncertainty (sy) column provided. Defaulting to sqrt(y).")

        # Extract x, y, and sy data
        x = data[:, 0]
        y = data[:, 1]
        sy = data[:, 2] if data.shape[1] > 2 else np.sqrt(y)

        # Attach the data to the experiment's datastore
        self.datastore.pattern.x = x
        self.datastore.pattern.meas = y
        self.datastore.pattern.meas_su = sy

        print(paragraph("Data loaded successfully"))
        print(f"Experiment 🔬 '{self.id}'. Number of data points: {len(x)}")

    def show_meas_chart(self, x_min=None, x_max=None):
        pattern = self.datastore.pattern

        if pattern.meas is None or pattern.x is None:
            print(f"No measured data available for experiment {self.id}")
            return

        plotter = ChartPlotter()
        plotter.plot(
            y_values_list=[pattern.meas],
            x_values=pattern.x,
            x_min=x_min,
            x_max=x_max,
            title=paragraph(f"Measured data for experiment 🔬 '{self.id}'"),
            labels=['meas']
        )


class SingleCrystalExperiment(BaseExperiment):
    """Powder experiment class with specific attributes."""

    def __init__(self,
                 id: str,
                 type: ExperimentType):
        super().__init__(id=id,
                         type=type)
        self.linked_crystal = None

    def show_meas_chart(self):
        print('Showing measured data chart is not implemented yet.')


class ExperimentFactory:
    """Creates Experiment instances with only relevant attributes."""
    _supported_classes = {
        "powder": PowderExperiment,
        "single crystal": SingleCrystalExperiment
    }

    @staticmethod
    def create(
            id: str,
            sample_form: str,
            beam_mode: str,
            radiation_probe: str
    ) -> Union[PowderExperiment, SingleCrystalExperiment]:
        """Dynamically creates an Experiment instance with relevant attributes."""
        expt_class = ExperimentFactory._supported_classes.get(sample_form)
        expt_type = ExperimentType(sample_form=sample_form,
                                   beam_mode=beam_mode,
                                   radiation_probe=radiation_probe)
        expt_class_obj = expt_class(id=id,
                                    type=expt_type)
        return expt_class_obj


# User exposed API for convenience
# TODO: Refactor based on the implementation of method add() in class Experiments
# TODO: Think of where to keep default values for sample_form, beam_mode, radiation_probe, as they are also defined in the
#  class ExperimentType
def Experiment(id: str,
               sample_form: str = "powder",
               beam_mode: str = "constant wavelength",
               radiation_probe: str = "neutron",
               data_path: str = None):
    experiment = ExperimentFactory.create(
        id=id,
        sample_form=sample_form,
        beam_mode=beam_mode,
        radiation_probe=radiation_probe
    )
    experiment._load_ascii_data_to_experiment(data_path)
    return experiment
