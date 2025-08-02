import time


def get_no_cache_headers():
    return {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }


async def measure_api_call(method, url, **kwargs):
    headers = get_no_cache_headers()
    if "headers" in kwargs:
        kwargs["headers"].update(headers)
    else:
        kwargs["headers"] = headers

    start_time = time.time()
    try:
        response = await method(url, **kwargs)
        end_time = time.time()
        duration = end_time - start_time
        return response, duration, None
    except Exception as e:
        end_time = time.time()
        duration = end_time - start_time
        return None, duration, str(e)

