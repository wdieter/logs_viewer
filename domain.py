import os
from typing import List, Callable
from dataclasses import dataclass

LOG_DIRECTORY = '/var/log'
NOT_SUPPORTED_FILE_TYPE_ERROR = "Error reading file: "

@dataclass
class File:
    file_name: str
    logs: List[str]

    def to_dict(self) -> dict:
        file_dict = {
            'file_name': self.file_name,
            'logs': self.logs
        }
        return file_dict


# todo maybe remove read_file_func as it's not used for testing anymore.
def get_logs(filename: str, n: int, keyword: str, read_file_func: Callable[[str], List[str]]) -> List[File]:
    """
    :param filename: either a file or a directory. if a directory is passed, this function will
        call itself recursively to get all logs from all files under that directory
    :param n: the number of lines to return from each file. Note this does not limit how many logs are
        returned if a directory is passed under filename
    :param keyword: filters log results to lines containing this keyword, case insensitive
    :param read_file_func: a function that takes a filename and produces a list of strings. injecting this dependency
        makes the function much easier to test and makes this function easier to extend
    :return: A list of File objects that match the query parameters.
    """
    list_files = []
    filepath = os.path.join(LOG_DIRECTORY, filename)
    if os.path.isfile(filepath):
        logs: List[str] = tail_log_file(filepath, read_file_func)
        filtered_logs = filter_logs(logs, keyword, n)
        if len(filtered_logs) > 0:
            list_files.append(File(file_name=filepath, logs=filtered_logs))
    elif os.path.isdir(filepath):
        for file in get_all_files(filepath):
            logs: List[File] = get_logs(file, n, keyword, read_file_func)
            list_files.extend(logs)
    else:
        raise FileNotFoundError
    return list_files

# todo add test
def tail_log_file(filepath: str, filereader: Callable[[str], List[str]]) -> List[str]:
    """
    Returns the last n lines from the log file.
    """

    try:
        raw_lines = filereader(filepath)
    except (OSError, UnicodeDecodeError) as error:
        return [f"{NOT_SUPPORTED_FILE_TYPE_ERROR} {error}"]

    # remove new lines from logfile, and new line from the log entries
    cleaned_logs = [log.strip() for log in raw_lines if log != "\n"]

    # return most recent logs first
    cleaned_logs.reverse()

    return cleaned_logs

# todo add test
def filter_logs(log_entries: List[str], keyword: str, n: int) -> List[str]:
    """
    Remove logs that don't contain the keyword or the NOT_SUPPORTED_FILE_TYPE_ERROR
    and limit number of logs by n
    """
    res = []
    for line in log_entries:
        append = False
        if NOT_SUPPORTED_FILE_TYPE_ERROR in line:
            append = True
        if keyword == "":
            append = True
        elif case_insensitive_contains(line, keyword):
            append = True

        if append:
            res.append(line)

    limit_logs_by_n = res[:n]
    return limit_logs_by_n


# Utils below

def case_insensitive_contains(text: str, substring: str) -> bool:
    return substring.lower() in text.lower()


def read_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as file:
        return file.readlines()


def get_all_files(directory: str):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

