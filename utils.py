from constants import COLORS, Logs, ArgsConsts, UIConsts
from time import sleep
import json
import sys
import os


class PrintUtils:
    """This class handles all of the different print formats and structures"""

    @classmethod
    def color(cls, colors_list, msg):
        """This method received color argument and a message and print it in the requested format"""
        return "{text_format}{msg}{end}".format(text_format="".join(colors_list), msg=msg, end=COLORS.END)

    @classmethod
    def main_screen_format(cls, msg):
        return cls.color([COLORS.BLUE, COLORS.BOLD], msg)

    @classmethod
    def header_format(cls, msg):
        return cls.color([COLORS.BOLD, COLORS.UNDERLINE], msg)

    @classmethod
    def error_format(cls, msg):
        return cls.color([COLORS.RED_BACKGROUND, COLORS.BOLD], msg)

    @classmethod
    def warning_format(cls, msg):
        return cls.color([COLORS.YELLOW, COLORS.BOLD], msg)


class ValidationUtil(object):
    """This class contain all of the arguments validators"""

    @classmethod
    def _handle_invalid_arguments(cls, log_to_print):
        """This method handle cases of invalid arguments. Print the log, pauses the script
        and returns False"""
        print(PrintUtils.warning_format(log_to_print))
        sleep(2)
        return False

    @classmethod
    def validate_regex_pattern(cls, regex_pattern):
        """This method validates the regex pattern that was received from the user.
        It should be in the expected structure 'relevant-bytes-prefixXXXX'. E.g: \x01XX"""
        if regex_pattern is None:
            return False
        if len(regex_pattern) < 2:
            return cls._handle_invalid_arguments(Logs.SHORT_REGEX_PATTERN_ERROR)
        elif regex_pattern[-1] != ArgsConsts.REGEX_SYMBOL:
            return cls._handle_invalid_arguments(Logs.REGEX_INVALID_SUFFIX_ERROR)
        elif ''.join(set(regex_pattern)) == ArgsConsts.REGEX_SYMBOL:
            return cls._handle_invalid_arguments(Logs.INVALID_REGEX_STRUCTURE_ERROR)
        return True

    @classmethod
    def validate_file_path(cls, file_path):
        """This method validates the file path that was retrieved from the user"""
        if file_path is None:
            return False
        elif not os.path.isfile(file_path):
            return cls._handle_invalid_arguments(Logs.MISSING_FILE_LOG.format(file_path))
        elif os.stat(file_path).st_size == 0:
            return cls._handle_invalid_arguments(Logs.EMPTY_FILE_LOG.format(file_path))
        return True

    @classmethod
    def validate_numeric_input(cls, user_input, option_list):
        """This method validates that the user insert a valid numeric input"""
        if user_input.isdigit() and int(user_input) in range(1, len(option_list)+1):
            return True
        elif user_input.lower().strip() == UIConsts.HELP:
            return UIConsts.HELP
        else:
            return cls._handle_invalid_arguments(Logs.INVALID_NUMERIC_INPUT_LOG % (1, len(option_list)))

    @classmethod
    def validate_threshold(cls, threshold):
        """This method validate the threshold that was received from the user"""
        if threshold is None:  # HELP
            return False
        if not threshold.isdigit():
            return cls._handle_invalid_arguments(Logs.INVALID_THRESHOLD_LOG)
        return True

    @classmethod
    def validate_mapper(cls, mapper):
        """This method validate the dictionary that was received by the user.
        The raw input received only strings so we'll have to check the validity of the dictionary"""
        if mapper is None:
            return False
        if mapper:
            mapper = mapper.replace("\'", "\"")
        try:
            json_object = json.loads(mapper)
            if not json_object:
                return cls._handle_invalid_arguments(Logs.EMPTY_MAPPER_LOG)
        except ValueError:
            return cls._handle_invalid_arguments(Logs.INVALID_MAPPER_LOG)
        return cls._validate_json_keys(dict_to_check=json_object)

    @classmethod
    def _validate_json_keys(cls, dict_to_check):
        """This method validates that all of the keys in the json are valid hex expressions"""
        invalid_hex_values = []
        for key in dict_to_check:
            try:
                bytes.fromhex(key)
            except ValueError:
                invalid_hex_values.append(key)
        if len(invalid_hex_values) > 0:
            return cls._handle_invalid_arguments(Logs.INVALID_JSON_KEYS_LOG.format(invalid_hex_values))
        return True


class ProgressBarUtil:
    """This class responsible on progress bar during the calculations"""
    MAX_NUMBER_OF_SYMBOL = 50
    PROGRESS_SYMBOL = '='

    @classmethod
    def make_progress(cls, current_index, max_index):
        """This module responsible on the progress bar print"""
        chunk_size = int(max_index / cls.MAX_NUMBER_OF_SYMBOL)
        if chunk_size and current_index % chunk_size == 0:
            current_chunk = (current_index//chunk_size)
            sys.stdout.write('\r')
            sys.stdout.write("[%-50s] %d%%" % (cls.PROGRESS_SYMBOL * current_chunk, min(2 * current_chunk, 100)))
            sys.stdout.flush()
