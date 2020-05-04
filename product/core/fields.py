from django.db import models


class VehicleTypeCharField(models.CharField):
    def from_db_value(self, value, expression, connection, context):
        if value == "Private Car":
            return "fourwheeler"
        elif value == "Twowheeler":
            return "twowheeler"
        else:
            return value

    def to_python(self, value):
        value = super(VehicleTypeCharField, self).to_python(value=value)
        if value == "Private Car":
            return "fourwheeler"
        elif value == "Twowheeler":
            return "twowheeler"
        else:
            return value