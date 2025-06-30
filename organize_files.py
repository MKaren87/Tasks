import os
import shutil
import argparse
from pathlib import Path

FILE_TYPES = {
    'Documents': ['.doc', '.docx', '.txt', '.odt'],
    'PDFs': ['.pdf'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
    'Spreadsheets': ['.xls', '.xlsx', '.csv'],
    'Presentations': ['.ppt', '.pptx'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Scripts': ['.py', '.js', '.sh', '.bat'],
    'Others': []
}

def get_category(extension):
    for category, extensions in FILE_TYPES.items():
        if extension.lower() in extensions:
            return category
    return 'Others'

def organize_files(source_path):
    for item in os.listdir(source_path):
        file_path = os.path.join(source_path, item)
        if os.path.isfile(file_path):
            ext = Path(file_path).suffix
            category = get_category(ext)
            category_dir = os.path.join(source_path, category)
            os.makedirs(category_dir, exist_ok=True)
            shutil.move(file_path, os.path.join(category_dir, item))

def main():
    parser = argparse.ArgumentParser(description="Organize files by type")
    parser.add_argument("source_dir", help="Path to the source directory")
    args = parser.parse_args()

    if os.path.isdir(args.source_dir):
        organize_files(args.source_dir)
        print(f"Files in '{args.source_dir}' have been organized by type.")
    else:
        print("The specified path is not a directory.")

if __name__ == "__main__":
    main()