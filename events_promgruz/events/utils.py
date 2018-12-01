from transliterate import translit


# helper function to generate image names
def image_name(instance, filename):
    """
    filename consists of transliterated filename and extension
    it is put it the folder with name that corresponds with instance name
    if name was in latin it stays the same
    """
    ext = filename.split('.')[1]
    filename = translit(filename.split('.')[0][:20], 'ru', reversed=True).replace(" ", "") + '.' + ext
    try:
        if instance.path:  # if it's a call from "Image" model
            if instance.location:
                location_name = translit(instance.location.name, 'ru', reversed=True).replace(" ", "")
                return "{}/{}".format(location_name, filename)
            else:
                event_name = translit(instance.event.name, 'ru', reversed=True).replace(" ", "")
                return "{}/{}".format(event_name, filename)
    except AttributeError:
        #  if it's a call from other models, not "Image"
        name = translit(instance.name[:35], 'ru', reversed=True).replace(" ", "")
        return "{}/{}".format(name, filename)
