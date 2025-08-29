class RequestException(Exception):
    pass

class _Session:
    def get(self, *args, **kwargs):
        raise RequestException("requests is not available")

    def post(self, *args, **kwargs):
        raise RequestException("requests is not available")


def get(*args, **kwargs):
    raise RequestException("requests is not available")


def post(*args, **kwargs):
    raise RequestException("requests is not available")


def Session(*args, **kwargs):
    return _Session()
