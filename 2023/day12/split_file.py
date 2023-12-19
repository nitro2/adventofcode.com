def write_to_files(input_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()

        # Ensure that the file has at least 1000 lines
        if len(lines) < 1000:
            print("Input file doesn't have 1000 lines.")
            return

        # Writing to 100 smaller files with 10 lines each
        file_count = 100
        lines_per_file = 10

        for i in range(file_count):
            output_file_name = f"input/input_{i+1}.txt"

            with open(output_file_name, 'w') as outfile:
                start_index = i * lines_per_file
                end_index = start_index + lines_per_file

                # Write 10 lines to the output file
                outfile.writelines(lines[start_index:end_index])

            print(f"File '{output_file_name}' written successfully.")

if __name__ == "__main__":
    input_file_name = 'input12.txt'  # Replace this with your input file name
    write_to_files(input_file_name)
