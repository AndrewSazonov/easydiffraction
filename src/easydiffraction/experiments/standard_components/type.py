from easydiffraction.core.component_base import StandardComponentBase
from easydiffraction.core.parameter import Descriptor


class ExperimentType(StandardComponentBase):
    cif_category_name = "_expt_type"

    def __init__(self,
                 sample_form: str = "powder",
                 beam_mode: str = "constant wavelength",
                 radiation_probe: str = "neutron"):
        self.sample_form: Descriptor = Descriptor(
            value=sample_form,
            cif_name="sample_form",
            description="..."
        )
        self.beam_mode: Descriptor = Descriptor(
            value=beam_mode,
            cif_name="beam_mode",
            description="..."
        )
        self.radiation_probe: Descriptor = Descriptor(
            value=radiation_probe,
            cif_name="radiation_probe",
            description="..."
        )