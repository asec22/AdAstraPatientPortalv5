from django.db import models
import datetime

class UpdatedAgeField(models.Field):
    date_field = None 

    def __init__(self, *args, **kwargs):
        self.date_field = kwargs.pop('date_field', None) 
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return value

    def from_db_value(self, value, expression, connection):
        return value

    def __str__(self):
        birth_date = getattr(self.instance, self.date_field)
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age
