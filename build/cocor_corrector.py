import re
import os

root_dir = os.getcwd()
full_path = os.path.join("..", "src", "parser", "Parser.py")
absolute_path = os.path.join(root_dir, full_path)

input_file = absolute_path
output_file = absolute_path

with open(input_file, "r") as file:
    content = file.read()

pattern = r"self.VeKrestKrest()"
replacement = "return self.VeKrestKrest()"
modified_content = re.sub(pattern, replacement, content)

pattern = r"from AstTree import"
replacement = "from parser.AstTree import"
modified_content = re.sub(pattern, replacement, modified_content)

pattern = r"from Scanner import"
replacement = "from parser.Scanner import"
modified_content = re.sub(pattern, replacement, modified_content)

with open(output_file, "w") as file:
    file.write(modified_content)
