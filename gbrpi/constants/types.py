from typing import Union, Iterable


FixedSizePrimitive = Union[int, float, bool]
Primitive = Union[FixedSizePrimitive, str, bytes, None]
ConnEntryValue = Union[Primitive, Iterable[Primitive]]
SerialData = Union[bytes, bytearray]

