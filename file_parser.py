
from constants import OutputConsts, ArgsConsts, UIConsts
from utils import ProgressBarUtil
import os


class FileParser:
    """This class is being used only after all of the arguments were validated, so this is
    an important prerequisite. It parses the binary file and calculates the results
    according to the mode and other arguments that were given by the user"""

    def __init__(self, **kwargs):
        self.mode = kwargs.get(ArgsConsts.MODE)
        self.file_path = kwargs.get(ArgsConsts.FILE_PATH)
        self.threshold = kwargs.get(ArgsConsts.THRESHOLD)
        self.mapper = kwargs.get(ArgsConsts.MAPPER)
        self.regex_pattern = kwargs.get(ArgsConsts.REGEX_PATTERN)

    def parse_file_and_calculate(self):
        """This method parses the binary file and calculates the results"""
        if self.mode == UIConsts.BASIC_MODE:
            return self._handle_basic_mode()
        elif self.mode == UIConsts.CUSTOM_MODE:
            return self._handle_custom_mode()
        else:  # Regex Mode
            requested_prefix, additional_bytes_length, comparator_type = self._prepare_args_for_regex_mode()
            return self._handle_regex_mode(requested_prefix, additional_bytes_length, comparator_type)

    def _handle_basic_mode(self):
        """This method parses the file and looks for repeating bytes sequences that
        are greater than the threshold argument"""
        results = []
        file_size = os.stat(self.file_path).st_size
        with open(self.file_path, mode='rb') as f:
            sequence_length, location = 0, 1
            byte = f.read(1)
            while byte:
                previous_byte = byte
                byte = f.read(1)
                location += 1
                if previous_byte == byte:
                    sequence_length += 1
                else:
                    if sequence_length >= self.threshold:
                        results.append(self._create_basic_result_record(previous_byte, location - 1, sequence_length))
                    sequence_length = 0
                ProgressBarUtil.make_progress(location, file_size)
        return {ArgsConsts.MODE: self.mode, OutputConsts.RESULTS: results}

    @staticmethod
    def _create_basic_result_record(byte, end_location_idx, sequence_length):
        """This method creates the result dictionary in the expected structure with
         the expected arguments for the basic mode"""
        sequence_range = (end_location_idx-sequence_length, end_location_idx)
        result = {OutputConsts.RANGE: sequence_range, OutputConsts.SIZE: sequence_length, OutputConsts.REP_BYTE: byte}
        return result

    def _prepare_args_for_regex_mode(self):
        """This method gets the expected regex structure from the user and returns a tuple with
        the requested prefix and the requested bytes length to find.
        There's a special case in case the user enters an Hex prefix (E.g: '\x00XXX), since the
        raw input gets it an a string and parses it in a different way. So this method checks for
        that and returns a prefix_bytes in a str type in this case, else it returns a byte.
        E.g: If the input will be: '\x00XXX' the return value will be ('00', 3).\
        In case the input will be: 'C123XX' the return value will be (b'C123', 2) """
        for index in range(len(self.regex_pattern)-1, -1, -1):
            if self.regex_pattern[index] != ArgsConsts.REGEX_SYMBOL:
                last_byte_prefix = index + 1
                prefix_bytes = self.regex_pattern[:last_byte_prefix]
                additional_bytes_length = len(self.regex_pattern[last_byte_prefix:])
                if prefix_bytes.startswith('\\x'):
                    prefix_bytes = prefix_bytes.strip('\\x')
                else:
                    prefix_bytes = prefix_bytes.encode()
                return prefix_bytes, additional_bytes_length, type(prefix_bytes)

    def _handle_regex_mode(self, requested_prefix, additional_bytes_length, comparator_type=bytes):
        """
        This method looks for all of the bytes that started with the prefix that was
        received by the user and saves all of the bytes sequence that starts with the requested prefix and
        that in the requested length.
        :param requested_prefix: The bytes prefix that we should look after
        :param additional_bytes_length: The additional bytes length that we should save in case we found
        the @param requested_prefix.
        :param comparator_type: There is a challenging situation if the user enters a prefix that starts with a "/".
        In this case we will compare strings and not bytes in order to support this.
        :return: A dictionary with the results: The mode and all the of the bytes array that fits the arguments
        """
        results = []
        with open(self.file_path, mode='rb') as f:
            bytes_stream = f.read()
        for i in range(len(bytes_stream)-1):
            current_byte = bytes_stream[i: i+1].hex() if comparator_type == str else bytes_stream[i: i+1]
            if current_byte == requested_prefix:
                results.append(bytes_stream[i: i + 1 + additional_bytes_length])
            ProgressBarUtil.make_progress(i, len(bytes_stream)-1)
        return {ArgsConsts.MODE: self.mode, OutputConsts.RESULTS: results}

    def _handle_custom_mode(self):
        """This method finds all of the appearances of the required hex strings in the file.
        First, it converts the hex string into a bytes array and than counts the number of time that it
        could be found in the file"""
        results = dict()
        with open(self.file_path, mode='rb') as f:
            bytes_stream = f.read()
        for hex_string, regular_expression in self.mapper.items():
            bytes_exp = bytes.fromhex(hex_string)
            counter, location = -1, 0
            while location != -1:
                location = bytes_stream.find(bytes_exp, location + 1)
                counter += 1
            results[regular_expression] = counter
        return {ArgsConsts.MODE: self.mode, OutputConsts.RESULTS: results}
