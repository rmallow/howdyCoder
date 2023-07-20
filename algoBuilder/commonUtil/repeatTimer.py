import threading


def setInterval(interval):
    def decorator(function):
        def wrapper(*args, timer=False, on_runtime_time=None, **kwargs):
            """Only start the timer if the kwarg timer is set to true, otherwise call function once normally"""
            if timer:
                stopped = threading.Event()

                def loop():  # executed in another thread
                    period = interval if on_runtime_time is None else on_runtime_time
                    while not stopped.wait(period):  # until stopped
                        function(*args, **kwargs)

                t = threading.Thread(target=loop)
                t.daemon = True  # stop if the program exits
                t.start()
                return stopped
            else:
                function(*args, **kwargs)

        return wrapper

    return decorator
