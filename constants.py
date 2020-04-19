import os


class ArgsConsts:
    MODE = 'mode'
    FILE_PATH = 'file_path'
    THRESHOLD = 'threshold'
    MAPPER = 'mapper'
    REGEX_SYMBOL = 'X'
    REGEX_PATTERN = 'bytes regex pattern'
    DICTIONARY_MAPPER = 'dictionary mapper (without new line between records)'


class UIConsts:
    RESOURCES_DIR = 'resources'
    MAIN_SCREEN_FILE_NAME = 'main_screen.txt'
    HELP_FILE_NAME = 'help_screen.txt'
    RESOURCES_PATH = os.path.realpath(RESOURCES_DIR)
    MAIN_SCREEN_FILE_PATH = os.path.join(os.path.dirname(__file__), RESOURCES_DIR, MAIN_SCREEN_FILE_NAME)
    HELP_FILE_PATH = os.path.join(os.path.dirname(__file__), RESOURCES_DIR, HELP_FILE_NAME)

    HELP = 'help'
    MODE = 'mode'
    MANDATORY = 'Mandatory Arguments'
    BASIC_MODE = 'Basic mode'
    CUSTOM_MODE = 'Custom mode'
    REGEX_MODE = 'Regex mode'
    MODE_OPTIONS = [BASIC_MODE, REGEX_MODE, CUSTOM_MODE]
    EXPLAIN_MODES = {BASIC_MODE: "(Find repeating sequence against a threshold)",
                     CUSTOM_MODE: "(Insert custom bytes json streams to locate)",
                     REGEX_MODE: "(Get matching bytes by prefix and a structure)"}


class COLORS:
    BLUE = '\033[94m'
    RED_BACKGROUND = '\033[41m'
    YELLOW = '\033[33m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


class Logs:
    INVALID_NUMERIC_INPUT_LOG = "\nInvalid input! The input must be a number between %d and %d."
    NUMERIC_SELECTION_MESSAGE = "\nPlease select one of the following options (%d-%d): "
    MAX_ATTEMPTS_ERROR_LOG = "There were too many failed attempts. Exiting..."
    MISSING_FILE_LOG = "Could not find the following file path: {}.\n"
    EMPTY_FILE_LOG = "This file is empty! Please provide a valid file.\n"
    EXIT_HELP_SCREEN_MESSAGE = "\nPlease press ENTER in order to continue\n"
    SHORT_REGEX_PATTERN_ERROR = "The regex pattern's length must be at least 2!"
    REGEX_INVALID_SUFFIX_ERROR = "Invalid suffix for the regex pattern! It must end with '{}'".format(
        ArgsConsts.REGEX_SYMBOL)
    INVALID_REGEX_STRUCTURE_ERROR = "The regex pattern must contain some bytes prefix"
    INVALID_THRESHOLD_LOG = "Invalid threshold! It must be a valid number"
    INVALID_MAPPER_LOG = "Invalid dictionary mapper! Please note that although the input is being\n" \
                         "retrieved as a string, the dictionary have to be in the expected structure."
    EMPTY_MAPPER_LOG = "The mapper must contain at least one key and value!"
    EXECUTION_FAILED_ERROR = "The execution failed due to the following error: {}\n"
    SEE_YOU_LATER_LOG = "\nSee you later!"
    INVALID_JSON_KEYS_LOG = "The following keys are invalid hex expressions: {}\n"


class OutputConsts:
    RESULTS = 'results'
    RANGE = 'range'
    SIZE = 'size'
    REP_BYTE = 'repeating_byte'
