"""Definition of input and output schemas.

Schemas are used for application interface. It can be used for any kind
of external interface, even DB layer, if necessary.

Most simple (and currently the onle used) examples are schemas for API
endpoints that take care of input data validation and output data
serialization.

Please keep in mind that Pydantic validates the data when instance of
``pydantic.BaseModel`` is created. Make sure you don't overvalidate
your data.
"""
