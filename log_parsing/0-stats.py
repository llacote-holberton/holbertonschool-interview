#!/usr/bin/python3
""" Script parsing provided log input to aggregate number of HTTP errors"""

import sys  # Required to read standard input either interactive or not.
import re   # Required to parse strings with Regular Expressions

# GOAL: provide perpettually updated summary of log file size and
#   aggregate count of identified HTTP error codes.
# NOTES:
# - New output should be displayed every 10 lines or when process ends.
# - Lines not respecting expected format will be "skipped" (but counted).

# GLOBAL VARIABLES
# 1. Set defining the only HTTP codes we are interested in.
#    Using set on purpose to stress unicity and facilitate validation.
supported_http_codes = {200, 301, 400, 401, 403, 404, 405, 500}
# 2. Initializing the counters
http_codes_counts = dict.fromkeys(supported_http_codes, 0)
# 3. Initializing the file size
file_size = 0


def get_expected_log_pattern():
    # r forces Python to NOT interpret any character which would otherwise
    #   make sense for it, such as "escaping character" \.

    # IMPORTANT: (?P<group_name>actual_regex_pattern) allows quick retrieval
    #   of a subset of the matched line.
    IP = r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    DATE = r"(?P<date>\d{4}-\d{2}-\d{2})"
    # Need to escape . which otherwise means "whatever character" in regex.
    TIME = r"(?P<time>\d{2}:\d{2}:\d{2}\.\d+)"
    URL = r'(?P<url>\"GET /projects/260 HTTP/1.1\")'
    # Confer https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
    HTTP_CODE = r"(?P<http_code>[1-5][0-9][0-9])"
    FILE_SIZE = r"(?P<file_size>\d+)"
    # Need to escape [] which otherwise define "character set" in regex.
    full_pattern = f"^{IP} - \[{DATE} {TIME}\] {URL} {HTTP_CODE} {FILE_SIZE}$"
    return full_pattern

# Previously validate_line_format, analyse_line
def get_log_info(line: string) -> False|(error_code, file_size):
    regex_match = re.search(log_expected_pattern, line)
    if regex_match is None:
        return False
    http_code = int(regex_match.group("http_code"))
    file_size = int(regex_match.group("file_size"))
    # print(f"@dev: Found: {http_code}, {file_size}")
    # print(supported_http_codes)
    if http_code in supported_http_codes:
        return (http_code, file_size)
    else:
        return False


def print_current_summary():
    print(f"File size: {file_size}")
    for code, count in sorted(http_codes_counts.items()):
        print(f"{code}: {count}")


if __name__ == "__main__":
    # Counter to keep track of log lines analyzed.
    lines_read = 0
    log_expected_pattern = get_expected_log_pattern()

    try:
        # while sys.stdin.readline() != "" BAD IDEA: line read during evaluation.
        # for line in sys.stdin.readline(): -> Readline ALREADY returns a line!!
        for line in sys.stdin:
            # print("This is the line read:\n", line)
            log_line_info = get_log_info(line)
            lines_read += 1
            # print(log_line_info)
            if isinstance(log_line_info, tuple):
                code = log_line_info[0]
                size = log_line_info[1]
                http_codes_counts[code] += 1
                file_size += size
            if lines_read % 10 == 0:
                print_current_summary()
    except KeyboardInterrupt:
        pass
    finally:
        print_current_summary()
        # print("End of script")
#
# === Chosen architecture for v1 ===
#
# Global dictionary which will store the counters for each supported HTTP code
# 
# Global variable for file_sizesupported_http_codes_counts = {200: 0, 201, 0 etc}
# file_size = 0
# Global variable for line read validation (regex)
# -> Made global for readability and ease of maintenance, but could be argued.
# log_expected_pattern
#
# Function analyzing line, directly returning the two informations we want
#   if line matches formatting requirements, thanks to regex "subgroups"
#   (I do hope Python supports it xd)
# validate_line_format(line: string) -> None|(error_code, file_size)
#
# Function charged to create a formatted print to summarize current counts
# print_summary()
#
# Orchestrator function (also charged for a final print
#   when script ends for whatever reason)
# main()

# ========== BRAINSTORMING ============
# === Architecture exploration ===
# validate_line_format(line: string): function to check line format
#   -> keep or skip.
#   directly return a tuple of error code and file size since it already had
#   to analyse everything?
# aggregate_errors(error_code): function to keep track of all errors,
#   return current count for error code after incrementing?
# aggregate_filesize(added_filesize): same for file size?
# main: orchestrator checking if atty, setting the loop in which...
#   - read line by line and send it to validate_line
#   - on success trigger other functions, in both cases increment line count
#   - catches exception "keyboard interrupt" and EOL
#   - ensures input closed properly and last lines outputted before closing.
#
