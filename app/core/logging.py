import logging

from app.core.config import settings


def configure_logging() -> None:
    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())

    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    handler.setFormatter(formatter)

    root.handlers.clear()
    root.addHandler(handler)
