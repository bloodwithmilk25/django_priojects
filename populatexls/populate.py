import os
import django
from django_xlspopulator.populator import Populator
os.environ.setdefault('DJANGO_SETTINGS_MODULE','populatexls.settings')
django.setup()
from basicapp.models import Test2


pop = Populator('C:/Users/Nikita/Desktop/SampleXLSFile_212kb.xls', Test2)
pop.populate()
