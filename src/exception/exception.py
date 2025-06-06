import sys

class networkException(Exception):
    def __init__(self, error_message , error_details: sys):
        self.error_message = error_message
        super().__init__(self.error_message)
        _,_,exc_tb = error_details.exc_info()

        self.line_no = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occurred in script: [{self.file_name}] at line number: [{self.line_no}] with error message: [{self.error_message}]"
    




