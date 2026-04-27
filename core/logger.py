import json
import logging
import sys
from datetime import datetime

from config import ROOT_DIR

LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Generate a unique filename for this execution run
RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"run_{RUN_TIMESTAMP}.log"


class JSONFormatter(logging.Formatter):
	"""Formatter that outputs JSON strings after parsing the LogRecord."""

	def format(self, record):
		log_record = {
			"timestamp": datetime.now().isoformat() + "Z",
			"level": record.levelname,
			"name": record.name,
		}

		# If the message is a dict, merge it, otherwise use 'message' key
		if isinstance(record.msg, dict):
			log_record.update(record.msg)
		else:
			log_record["message"] = record.getMessage()

		if record.exc_info:
			log_record["exc_info"] = self.formatException(record.exc_info)
		return json.dumps(log_record)


def setup_logging(verbose: bool = False):
	"""
	Initializes the root logger with a run-specific file handler
	and an optional console handler.
	"""
	root_logger = logging.getLogger()
	# Set to DEBUG to capture everything in the file
	root_logger.setLevel(logging.DEBUG)

	# Remove any existing handlers
	for handler in root_logger.handlers[:]:
		root_logger.removeHandler(handler)

	# 1. File Handler (Always JSON, always DEBUG level)
	file_handler = logging.FileHandler(LOG_FILE)
	file_handler.setFormatter(JSONFormatter())
	file_handler.setLevel(logging.DEBUG)
	root_logger.addHandler(file_handler)

	# 2. Console Handler (Only if verbose, standard text for readability)
	if verbose:
		console_handler = logging.StreamHandler(sys.stdout)
		console_fmt = logging.Formatter(
			"%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
		)
		console_handler.setFormatter(console_fmt)
		console_handler.setLevel(logging.INFO)
		root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
	"""Return a logger with the specified name."""
	return logging.getLogger(name)
