from constants import UIConsts, Logs, ArgsConsts
from utils import PrintUtils, ValidationUtil
import json
import os


class ArgParser:
    """This class interacts with the user in order to receive, validate and parse the arguments
    for the patterns calculation."""

    def __init__(self):
        self.num_of_attempts = 3
        self.arguments = dict()

    def parse_args(self):
        """This method manages the entire section in front of the user"""
        is_valid = self._general_argument_parser(UIConsts.MANDATORY)
        if is_valid:
            is_valid = self._general_argument_parser(self.arguments[ArgsConsts.MODE])
        if not is_valid:
            print(PrintUtils.error_format(Logs.MAX_ATTEMPTS_ERROR_LOG))
            return None
        return self.arguments

    def _general_argument_parser(self, args_group):
        """This method handles different groups of arguments parsing.
        It provides any args group three attempts to get the valid arguments from the user."""
        parser_handler = {UIConsts.MANDATORY: self._parse_mandatory_arguments,
                          UIConsts.BASIC_MODE: self._parse_basic_mode_arguments,
                          UIConsts.REGEX_MODE: self._parse_regex_mode_arguments,
                          UIConsts.CUSTOM_MODE: self._parse_custom_mode_arguments}
        while self.num_of_attempts > 0:
            is_valid = parser_handler[args_group]()
            if not is_valid:
                continue
            else:
                self.num_of_attempts = 3
                return True
        return False

    def _parse_mandatory_arguments(self):
        """This method parses the two basic arguments that are relevant for
        all of the modes: The mode and the file path"""
        mode = self._present_option_to_choose(UIConsts.MODE, UIConsts.MODE_OPTIONS, UIConsts.EXPLAIN_MODES)
        if mode is None:  # Invalid value
            self.num_of_attempts -= 1
            return False
        self.arguments[ArgsConsts.MODE] = mode
        file_path = self._get_file_path()
        if file_path is None:
            self.num_of_attempts -= 1
            return False
        self.arguments[ArgsConsts.FILE_PATH] = file_path
        return True

    def _parse_basic_mode_arguments(self):
        """This method parses the relevant arguments for the basic mode"""
        threshold = self._present_option_to_choose(ArgsConsts.THRESHOLD)
        if not ValidationUtil.validate_threshold(threshold):
            self.num_of_attempts -= 1
            return False
        self.arguments[ArgsConsts.THRESHOLD] = int(threshold)
        return True

    def _parse_custom_mode_arguments(self):
        """This method parses the relevant arguments for the custom mode"""
        mapper = self._present_option_to_choose(ArgsConsts.DICTIONARY_MAPPER)
        if not ValidationUtil.validate_mapper(mapper):
            self.num_of_attempts -= 1
            return False
        mapper = mapper.replace("\'", "\"")
        self.arguments[ArgsConsts.MAPPER] = json.loads(mapper)
        return True

    def _parse_regex_mode_arguments(self):
        """
        This method parses the relevant arguments for the regex mode.
        The regex pattern must be in the following structure: 'relevant-byte-prefixXXXX'. E.g: \x01XX
        (Requested bytes prefix and than X symbols in order to get the required structure and length)
        """
        regex_pattern = self._present_option_to_choose(ArgsConsts.REGEX_PATTERN)
        if not ValidationUtil.validate_regex_pattern(regex_pattern):  # Invalid regex pattern
            self.num_of_attempts -= 1
            return False
        self.arguments[ArgsConsts.REGEX_PATTERN] = regex_pattern
        return True

    def _present_option_to_choose(self, title, options_list=None, explanation_dict=None):
        """
        This method presents the current arguments that need to be retrieved by the user.
        :param title: The input request that will displayed on the CLI. E.g: `file path`
        :param options_list: A list with options to display
        :param explanation_dict: A dictionary with message per option to present
        :rtype: str with the received input, in case of an error or help request None value will be returned
        """
        self._print_welcome_message()
        user_input = self._print_selections_and_get_input(title, options_list, explanation_dict)
        if user_input is not None and user_input.lower().strip() == UIConsts.HELP:
            self._handle_help_request()
            return None
        return user_input

    def _handle_help_request(self):
        """This method handles help request. It presents the help file and waits for the
        user's response (Enter to continue or Ctrl + C to exit)."""
        os.system('clear')
        self.num_of_attempts += 1  # This is not a failed attempt but we'll restart the process
        with open(UIConsts.HELP_FILE_PATH) as f:
            for d in f.read().split("\n"):
                print(d)
        input(Logs.EXIT_HELP_SCREEN_MESSAGE)

    def _get_file_path(self):
        file_path = self._present_option_to_choose("file path")
        return file_path if ValidationUtil.validate_file_path(file_path) else None

    @staticmethod
    def _print_welcome_message():
        os.system('clear')
        with open(UIConsts.MAIN_SCREEN_FILE_PATH) as f:
            for d in f.read().split("\n"):
                print(PrintUtils.main_screen_format(d))

    def _print_selections_and_get_input(self, title, option_list=None, explanation_dict=None):
        """
        This method responsible for every interaction with the user in order to get the arguments.
        It support both closed options (choice from a limited list) and raw input
        :param title: The name of the arguments that is being retrieved
        :param option_list: A list with string options to choose (E.g: ['opt1', 'opt2', 'opt3']
        :param explanation_dict: A dictionary that maps an explanation for every option
        :return: The user's input
        """
        if option_list is not None:
            if title:
                print(PrintUtils.header_format("Please choose a {}\n".format(title)))
            for index, option in enumerate(option_list):
                print("\t{0}. {1}   {2}".format(index+1, option, explanation_dict.get(option)))
            user_input = input(Logs.NUMERIC_SELECTION_MESSAGE % (1, len(option_list))).strip()
            return self._handle_numeric_user_input_section(user_input, option_list)
        else:
            user_input = input("\nPlease insert a {}: ".format(title)).strip()
            return user_input

    @staticmethod
    def _handle_numeric_user_input_section(user_input, option_list):
        """This method handles numeric options during input retrieving"""
        if ValidationUtil.validate_numeric_input(user_input, option_list):
            return option_list[int(user_input) - 1] if user_input.lower().strip() != UIConsts.HELP else user_input
        return None
