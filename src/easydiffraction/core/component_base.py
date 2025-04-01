from abc import ABC, abstractmethod

from easydiffraction.utils.formatting import error
from easydiffraction.core.parameter import Parameter, Descriptor


class StandardComponentBase(ABC):
    """
    Base class for experiment and sample model components.
    Provides common functionality for CIF export and parameter handling.
    """
    cif_category_name = None  # Should be set in the derived class (e.g., "_instr_setup")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._locked = False  # If adding new attributes is locked

    def __getattr__(self, name):
        """
        If the attribute is a Parameter or Descriptor, return its value by default
        """
        attr = self.__dict__.get(name, None)
        if isinstance(attr, (Parameter, Descriptor)):
            return attr.value
        raise AttributeError(f"{name} not found")

    def __setattr__(self, name, value):
        """
        If an object is locked for adding new attributes, raise an error.
        If the attribute 'name' does not exist, add it.
        If the attribute 'name' exists and is a Parameter or Descriptor, set its value.
        """
        if hasattr(self, "_locked") and self._locked:
            if not hasattr(self, name):
                #raise AttributeError(f"Cannot add new attribute '{name}' to locked class '{self.__class__.__name__}'")
                print(error(f"Cannot add new parameter '{name}'"))
                return

        attr = self.__dict__.get(name, None)
        if isinstance(attr, (Descriptor, Parameter)):
            attr.value = value
        else:
            super().__setattr__(name, value)

    def as_cif(self):
        """
        Export parameters to CIF format with uncertainties and units.
        """
        if not self.cif_category_name:
            raise ValueError("cif_category_name must be defined in the derived class.")

        lines = []

        # Iterate over all attributes of the instance
        for attr_name in dir(self):

            # Skip internal attributes and methods
            if attr_name.startswith('_'):
                continue

            attr_obj = getattr(self, attr_name)

            # Skip methods and non-Descriptor/non-Parameter attributes
            if not isinstance(attr_obj, (Descriptor, Parameter)):
                continue

            full_cif_name = f"{self.cif_category_name}.{attr_obj.cif_name}"

            formatted_value = attr_obj.value
            if isinstance(formatted_value, str) and " " in formatted_value:
                # If the value is a string with spaces, wrap it in double quotes
                formatted_value = f'"{formatted_value}"'

            line = f"{full_cif_name} {formatted_value}"

            # Append units as comment (if any)
            if hasattr(attr_obj, "units") and attr_obj.units:
                line += f"  # units: {attr_obj.units}"

            lines.append(line)

        return "\n".join(lines)