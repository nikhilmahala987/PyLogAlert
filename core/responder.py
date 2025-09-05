import subprocess
import json
import sys

def trigger_playbook(playbook_name, alert_data):
    """
    Executes a playbook script safely using subprocess.

    Args:
        playbook_name (str): The filename of the playbook in the /playbooks folder.
        alert_data (dict): The dictionary containing alert details.
    """
    try:
        # Construct the full path to the playbook.
        playbook_path = f"playbooks/{playbook_name}"

        # Safely serialize the alert dictionary into a JSON string.
        alert_json_string = json.dumps(alert_data)

        # Build the command as a LIST of arguments. This is the most secure way
        # to call a subprocess and prevents command injection vulnerabilities.
        command = [
            sys.executable,      # The path to the current Python interpreter
            playbook_path,       # The script to run
            alert_json_string    # The data, passed as a single argument
        ]

        # For debugging, it's helpful to see the command you're running.
        # print(f"DEBUG: Running command: {command}")

        # Execute the command.
        result = subprocess.run(
            command,
            capture_output=True,  # Capture the script's print statements
            text=True,            # Decode the output as text
            check=True            # If the script fails, raise an exception
        )
        
        # Print the output from the playbook script if it was successful.
        print(result.stdout)

    except FileNotFoundError:
        print(f"ERROR: Responder failed. Playbook '{playbook_path}' not found.")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Playbook '{playbook_path}' failed with an error.")
        print(f"--- Playbook's Error Output ---\n{e.stderr}")
    except Exception as e:
        print(f"An unexpected error occurred in the responder: {e}")