# Purpur Tentakel
# Spielewiese 1
# Python 3.10

self.organisation_data = {
    'ID': 2,
    'name': '1 FC. Hinkebein Nord-West 2.Manschaft Herren',
    'street': 'Straße',
    'number': '23a',
    'zip_code': '5211445',
    'city': 'Musterstadt',
    'country': 'Deutschland',
    'bank_name': 'Superbank',
    'bank_owner': 'Mathes Müller',
    'bank_IBAN': 'DE ganz viele Zahlen',
    'bank_BIC': 'DEIIHNFGT536',
    'contact_person': (2, 'Anyway', 'Hannes'),
    'web_link': 'www.link.de',
    'extra_text': '** Deutscher Meister 1967 **\n** Juniorenmeister NRW 2006 **'
}

ID = self.organisation_data['contact_person'][0]  # Expected type 'int', got 'str' instead
