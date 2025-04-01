from easydiffraction.utils.formatting import paragraph, warning
import tabulate

from easydiffraction.core.parameter import Parameter, Descriptor
from easydiffraction.core.component_base import StandardComponentBase


# --- Mixins ---
class ConstantWavelengthBroadeningMixin:
    def _add_constant_wavelength_broadening(self):
        self.broad_gauss_u: Parameter = Parameter(
            value=0.01,
            cif_name="broad_gauss_u",
            units="deg²",
            description="Gaussian broadening coefficient (dependent on sample size and instrument resolution)"
        )
        self.broad_gauss_v: Parameter = Parameter(
            value=-0.01,
            cif_name="broad_gauss_v",
            units="deg²",
            description="Gaussian broadening coefficient (instrumental broadening contribution)"
        )
        self.broad_gauss_w: Parameter = Parameter(
            value=0.02,
            cif_name="broad_gauss_w",
            units="deg²",
            description="Gaussian broadening coefficient (instrumental broadening contribution)"
        )
        self.broad_lorentz_x: Parameter = Parameter(
            value=0.0,
            cif_name="broad_lorentz_x",
            units="deg",
            description="Lorentzian broadening coefficient (dependent on sample strain effects)"
        )
        self.broad_lorentz_y: Parameter = Parameter(
            value=0.0,
            cif_name="broad_lorentz_y",
            units="deg",
            description="Lorentzian broadening coefficient (dependent on microstructural defects and strain)"
        )


class TimeOfFlightBroadeningMixin:
    def _add_time_of_flight_broadening(self):
        self.broad_gauss_sigma_0: Parameter = Parameter(0.0, "gauss_sigma_0", "µs²", "Gaussian broadening (instrument resolution)")
        self.broad_gauss_sigma_1: Parameter = Parameter(0.0, "gauss_sigma_1", "µs/Å", "Gaussian broadening (dependent on d-spacing)")
        self.broad_gauss_sigma_2: Parameter = Parameter(0.0, "gauss_sigma_2", "µs²/Å²", "Gaussian broadening (instrument-dependent)")
        self.broad_lorentz_gamma_0: Parameter = Parameter(0.0, "lorentz_gamma_0", "µs", "Lorentzian broadening (microstrain)")
        self.broad_lorentz_gamma_1: Parameter = Parameter(0.0, "lorentz_gamma_1", "µs/Å", "Lorentzian broadening (d-spacing dependent)")
        self.broad_lorentz_gamma_2: Parameter = Parameter(0.0, "lorentz_gamma_2", "µs²/Å²", "Lorentzian broadening (instrument-dependent)")


class EmpiricalAsymmetryMixin:
    def _add_empirical_asymmetry(self):
        self.asym_empir_1 = Parameter(0.1, "asym_empir_1", "", "Empirical asymmetry coefficient p1")
        self.asym_empir_2 = Parameter(0.2, "asym_empir_2", "", "Empirical asymmetry coefficient p2")
        self.asym_empir_3 = Parameter(0.3, "asym_empir_3", "", "Empirical asymmetry coefficient p3")
        self.asym_empir_4 = Parameter(0.4, "asym_empir_4", "", "Empirical asymmetry coefficient p4")


class FCJAsymmetryMixin:
    def _add_fcj_asymmetry(self):
        self.asym_fcj_1 = Parameter(0.01, "asym_fcj_1", "", "FCJ asymmetry coefficient 1")
        self.asym_fcj_2 = Parameter(0.02, "asym_fcj_2", "", "FCJ asymmetry coefficient 2")


class IkedaCarpenterAsymmetryMixin:
    def _add_ikeda_carpenter_asymmetry(self):
        self.asym_alpha_0 = Parameter(0.01, "asym_alpha_0", "", "Ikeda-Carpenter asymmetry parameter α₀")
        self.asym_alpha_1 = Parameter(0.02, "asym_alpha_1", "", "Ikeda-Carpenter asymmetry parameter α₁")

class PeakBase(StandardComponentBase):
    cif_category_name = "_peak"

class ConstantWavelengthPseudoVoigt(PeakBase, ConstantWavelengthBroadeningMixin):
    _description = "Pseudo-Voigt profile"
    def __init__(self):
        super().__init__()
        self._add_constant_wavelength_broadening()


class ConstantWavelengthSplitPseudoVoigt(PeakBase, ConstantWavelengthBroadeningMixin, EmpiricalAsymmetryMixin):
    _description = "Split pseudo-Voigt profile"
    def __init__(self):
        super().__init__()
        self._add_constant_wavelength_broadening()
        self._add_empirical_asymmetry()


class ConstantWavelengthThompsonCoxHastings(PeakBase, ConstantWavelengthBroadeningMixin, FCJAsymmetryMixin):
    _description = "Thompson-Cox-Hastings profile"
    def __init__(self):
        super().__init__()
        self._add_constant_wavelength_broadening()
        self._add_fcj_asymmetry()


class TimeOfFlightPseudoVoigt(PeakBase, TimeOfFlightBroadeningMixin):
    _description = "Pseudo-Voigt profile"
    def __init__(self):
        super().__init__()
        self._add_time_of_flight_broadening()


class TimeOfFlightIkedaCarpenter(PeakBase, TimeOfFlightBroadeningMixin, IkedaCarpenterAsymmetryMixin):
    _description = "Ikeda-Carpenter profile"
    def __init__(self):
        super().__init__()
        self._add_time_of_flight_broadening()
        self._add_ikeda_carpenter_asymmetry()


class TimeOfFlightPseudoVoigtIkedaCarpenter(PeakBase, TimeOfFlightBroadeningMixin, IkedaCarpenterAsymmetryMixin):
    _description = "Pseudo-Voigt * Ikeda-Carpenter profile"
    def __init__(self):
        super().__init__()
        self._add_time_of_flight_broadening()
        self._add_ikeda_carpenter_asymmetry()


class TimeOfFlightPseudoVoigtBackToBackExponential(PeakBase, TimeOfFlightBroadeningMixin, IkedaCarpenterAsymmetryMixin):
    _description = "Pseudo-Voigt * Back-to-Back Exponential profile"
    def __init__(self):
        super().__init__()
        self._add_time_of_flight_broadening()
        self._add_ikeda_carpenter_asymmetry()


# --- Peak Controller ---
class PeakController:
    def __init__(self, beam_mode: str, profile_type: str = None):
        self._locked = False  # Unlock during initialization
        self._beam_mode = beam_mode
        self._supported_profiles = PeakFactory._supported_profiles[beam_mode]
        if profile_type is None:
            profile_type = next(iter(self._supported_profiles))
        self._profile_type = Descriptor(profile_type, cif_name="profile_typ", description="Selected peak profile")
        self._profile_instance = self._create_profile(profile_type)
        self._locked = True  # Lock after setup

    def __setattr__(self, name, value):
        if hasattr(self, "_locked") and self._locked:
            if not hasattr(self, name):
                raise AttributeError(f"Cannot add new attribute '{name}' to locked instance of '{self.__class__.__name__}'")

        current = getattr(self, name, None)
        if isinstance(current, Parameter):
            current.value = value
        else:
            super().__setattr__(name, value)

    def __getattr__(self, name):
        profile = self.__dict__.get("_profile_instance", None)
        if profile:
            return getattr(profile, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _create_profile(self, profile_type):
        cls = self._supported_profiles[profile_type]
        return cls()

    @property
    def profile_type(self):
        return self._profile_type.value

    @profile_type.setter
    def profile_type(self, new_type: str):
        if new_type not in self._supported_profiles:
            print(warning(f"Unknown peak profile '{new_type}'"))
            return
        self._profile_type.value = new_type
        self._profile_instance = self._create_profile(new_type)
        print(paragraph("Current peak profile changed to"))
        print(new_type)

    def show_supported_profiles(self):
        table = [
            [name, cls._description]
            for name, cls in self._supported_profiles.items()
        ]
        print(paragraph("Supported peak profiles"))
        print(tabulate.tabulate(table, headers=["Name", "Description"], tablefmt="fancy_outline"))

    def show_current_profile(self):
        print(paragraph("Current peak profile"))
        print(self._profile_type.value)



# --- Factory ---
class PeakFactory:
    _supported_profiles = {
        "constant wavelength": {
            "pseudo-voigt": ConstantWavelengthPseudoVoigt,
            "split pseudo-voigt": ConstantWavelengthSplitPseudoVoigt,
            "thompson-cox-hastings": ConstantWavelengthThompsonCoxHastings
        },
        "time-of-flight": {
            "pseudo-voigt": TimeOfFlightPseudoVoigt,
            "ikeda-carpenter": TimeOfFlightIkedaCarpenter,
            "pseudo-voigt * ikeda-carpenter": TimeOfFlightPseudoVoigtIkedaCarpenter,
            "pseudo-voigt * back-to-back": TimeOfFlightPseudoVoigtBackToBackExponential
        }
    }

    @classmethod
    def create(cls, beam_mode, profile_type=None):
        return PeakController(beam_mode, profile_type)