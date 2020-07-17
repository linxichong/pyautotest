import yaml
import logging
import time
from logging import LogRecord

class WidgetLogger(logging.Handler):
    def __init__(self, widget):
        logging.Handler.__init__(self)
        self.widget = widget

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(threadName)s - %(message)s")
        self.setFormatter(formatter)
        self.level_colors = {
            'INFO': 'black',
            'DEBUG': 'grey',
            'WARNING': 'orange',
            'ERROR': 'red',
            'CRITICAL': 'red'
        }

    def emit(self, record: LogRecord):
        self.widget.Update(
            value=self.format(record) + '\n',
            append=True,
            text_color_for_value=self.level_colors[record.levelname])
