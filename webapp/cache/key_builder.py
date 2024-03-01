from conf.config import settings


def get_file_resize_cache(task_id: str) -> str:
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:file_resize:{task_id}'


def get_dishes_cache(category: str = None):
    if category is not None:
        return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:dishes:{category}'
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:dishes'


def get_dish_by_id_cache(dish_id: int):
    return f'{settings.REDIS_SIRIUS_CACHE_PREFIX}:dish:{dish_id}'
