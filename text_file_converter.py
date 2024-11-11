"""File converter module"""
import os
import mimetypes
import logging
import shutil


class TextFileConverter:
    """
    Converts text files to UTF-8 encoding and saves them in a specified output directory.
    """

    def __init__(
        self, output_directory: str, processed_directory: str, logger: logging.Logger
    ) -> None:
        """
        Initializes the TextFileConverter with an output directory and logger.
        Creates the output directory if it does not exist.

        Args:
            output_directory (str): Directory where converted files will be saved.
            processed_directory (str): Directory where processed files will be moved.
            logger (logging.Logger): Logger instance for logging events.
        """
        self.output_directory = output_directory
        self.processed_directory = processed_directory
        self.logger = logger

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
            self.logger.debug(f"Output directory created: {output_directory}")

    @staticmethod
    def _is_text_file(file_path: str) -> bool:
        """
        Checks if the specified file is a text file based on its extension and MIME type.

        Args:
            file_path (str): Path to the file to check.

        Returns:
            bool: True if the file is a text file, False otherwise.
        """
        if not file_path.endswith(".txt"):
            return False
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type == "text/plain"

    def convert_file_to_utf8(self, file_path: str) -> bool:
        """
        Converts a file to UTF-8 encoding and saves it in the output directory.

        Args:
            file_path (str): Path to the file to be converted.

        Returns:
            bool: True if the file was successfully converted, False if an error occurred.
        """
        if not self._is_text_file(file_path):
            self.logger.warning(f"File {file_path} is not a supported text file.")
            return False

        base_name = os.path.basename(file_path)
        output_name = f"{os.path.splitext(base_name)[0]}_utf8_converted.txt"
        output_path = os.path.join(self.output_directory, output_name)
        try:
            with open(file_path, "r", errors="replace") as file, open(
                output_path, "w", encoding="utf-8"
            ) as utf8_file:
                while chunk := file.read(1024):
                    utf8_file.write(chunk)
            self.logger.debug(
                f"File {file_path} successfully converted and saved as {output_path}."
            )
            processed_path = os.path.join(
                self.processed_directory, os.path.basename(file_path)
            )
            shutil.move(file_path, processed_path)
            self.logger.debug(f"Original file {file_path} moved to {processed_path}.")
            return True
        except Exception as e:
            self.logger.error(f"Error converting file {file_path}: {e}")
            return False
