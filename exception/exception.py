import sys

class AppException(Exception):
    def __init__(self, message: Exception, errorDetail: sys):
        super.__init__(message)

        self.error_message = AppException.errorMessageDetail(message=message, errorDetail=errorDetail)


    @staticmethod
    def errorMessageDetail(message, errorDetail):
        """
            error: Exception object raise from module
            error_detail: is sys module contains detail information about system execution information.
        """
        _, _, exc_tb = errorDetail.exc_info()
        # extracting file name from exception traceback
        file_name = exc_tb.tb_frame.f_code.co_filename

        # preparing error message
        errorMessage = f"Error occurred python script name [{file_name}]" \
                        f" line number [{exc_tb.tb_lineno}] error message [{error}]."

        return errorMessage

    def __repr__(self):
        """
        Formating object of AppException
        """
        return AppException.__name__.__str__()

    def __str__(self):
        """
        Formating how a object should be visible if used in print statement.
        """
        return self.error_message