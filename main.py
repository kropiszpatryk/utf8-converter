"""Main run module"""
import os
import shutil
import queue

from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
from watchdog.observers import Observer
from concurrent.futures import ThreadPoolExecutor, Future
from logger import init_logger
from observers import NewFileHandler
from text_file_converter import TextFileConverter


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
logger = init_logger()


class FileConversionManager:
    """
    Manages folder monitoring, file queuing, and text file conversion to UTF-8.
    """

    def __init__(
        self, input_directory: str, output_directory: str, max_workers: int = 2
    ) -> None:
        """
        Initializes the file conversion manager with logger, converter, and counters.

        Args:
            input_directory (str): Directory to monitor for new files.
            output_directory (str): Directory to save converted files.
            max_workers (int): Maximum number of concurrent worker threads. Default is 2.
        """

        self.input_directory = input_directory
        self.processed_directory = os.path.join(self.input_directory, "processed")
        self.error_directory = os.path.join(self.input_directory, "errors")
        os.makedirs(self.processed_directory, exist_ok=True)
        os.makedirs(self.error_directory, exist_ok=True)
        self.converter = TextFileConverter(
            output_directory, self.processed_directory, logger
        )
        self.file_queue = queue.Queue()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.total_files = 0
        self.processed_files = 0
        self.process_existing_files()

    def process_existing_files(self) -> None:
        """
        Processes any .txt files that already exist in the input directory at startup.
        """
        existing_files = [
            f for f in os.listdir(self.input_directory) if f.endswith(".txt")
        ]
        for file_name in existing_files:
            file_path = os.path.join(self.input_directory, file_name)
            self.total_files += 1
            future = self.executor.submit(
                self.converter.convert_file_to_utf8, file_path
            )
            future.add_done_callback(self.update_progress_callback(file_path))

        if self.total_files > 0:
            logger.info(f"Found {self.total_files} existing .txt files to process.")
            self.log_progress_bar()

    def increment_total_files(self) -> None:
        """
        Increases the total file count and updates the progress bar.
        """
        self.total_files += 1
        self.log_progress_bar()

    def log_progress_bar(self) -> None:
        """
        Logs a text-based progress bar to the terminal based on the number of processed files.
        """
        if self.total_files > 0:
            progress_ratio = self.processed_files / self.total_files
            progress_bar = f"[{'#' * int(progress_ratio * 30):<30}]"
            logger.info(
                f"Progress: {progress_bar} {self.processed_files}/{self.total_files} files processed."
            )

    def update_progress_callback(self, file_path: str):
        """
        Returns a callback function that updates the progress bar after processing a file.

        Args:
            file_path (str): Path of the file being processed.
        """

        def callback(future: Future) -> None:
            self.processed_files += 1
            self.log_progress_bar()
            logger.debug(f"File processed: {file_path}")

        return callback

    def process_files(self) -> None:
        """
        Processes files in the queue by submitting conversion tasks to the executor.
        Updates progress on task completion.
        """
        while True:
            file_path = self.file_queue.get()
            future = self.executor.submit(
                self.converter.convert_file_to_utf8, file_path
            )
            if not future.result():
                shutil.move(file_path, self.error_directory)
            future.add_done_callback(self.update_progress_callback(file_path))

    def monitor_folder(self) -> None:
        """
        Monitors the specified input directory for new files and adds them to the processing queue.
        Starts the folder monitoring observer and manages graceful shutdown on interrupt.
        """
        event_handler = NewFileHandler(self.file_queue, logger, self)
        observer = Observer()
        observer.schedule(event_handler, self.input_directory, recursive=False)
        observer.start()

        logger.info(f"Monitoring folder: {self.input_directory}")

        try:
            self.total_files = sum(
                1
                for file in os.listdir(self.input_directory)
                if file.endswith(".txt")
                and os.path.isfile(os.path.join(self.input_directory, file))
            )
            self.process_files()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


if __name__ == "__main__":
    input_directory: Optional[str] = os.getenv("INPUT_DIRECTORY")
    output_directory: Optional[str] = os.getenv("OUTPUT_DIRECTORY")
    max_workers: int = int(os.getenv("MAX_WORKERS", "2"))

    if input_directory and output_directory:
        manager = FileConversionManager(
            input_directory, output_directory, max_workers=max_workers
        )
        manager.monitor_folder()
    else:
        logger.error(
            "Error: INPUT_DIRECTORY and OUTPUT_DIRECTORY must be set in the environment."
        )
