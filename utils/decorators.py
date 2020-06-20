import threading

def async_call(callback=None):
    """Decorator that calls a function asynchronously.

    Args:
        callback (func, optional): The function to apply to the result of the
            wrapped function when it is successfully returned. Defaults to None.

    Returns:
        func: The decorated function.
    """
    def async_wrapper(func):
        def wrapper(*args, **kwargs):

            def thread_call(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                except Exception as exc:
                    print("Thread has terminated with error: " + str(exc))
                    raise
                if callback:
                    callback(result)

            thr = threading.Thread(target=thread_call, args=args, kwargs=kwargs)
            thr.start()

        return wrapper
    return async_wrapper
