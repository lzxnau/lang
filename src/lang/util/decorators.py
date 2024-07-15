"""
Lang Project Decorators Module in util.

Version: 2024.07.10.01
"""


class Timer:
    """Timer Decorator Class."""

    @staticmethod
    def fxn_run(fxn):
        """Get running time of a function."""
        import time

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = fxn(*args, **kwargs)
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

            return result

        return wrapper
