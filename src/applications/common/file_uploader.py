import pathlib

from django.conf import settings
from django.db import models
import hashlib
import secrets


def upload_file(instance: models.Model, filename: str) -> pathlib.Path:
    filename = pathlib.Path(filename)
    vector = secrets.token_hex(16)
    filename = (
        hashlib.sha256(
            f"{vector}:{filename.name}".encode(),
        ).hexdigest()
        + "."
        + filename.suffix
    )
    return settings.MEDIA_ROOT / "uploads" / instance.__class__.__name__ / filename
