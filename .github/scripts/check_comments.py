import os
import sys

def calculate_comment_percentage(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        total_lines = 0
        comment_lines = 0
        for line in file:
            total_lines += 1
            if line.strip().startswith('#'):
                comment_lines += 1
        if total_lines == 0:
            return 0  # Avoid division by zero
        return (comment_lines / total_lines) * 100

def process_folder(folder_path):
    desired_comment_percentage = 20.0
    print(f"Every file should have at least {desired_comment_percentage:.2f}% of lines commented.")

    total_comment_percentage = 0
    total_files = 0
    successful_check = True;

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):  # You can adjust the file extension as needed
                file_path = os.path.join(root, file)
                comment_percentage = calculate_comment_percentage(file_path)
                print(f"{file}: {comment_percentage:.2f}%")
                total_comment_percentage += comment_percentage
                if comment_percentage < desired_comment_percentage:
                    successful_check = False

                total_files += 1
                

    if total_files == 0:
        print("No Python files found in the specified folder.")
    else:
        average_comment_percentage = total_comment_percentage / total_files
        print(f"\nAverage Comment Percentage: {average_comment_percentage:.2f}%")
        if successful_check == False:
            print(f"\nAt least one file had less than {desired_comment_percentage:.2f}% of commented lines.\nPlease be sure to add proper documentation to those files.")
            exit(1) # Should fail the CI?

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_path>")
        sys.exit(1)

    folder_path = sys.argv[1]
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        sys.exit(1)

    process_folder(folder_path)
