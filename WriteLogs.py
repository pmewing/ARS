import time


class Log:
    def __init__(self, log_line: str, log_path: str, erase_file: bool):
        """
        This class will be used to write a specified log line to a certain file. The date and time will be calculated.
        The only input needed is the exact line to write, and the path of the log file.

        Data written to the log file will be appended to the end of the path.
        If you would like to erase the log path and start fresh, pass `True` for erase_file

        :param str log_line: This is the exact line that should be written to the file
        :param str log_path: This is the exact path to the log file that should be written to.
        :param bool erase_file: If you would like to erase the log file and start new, pass True here
        """
        """
        The following options are used to format the date/time of logs
        %Y  Year with century as a decimal number.
        %m  Month as a decimal number [01,12].
        %d  Day of the month as a decimal number [01,31].

        %H  Hour (24-hour clock) as a decimal number [00,23].
        %M  Minute as a decimal number [00,59].
        """
        date = time.strftime("%Y-%m-%d %H:%M")
        if erase_file:
            output_file = open(log_path, 'w')
        else:
            output_file = open(log_path, 'a')

        output_file.write( "{0} | {1}\n".format(date, log_line) )
        output_file.close()
