import time
from flask import current_app

def timeit(method):
    """Method for calculating the time taken."""

    def timed(*args, **kw):
        """Wrapper for calculating the time taken."""
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            current_app.logger.debug(
                "{} {} ms".format(method.__name__, (te - ts) * 1000)
            )
        return result

    return timed

