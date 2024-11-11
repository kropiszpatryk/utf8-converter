from watchdog.events import FileSystemEventHandler, FileSystemEvent
import logging
from queue import Queue
from typing import Any


class NewFileHandler(FileSystemEventHandler):
    """
    Watches for new file events in a specified directory and adds detected files to a processing queue.
    """

    def __init__(self, file_queue: Queue, logger: logging.Logger, manager: Any) -> None:
        """
        Initializes the file event handler.

        Args:
            file_queue (Queue): Queue to add new files for processing.
            logger (logging.Logger): Logger instance for logging events.
            manager (Any): Reference to the FileConversionManager instance to update total file count.
        """
        super().__init__()
        self.file_queue = file_queue
        self.logger = logger
        self.manager = manager

    def on_created(self, event: FileSystemEvent) -> None:
        """
        Triggered when a new file is created in the monitored directory.
        Adds the file to the processing queue and updates the total file count.

        Args:
            event (FileSystemEvent): Event data for the created file.
        """
        if not event.is_directory:
            self.logger.debug(f"New file detected: {event.src_path}")
            self.file_queue.put(event.src_path)
            self.manager.increment_total_files()
