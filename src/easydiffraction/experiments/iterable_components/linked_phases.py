from easydiffraction.core.parameter import (Parameter,
                                            Descriptor)
from easydiffraction.core.component_base import (IterableComponent,
                                                 IterableComponentRow)


class LinkedPhase(IterableComponentRow):
    def __init__(self, id: str, scale: float):
        super().__init__()

        self.id = Descriptor(
            value=id,
            cif_name="id"
        )
        self.scale = Parameter(
            value=scale,
            cif_name="scale"
        )


class LinkedPhases(IterableComponent):
    cif_category_name = "_pd_phase_block"

    def add(self, id: str, scale: float):
        phase = LinkedPhase(id, scale)
        self._rows.append(phase)
