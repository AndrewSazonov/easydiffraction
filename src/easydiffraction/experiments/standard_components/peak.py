from easydiffraction.core.parameter import Parameter, Descriptor

class Broadening:
    """Encapsulates all possible peak broadening parameters as attributes."""

    # Constant wavelength specific parameters
    broad_gauss_u: Parameter = Parameter(
        value=0.0333,
        cif_name="broad_gauss_u",
        units="deg²",
        description="Gaussian broadening coefficient (dependent on sample size and instrument resolution)"
    )

    broad_gauss_v: Parameter = Parameter(
        value=-0.01,
        cif_name="broad_gauss_v",
        units="deg²",
        description="Gaussian broadening coefficient (instrumental broadening contribution)"
    )
    broad_gauss_w: Parameter = Parameter(
        value=0.02,
        cif_name="gauss_w",
        units="deg²",
        description="Gaussian broadening coefficient (instrumental broadening contribution)"
    )
    broad_lorentz_x: Parameter = Parameter(
        value=0.0,
        cif_name="broad_lorentz_x",
        units="deg",
        description="Lorentzian broadening coefficient (dependent on sample strain effects)"
    )
    broad_lorentz_y: Parameter = Parameter(
        value=0.0,
        cif_name="broad_lorentz_y",
        units="deg",
        description="Lorentzian broadening coefficient (dependent on microstructural defects and strain)"
    )
    broad_mix_eta: Descriptor = Descriptor(
        value=0.0,
        cif_name="broad_mix_eta",
        description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian broadening (not refined directly, calculated from X and Y parameters)",
        editable=False
    )

    # Time-of-flight specific parameters
    broad_gauss_sigma_0: Parameter = Parameter(
        value=0.0,
        cif_name="gauss_sigma_0",
        units="µs²",
        description="Gaussian broadening coefficient (instrumental resolution)"
    )
    broad_gauss_sigma_1: Parameter = Parameter(
        value=0.0,
        cif_name="gauss_sigma_1",
        units="µs/Å",
        description="Gaussian broadening coefficient (dependent on d-spacing)"
    )
    broad_gauss_sigma_2: Parameter = Parameter(
        value=0.0,
        cif_name="gauss_sigma_2",
        units="µs²/Å²",
        description="Gaussian broadening coefficient (instrument-dependent term)"
    )
    broad_lorentz_gamma_0: Parameter = Parameter(
        value=0.0,
        cif_name="lorentz_gamma_0",
        units="µs",
        description="Lorentzian broadening coefficient (dependent on microstrain effects)"
    )
    broad_lorentz_gamma_1: Parameter = Parameter(
        value=0.0,
        cif_name="lorentz_gamma_1",
        units="µs/Å",
        description="Lorentzian broadening coefficient (dependent on d-spacing)"
    )
    broad_lorentz_gamma_2: Parameter = Parameter(
        value=0.0,
        cif_name="lorentz_gamma_2",
        units="µs²/Å²",
        description="Lorentzian broadening coefficient (instrumental-dependent term)"
    )
    broad_mix_beta_0: Parameter = Parameter(
        value=0.0,
        cif_name="mix_beta_0",
        units="deg",
        description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
    )
    broad_mix_beta_1: Parameter = Parameter(
        value=0.0,
        cif_name="mix_beta_1",
        units="deg",
        description="Mixing parameter. Defines the ratio of Gaussian to Lorentzian contributions in TOF profiles"
    )


class Asymmetry:
    """Encapsulates all possible peak asymmetry parameters as attributes."""

    asym_empir_1: Parameter = Parameter(
        value=0.1,
        cif_name="asym_empir_1",
        units="",
        description="Empirical asymmetry coefficient p1"
    )
    asym_empir_2: Parameter = Parameter(
        value=0.2,
        cif_name="asym_empir_2",
        units="",
        description="Empirical asymmetry coefficient p2"
    )
    asym_empir_3: Parameter = Parameter(
        value=0.3,
        cif_name="asym_empir_3",
        units="",
        description="Empirical asymmetry coefficient p3"
    )
    asym_empir_4: Parameter = Parameter(
        value=0.4,
        cif_name="asym_empir_4",
        units="",
        description="Empirical asymmetry coefficient p4"
    )
    asym_fcj_1: Parameter = Parameter(
        value=0.01,
        cif_name="asym_fcj_1",
        units="",
        description="FCJ asymmetry coefficient 1"
    )
    asym_fcj_2: Parameter = Parameter(
        value=0.02,
        cif_name="asym_fcj_2",
        units="",
        description="FCJ asymmetry coefficient 2"
    )
    asym_alpha_0: Parameter = Parameter(
        value=0.01,
        cif_name="asym_alpha_0",
        units="",
        description="Ikeda-Carpenter asymmetry parameter α₀"
    )
    asym_alpha_1: Parameter = Parameter(
        value=0.02,
        cif_name="asym_alpha_1",
        units="",
        description="Ikeda-Carpenter asymmetry parameter α₁"
    )


class Peak:
    """Handles peak profile configurations, broadening, and asymmetry parameters dynamically."""

    _PROFILE_TYPES = {
        "constant_wavelength": {
            "pseudo-voigt": [
                Broadening.broad_gauss_u, Broadening.broad_gauss_v, Broadening.broad_gauss_w,
                Broadening.broad_lorentz_x, Broadening.broad_lorentz_y
            ],
            "split pseudo-voigt": [
                Broadening.broad_gauss_u, Broadening.broad_gauss_v, Broadening.broad_gauss_w,
                Broadening.broad_lorentz_x, Broadening.broad_lorentz_y,
                Asymmetry.asym_empir_1, Asymmetry.asym_empir_2, Asymmetry.asym_empir_3, Asymmetry.asym_empir_4
            ],
            "thompson-cox-hastings * fcj": [
                Broadening.broad_gauss_u, Broadening.broad_gauss_v, Broadening.broad_gauss_w,
                Broadening.broad_lorentz_x, Broadening.broad_lorentz_y,
                Asymmetry.asym_fcj_1, Asymmetry.asym_fcj_2
            ]
        },
        "time_of_flight": {
            "pseudo-voigt": [
                Broadening.broad_gauss_sigma_0, Broadening.broad_gauss_sigma_1, Broadening.broad_gauss_sigma_2,
                Broadening.broad_lorentz_gamma_0, Broadening.broad_lorentz_gamma_1, Broadening.broad_lorentz_gamma_2
            ],
            "ikeda-carpenter": [
                Broadening.broad_gauss_sigma_0, Broadening.broad_gauss_sigma_1, Broadening.broad_gauss_sigma_2,
                Asymmetry.asym_alpha_0, Asymmetry.asym_alpha_1
            ],
            "pseudo-voigt * ikeda-carpenter": [
                Broadening.broad_gauss_sigma_0, Broadening.broad_gauss_sigma_1, Broadening.broad_gauss_sigma_2,
                Broadening.broad_lorentz_gamma_0, Broadening.broad_lorentz_gamma_1, Broadening.broad_lorentz_gamma_2,
                Asymmetry.asym_alpha_0, Asymmetry.asym_alpha_1
            ],
            "pseudo-voigt * back-to-back exponential": [
                Broadening.broad_gauss_sigma_0, Broadening.broad_gauss_sigma_1, Broadening.broad_gauss_sigma_2,
                Broadening.broad_lorentz_gamma_0, Broadening.broad_lorentz_gamma_1, Broadening.broad_lorentz_gamma_2,
                Asymmetry.asym_alpha_0, Asymmetry.asym_alpha_1
            ]
        }
    }

    def __init__(self, expt_mode: str):
        """
        Initialize the Peak class with experiment mode and dynamically attach relevant parameters.

        :param expt_mode: 'constant_wavelength' or 'time_of_flight'
        """
        super().__setattr__("_expt_mode", expt_mode)
        super().__setattr__("_profile_type", "pseudo-voigt")  # Default profile type
        super().__setattr__("_valid_params", self._PROFILE_TYPES[expt_mode][self._profile_type])

        self._attach_parameters()

    def __setattr__(self, name, value):
        """
        Custom attribute setter:
        - Allows setting predefined attributes
        - Updates `.value` for `Parameter` attributes
        - Prevents dynamically adding new attributes
        """
        if hasattr(type(self), name) and isinstance(getattr(type(self), name), property):
            # If the attribute is a property, call its setter
            object.__setattr__(self, name, value)
        elif name in self.__dict__:
            param = self.__dict__[name]
            if isinstance(param, Parameter):
                param.value = value
            else:
                super().__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot add new attribute '{name}'. Only predefined attributes are allowed.")

    def _attach_parameters(self):
        """
        Dynamically attaches broadening and asymmetry parameters as attributes.
        """
        for param in self._valid_params:
            super().__setattr__(param.cif_name, param)

    def _detach_parameters(self):
        """
        Removes previously attached parameters when changing profile type.
        """
        for param in self._valid_params:
            if hasattr(self, param.cif_name):
                delattr(self, param.cif_name)

    @property
    def profile_type(self):
        """
        Gets the current peak profile type.
        """
        return self._profile_type

    @profile_type.setter
    def profile_type(self, value: str):
        """
        Changes the peak profile type and updates attached parameters dynamically.

        :param value: New profile type (e.g., 'pseudo-voigt', 'ikeda-carpenter')
        :raises ValueError: If profile type is not valid for the given experiment mode.
        """
        if value not in self._PROFILE_TYPES[self._expt_mode]:
            raise ValueError(
                f'Invalid profile type: "{value}". Valid options are {list(self._PROFILE_TYPES[self._expt_mode].keys())}.')

        # Remove old parameters
        self._detach_parameters()

        # Set new profile type
        self._profile_type = value
        self._valid_params = self._PROFILE_TYPES[self._expt_mode][self._profile_type]

        # Attach new parameters
        self._attach_parameters()