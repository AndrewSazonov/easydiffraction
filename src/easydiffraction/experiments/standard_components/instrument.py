from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.core.parameter import Parameter


class InstrumentBase(StandardComponentBase):
    cif_category_name = "_instr"

    def __init__(self, type_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._type = type_name

    @property
    def type(self):
        return self._type


class ConstantWavelengthInstrument(InstrumentBase):
    def __init__(self):
        super().__init__("constant wavelength")

        self.setup_wavelength = Parameter(
            value=1.5406,
            cif_name="wavelength",
            units="Å",
            description="Incident neutron or X-ray wavelength"
        )
        self.calib_twotheta_offset = Parameter(
            value=0,
            cif_name="2theta_offset",
            units="deg",
            description="Instrument misalignment offset"
        )

        self._locked = True  # Lock further attribute additions


class TimeOfFlightInstrument(InstrumentBase):
    def __init__(self):
        super().__init__("time-of-flight")

        self.setup_twotheta_bank = Parameter(
            value=-0.01,
            cif_name="2theta_bank",
            units="deg",
            description="Detector bank position"
        )
        self.calib_d_to_tof_offset = Parameter(
            value=0.1,
            cif_name="d_to_tof_offset",
            units="µs",
            description="TOF offset"
        )
        self.calib_d_to_tof_linear = Parameter(
            value=0.2,
            cif_name="d_to_tof_linear",
            units="µs/Å",
            description="TOF linear conversion"
        )
        self.calib_d_to_tof_quad = Parameter(
            value=0.3,
            cif_name="d_to_tof_quad",
            units="µs/Å²",
            description="TOF quadratic correction"
        )
        self.calib_d_to_tof_recip = Parameter(
            value=0.4,
            cif_name="d_to_tof_recip",
            units="µs·Å",
            description="TOF reciprocal velocity correction"
        )

        self._locked = True  # Lock further attribute additions


class InstrumentFactory:
    _supported = {
        "constant wavelength": ConstantWavelengthInstrument,
        "time-of-flight": TimeOfFlightInstrument
    }

    @classmethod
    def create(cls, beam_mode='constant wavelength'):
        if beam_mode not in cls._supported:
            supported = list(cls._supported.keys())

            raise ValueError(
                f"Unsupported beam mode: '{beam_mode}'.\n "
                f"Supported beam modes are: {supported}"
            )

        instrument_class = cls._supported[beam_mode]
        return instrument_class()