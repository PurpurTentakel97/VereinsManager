# Purpur Tentakel
# Spielewiese 3
# Python 3.10

entry = input("Hier input eingeben\n")

print(entry)

try:
    entry = int(entry)
    print(entry)

except ValueError:
    print("invalider Input")
