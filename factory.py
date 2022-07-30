from objects import Spectrum
from viewer import Figure


class Factory():
    def __init__(self, conf_path=None, conf_args=None):
        assert conf_path or conf_args, 'Either config path or CLI args should be specified.'
        
        