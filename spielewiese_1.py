# Purpur Tentakel
# Spielewiese 1
# Python 3.10

file = "12233.52415.pdf52634"

file_parts = file.split(".")

print(file_parts)

file_type = file_parts[-1]

print(file_type)

file = file[:-(len(file_type) + 1)]

print(file)