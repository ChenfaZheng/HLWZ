

class Spectrum():
    UID = 0

    def __init__(self, name: str=None, details: dict=None) -> None:
        '''
        Base class of spectrums

        Input:
        -----
        name: str
            Name of the moleculer 

        details: dict[key: float, value: float]
            Dict of spectrum's frequency (Hz) and intensity (count/second)

        Return:
        -----
        None
        '''
        self.update_uid()
        self.name = name
        self.details = details

    def update_uid(self) -> None:
        self.uid = Spectrum.UID
        Spectrum.UID += 1

    def get_name(self) -> str:
        return self.name

    def get_intensities(self) -> list[float]:
        return [v for k, v in self.details.items()]

    def get_frequencies(self) -> list[float]:
        return [k for k, v in self.details.items()]

    def get_details(self):
        return self.details.copy()