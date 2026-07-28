class LittleHardHatError(Exception):
    """Eccezione base per tutti gli errori dell'SDK littlehardhat."""

class LittleHardHatConnectionError(LittleHardHatError):
    """Sollevata quando la board non è raggiungibile."""

class LittleHardHatTimeoutError(LittleHardHatError):
    """Sollevata quando la board non risponde entro il timeout."""

class LittleHardHatResponseError(LittleHardHatError):
    """Sollevata quando la board risponde con uno stato di errore HTT."""