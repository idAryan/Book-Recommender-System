import os
import sys
import traceback

class AppException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(str(error_message))
        _, _, exc_tb = error_detail.exc_info()
        self.error_message = self.get_detailed_error_message(error_message, exc_tb)

    def get_detailed_error_message(self, error_message, tb):
        if tb:
            file_name = tb.tb_frame.f_code.co_filename
            line_number = tb.tb_lineno
            folder_name = os.path.dirname(file_name)
        else:
            file_name = "Unavailable"
            line_number = -1
            folder_name = "Unavailable"

        return (
            f"Error: {error_message}\n"
            f"File: {file_name}\n"
            f"Line: {line_number}\n"
            f"Folder: {folder_name}"
        )

    def __str__(self):
        return self.error_message
