import functools
import inspect
import logging

from food_co2_estimator.pydantic_models.recipe_extractor import EnrichedRecipe

logger = logging.getLogger("CO2Estimator")


def log_with_url(func):
    """
    Decorator that tries to find 'url' in the call.
      1) If kwargs['url'] is present, use that.
      2) Else if kwargs['recipe'] is an EnrichedRecipe with a .url field, use that.
      3) Else use "NO_URL_FOUND".
    Logs 'Calling function...' before and 'Finished function...' after.
    """

    def _get_url(args, kwargs: dict[str, str]):
        extracted_url = kwargs.get("url", None)
        if extracted_url is not None:
            return extracted_url

        all_args = [arg for arg in args] + [value for value in kwargs.values()]
        for arg in all_args:
            if isinstance(arg, EnrichedRecipe):
                return arg.url

        return "NO_URL_FOUND"

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        # Try to get url from kwargs['url']
        extracted_url = _get_url(args, kwargs)

        logger.info("URL=%s: Calling function: %s", extracted_url, func.__name__)
        result = func(*args, **kwargs)
        logger.info("URL=%s: Finished function: %s", extracted_url, func.__name__)
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        extracted_url = _get_url(args, kwargs)
        logger.info("URL=%s: Calling function: %s", extracted_url, func.__name__)
        result = await func(*args, **kwargs)
        logger.info("URL=%s: Finished function: %s", extracted_url, func.__name__)
        return result

    # Return the async or sync wrapper depending on the original function
    if inspect.iscoroutinefunction(func):
        return async_wrapper

    return sync_wrapper
