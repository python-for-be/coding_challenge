from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from src.models.user import User
from src.models.address import Address


class AddressFactory(SQLAlchemyFactory[Address]):
    """Factory for creating Address model instances."""

    __model__ = Address
    __set_relationships__ = False


class UserFactory(SQLAlchemyFactory[User]):
    """Factory for creating User model instances."""

    __model__ = User
    __set_relationships__ = True

    address = AddressFactory
