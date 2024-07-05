from csv import DictReader;
from os import walk;
from shutil import copyfile;
from configparser import ConfigParser
def main():
    config = ConfigParser()
    config.read("config.ini")
    # CSV Filter config
    CSV_NAME = config.get("CSV", "name")
    FIELD = config.get("CSV", "field")
    VALUE = config.get("CSV", "value")

    # Image config
    IMAGE_DIR = config.get("IMAGE", "dir")
    IMAGE_FORMAT = config.get("IMAGE", "format")

    # Output config
    OUTPUT_DIR = config.get("OUTPUT", "dir")

    image_numbers = filter_csv(CSV_NAME, FIELD, VALUE) # Filter csv to get ID's and names

    images = get_images(IMAGE_DIR, IMAGE_FORMAT, OUTPUT_DIR, image_numbers) # Filter through image directory to get source and dest paths

    copy_files(images, OUTPUT_DIR) # copy files into destination paths

def filter_csv(csv_name, filter_field, filter_value):
    csv_file = open(csv_name, newline='')
    csv_reader = DictReader(csv_file)
    numbers = {}
    for row in csv_reader:
        if row[filter_field] == filter_value:
            numbers[row["Main ID"]] = row["Name"].replace(",", "").replace(" ", "") # This is an additional data i want to extract so it's hardcoded
    return numbers
def get_images(image_dir, image_format, output_dir, image_numbers):
    results = {}
    notfound_count = 0
    count = 0 
    for id in image_numbers:
        for root, dir, files in walk(image_dir):
            if (id + image_format) in files:
                results[(image_dir + "/" + id + image_format)] = f"{output_dir}/{image_numbers[id]}_{id + image_format}"
                count +=1
            else:
                notfound_count += 1
                print(f"Image not found for {id}!")

    print(f"Found images for {count} members. {notfound_count} did not have an image available")
    auth = input("Type 'y' to continue: ")
    if auth == 'y':
        return(results)
    else:
        print("Exiting")
        exit(0)

def copy_files(file_ops, output): #takes a dictionary with the key as the source and the value as the destination 
    for file in file_ops:
        print(file)
    print(f"These files will be copied to the folder: {output}")
    auth = input("Type 'y' to confirm the copy of these files: ")
    if auth == 'y':
        for file in file_ops:
            copyfile(file, file_ops[file])
    else:
        print("Exiting")

if __name__ == "__main__":
    main()