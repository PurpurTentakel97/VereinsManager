# Purpur Tentakel
# Spielewiese 3
# Python 3.10


test: str = "<name> ist ein Bauarbeiter"
if "<name>" in test:
    print("yes")
else:
    print("no")
print(test)
test = test.replace("<name>", "Hans-Peter")
print(test)
test = test.replace("<job>", "Müller")
print(test)


