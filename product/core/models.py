from django.db import models


def get_verbose_format(value):
    return " ".join(map(str.capitalize, value.split("_")))


class AbstractBaseModel(object):
    def __str__(self):
        try:
            return self.name
        except Exception:
            try:
                return self.title
            except Exception:
                return ""


class BaseModel(AbstractBaseModel, models.Model):

    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        update_fields = kwargs.get("update_fields")
        if not update_fields:
            update_fields = list(update_fields)
            update_fields.append("modified_date")
            kwargs["update_fields"] = update_fields
        return super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


# class Insurer(BaseAuthorModel):
#     name = models.CharField(max_length=200)
#     slug = AutoSlugField(
#         populate_from="name", always_update=True, unique=True, max_length=200
#     )
#     logo = ImageWithThumbsField(
#         upload_to=get_insurer_logo_path, sizes=(("s", 300, 300), ("t", 500, 500))
#     )
#     body = models.TextField(blank=True)
#     company = models.ForeignKey("core.Company")

class User(models.Model):
    pass


class Tracker(models.Model):
    pass


class Policy(models.Model):
    pass


class SalesChannel(BaseModel):
    CAR_DEKHO = "cardekho"
    UBER = "uber"
    COVERFOX = "coverfox"
    DEALER = "dealer"
    POS = "pos"
    INSURER = "insurer"
    OLA = "ola"
    SHOPCLUES = "shopclues"
    QUICKRIDE = "quickride"
    SEEGLOB = "seeglob"
    GAADIKEY = "gaadikey"
    BENEFITHUB = "benefithub"
    RSA365 = "rsa365"
    VASCO = "vasco"
    ANTILOG = "antilog"
    SCRIPBOX = "scripbox"
    CIMS = "cims"
    AKOYA = "akoya"

    SLUG_CHOICES = (
        (CAR_DEKHO, get_verbose_format(CAR_DEKHO)),
        (UBER, get_verbose_format(UBER)),
        (COVERFOX, get_verbose_format(COVERFOX)),
        (DEALER, get_verbose_format(DEALER)),
        (POS, get_verbose_format(POS)),
        (INSURER, get_verbose_format(INSURER)),
        (OLA, get_verbose_format(OLA)),
        (SHOPCLUES, get_verbose_format(SHOPCLUES)),
        (QUICKRIDE, get_verbose_format(QUICKRIDE)),
        (SEEGLOB, get_verbose_format(SEEGLOB)),
        (GAADIKEY, get_verbose_format(GAADIKEY)),
        (BENEFITHUB, get_verbose_format(BENEFITHUB)),
        (RSA365, get_verbose_format(RSA365)),
        (VASCO, get_verbose_format(VASCO)),
        (ANTILOG, get_verbose_format(ANTILOG)),
        (SCRIPBOX, get_verbose_format(SCRIPBOX)),
        (CIMS, get_verbose_format(CIMS)),
        (AKOYA, get_verbose_format(AKOYA)),
    )
    name = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True, choices=SLUG_CHOICES)
    business_type = models.CharField(max_length=32, null=True, choices=SLUG_CHOICES)

    def __str__(self):
        return "{} ({})".format(self.name, self.slug)

# class NullBaseModel(AbstractBaseModel, models.Model):
#
#     created_on = models.DateTimeField(auto_now_add=True, null=True)
#     modified_on = models.DateTimeField(auto_now=True, null=True)
#
#     def save(self, *args, **kwargs):
#         update_fields = kwargs.get("update_fields")
#         if update_fields is not None and len(update_fields) != 0:
#             update_fields = list(update_fields)
#             update_fields.append("modified_on")
#             kwargs["update_fields"] = update_fields
#         return super(NullBaseModel, self).save(*args, **kwargs)
#
#     class Meta:
#         abstract = True

