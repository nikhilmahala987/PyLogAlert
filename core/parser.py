import json
import re
import shlex


# raw_line="Sep 1 10:00:03 main-server sshd[1234]: Disconnecting authenticating user root 185.191.171.13 port 44326 [preauth]"
def parse_log_line(raw_line):
    # Step 1: Clean the input
    clean_line = raw_line.strip()
    
    # Step 2: Skip empty lines
    if not clean_line:
        return None
    
    # Step 3: Try different parsing strategies
    parsed_data = None
    
    # Strategy 1: Try parsing as JSON (most common for modern apps like Wazuh)
    parsed_data = _try_parse_json(clean_line)
    if parsed_data:
        return parsed_data
        
    # Strategy 2: Try parsing as a key-value pair log
    parsed_data = _try_parse_key_value(clean_line)
    if parsed_data:
        return parsed_data
        
    # Strategy 3: Try parsing with a predefined regex pattern
    parsed_data = _try_parse_with_regex(clean_line)
    if parsed_data:
        return parsed_data
        
    # Strategy 4: If all else fails, return the raw line in a structured way
    return {
        'message': clean_line,
        'parse_error': True,
        'raw_line': clean_line
    }

def _try_parse_json(line):
    """Attempts to parse a line as JSON. Returns None if it fails."""
    try:
        log_entry = json.loads(line)
        # Add a marker that this was successfully parsed as JSON
        if isinstance(log_entry, dict):
            log_entry['_parse_format'] = 'json'
        return log_entry
    except json.JSONDecodeError:
        return None
    
    import shlex  # For smart splitting that handles quotes

def _try_parse_key_value(line):
    """
    Attempts to parse key=value pairs. Common in many log formats.
    """
    # Check if the line looks like it has key=value pairs
    if '=' not in line:
        return None
        
    try:
        parsed_dict = {}
        # Use shlex.split to handle quoted values correctly
        parts = shlex.split(line)
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)  # Split on first '=' only
                parsed_dict[key.strip()] = value.strip()
        if parsed_dict:
            parsed_dict['_parse_format'] = 'key_value'
            return parsed_dict
    except ValueError:
        pass
    return None

def _try_parse_with_regex(line):
    """
    Attempts to parse using a predefined regex pattern.
    Example for a common Apache-style log format.
    """
    # Example pattern for a common web server log format
    apache_pattern = r'^(\S+) (\S+) (\S+) \[([\w:/]+\s[+\-]\d{4})\] "(\S+) (\S+)\s*(\S*)\s*" (\d{3}) (\S+)'
    
    match = re.match(apache_pattern, line)
    if match:
        groups = match.groups()
        return {
            'ip_address': groups[0],
            'client_id': groups[1],
            'user_id': groups[2],
            'timestamp': groups[3],
            'http_method': groups[4],
            'request_url': groups[5],
            'http_version': groups[6],
            'status_code': groups[7],
            'response_size': groups[8],
            '_parse_format': 'regex_apache'
        }
    return None
