from .options_model import OptionsModel


class OptionsController:
    def __init__(self, view: 'FDOptionsScreen', api_client: 'APIClient'):
        self.view = view
        self.api_client = api_client

        self.model = OptionsModel(self.api_client)
        self.view.set_controller(self)
