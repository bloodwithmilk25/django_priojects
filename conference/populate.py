import os
import django
from django_xlspopulator.populator import Populator
os.environ.setdefault('DJANGO_SETTINGS_MODULE','conference.settings')
django.setup()
from event.models import Speaker


pop = Populator('C:/Users/Nikita/Desktop/speakers.xls', Speaker)
pop.populate()