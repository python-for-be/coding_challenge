from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, field_validator

from src.core.exceptions import DateFormatError, MinimumAgeError
from src.core.utils import calculate_age


class AddressCreateSchema(BaseModel):
    """Schema for creating a new address.

    Attributes:
        city (str): The city name.
        country (str): The country name.
        number (str): The house or building number.
        postcode (str): The postal code.
        street_name (str): The name of the street.
    """

    city: str
    country: str
    number: str
    postcode: str
    street_name: str


class UserCreateSchema(BaseModel):
    """Schema for creating a new user.

    Attributes:
        firstname (str): The first name of the user.
        lastname (str): The last name of the user.
        date_of_birth (date): The user's date of birth.
        address (AddressCreateSchema): The user's address information.
    """

    firstname: str
    lastname: str
    date_of_birth: date
    address: AddressCreateSchema

    @field_validator("date_of_birth", mode="before")
    def validate_date_of_birth(cls, value: str) -> str:
        """Validates date format matches YYYY-MM-DD."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise DateFormatError("Invalid date format, expected YYYY-MM-DD")

        user_age = calculate_age(date_of_birth=value)

        if user_age < 16:
            raise MinimumAgeError("User age must be at least 16 years old.")
        return value


class UserUpdateSchema(BaseModel):
    """Schema for updating an existing user.

    Attributes:
        firstname (str): The first name of the user.
        lastname (str): The last name of the user.
        date_of_birth (date): The user's date of birth.
        address (AddressCreateSchema): The user's address information.
    """

    firstname: str
    lastname: str
    date_of_birth: date
    address: AddressCreateSchema

    @field_validator("date_of_birth", mode="before")
    def validate_date_of_birth(cls, value: str) -> str:
        """Validates date format matches YYYY-MM-DD."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise DateFormatError("Invalid date format, expected YYYY-MM-DD")

        user_age = calculate_age(date_of_birth=value)

        if user_age < 16:
            raise MinimumAgeError("User age must be at least 16 years old.")
        return value


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
