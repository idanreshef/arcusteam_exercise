from arguments_parser import ArgParser
from file_parser import FileParser
from utils import PrintUtils
from constants import Logs


def execute():
    try:
        arguments = ArgParser().parse_args()
        if arguments:
            print("Calculating....\n")
            return FileParser(**arguments).parse_file_and_calculate()
    except KeyboardInterrupt:
        print(PrintUtils.main_screen_format(Logs.SEE_YOU_LATER_LOG))
    except Exception as err:
        print(PrintUtils.error_format(Logs.EXECUTION_FAILED_ERROR.format(err)))
        raise err



if __name__ == '__main__':
    results = execute()
    if results:
        print('\n')
        print(results)
