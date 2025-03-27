from typing import Optional, Type

from easydiffraction.core.parameter import Descriptor, Parameter
from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.utils.formatting import warning


class PeakBroadBase(StandardComponentBase):
    """
    Base class for peak broadening components.

    This class serves as a foundation for different peak broadening models,
    ensuring common properties and behavior.
    """
    cif_category_name: str = "_peak_broad"

    def __init__(self, *args, **kwargs):
        """
        Initializes the base class for peak broadening.

        Args:
            *args: Positional arguments for the base class.
            **kwargs: Keyword arguments for the base class.
        """
        super().__init__(*args, **kwargs)


class PeakBroadConstWavelength(PeakBroadBase):
    """
    Adds constant wavelength peak broadening parameters.

    This class defines parameters specific to constant wavelength peak broadening.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the constant wavelength peak broadening parameters.

        Args:
            *args: Positional arguments for the base class.
            **kwargs: Keyword arguments for the base class.
        """
        super().__init__(*args, **kwargs)
        self.gauss_u = Parameter(
            value=0.01,
            cif_name="gauss_u",
            units="deg²",
            description="Gaussian broadening coefficient (dependent on sample size and instrument resolution)"
        )
        self.gauss_v = Parameter(
            value=-0.01,
            cif_name="gauss_v",
            units="deg²",
            description="Gaussian broadening coefficient (instrumental broadening contribution)"
        )
        self.gauss_w = Parameter(
            value=0.02,
            cif_name="gauss_w",
            units="deg²",
            description="Gaussian broadening coefficient (instrumental broadening contribution)"
        )
        self.lorentz_x = Parameter(
            value=0.0,
            cif_name="lorentz_x",
            units="deg",
            description="Lorentzian broadening coefficient (dependent on sample strain effects)"
        )
        self.lorentz_y = Parameter(
            value=0.0,
            cif_name="lorentz_y",
            units="deg",
            description="Lorentzian broadening coefficient (dependent on microstructural defects and strain)"
        )
        self.mix_eta = Descriptor(
            value=0.0,
            cif_name="mix_eta",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian broadening (not refined directly, calculated from X and Y parameters)",
            editable=False
        )


class PeakBroadTimeOfFlight(PeakBroadBase):
    """
    Adds time-of-flight peak broadening parameters.

    This class defines parameters specific to time-of-flight peak broadening.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the time-of-flight peak broadening parameters.

        Args:
            *args: Positional arguments for the base class.
            **kwargs: Keyword arguments for the base class.
        """
        super().__init__(*args, **kwargs)
        self.gauss_sigma_0 = Parameter(
            value=0.0,
            cif_name="gauss_sigma_0",
            units="µs²",
            description="Gaussian broadening coefficient (instrumental resolution)"
        )
        self.gauss_sigma_1 = Parameter(
            value=0.0,
            cif_name="gauss_sigma_1",
            units="µs/Å",
            description="Gaussian broadening coefficient (dependent on d-spacing)"
        )
        self.gauss_sigma_2 = Parameter(
            value=0.0,
            cif_name="gauss_sigma_2",
            units="µs²/Å²",
            description="Gaussian broadening coefficient (instrument-dependent term)"
        )
        self.lorentz_gamma_0 = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_0",
            units="µs",
            description="Lorentzian broadening coefficient (dependent on microstrain effects)"
        )
        self.lorentz_gamma_1 = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_1",
            units="µs/Å",
            description="Lorentzian broadening coefficient (dependent on d-spacing)"
        )
        self.lorentz_gamma_2 = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_2",
            units="µs²/Å²",
            description="Lorentzian broadening coefficient (instrumental-dependent term)"
        )
        self.mix_beta_0 = Parameter(
            value=0.0,
            cif_name="mix_beta_0",
            units="deg",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
        )
        self.mix_beta_1 = Parameter(
            value=0.0,
            cif_name="mix_beta_1",
            units="deg",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
        )


class PeakBroadFactory:
    """
    Factory class for creating peak broadening instances based on experiment mode.

    This factory determines which peak broadening model should be used
    based on diffraction mode and experiment type.
    """

    _peak_broad_classes = {
        "constant_wavelength": PeakBroadConstWavelength,
        "time_of_flight": PeakBroadTimeOfFlight
    }

    @staticmethod
    def create(diffr_mode: str, expt_mode: str) -> Optional[PeakBroadBase]:
        """
        Creates a peak broadening instance based on diffraction mode and experiment mode.

        Args:
            diffr_mode (str): Diffraction mode ('powder', 'single_crystal', etc.).
            expt_mode (str): Experiment mode ('constant_wavelength', 'time_of_flight').

        Returns:
            Optional[PeakBroadBase]: An instance of the appropriate peak broadening class,
                                     or None if peak broadening is not applicable.
        """
        # Peak broadening is only applicable to 'powder' diffraction mode
        if diffr_mode != "powder":
            print(warning(f"Peak broadening is not supported for diffraction mode '{diffr_mode}'. It will not be created."))
            return None  # Ensure peak broadening attribute is not added

        peak_broad_class: Optional[Type[PeakBroadBase]] = PeakBroadFactory.get_class(expt_mode)
        if peak_broad_class is None:
            print(warning(f"No valid peak broadening class found for experiment mode '{expt_mode}'"))
            return None

        return peak_broad_class()  # Instantiate the class

    @staticmethod
    def get_class(expt_mode: str) -> Optional[Type[PeakBroadBase]]:
        """
        Retrieves the appropriate peak broadening class based on experiment mode.

        Args:
            expt_mode (str): The experiment mode.

        Returns:
            Optional[Type[PeakBroadBase]]: The corresponding peak broadening class, or None if not found.
        """
        return PeakBroadFactory._peak_broad_classes.get(expt_mode, None)