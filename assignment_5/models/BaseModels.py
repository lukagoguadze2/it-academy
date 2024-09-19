from datetime import datetime
from datetime import date as datetime_date
from typing import Optional, Dict
from abc import ABC, abstractmethod


class BaseModel(ABC):
    """Base abstract class with common methods for all models."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate the model data."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict) -> 'BaseModel':
        """Create an instance from a dictionary."""
        pass

    @staticmethod
    def _validate_string(value: Optional[str], field_name: str) -> bool:
        """Helper method to validate strings."""
        if value is None or not isinstance(value, str) or not value.strip():
            print(f"Invalid value for {field_name}")
            return False
        return True

    @staticmethod
    def _validate_int(value: Optional[int], field_name: str) -> bool:
        """Helper method to validate integers."""
        if value is None or not isinstance(value, int) or value < 0:
            print(f"Invalid value for {field_name}")
            return False
        return True

    @staticmethod
    def _convert_datetime(value: str | datetime) -> str:
        if isinstance(value, datetime) or isinstance(value, datetime_date):
            return value.strftime("%Y-%m-%d")

        return value


class AuthorBase(BaseModel):
    def __init__(
            self, name: Optional[str] = None,
            last_name: Optional[str] = None,
            date_of_birth: Optional[str | datetime | datetime_date] = None,
            place_of_birth: Optional[str] = None
    ):
        self.__name = name
        self.__last_name = last_name
        self.__date_of_birth = self._convert_datetime(date_of_birth)
        self.__place_of_birth = place_of_birth

    # Name property
    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: Optional[str]):
        self.__name = value

    # Last name property
    @property
    def last_name(self) -> Optional[str]:
        return self.__last_name

    @last_name.setter
    def last_name(self, value: Optional[str]):
        self.__last_name = value

    # Date of birth property
    @property
    def date_of_birth(self) -> Optional[str]:
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: Optional[str | datetime]):
        if value is not None:
            value = self._convert_datetime(value=value)
        self.__date_of_birth = value

    # Place of birth property
    @property
    def place_of_birth(self) -> Optional[str]:
        return self.__place_of_birth

    @place_of_birth.setter
    def place_of_birth(self, value: Optional[str]):
        self.__place_of_birth = value

    def validate(self) -> bool:
        return (self._validate_string(self.__name, "name") and
                self._validate_string(self.__last_name, "last_name") and
                self._validate_string(self.__date_of_birth, "date_of_birth") and
                self._validate_string(self.__place_of_birth, "place_of_birth"))

    @classmethod
    def from_dict(cls, data: Dict) -> 'AuthorBase':
        return cls(
            name=data.get("name"),
            last_name=data.get("last_name"),
            date_of_birth=data.get("date_of_birth"),
            place_of_birth=data.get("place_of_birth")
        )

    @abstractmethod
    def save(self):
        pass


class BookBase(BaseModel):
    def __init__(
            self, name: Optional[str] = None,
            category_name: Optional[str] = None,
            number_of_pages: int = 0, date_of_issue: Optional[str | datetime] = None,
            author_id: Optional[int] = None
    ):
        self.__name = name
        self.__category_name = category_name
        self.__number_of_pages = number_of_pages
        self.__date_of_issue = self._convert_datetime(date_of_issue)
        self.__author_id = author_id

    # Name property
    @property
    def name(self) -> Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: Optional[str]):
        self.__name = value

    # Category name property
    @property
    def category_name(self) -> Optional[str]:
        return self.__category_name

    @category_name.setter
    def category_name(self, value: Optional[str]):
        self.__category_name = value

    # Number of pages property
    @property
    def number_of_pages(self) -> int:
        return self.__number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, value: int):
        self.__number_of_pages = value

    # Date of issue property
    @property
    def date_of_issue(self) -> Optional[str]:
        return self.__date_of_issue

    @date_of_issue.setter
    def date_of_issue(self, value: Optional[str | datetime]):
        if value is not None:
            value = self._convert_datetime(value)
        self.__date_of_issue = value

    # Author ID property
    @property
    def author_id(self) -> int:
        return self.__author_id

    @author_id.setter
    def author_id(self, value: int):
        self.__author_id = value

    def validate(self) -> bool:
        return (self._validate_string(self.__name, "name") and
                self._validate_string(self.__category_name, "category_name") and
                self._validate_int(self.__number_of_pages, "number_of_pages") and
                self._validate_string(self.__date_of_issue, "date_of_issue") and
                self._validate_int(self.__author_id, "author_id"))

    @classmethod
    def from_dict(cls, data: Dict) -> 'BookBase':
        return cls(
            name=data.get("name"),
            category_name=data.get("category_name"),
            number_of_pages=data.get("number_of_pages"),
            date_of_issue=data.get("date_of_issue"),
            author_id=data.get("author_id")
        )

    @abstractmethod
    def save(self):
        pass
