import random
import shlex


def product_images_directory_path(instance, filename: str) -> str:
    filename = shlex.quote(filename)[:10]
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product_id,
        filename=filename,
    )


def product_main_photo_directory_path(instance, filename: str) -> str:
    filename = shlex.quote(filename)[:10]
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.id,
        filename=filename,
    )


def category_images_directory_path(instance, filename: str) -> str:
    filename = shlex.quote(filename)[:10]
    return "categories/category_{pk}/images/{filename}".format(
        pk=instance.id,
        filename=filename,
    )


def random_category_image() -> str:
    return random.choice(
        [f'fixtures/images/departments/{num}.svg' for num in range(1, 13)]
    )
