# core/parser.py
import re

LOG_REGEX = re.compile(
    r"^(?P<timestamp>\w+\s+\d+\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<hostname>\S+)\s+"
    r"(?P<process_name>\w+)(?:\[(?P<pid>\d+)\])?:\s+"
    r"(?P<message>.*)$"
)

# This is a simpler regex just to find an IPv4 address within a message.
IP_REGEX = re.compile(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b")


def parse_log_line(line):
    match = LOG_REGEX.match(line)
    
    if not match:
        # If the line doesn't match our main syslog format, ignore it.
        return None
        
    # Convert the regex match into a dictionary.
    log_data = match.groupdict()
    
    # Now, try to find an IP address within the message part of the log.
    ip_match = IP_REGEX.search(log_data['message'])
    
    if ip_match:
        # If we found an IP, add it to our dictionary.
        log_data['source_ip'] = ip_match.group(1)
    else:
        # Otherwise, set the source_ip to None.
        log_data['source_ip'] = None
        
    return log_data