import os
from typing import List
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


def get_logs(filename: str, n: int, keyword: str) -> List[File]:
    """
    :param filename: either a file or a directory. if a directory is passed, this function will
        call itself recursively to get all logs from all files under that directory
    :param n: the number of lines to return from each file. Note this does not limit how many logs are
        returned if a directory is passed under filename
    :param keyword: filters log results to lines containing this keyword, case insensitive
    :return: A list of File objects that match the query parameters.

    aim to return n lines to the client. This means scanning the file from the bottom, and reading until we:
        - have n lines that match the keyword (if provided)
        - or have scanned the whole file
    """
    list_files = []
    filepath = os.path.join(LOG_DIRECTORY, filename)
    if os.path.isfile(filepath):
        logs_generator = reverse_readline(filepath)
        filtered_logs = filter_logs(logs_generator, keyword, n)
        if len(filtered_logs) > 0:
            list_files.append(File(file_name=filepath, logs=filtered_logs))
    elif os.path.isdir(filepath):
        for file in get_all_files(filepath):
            logs: List[File] = get_logs(file, n, keyword)
            list_files.extend(logs)
    else:
        raise FileNotFoundError
    return list_files


def filter_logs(log_entries, keyword: str, n: int) -> List[str]:
    """
    attempt to return n logs that match the keyword if set
    """
    res = []
    while len(res) < n:
        try:
            line: str = next(log_entries)
            if keyword != "":
                if case_insensitive_contains(line, keyword):
                    res.append(line)
            else:
                res.append(line)
        except StopIteration:
            return res
        except (OSError, UnicodeDecodeError) as error:
            return [f"{NOT_SUPPORTED_FILE_TYPE_ERROR} {error}"]
    return res


# Utils below

def case_insensitive_contains(text: str, substring: str) -> bool:
    return substring.lower() in text.lower()


def read_file(filepath: str) -> List[str]:
    with open(filepath, 'r') as file:
        return file.readlines()


def reverse_readline(filename: str, buf_size=8192):
    """
    A generator that returns the lines of a file in reverse order.
    reads from the file in reverse order in chunks of size `buf_size`.
    This allows us to read arbitrarily large files in a memory efficient way.
    copied from: https://stackoverflow.com/questions/2301789/how-to-read-a-file-in-reverse-order
    """

    with open(filename, 'rb') as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        file_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(file_size, offset + buf_size)
            fh.seek(file_size - offset)
            buffer = fh.read(min(remaining_size, buf_size))
            # remove file's last "\n" if it exists, only for the first buffer
            if remaining_size == file_size and buffer[-1] == ord('\n'):
                buffer = buffer[:-1]
            remaining_size -= buf_size
            lines = buffer.split('\n'.encode())
            # append last chunk's segment to this chunk's last line
            if segment is not None:
                lines[-1] += segment
            segment = lines[0]
            lines = lines[1:]
            # yield lines in this chunk except the segment
            for line in reversed(lines):
                # only decode on a parsed line, to avoid utf-8 decode error
                yield line.decode()
        # Don't yield None if the file was empty
        if segment is not None:
            yield segment.decode()


def get_all_files(directory: str):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

