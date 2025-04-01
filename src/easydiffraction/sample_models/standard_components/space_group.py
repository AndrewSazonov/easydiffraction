from easydiffraction.core.component_base import StandardComponent
from easydiffraction.core.parameter import Descriptor


class SpaceGroup(StandardComponent):
    """
    Represents the space group of a sample model.
    """
    cif_category_name = "_space_group"

    def __init__(self, name="P1"):
        super().__init__()

        self.name = Descriptor(
            value=name,
            cif_name="name_H-M_alt"
        )

