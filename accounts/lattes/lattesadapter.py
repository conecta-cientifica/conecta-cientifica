class LattesAdapter():
    def __init__(self, lattes_api):
        self.lattes_api = lattes_api

    def __del__(self):
        del self.lattes_api

    def get_lattes_profile(self, lattes_id):
        return self.lattes_api.get_profile_by_lattes_id(lattes_id)