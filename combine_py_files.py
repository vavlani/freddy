import os

def combine_py_files(base_folder, output_file):
    with open(output_file, 'w') as outfile:
        for root, _, files in os.walk(base_folder):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    outfile.write(f"{file_path}\n")
                    with open(file_path, 'r') as infile:
                        outfile.write(infile.read())
                    outfile.write("\n\n")

if __name__ == "__main__":
    base_folder = "./"
    output_file = "combined_files.txt"
    combine_py_files(base_folder, output_file)
