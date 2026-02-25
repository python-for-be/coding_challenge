from datetime import date, datetime


def calculate_age(date_of_birth: str) -> int:
    """Calculates age based on the current date.

    Args:
        date_of_birth (date): date of birth to determine age.

    Returns:
        int: age in years.
    """
    today = date.today()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

    return age
