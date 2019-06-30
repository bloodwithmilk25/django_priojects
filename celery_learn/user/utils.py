# helper function to generate image names
def image_name(instance, filename):
    ext = filename.split('.')[1]
    filename = f'{instance.pk}.{ext}'
    return f'avatars/{filename}'
