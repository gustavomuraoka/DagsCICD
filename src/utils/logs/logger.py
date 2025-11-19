"""
This module defines a custom logger with a customized log format.
"""
import logging


# OopCompanion:suppressRename

class CustomFormatter(logging.Formatter):
    """
    Custom log formatter that adds filename and line number to log messages.
    """

    def format(self, record):
        filename: str = f'[{record.filename}:{record.lineno}]'
        formatted_message: str = super().format(record)
        return formatted_message.replace(f'[{record.filename}:{record.lineno}]', filename.rjust(40))


def logger_sub_title(title, length=120, character='#'):
    logger_title(title=title, length=length, character=character, subtitle=True)


def logger_title(title, length=120, character='#', subtitle=False):
    side_length: str = (length - len(title) - 4) // 2

    border: str = character * length
    if len(title) + 4 > length:
        title = title[:length - 6] + "..."
    centered_title: str = character * side_length + "  " + title + "  " + character * side_length

    if (len(centered_title) < length):
        centered_title += character * (length - len(centered_title))

    if not subtitle:
        logger.info(border)
    logger.info(centered_title)
    if not subtitle:
        logger.info(border)


# Create a StreamHandler with a custom formatter
handler = logging.StreamHandler()
TEMPLATE: str = '%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s'
formatter: CustomFormatter = CustomFormatter(TEMPLATE, datefmt='%d-%b-%Y %H:%M:%S')
handler.setFormatter(formatter)

# Create a logger and configure it
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
