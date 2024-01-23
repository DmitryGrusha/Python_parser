import os

file_format = ".json"
main_file = "id.txt"
split_char = "|"

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


# NEW ID

def create_new_id():
    with open(main_file, 'r') as file:
        ids_list = file.read().split(split_char)
        filtered_list = [item for item in ids_list if item != '']
        if filtered_list:
            last_id = filtered_list[-1]
            int_value = int(last_id)
            new_id = int_value + 1
            return new_id
        else:
            return 1


def save_new_id(new_id):
    initial = False
    with open(main_file, 'r') as file:
        ids_list = file.read()
        if not ids_list:
            initial = True

    with open(main_file, 'a') as file:
        if initial:
            file.write(str(new_id))
        else:
            file.write(split_char + str(new_id))