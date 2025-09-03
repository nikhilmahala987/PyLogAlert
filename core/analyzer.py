
def analyze_log(parsed_log):
    if not parsed_log:
        return {'triggered': False}

    process = parsed_log.get('process_name')
    message = parsed_log.get('message', '') # Using '' as a default avoids errors

    # This is the rule logic, translated directly from the recipe.
    if process == 'sshd' and 'Failed password' in message:
        # If both conditions are true, we return the alert dictionary.
        return {
            'triggered': True,
            'rule_name': 'SSHD Failed Login'
        }

    return {'triggered': False}