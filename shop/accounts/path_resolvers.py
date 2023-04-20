import shlex
from datetime import datetime


def profile_avatar_path(instance, filename: str) -> str:
    """Return processed path to save user's avatar"""
    today = datetime.today()
    safe_filename = shlex.quote(filename)
    filename = "_".join([str(today), instance.user.username, safe_filename])
    return "accounts/user_{pk}/profile/avatar/{filename}".format(
        pk=instance.user.pk,
        filename=filename,
    )
