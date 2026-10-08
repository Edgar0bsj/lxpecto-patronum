class NivelDeEnsinoError(Exception):
    def __init__(self, message: str, obs: str = None):
        self.message = message
        self.obs = obs
        super().__init__(message)
