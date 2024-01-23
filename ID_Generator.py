import os

file_format = ".json"

def generate_id():
    directory_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'English_Books')
    files = os.listdir(directory_path)
    files = [f for f in files if os.path.isfile(os.path.join(directory_path, f))]
    max_number = 0

    for file in files:
        if file.endswith(file_format):
            try:
                file_number = int(os.path.splitext(file)[0])
                max_number = max(max_number, file_number)
            except ValueError:
                pass

    return max_number + 1
