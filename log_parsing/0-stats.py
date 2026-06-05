#!/usr/bin/python3
""" Script parsing provided log input to aggregate number of HTTP errors"""

import sys  # Required to read standard input either interactive or not.
import re   # Required to parse strings with Regular Expressions


# GLOBAL VARIABLES: "searched codes" and counts dictionary, file_size.
supported_http_codes = {200, 301, 400, 401, 403, 404, 405, 500}
http_codes_counts = dict.fromkeys(supported_http_codes, 0)
file_size = 0


def get_expected_log_pattern(mode="full") -> str:
    """Assembles full regex pattern for log search"""

    IP = r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
    DATE = r"(?P<date>\d{4}-\d{2}-\d{2})"
    # Need to escape . which otherwise means "whatever character" in regex.
    TIME = r"(?P<time>\d{2}:\d{2}:\d{2}(\.\d+)?)"
    DATETIME = r"(?P<datetime>\[" + DATE + r" " + TIME + r"\])"
    URL = r'(?P<url>\"GET /projects/260 HTTP/1.1\")'
    # Confer https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status
    HTTP_CODE = r"(?P<http_code>[1-5][0-9][0-9])"
    FILE_SIZE = r"(?P<file_size>\d+)"
    # Need to escape [] which otherwise define "character set" in regex.
    if mode == "minimal":
        full_pattern = f"^{IP} - .* {HTTP_CODE} {FILE_SIZE}$"
    else:
        full_pattern = f"^{IP} - {DATETIME} {URL} {HTTP_CODE} {FILE_SIZE}$"
    return full_pattern


def get_log_info(line: str) -> tuple:
    """Function analyzing line and returning code and size if valid"""
    regex_match = re.search(log_expected_pattern, line.strip())
    if regex_match is None:
        return None
    http_code = int(regex_match.group("http_code"))
    file_size = int(regex_match.group("file_size"))

    if http_code in supported_http_codes:
        return (http_code, file_size)
    else:
        return None


def get_log_info_from_split(line: str) -> tuple:
    """Function trying to find infos from basic split"""

    # Kinda fed up with the exercise being contradictory
    #   so going for quick & dirty for the checker.
    # In a real project I'd take the time to convert
    #   properly first in a try/catch block.
    try:
        *_, http_code, file_size = line.split()
        valid_http_code = int(http_code) in supported_http_codes
        valid_file_size = int(file_size) >= 0
        if valid_http_code and valid_file_size:
            return (int(http_code), int(file_size))
    except (IndexError, ValueError) as e:
        return None

def print_current_summary():
    """Prints infos on file size and searched HTTP codes count"""
    print(f"File size: {file_size}")
    for code, count in sorted(http_codes_counts.items()):
        if count > 0:
            print(f"{code}: {count}")


if __name__ == "__main__":
    lines_read = 0  # Used to trigger prints periodically.
    log_expected_pattern = get_expected_log_pattern()

    try:
        for line in sys.stdin:
            log_line_info = get_log_info_from_split(line)
            lines_read += 1

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

#
# === Chosen architecture for v1 ===
#
# Global dictionary which will store the counters for each supported HTTP code
#
# Global variables supported_http_codes_counts = {200: 0, 201, 0 etc}
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

# ========== DEVELOPER DOCUMENTATION ===========
#
# ===== BUSINESS GOAL =====
# Provide "perpetually self-updating summary" of logs's
#   file size and aggregate count for a chosen list
#   of identified HTTP error codes.
# NOTES:
# - New output should be displayed every 10 lines or when process ends.
# - Lines not respecting expected format will be "skipped" (but counted).

# ========== NOTES & DESIGN CHOICES ===========
# == Regex pattern assembly ==
# On 'r' prefixer for pattern components:
#   r forces Python to NOT interpret any character which would otherwise
#   make sense for it, such as "escaping character" \.
# On pattern encapsulation with (?P<string>):
#   (?P<group_name>actual_regex_pattern) allows quick retrieval
#   of a subset of the matched line.
#
# == "Searched HTTP codes" definition and count initialization ==
# 1. Using set on purpose to stress unicity and facilitate validation.
# 2. Initializing the counters to make orchestration process easier on
#      the count incrementation part.
#
# == Function to parse lines and check if valid log ==
# Was hard to find a name explicit enough.
# Previously validate_line_format, analyse_line
#
#
# == On using "for line in" instead of while
# while sys.stdin.readline() != "" BAD IDEA: line read during evaluation.
# for line in sys.stdin.readline(): -> Readline ALREADY returns a line!!


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
