from django.db import models


class RateChoices(models.IntegerChoices):
    """
    Enum class for review rate
    """
    VERY_BAD = 1
    BAD = 2
    NOT_BAD = 3
    GOOD = 4
    VERY_GOOD = 5
