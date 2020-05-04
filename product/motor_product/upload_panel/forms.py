import os

from django import forms
from django.core.exceptions import ValidationError

from motor_product.constants import Constants


def validate_file_extension(value):
    import os

    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".xlsx", ".xls"]
    if ext not in valid_extensions:
        raise ValidationError("File not supported! (Please use .xlsx or .xls)")


class UploadFileForm(forms.Form):
    INSURER = (
        ("dhfl", "DHFL"),
        ("bajaj_allianz", "Bajaj Allianz"),
        ("bharti_axa", "Bharti AXA"),
        ("future_generali", "Future Generali"),
        ("hdfc_ergo", "HDFC ERGO"),
        ("liberty_videocon", "Liberty Videocon"),
        ("new_india", "New India"),
        ("oriental", "Oriental"),
        ("reliance", "Reliance"),
        ("universal_sompo", "Universal Sompo"),
        ("kotak_general", "Kotak General Insurance"),
        ("royal_sundaram", "Royal Sundaram General Insurance"),
        ("shriram", "Shiram General Insurance"),
        ("magma_hdi", "Magma HDI General Insurance"),
        ("go_digit", "Go Digit General Insurance"),
        ("edelweiss", "Edelweiss"),
        ("icici_lombard", "ICICI Lombard"),
        ("national", "National Insurance"),
        ("acko", "Acko"),
    )
    VEHICLE_TYPE = (
        ("fourwheeler", "Four Wheeler"),
        ("twowheeler", "Two Wheeler"),
        ("pcv", "PCV"),
        ("gcv", "GCV"),
    )
    VEHICLE_CATEGORY = (
        (Constants.VehicleCategory.PRIVATE, Constants.VehicleCategory.PRIVATE),
        (Constants.VehicleCategory.COMMERCIAL, Constants.VehicleCategory.COMMERCIAL)
    )
    insurer = forms.ChoiceField(choices=INSURER)
    vehicle_category = forms.ChoiceField(choices=VEHICLE_CATEGORY)
    vehicle_type = forms.ChoiceField(choices=VEHICLE_TYPE)
    file = forms.FileField(validators=[validate_file_extension])