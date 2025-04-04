from easydiffraction.core.parameter import (Parameter,
                                            Descriptor)
from easydiffraction.core.component import (IterableComponent,
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

        self._locked = True  # Lock further attribute additions


class LinkedPhases(IterableComponent):
    @property
    def cif_category_name(self):
        return "_pd_phase_block"

    def add(self, id: str, scale: float):
        phase = LinkedPhase(id, scale)
        self._rows.append(phase)
