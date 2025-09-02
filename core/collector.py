def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Yield the line, stripping whitespace (like newline characters)
                yield line.strip()
    except FileNotFoundError:
        print(f"Error: The log file was not found at {file_path}")
        # Re-raise the exception to halt execution, or yield nothing
        raise
    except IOError as e:
        print(f"Error: Could not read the file {file_path}. {e}")
        raise