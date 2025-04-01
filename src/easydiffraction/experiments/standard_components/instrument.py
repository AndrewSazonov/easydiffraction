from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.core.parameter import Parameter

class Setup:
    """Encapsulates all possible default instrument setup parameters as attributes."""

    def __init__(self):
        # Constant wavelength specific parameters
        self.wavelength: Parameter = Parameter(
            value=1.5406,
            cif_name="wavelength",
            units="Å",
            description="Incident neutron or X-ray wavelength"
        )

        # Time-of-flight specific parameters
        self.twotheta_bank: Parameter = Parameter(
            value=-0.01,
            cif_name="2theta_bank",
            units="deg",
            description="Position of the detector bank in TOF experiments"
        )


class Calibration:
    """Encapsulates all possible default instrument calibration parameters as attributes."""

    def __init__(self):
        # Constant wavelength specific parameters
        self.twotheta_offset: Parameter = Parameter(
            value=0,
            cif_name="2theta_offset",
            units="deg",
            description="Accounts for instrument misalignment, leading to a constant shift in peak positions"
        )

        # Time-of-flight specific parameters
        self.d_to_tof_offset: Parameter = Parameter(
            value=0.1,
            cif_name="d_to_tof_offset",
            units="µs",
            description="A constant offset in TOF scale, representing an instrument-dependent time delay correction"
        )
        self.d_to_tof_linear: Parameter = Parameter(
            value=0.2,
            cif_name="d_to_tof_linear",
            units="µs/Å",
            description="The primary scaling factor that converts d-spacing (d) to time-of-flight (TOF) using a linear relationship"
        )
        self.d_to_tof_quad: Parameter = Parameter(
            value=0.3,
            cif_name="d_to_tof_quad",
            units="µs/Å²",
            description="A quadratic correction term that refines the non-linearity in the d-spacing to TOF conversion"
        )
        self.d_to_tof_recip: Parameter = Parameter(
            value=0.4,
            cif_name="d_to_tof_recip",
            units="µs·Å",
            description="A velocity-dependent correction term, introduced to compensate for neutron velocity dispersion"
        )


class ConstantWavelength:
    def __init__(self):
        self.setup_wavelength = Setup().wavelength
        self.calib_twotheta_offset = Calibration().twotheta_offset


class TimeOfFlight:
    def __init__(self):
        self.setup_twotheta_bank = Setup().twotheta_bank
        self.setup_d_to_tof_offset = Calibration().d_to_tof_offset
        self.setup_d_to_tof_linear = Calibration().d_to_tof_linear
        self.setup_d_to_tof_quad = Calibration().d_to_tof_quad
        self.setup_d_to_tof_recip = Calibration().d_to_tof_recip


class Instrument(StandardComponentBase):
    cif_category_name = "_instr"

    def __init__(self, beam_mode: str):
        self._beam_mode = beam_mode
        self._attach_attributes(self._beam_mode)
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

    def _attach_attributes(self, beam_mode: str):
        new_class = InstrumentFactory._supported_classes[beam_mode]
        new_obj = new_class()

        # Collect names of new attributes
        new_attrs = {
            name for name in dir(new_obj)
            if not name.startswith("_") and not callable(getattr(new_obj, name))
        }

        # Remove old Parameter-type attributes that are not in the new profile
        for attr in dir(self):
            val = getattr(self, attr)
            if isinstance(val, Parameter) and attr not in new_attrs:
                delattr(self, attr)

        # Assign new Parameter-type attributes for the new profile type
        self._locked = False
        for attr in new_attrs:
            setattr(self, attr, getattr(new_obj, attr))
        self._locked = True


class InstrumentFactory:
    _supported_classes = {
        "constant wavelength": ConstantWavelength,
        "time-of-flight": TimeOfFlight
    }

    @classmethod
    def create(cls, beam_mode='constant wavelength'):
        """
        Create and return a Peak instance configured for a specific experimental mode and profile.
        """
        if beam_mode not in cls._supported_classes:
            supported_beam_modes = list(cls._supported_classes.keys())

            raise ValueError(
                f"Unsupported beam mode: '{beam_mode}'.\n "
                f"Supported beam modes are: {supported_beam_modes}"
            )

        return Instrument(beam_mode)
