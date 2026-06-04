#!/usr/bin/python3
""" Script parsing provided log input to aggregate number of HTTP errors"""

import sys  # Required to read standard input either interactive or not.


# GOAL: provide perpettually updated summary of log file size and
#   aggregate count of identified HTTP error codes.
# NOTES:
# - New output should be displayed every 10 lines or when process ends.
# - Lines not respecting expected format will be "skipped" (but counted).


#
# === Chosen architecture for v1 ===
#
# Global dictionary which will store the counters for each supported HTTP code
# supported_http_codes_counts = {200: 0, 201, 0 etc}
# Global variable for file_size
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
