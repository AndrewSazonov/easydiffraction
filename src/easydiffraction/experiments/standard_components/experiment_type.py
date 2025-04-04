from easydiffraction.core.component import StandardComponent
from easydiffraction.core.parameter import Descriptor


class ExperimentType(StandardComponent):
    @property
    def cif_category_name(self):
        return "_expt_type"

    def __init__(self,
                 sample_form: str,
                 beam_mode: str,
                 radiation_probe: str):
        super().__init__()

        self.sample_form: Descriptor = Descriptor(
            value=sample_form,
            cif_name="sample_form",
            description="Specifies whether the diffraction data corresponds to powder diffraction or single crystal diffraction"
        )
        self.beam_mode: Descriptor = Descriptor(
            value=beam_mode,
            cif_name="beam_mode",
            description="Defines whether the measurement is performed with a constant wavelength (CW) or time-of-flight (TOF) method"
        )
        self.radiation_probe: Descriptor = Descriptor(
            value=radiation_probe,
            cif_name="radiation_probe",
            description="Specifies whether the measurement uses neutrons or X-rays"
        )

        self._locked = True  # Lock further attribute additions
