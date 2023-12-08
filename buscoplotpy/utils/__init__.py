# File: __init__.py

# Questo può essere vuoto se non hai bisogno di eseguire alcuna inizializzazione specifica.
# Tuttavia, spesso vengono inseriti import di moduli o variabili qui.

# Esempio: importare un modulo
from load_busco_fulltable import load_busco_fulltable
from load_json_summary import load_json_summary

# Esempio: importare una funzione da un modulo all'interno del pacchetto
class MyClass:
    def __init__(self, version):
        """
        Initializes an instance of MyClass with the given version.

        Args:
            version (str): The version number of the instance.
        """
        self.version = version
# Esempio: definire una variabile
versione = "1.0"

# Esempio: eseguire un'azione all'importazione del pacchetto
print("Il pacchetto è stato importato!")