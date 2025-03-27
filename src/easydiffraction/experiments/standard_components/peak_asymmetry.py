from typing import Optional, Type
from easydiffraction.core.parameter import Parameter
from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.utils.formatting import warning


class PeakAsymmBase(StandardComponentBase):
    """
    Base class for peak asymmetry components.

    This class serves as a foundation for different peak asymmetry models,
    ensuring common properties and behavior.
    """
    cif_category_name = "_peak_asymm"

    def __init__(self, diffr_mode: Optional[str] = None, expt_mode: Optional[str] = None, *args, **kwargs) -> None:
        """
        Initializes the base class for peak asymmetry.

        Args:
            diffr_mode (Optional[str]): The diffraction mode (e.g., 'powder', 'single_crystal').
            expt_mode (Optional[str]): The experiment mode (e.g., 'constant_wavelength', 'time_of_flight').
        """
        super().__init__(*args, **kwargs)
        self._type: Optional[str] = None
        self._diffr_mode: Optional[str] = diffr_mode  # Store diffraction mode privately
        self._expt_mode: Optional[str] = expt_mode  # Store experiment mode privately

    @property
    def type(self) -> Optional[str]:
        """
        Returns the type of peak asymmetry.

        Returns:
            Optional[str]: The peak asymmetry type.
        """
        return self._type

    @type.setter
    def type(self, new_type: str) -> None:
        """
        Updates the peak asymmetry type dynamically while ensuring private attributes persist.

        Args:
            new_type (str): New peak asymmetry type.
        """
        new_instance = PeakAsymmetryFactory.create(self._diffr_mode, self._expt_mode, new_type)
        if new_instance:
            # Preserve private attributes
            new_instance._diffr_mode = self._diffr_mode
            new_instance._expt_mode = self._expt_mode

            # Remove all non-private attributes
            for key in list(self.__dict__.keys()):
                if not key.startswith("_"):
                    del self.__dict__[key]

            # Update attributes from the new instance
            for key, value in new_instance.__dict__.items():
                setattr(self, key, value)

            self._type = new_type  # Explicitly update type


class PeakAsymmEmpirConstWavelength(PeakAsymmBase):
    """
    Peak asymmetry model for empirical constant wavelength.

    This model includes parameters for empirical peak asymmetry.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the empirical constant wavelength peak asymmetry model.
        """
        super().__init__(*args, **kwargs)
        self._type = "empirical"
        self.asy_1: Parameter = Parameter(
            value=0.0,
            cif_name="asy_1"
        )
        self.asy_2: Parameter = Parameter(
            value=0.0,
            cif_name="asy_2"
        )
        self.asy_3: Parameter = Parameter(
            value=0.0,
            cif_name="asy_3"
        )
        self.asy_4: Parameter = Parameter(
            value=0.0,
            cif_name="asy_4"
        )


class PeakAsymmFingerConstWavelength(PeakAsymmBase):
    """
    Peak asymmetry model using Finger's formulation for constant wavelength.

    This model implements the L. Finger formulation for axial divergence.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the Finger's constant wavelength peak asymmetry model.
        """
        super().__init__(*args, **kwargs)
        self._type = "finger"
        self.s_l: Parameter = Parameter(
            value=0.0,
            cif_name="s_l"
        )
        self.d_l: Parameter = Parameter(
            value=0.0,
            cif_name="d_l"
        )


class PeakAsymmTimeOfFlight(PeakAsymmBase):
    """
    Peak asymmetry model for time-of-flight experiments.

    This model includes parameters specific to TOF peak asymmetry.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes the time-of-flight peak asymmetry model.
        """
        super().__init__(*args, **kwargs)
        self._type = "finger"
        self.alpha_0: Parameter = Parameter(
            value=0.0,
            cif_name="alpha_0"
        )
        self.alpha_1: Parameter = Parameter(
            value=0.0,
            cif_name="alpha_1"
        )


class PeakAsymmetryFactory:
    """
    Factory class for creating peak asymmetry instances based on experiment mode.

    This factory determines which peak asymmetry model should be used
    based on diffraction mode and experiment type.
    """

    _peak_asymm_classes = {
        "constant_wavelength": {
            "default": PeakAsymmEmpirConstWavelength,
            "empirical": PeakAsymmEmpirConstWavelength,
            "finger": PeakAsymmFingerConstWavelength,
        },
        "time_of_flight": {
            "default": PeakAsymmTimeOfFlight,
            "finger": PeakAsymmTimeOfFlight,
        }
    }

    @staticmethod
    def create(diffr_mode: str, expt_mode: str, asymm_type: str = 'default') -> Optional[PeakAsymmBase]:
        """
        Creates a peak asymmetry instance based on diffraction mode and experiment mode.

        Args:
            diffr_mode (str): Diffraction mode ('powder', 'single_crystal', etc.).
            expt_mode (str): Experiment mode ('constant_wavelength', 'time_of_flight').
            asymm_type (str): Type of peak asymmetry (default: 'default').

        Returns:
            Optional[PeakAsymmBase]: An instance of the appropriate peak asymmetry class,
                                     or None if peak asymmetry is not applicable.
        """

        # Peak asymmetry is only applicable to 'powder' diffraction mode
        if diffr_mode != "powder":
            print(warning(f"Peak asymmetry is not supported for diffraction mode '{diffr_mode}'. It will not be created."))
            return None  # Ensure peak_asymm attribute is not added

        peak_asymm_class = PeakAsymmetryFactory.get_class(expt_mode, asymm_type)
        if not peak_asymm_class:
            print(warning(f"No valid peak asymmetry class found for experiment mode '{expt_mode}' with asymmetry type '{asymm_type}'"))
            return None

        return peak_asymm_class(diffr_mode=diffr_mode, expt_mode=expt_mode)  # Instantiate the class

    @staticmethod
    def get_class(expt_mode: str, asymm_type: str) -> Optional[Type[PeakAsymmBase]]:
        """
        Retrieves the appropriate peak asymmetry class based on experiment mode and type.

        Args:
            expt_mode (str): The experiment mode.
            asymm_type (str): The peak asymmetry type.

        Returns:
            Optional[Type[PeakAsymmBase]]: The corresponding peak asymmetry class, or None if not found.
        """
        return PeakAsymmetryFactory._peak_asymm_classes.get(expt_mode, {}).get(asymm_type, None)