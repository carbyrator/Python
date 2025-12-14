import sys
import logging
import functools

def logger(func=None, *, handle=None):
    """
    Декоратор для логирования
    """
    if func is None:
        def decorator(f):
            return logger(f, handle=handle)
        return decorator

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Если handle не передан, используем sys.stdout по умолчанию
        log_handle = handle if handle is not None else sys.stdout

        # Начало вызова
        start_msg = f"Начало {func.__name__} с args={args}, kwargs={kwargs}"

        # Если передан логгер из logging
        if isinstance(log_handle, logging.Logger):
            log_handle.info(start_msg)

            try:
                result = func(*args, **kwargs)
                success_msg = f"Успех {func.__name__}: {result}"
                log_handle.info(success_msg)
                log_handle.info(f"Returned value: {result}")
                return result
            except Exception as e:
                error_msg = f"Ошибка {func.__name__}: {type(e).__name__}: {e}"
                log_handle.error(error_msg)
                raise
        else:
            # Если handle это обычный файл или stdout
            log_handle.write(f"INFO: {start_msg}\n")

            try:
                result = func(*args, **kwargs)
                success_msg = f"INFO: Успех {func.__name__}: {result}\n"
                log_handle.write(success_msg)
                log_handle.write(f"Returned value: {result}\n")
                return result
            except Exception as e:
                error_msg = f"ERROR: Ошибка {func.__name__}: {type(e).__name__}: {e}\n"
                log_handle.write(error_msg)
                raise

    return wrapper
