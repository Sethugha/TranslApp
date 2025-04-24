with open('language_code.txt', 'r') as file:
    language_code = file.read()

language_code = language_code.replace("'", '"')

with open('language_code.txt', 'w') as file:
    file.write(language_code)