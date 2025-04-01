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
        if not self.cif_category_name:
            raise ValueError("cif_category_name must be defined in the derived class.")

        records = []

        for attr_name in dir(self):
            if attr_name.startswith('_'):
                continue

            attr_obj = getattr(self, attr_name)
            if not isinstance(attr_obj, (Descriptor, Parameter)):
                continue

            tag = f"{self.cif_category_name}.{attr_obj.cif_name}"
            value = attr_obj.value
            unit = getattr(attr_obj, "units", None)

            if isinstance(value, float):
                float_str = f"{value:.6f}".rstrip('0')
                if float_str.endswith('.'):
                    float_str += '0'
                val_str = float_str
            elif isinstance(value, str):
                val_str = f'"{value}"' if ' ' in value else value
            else:
                val_str = str(value)

            records.append((tag, val_str, unit))

        max_tag_len = max(len(tag) for tag, _, _ in records)
        float_parts = []
        string_lengths = []
        for _, val, _ in records:
            if '.' in val and not val.startswith('"'):
                sign = '-' if val.startswith('-') else ''
                int_part, _, dec_part = val.lstrip('-').partition('.')
                float_parts.append((sign, int_part, dec_part))
            elif val.isalpha() or val.startswith('"'):
                string_lengths.append(len(val))

        max_int_part = max((len(sign + int_part) for sign, int_part, _ in float_parts), default=0)
        max_dec_part = max((len(dec_part) for _, _, dec_part in float_parts), default=0)
        max_float_length = max((len(f"{sign}{int_part}.{dec_part}") for sign, int_part, dec_part in float_parts), default=0)
        max_string_length = max(string_lengths, default=0)
        value_column_width = max(max_float_length, max_string_length) + 2

        formatted_records = []
        for tag, val, unit in records:
            if '.' in val and not val.startswith('"'):  # float
                sign = '-' if val.startswith('-') else ''
                int_part, _, dec_part = val.lstrip('-').partition('.')
                int_full = sign + int_part.rjust(max_int_part - len(sign))
                dec_full = dec_part.ljust(max_dec_part)
                formatted = f"{int_full}.{dec_full}".ljust(value_column_width)
            elif val.replace('-', '').isdigit():  # int
                formatted = val.rjust(max_int_part).ljust(value_column_width)
            else:  # string
                formatted = val.ljust(value_column_width)

            formatted_records.append((tag, formatted, unit))

        lines = []
        for tag, val_fmt, unit in formatted_records:
            tag_part = tag.ljust(max_tag_len + 2)
            val_part = val_fmt.ljust(value_column_width)
            comment = f"# units: {unit}" if unit else ""
            line = f"{tag_part}{val_part}{comment}"
            lines.append(line)

        return "\n".join(lines)
