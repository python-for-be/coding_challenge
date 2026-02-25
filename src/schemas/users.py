from pydantic import BaseModel, ConfigDict
from datetime import date


class Address(BaseModel):
    """Schema for the address of a user.

    Attributes:
        city (str): City of the address.
        country (str): Country of the address.
        number (str): House number of the address.
        street_name (str): Street name of the address.
        postcode (str): Postal code of the address.
    """

    model_config = ConfigDict(from_attributes=True)

    city: str
    country: str
    number: str
    street_name: str
    postcode: str


class UsersResponse(BaseModel):
    """Schema for the response of a user.

    Attributes:
        address (Address): The address of the user.
        date_of_birth (datetime.date): When the user was born.
        firstname (str): The first name of the user.
        id (int): Unique identifier of the user.
        lastname (str): The last name of the user.

    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    firstname: str
    lastname: str
    date_of_birth: date
    address: Address
