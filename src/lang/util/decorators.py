"""
Lang Project Decorators Module in util.

Version: 2024.07.10.01
"""

import time


class Timer:
    """Timer Decorator Class."""

    @staticmethod
    def fxn_run(fxn):
        """Get the running time of a function."""

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = fxn(*args, **kwargs)
            Timer.helper_run_time(args, fxn, start_time)
            return result

        return wrapper

    @staticmethod
    def afxn_run(fxn):
        """Get the running time of an async function."""

        async def wrapper(*args, **kwargs):
            start_time = time.time()
            result = await fxn(*args, **kwargs)
            Timer.helper_run_time(args, fxn, start_time)
            return result

        return wrapper

    @staticmethod
    def helper_run_time(args, fxn, start_time) -> None:
        """Get running time: helper function."""
        end_time = time.time()
        elapsed_time = end_time - start_time
        minutes, seconds = divmod(int(elapsed_time), 60)
        class_name = args[0].__class__.__name__ if args else fxn.__module__
        if minutes == 0:
            rtime = f"{seconds}s"
        else:
            rtime = f"{minutes}m {seconds}s"
        text = f"{class_name}.{fxn.__name__} took {rtime} to execute.\n"
        print(text)
