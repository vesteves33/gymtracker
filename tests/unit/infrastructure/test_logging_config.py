import logging

from app.infrastructure.logging_config import configure_logging


def test_configure_logging_define_formato_estruturado():
    configure_logging()

    root = logging.getLogger()
    assert root.level == logging.INFO
    assert len(root.handlers) >= 1
    formatter = root.handlers[0].formatter
    assert formatter is not None
    assert "level=" in formatter._fmt
    assert "logger=" in formatter._fmt
