from easydiffraction.experiments.experiment_base import BaseExperiment
from easydiffraction.experiments.experiment_mixins.powder_experiment import PowderExperimentMixin

# Component imports
from easydiffraction.experiments.standard_components.instrument_setup import (
    InstrSetupBase,
    InstrSetupConstWavelengthMixin,
    InstrSetupTimeOfFlightMixin,
)
from easydiffraction.experiments.standard_components.instrument_calibration import (
    InstrCalibBase,
    InstrCalibConstWavelengthMixin,
    InstrCalibTimeOfFlightMixin,
)
from easydiffraction.experiments.standard_components.peak_profile import (
    PeakProfileBase,
    PeakProfileConstWavelengthMixin,
    PeakProfileTimeOfFlightMixin,
)
from easydiffraction.experiments.standard_components.peak_broadening import PeakBroadFactory
from easydiffraction.experiments.standard_components.peak_asymmetry import PeakAsymmetryFactory
from easydiffraction.experiments.iterable_components.linked_phases import LinkedPhases
from easydiffraction.experiments.iterable_components.background import BackgroundFactory
from easydiffraction.experiments.iterable_components.datastore import DatastoreFactory


class ExperimentFactory:
    """Factory for creating dynamically assembled Experiment instances."""

    @staticmethod
    def create_experiment(id: str, diffr_mode: str, expt_mode: str, radiation_probe: str) -> BaseExperiment:
        """
        Creates a dynamically assembled Experiment instance based on diffraction mode,
        experiment mode, and radiation probe.

        Args:
            id (str): Identifier for the experiment.
            diffr_mode (str): Diffraction mode ('powder', 'single_crystal').
            expt_mode (str): Experiment mode ('constant_wavelength', 'time_of_flight').
            radiation_probe (str): Type of radiation probe used.

        Returns:
            BaseExperiment: A dynamically created Experiment instance.
        """
        # Collect experiment_mixins based on the experiment type
        experiment_mixins = []

        if diffr_mode == "powder":
            experiment_mixins.append(PowderExperimentMixin)
        elif diffr_mode == "single_crystal":
            raise NotImplementedError("Single crystal experiments are not yet supported.")

        # Create class bases. BaseExperiment comes last
        bases = tuple(experiment_mixins + [BaseExperiment])

        # Dynamically assemble class
        ExperimentCls = type(
            f"Experiment__{diffr_mode}__{expt_mode}__{radiation_probe}",
            bases,
            {}
        )

        # Create instance of dynamically assembled class
        instance = ExperimentCls(id=id,
                                 diffr_mode=diffr_mode,
                                 expt_mode=expt_mode,
                                 radiation_probe=radiation_probe)

        # Attach instrument setup and calibration components
        instance.instr_setup = ExperimentFactory._create_component(
            InstrSetupBase,
            ExperimentFactory._get_instr_setup_mixins(expt_mode),
            "InstrSetup"
        )
        instance.instr_calib = ExperimentFactory._create_component(
            InstrCalibBase,
            ExperimentFactory._get_instr_calib_mixins(expt_mode),
            "InstrCalib"
        )

        # Attach peak profile, broadening, and asymmetry components
        instance.peak_profile = ExperimentFactory._create_component(
            PeakProfileBase,
            ExperimentFactory._get_peak_profile_mixins(diffr_mode, expt_mode),
            "PeakProfile"
        )

        peak_broad = PeakBroadFactory.create(diffr_mode, expt_mode)
        if peak_broad is not None:
            instance.peak_broad = peak_broad
        peak_asymm = PeakAsymmetryFactory.create(diffr_mode, expt_mode)
        if peak_asymm is not None:
            instance.peak_asymm = peak_asymm

        # Attach a linked phases component
        instance.linked_phases = LinkedPhases()

        # Attach a background component
        instance.background = BackgroundFactory.create_background("point")

        # Attach a datastore component
        instance.datastore = DatastoreFactory.create_datastore(diffr_mode, instance)

        return instance

    @staticmethod
    def _create_component(base_cls, mixins, class_name):
        """
        Dynamically creates a component class with the given base class and mixins.

        Args:
            base_cls (class): Base component class.
            mixins (list): List of mixin classes.
            class_name (str): Name of the dynamically created class.

        Returns:
            object: An instance of the dynamically created component class.
        """
        if not mixins:
            return None
        bases = tuple([base_cls] + mixins)
        ComponentCls = type(class_name, bases, {})
        return ComponentCls()

    @staticmethod
    def _get_instr_setup_mixins(expt_mode: str) -> list:
        """
        Retrieves the appropriate mixins for instrument setup based on the experiment mode.

        Args:
            expt_mode (str): Experiment mode.

        Returns:
            list: List of mixin classes for instrument setup.
        """
        return {
            "constant_wavelength": [InstrSetupConstWavelengthMixin],
            "time_of_flight": [InstrSetupTimeOfFlightMixin]
        }.get(expt_mode, [])

    @staticmethod
    def _get_instr_calib_mixins(expt_mode: str) -> list:
        """
        Retrieves the appropriate mixins for instrument calibration based on the experiment mode.

        Args:
            expt_mode (str): Experiment mode.

        Returns:
            list: List of mixin classes for instrument calibration.
        """
        return {
            "constant_wavelength": [InstrCalibConstWavelengthMixin],
            "time_of_flight": [InstrCalibTimeOfFlightMixin]
        }.get(expt_mode, [])

    @staticmethod
    def _get_peak_profile_mixins(diffr_mode: str, expt_mode: str) -> list:
        """
        Retrieves the appropriate mixins for peak profile based on diffraction and experiment mode.

        Args:
            diffr_mode (str): Diffraction mode ('powder', 'single_crystal').
            expt_mode (str): Experiment mode.

        Returns:
            list: List of mixin classes for peak profile.
        """
        if diffr_mode != "powder":
            return []
        return {
            "constant_wavelength": [PeakProfileConstWavelengthMixin],
            "time_of_flight": [PeakProfileTimeOfFlightMixin]
        }.get(expt_mode, [])

    @staticmethod
    def _get_peak_broad_mixins(diffr_mode: str, expt_mode: str) -> list:
        """
        Retrieves the appropriate mixins for peak broadening based on diffraction and experiment mode.

        Args:
            diffr_mode (str): Diffraction mode ('powder', 'single_crystal').
            expt_mode (str): Experiment mode.

        Returns:
            list: List of mixin classes for peak broadening.
        """
        if diffr_mode != "powder":
            return []
        return {
            "constant_wavelength": [PeakBroadConstWavelengthMixin],
            "time_of_flight": [PeakBroadTimeOfFlightMixin]
        }.get(expt_mode, [])
