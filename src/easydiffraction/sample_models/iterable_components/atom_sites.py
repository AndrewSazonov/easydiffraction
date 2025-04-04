from easydiffraction.core.parameter import (Parameter,
                                            Descriptor)
from easydiffraction.core.component import (IterableComponent,
                                            IterableComponentRow)


class AtomSite(IterableComponentRow):
    """
    Represents a single atom site within the crystal structure.
    """
    def __init__(self,
                 label: str,
                 type_symbol: str,
                 fract_x: float,
                 fract_y: float,
                 fract_z: float,
                 occupancy: float = 1.0,
                 b_iso: float = 0.0,
                 adp_type: str = "Biso"):  # TODO: add support for Uiso, Uani and Bani
        super().__init__()

        self.label = Descriptor(
            value=label,
            cif_name="label"
        )
        self.type_symbol = Descriptor(
            value=type_symbol,
            cif_name="type_symbol"
        )
        self.adp_type = Descriptor(
            value=adp_type,
            cif_name="ADP_type"
        )
        self.fract_x = Parameter(
            value=fract_x,
            cif_name="fract_x"
        )
        self.fract_y = Parameter(
            value=fract_y,
            cif_name="fract_y"
        )
        self.fract_z = Parameter(
            value=fract_z,
            cif_name="fract_z"
        )
        self.occupancy = Parameter(
            value=occupancy,
            cif_name="occupancy"
        )
        self.b_iso = Parameter(
            value=b_iso,
            cif_name="B_iso_or_equiv"
        )


class AtomSites(IterableComponent):
    """
    Collection of AtomSite instances.
    Provides methods to add, show, and access atom sites.
    """
    @property
    def cif_category_name(self):
        return "_atom_site"

    def add(self,
            label: str,
            type_symbol: str,
            fract_x: float,
            fract_y: float,
            fract_z: float,
            occupancy: float = 1.0,
            b_iso: float = 0.0,
            adp_type: str = "Biso"):
        """
        Add a new atom site to the collection.
        """
        site = AtomSite(label,
                        type_symbol,
                        fract_x,
                        fract_y,
                        fract_z,
                        occupancy,
                        b_iso,
                        adp_type)
        self._rows.append(site)
