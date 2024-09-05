import re
import os

def get_file_path( file_name , ext = ".html" , dir = "./files") -> str:
    for file in os.listdir(dir):
        if file.endswith(ext):
            if file == file_name+ext:
                return os.path.join(dir, file)
    return None

def find_files(HTTP_request) -> list[str]:
    files = re.findall(  r"(?<=GET \/).*?(?= HTTP)", HTTP_request )
    return files
