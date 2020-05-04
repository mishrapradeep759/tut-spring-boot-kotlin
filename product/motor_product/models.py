import copy
import datetime
import json
import random
import re

from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _
from django.db import models
import uuid

from motor_product.constants import Constants
from core import models as core_models
from core.fields import VehicleTypeCharField


class Insurer(models.Model):
    title = models.CharField(_("title"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=70, unique=True)
    body = models.TextField(_("body"), blank=True)


class MakeQuerySet(models.QuerySet):
    def active(self, vehicle_type):
        if vehicle_type == Constants.VehicleType.FOURWHEELER:
            return self.filter(is_active_for_fourwheeler=True)
        elif vehicle_type == Constants.VehicleType.TWOWHEELER:
            return self.filter(is_active_for_twowheeler=True)
        else:
            return self

    def popular(self, vehicle_type):
        if vehicle_type == Constants.VehicleType.FOURWHEELER:
            return self.filter(is_popular_for_fourwheeler=True)
        elif vehicle_type == Constants.VehicleType.TWOWHEELER:
            return self.filter(is_popular_for_twowheeler=True)
        else:
            return self


class MakeManager(models.Manager):
    def get_all_makes(self):
        return self.all()


class Make(core_models.BaseModel):
    name = models.CharField(_("name"), max_length=70, unique=True)
    is_active_for_twowheeler = models.BooleanField(default=True)
    is_active_for_fourwheeler = models.BooleanField(default=True)
    is_popular_for_fourwheeler = models.NullBooleanField()
    is_popular_for_twowheeler = models.NullBooleanField()
    is_popular = models.BooleanField(default=False)
    objects = MakeManager.from_queryset(MakeQuerySet)()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class ModelManager(models.Manager):
    def get_models_for_make(self, make):
        return self.filter(make=make)


class Model(core_models.BaseModel):
    make = models.ForeignKey(Make, blank=True, null=True, on_delete=models.PROTECT)
    name = models.CharField(_("name"), max_length=150)

    objects = ModelManager()

    class Meta:
        unique_together = ("make", "name")
        ordering = ("name",)

    def __str__(self):
        return "%s : %s" % (self.make.name, self.name)


class VehicleMaster(models.Model):
    # objects = VehicleMasterManager()

    make = models.ForeignKey(Make, on_delete=models.CASCADE)  # maruti
    model = models.ForeignKey(Model, on_delete=models.CASCADE)  # wagon r
    variant = models.CharField(max_length=250, db_index=True)  # LSI
    cc = models.IntegerField()
    seating_capacity = models.IntegerField()
    ex_showroom_price = models.FloatField(blank=True, null=True)
    fuel_type = models.CharField(max_length=50, choices=Constants.FuelType.FUEL_CHOICES)
    vehicle_segment = models.CharField(
        max_length=250, blank=True, choices=Constants.VehicleSegment.VEHICLE_SEGMENT_CHOICES
    )
    sub_vehicles = models.ManyToManyField("Vehicle", through="VehicleMapping")
    vehicle_type = VehicleTypeCharField(
        max_length=25,
        choices=Constants.VehicleType.VEHICLE_TYPE_CHOICES,
        default=Constants.VehicleType.FOURWHEELER,
    )
    vehicle_category = models.CharField(
        max_length=25,
        choices=Constants.VehicleCategory.VEHICLE_CATEGORY_CHOICES,
        default=Constants.VehicleCategory.PRIVATE,
        null=False,
    )
    gross_vehicle_weight = models.FloatField(blank=True, null=True)
    sales_channels = models.ManyToManyField(core_models.SalesChannel)
    number_of_wheels = models.IntegerField(blank=True, null=True)


class Vehicle(models.Model):
    insurer = models.ForeignKey(Insurer, blank=True, null=True, on_delete=models.PROTECT)
    vehicle_code = models.CharField(max_length=250, blank=True)
    name = models.CharField(max_length=250, blank=True)
    make = models.CharField(max_length=250, blank=True)
    make_code = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=250, blank=True)
    model_code = models.CharField(max_length=50, blank=True)
    variant = models.CharField(max_length=250, blank=True)
    variant_code = models.CharField(max_length=50, blank=True)
    cc = models.IntegerField(blank=True, null=True)
    seating_capacity = models.IntegerField(blank=True, null=True)
    fuel_type = models.CharField(max_length=50, blank=True)
    vehicle_segment = models.CharField(max_length=250, blank=True)
    number_of_wheels = models.IntegerField(blank=True, null=True)
    ex_showroom_price = models.CharField(max_length=20, blank=True)
    base_rate_discount = models.FloatField(blank=True, null=True)
    risk_based_discount = models.FloatField(blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)
    processing_level = models.CharField(
        max_length=20, null=False, default="unprocessed"
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    vehicle_type = VehicleTypeCharField(
        max_length=25,
        choices=Constants.VehicleType.VEHICLE_TYPE_CHOICES,
        default=Constants.VehicleType.FOURWHEELER,
    )
    gross_vehicle_weight = models.FloatField(blank=True, null=True)
    extra_data = JSONField(
        _("vehicle_data"), blank=True, default=dict, null=True
    )
    vehicle_category = models.CharField(
        max_length=25,
        choices=Constants.VehicleCategory.VEHICLE_CATEGORY_CHOICES,
        default=Constants.VehicleCategory.PRIVATE,
    )
    is_declined = models.NullBooleanField(default=False)

    def __str__(self):
        return "%s %s %s %s %s - %s|%s" % (
            self.make,
            self.model,
            self.variant,
            self.fuel_type,
            self.cc,
            self.insurer.title,
            self.vehicle_category,
        )


class VehicleMapping(models.Model):
    master_vehicle = models.ForeignKey(VehicleMaster, blank=True, null=True, on_delete=models.SET_NULL)
    mapped_vehicle = models.ForeignKey(Vehicle, blank=True, null=True, on_delete=models.SET_NULL)
    insurer = models.ForeignKey("Insurer", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        unique_together = ("master_vehicle", "insurer")

    def save(self, *args, **kwargs):
        self.insurer = self.mapped_vehicle.insurer
        super(VehicleMapping, self).save(*args, **kwargs)


class Quote(models.Model):
    OFFLINE_TYPE = "offline"
    ONLINE_TYPE = "online"
    type_choices = ((OFFLINE_TYPE, "Offline"), (ONLINE_TYPE, "Online"))

    quote_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    vehicle = models.ForeignKey(
        VehicleMaster, blank=True, null=True, on_delete=models.SET_NULL
    )
    is_new = models.BooleanField(default=True)
    date_of_manufacture = models.DateField(blank=True, null=True)
    raw_data = JSONField(_("request_data"), blank=True, default=dict)
    is_processed = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    category = models.CharField(
        max_length=25,
        choices=Constants.VehicleCategory.VEHICLE_CATEGORY_CHOICES,
        default=Constants.VehicleCategory.PRIVATE,
        null=True,
    )
    type = models.CharField(
        "quote type", max_length=20, default=ONLINE_TYPE, choices=type_choices
    )

    tracker = models.ForeignKey(
        "core.Tracker", related_name="motor_quotes", on_delete=models.PROTECT
    )
    parent_quote = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="child_quotes",
    )
    previous_policy = models.ForeignKey(
        "core.Policy", null=True, blank=True, related_name="motor_product_quotes", on_delete=models.PROTECT
    )
    # previous_hybrid_policy = models.ForeignKey(
    #     "core.Policy", null=True, blank=True, related_name="hybrid_renewal_quotes"
    # )
    sales_channel = models.ForeignKey(
        "core.SalesChannel", null=True, blank=True, on_delete=models.PROTECT
    )
    policy_type = models.CharField(
        max_length=20, null=True, choices=Constants.PolicyType.POLICY_TYPE_CHOICES
    )
    original_quote_created_by = models.ForeignKey("core.User", null=True, on_delete=models.SET_NULL)
    created_by = models.ForeignKey(
        "core.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_motor_quotes",
    )
    registration_number = models.CharField(
        _("Registration Number"), max_length=32, db_index=True, blank=True, null=True
    )


class CarQuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super(CarQuoteManager, self)
            .get_queryset()
            .filter(vehicle__vehicle_type=Constants.VehicleType.FOURWHEELER)
        )


class CarQuote(Quote):
    objects = CarQuoteManager()

    class Meta:
        proxy = True


class BikeQuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super(BikeQuoteManager, self)
            .get_queryset()
            .filter(vehicle__vehicle_type=Constants.VehicleType.TWOWHEELER)
        )


class BikeQuote(Quote):
    objects = BikeQuoteManager()

    class Meta:
        proxy = True


class CommercialCarQuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super(CommercialCarQuoteManager, self)
            .get_queryset()
            .filter(category=Constants.VehicleCategory.COMMERCIAL)
        )


class CommercialCarQuote(Quote):
    objects = CommercialCarQuoteManager()

    class Meta:
        proxy = True


class PCVQuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super(PCVQuoteManager, self)
            .get_queryset()
            .filter(vehicle__vehicle_type=Constants.VehicleType.PCV)
        )


class GCVQuoteManager(models.Manager):
    def get_queryset(self):
        return (
            super(GCVQuoteManager, self)
            .get_queryset()
            .filter(vehicle__vehicle_type=Constants.VehicleType.GCV)
        )


class PCVQuote(Quote):
    objects = PCVQuoteManager()

    class Meta:
        proxy = True


class GCVQuote(Quote):
    objects = GCVQuoteManager()

    class Meta:
        proxy = True


class Address(core_models.BaseModel ):
    ADDRESS_CATEGORY_CHOICES = (("URBAN", "Urban"), ("RURAL", "Rural"))
    category = models.CharField(max_length=10, choices=ADDRESS_CATEGORY_CHOICES)
    line_1 = models.CharField(_("Street"), max_length=100)
    line_2 = models.CharField(_("Street"), max_length=100, blank=True)
    landmark = models.TextField(_("Landmark"), blank=True)
    city = models.CharField(_("City"), max_length=100)
    district = models.CharField(_("District"), max_length=100, default="")
    state = models.CharField(_("State"), max_length=100)
    pincode = models.CharField(_("Pincode"), max_length=10)
    country = models.CharField(_("Country"), max_length=100)
    raw = JSONField(_("raw"), blank=True, default=dict)


class ContactDetail(core_models.BaseModel):
    address = models.ForeignKey(Address, blank=True, null=True, on_delete=models.SET_NULL)
    address_type = models.CharField(max_length=30, choices=Constants.Contact.ADDRESS_TYPE_CHOICES)
    email = models.EmailField(_("Email"))
    mobile = models.CharField(_("Mobile"), max_length=11, db_index=True)
    landline = models.CharField(_("Landline"), max_length=12)
    date_of_birth = models.DateField(blank=True, null=True)
    title = models.CharField(
        max_length=10, choices=Constants.Gender.TITLE_CHOICES, null=True, blank=True
    )
    first_name = models.CharField(
        _("First name"), max_length=255, null=True, blank=True, db_index=True
    )
    middle_name = models.CharField(_("First name"), max_length=255, blank=True)
    last_name = models.CharField(
        _("Last name"), max_length=255, null=True, blank=True, db_index=True
    )
    gender = models.CharField(
        _("Gender"), max_length=20, choices=Constants.Gender.GENDER_CHOICES, null=True, blank=True
    )
    father_first_name = models.CharField(_("Father's first name"), max_length=255)
    father_last_name = models.CharField(
        _("Father's last name"), max_length=255, blank=True
    )
    send_email = models.BooleanField(default=False)
    send_sms = models.BooleanField(default=False)
    phone_call = models.BooleanField(default=False)
    nationality = models.CharField(max_length=50)
    is_corporate_customer = models.BooleanField(default=False)
    company_name = models.CharField(
        _("Company name"), max_length=255, null=True, blank=True
    )
    raw = JSONField(_("raw"), blank=True, default=dict)

    @property
    def full_name(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}"
        return " ".join(full_name.split())


