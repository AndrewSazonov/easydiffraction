import tabulate

from easydiffraction.utils.formatting import paragraph, warning
from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.core.parameter import Parameter, Descriptor

class Broadening:
    """Encapsulates all possible peak broadening parameters as attributes."""

    def __init__(self):
        # Constant wavelength specific parameters
        self.broad_gauss_u: Parameter = Parameter(
            value=0.0333,
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
            cif_name="gauss_w",  # TODO: fix name
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
        self.broad_mix_eta: Descriptor = Descriptor(
            value=0.0,
            cif_name="broad_mix_eta",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian broadening (not refined directly, calculated from X and Y parameters)",
            editable=False
        )

        # Time-of-flight specific parameters
        self.broad_gauss_sigma_0: Parameter = Parameter(
            value=0.0,
            cif_name="gauss_sigma_0",
            units="µs²",
            description="Gaussian broadening coefficient (instrumental resolution)"
        )
        self.broad_gauss_sigma_1: Parameter = Parameter(
            value=0.0,
            cif_name="gauss_sigma_1",
            units="µs/Å",
            description="Gaussian broadening coefficient (dependent on d-spacing)"
        )
        self.broad_gauss_sigma_2: Parameter = Parameter(
            value=0.0,
            cif_name="gauss_sigma_2",
            units="µs²/Å²",
            description="Gaussian broadening coefficient (instrument-dependent term)"
        )
        self.broad_lorentz_gamma_0: Parameter = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_0",
            units="µs",
            description="Lorentzian broadening coefficient (dependent on microstrain effects)"
        )
        self.broad_lorentz_gamma_1: Parameter = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_1",
            units="µs/Å",
            description="Lorentzian broadening coefficient (dependent on d-spacing)"
        )
        self.broad_lorentz_gamma_2: Parameter = Parameter(
            value=0.0,
            cif_name="lorentz_gamma_2",
            units="µs²/Å²",
            description="Lorentzian broadening coefficient (instrumental-dependent term)"
        )
        self.broad_mix_beta_0: Parameter = Parameter(
            value=0.0,
            cif_name="mix_beta_0",
            units="deg",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
        )
        self.broad_mix_beta_1: Parameter = Parameter(
            value=0.0,
            cif_name="mix_beta_1",
            units="deg",
            description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
        )


class Asymmetry:
    """Encapsulates all possible peak asymmetry parameters as attributes."""

    def __init__(self):
        self.asym_empir_1: Parameter = Parameter(
            value=0.1,
            cif_name="asym_empir_1",
            units="",
            description="Empirical asymmetry coefficient p1"
        )
        self.asym_empir_2: Parameter = Parameter(
            value=0.2,
            cif_name="asym_empir_2",
            units="",
            description="Empirical asymmetry coefficient p2"
        )
        self.asym_empir_3: Parameter = Parameter(
            value=0.3,
            cif_name="asym_empir_3",
            units="",
            description="Empirical asymmetry coefficient p3"
        )
        self.asym_empir_4: Parameter = Parameter(
            value=0.4,
            cif_name="asym_empir_4",
            units="",
            description="Empirical asymmetry coefficient p4"
        )
        self.asym_fcj_1: Parameter = Parameter(
            value=0.01,
            cif_name="asym_fcj_1",
            units="",
            description="FCJ asymmetry coefficient 1"
        )
        self.asym_fcj_2: Parameter = Parameter(
            value=0.02,
            cif_name="asym_fcj_2",
            units="",
            description="FCJ asymmetry coefficient 2"
        )
        self.asym_alpha_0: Parameter = Parameter(
            value=0.01,
            cif_name="asym_alpha_0",
            units="",
            description="Ikeda-Carpenter asymmetry parameter α₀"
        )
        self.asym_alpha_1: Parameter = Parameter(
            value=0.02,
            cif_name="asym_alpha_1",
            units="",
            description="Ikeda-Carpenter asymmetry parameter α₁"
        )


class ConstantWavelengthPseudoVoigt:
    _description = 'Pseudo-Voigt profile'
    def __init__(self):
        self.broad_gauss_u = Broadening().broad_gauss_u
        self.broad_gauss_v = Broadening().broad_gauss_v
        self.broad_gauss_w = Broadening().broad_gauss_w
        self.broad_lorentz_x = Broadening().broad_lorentz_x
        self.broad_lorentz_y = Broadening().broad_lorentz_y

class ConstantWavelengthSplitPseudoVoigt:
    _description = 'Split pseudo-Voigt profile'
    def __init__(self):
        self.broad_gauss_u = Broadening().broad_gauss_u
        self.broad_gauss_v = Broadening().broad_gauss_v
        self.broad_gauss_w = Broadening().broad_gauss_w
        self.broad_lorentz_x = Broadening().broad_lorentz_x
        self.broad_lorentz_y = Broadening().broad_lorentz_y
        self.asym_empir_1 = Asymmetry().asym_empir_1
        self.asym_empir_2 = Asymmetry().asym_empir_2
        self.asym_empir_3 = Asymmetry().asym_empir_3
        self.asym_empir_4 = Asymmetry().asym_empir_4

class ConstantWavelengthThompsonCoxHastings:
    _description = 'Thompson-Cox-Hastings profile'
    def __init__(self):
        self.broad_gauss_u = Broadening().broad_gauss_u
        self.broad_gauss_v = Broadening().broad_gauss_v
        self.broad_gauss_w = Broadening().broad_gauss_w
        self.broad_lorentz_x = Broadening().broad_lorentz_x
        self.broad_lorentz_y = Broadening().broad_lorentz_y
        self.asym_fcj_1 = Asymmetry().asym_fcj_1
        self.asym_fcj_2 = Asymmetry().asym_fcj_2

class TimeOfFlightPseudoVoigt:
    _description = 'Pseudo-Voigt profile'
    def __init__(self):
        self.broad_gauss_sigma_0 = Broadening().broad_gauss_sigma_0
        self.broad_gauss_sigma_1 = Broadening().broad_gauss_sigma_1
        self.broad_gauss_sigma_2 = Broadening().broad_gauss_sigma_2
        self.broad_lorentz_gamma_0 = Broadening().broad_lorentz_gamma_0
        self.broad_lorentz_gamma_1 = Broadening().broad_lorentz_gamma_1
        self.broad_lorentz_gamma_2 = Broadening().broad_lorentz_gamma_2

class TimeOfFlightIkedaCarpenter:
    _description = 'Ikeda-Carpenter profile'
    def __init__(self):
        self.broad_gauss_sigma_0 = Broadening().broad_gauss_sigma_0
        self.broad_gauss_sigma_1 = Broadening().broad_gauss_sigma_1
        self.broad_gauss_sigma_2 = Broadening().broad_gauss_sigma_2
        self.asym_alpha_0 = Asymmetry().asym_alpha_0
        self.asym_alpha_1 = Asymmetry().asym_alpha_1

class TimeOfFlightPseudoVoigtIkedaCarpenter:
    _description = 'Pseudo-Voigt * Ikeda-Carpenter profile'
    def __init__(self):
        self.broad_gauss_sigma_0 = Broadening().broad_gauss_sigma_0
        self.broad_gauss_sigma_1 = Broadening().broad_gauss_sigma_1
        self.broad_gauss_sigma_2 = Broadening().broad_gauss_sigma_2
        self.broad_lorentz_gamma_0 = Broadening().broad_lorentz_gamma_0
        self.broad_lorentz_gamma_1 = Broadening().broad_lorentz_gamma_1
        self.broad_lorentz_gamma_2 = Broadening().broad_lorentz_gamma_2
        self.asym_alpha_0 = Asymmetry().asym_alpha_0
        self.asym_alpha_1 = Asymmetry().asym_alpha_1

class TimeOfFlightPseudoVoigtBackToBackExponential:
    _description = 'Convolution of pseudo-Voigt with back-to-back exponential functions.'
    def __init__(self):
        self.broad_gauss_sigma_0 = Broadening().broad_gauss_sigma_0
        self.broad_gauss_sigma_1 = Broadening().broad_gauss_sigma_1
        self.broad_gauss_sigma_2 = Broadening().broad_gauss_sigma_2
        self.broad_lorentz_gamma_0 = Broadening().broad_lorentz_gamma_0
        self.broad_lorentz_gamma_1 = Broadening().broad_lorentz_gamma_1
        self.broad_lorentz_gamma_2 = Broadening().broad_lorentz_gamma_2
        self.asym_alpha_0 = Asymmetry().asym_alpha_0
        self.asym_alpha_1 = Asymmetry().asym_alpha_1

class Peak(StandardComponentBase):
    cif_category_name = "_peak"

    def __init__(self, beam_mode: str):
        self._beam_mode = beam_mode
        self._supported_profiles = self._get_supported_profiles(beam_mode)
        self._profile_type = self._get_default_profile()
        self._attach_attributes(self._profile_type.value)
        self._locked = True  # Lock further attribute additions

    def __setattr__(self, name, value):
        if hasattr(self, '_locked') and self._locked:
            if not hasattr(self, name):
                raise AttributeError(f"Cannot add new attribute '{name}' to locked class '{self.__class__.__name__}'")

        current = getattr(self, name, None)
        if isinstance(current, Parameter):
            current.value = value
        else:
            super().__setattr__(name, value)

    def _get_supported_profiles(self, beam_mode: str):
        return PeakFactory._supported_profiles[beam_mode]

    def _get_default_profile(self):
        default_profile = next(iter(self._supported_profiles))
        return Descriptor(
            value=default_profile,
            cif_name="profile_typ",
            description="..."
        )

    def _attach_attributes(self, profile_type: str):
        self._profile_type.value = profile_type

        profile_class = self._supported_profiles[self._profile_type.value]
        new_profile_obj = profile_class()

        # Collect names of new attributes
        new_attrs = {
            name for name in dir(new_profile_obj)
            if not name.startswith("_") and not callable(getattr(new_profile_obj, name))
        }

        # Remove old Parameter-type attributes that are not in the new profile
        for attr in dir(self):
            val = getattr(self, attr)
            if isinstance(val, Parameter) and attr not in new_attrs:
                delattr(self, attr)

        # Assign new Parameter-type attributes for the new profile type
        self._locked = False
        for attr in new_attrs:
            setattr(self, attr, getattr(new_profile_obj, attr))
        self._locked = True

    @property
    def profile_type(self):
        return self._profile_type

    @profile_type.setter
    def profile_type(self, name: str):
        if name in self._supported_profiles:
            print(paragraph("Current peak profile changed to"))
            print(name)
        else:
            supported_profiles = list(self._supported_profiles.keys())
            print(warning(f"Unknown peak profile '{name}'"))
            print(f'Supported peak profiles: {supported_profiles}')
            print(f"For more information, use 'show_supported_profiles()'")

    def show_supported_profiles(self):
        header = ["Peak profile", "Description"]
        table_data = []

        for name, config in self._supported_profiles.items():
            description = getattr(config, '_description', 'No description provided.')
            table_data.append([name, description])

        print(paragraph("Supported peak profiles"))
        print(tabulate.tabulate(
            table_data,
            headers=header,
            tablefmt="fancy_outline",
            numalign="left",
            stralign="left",
            showindex=False
        ))

    def show_current_profile(self):
        print(paragraph("Current peak profile"))
        print(self._profile_type.value)


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
            "pseudo-voigt * back-to-back": TimeOfFlightPseudoVoigtBackToBackExponential,
        }
    }

    @classmethod
    def create(cls, beam_mode, profile_type=None):
        """
        Create and return a Peak instance configured for a specific experimental mode and profile.
        """
        if beam_mode not in cls._supported_profiles:
            raise ValueError(f"Unsupported beam mode: '{beam_mode}'")

        supported_profiles = cls._supported_profiles[beam_mode]

        if profile_type is not None and profile_type not in supported_profiles:
            raise ValueError(
                f"Unsupported profile type '{profile_type}' for mode '{beam_mode}'.\n"
                f"Supported profiles are: {list(supported_profiles.keys())}"
            )

        return Peak(beam_mode)
