class Constants:
    class Products:
        CAR = "car"
        BIKE = "bike"

    class VehicleCategory:
        PRIVATE = "Private"
        COMMERCIAL = "Commercial"
        VEHICLE_CATEGORIES = [PRIVATE, COMMERCIAL]
        VEHICLE_CATEGORY_CHOICES = ((PRIVATE, PRIVATE), (COMMERCIAL, COMMERCIAL))

        # def get_vehicle_category_choices(cls):
        #     return ((cls.PRIVATE, "Private"), (cls.COMMERCIAL, "Commercial"))

    class VehicleType:
        TWOWHEELER = "twowheeler"
        FOURWHEELER = "fourwheeler"
        GCV = "gcv"
        PCV = "pcv"
        AUTO = "auto"
        LCV = "lcv"
        HCV = "hcv"
        TAXI = "taxi"
        TRACTOR = "tractor"
        MISCELLANEOUS = "miscellaneous"
        # STANDALONEPA = "standalonepa"

        VEHICLE_TYPES = [FOURWHEELER, TWOWHEELER, GCV]

        DISPLAY_VEHICLE_TYPES = {FOURWHEELER: "Car", TWOWHEELER: "Bike", PCV: "pcv", GCV: GCV}

        VEHICLE_TYPE_CHOICES = (
            (FOURWHEELER, "Private Car"),
            (TWOWHEELER, "Two Wheeler"),
            (GCV, "Goods Carrier Vehicle"),
            (PCV, "Passenger Carrying Vehicle"),
            (AUTO, "Auto"),
        )

    class CoverageType:
        COMPREHENSIVE = "comprehensive"
        THIRD_PARTY = "third_party"
        HYBRID = "hybrid"
        OWN_DAMAGE = "own_damage"

        COVERAGE_TYPES = [COMPREHENSIVE, THIRD_PARTY, HYBRID, OWN_DAMAGE]

        COVERAGE_TYPE_CHOICES = (
            (COMPREHENSIVE, "Comprehensive"),
            (THIRD_PARTY, "Third Party"),
            (HYBRID, "Hybrid"),
            (OWN_DAMAGE, "Own Damage"),
        )

    class PolicyType:
        NEW = "new"
        RENEW = "renew"
        EXPIRED = "expired"
        USED = "used"
        OTHER = "other"

        POLICY_TYPE_CHOICES = (
            (NEW, "New"),
            (RENEW, "Renew"),
            (EXPIRED, "Expired"),
            (USED, "Used"),
        )

    class TransactionStatus:
        DRAFT = "DRAFT"
        PENDING = "PENDING"
        IN_PROCESS = "IN_PROCESS"
        COMPLETED = "COMPLETED"
        CANCELLED = "CANCELLED"
        FAILED = "FAILED"
        MANUAL_COMPLETED = "MANUAL COMPLETED"
        PROPOSAL_FAILED = "PROPOSAL FAILED"
        FORM_EXPIRED = "FORM_EXPIRED"
        COMPLETED_STATUS_LIST = [COMPLETED, MANUAL_COMPLETED]

    class RTOZone:
        ZONE_A = "A"
        ZONE_B = "B"
        ZONE_C = "C"
        ZONE_CHOICES = ((ZONE_A, ZONE_A), (ZONE_B, ZONE_B), (ZONE_C, ZONE_C))

    class Platform:
        DESKTOP = "desktop"
        MOBILE = "mobile"

    class QuoteErrorsMessage:
        MESSAGES = {
            "INSURER_DOWN": "Insurer server down",
            "TOO_OLD": "%s's too old to be insured.",
            "RTO_NOT_COVERED": "RTO not covered by insurer.",
        }

    class FuelType:
        PETROL = "PETROL"
        DIESEL = "DIESEL"
        ELECTRICITY = "ELECTRICITY"
        INTERNAL_LPG_CNG = "INTERNAL_LPG_CNG"
        FUEL_CHOICES = (
            (PETROL, "Petrol"),
            (DIESEL, "Diesel"),
            (ELECTRICITY, "Electricity"),
            (INTERNAL_LPG_CNG, "Internal LPG / CNG"),
        )

    class VehicleSegment:
        COMPACT_CARS = "COMPACT_CARS"
        HIGH_END_CARS = "HIGH_END_CARS"
        MIDSIZE_CARS = "MIDSIZE_CARS"
        MULTIUTILITY_VEHICLES = "MULTIUTILITY_VEHICLES"
        SMALL_SIZE_VEHICLES = "SMALL_SIZE_VEHICLES"
        SPORTS_UTILITY_VEHICLES = "SPORTS_UTILITY_VEHICLES"
        VEHICLE_SEGMENT_CHOICES = (
            (COMPACT_CARS, "Compact Cars"),
            (HIGH_END_CARS, "High End Cars"),
            (MIDSIZE_CARS, "Midsize Cars"),
            (MULTIUTILITY_VEHICLES, "Multi-utility Vehicles"),
            (SMALL_SIZE_VEHICLES, "Small Sized Vehicles"),
            (SPORTS_UTILITY_VEHICLES, "Sports and Utility Vehicles"),
        )

    class Contact:
        COMMUNICATION_ADDRESS = "COMMUNICATION_ADDRESS"
        PERMANENT_ADDRESS = "PERMANENT_ADDRESS"
        BILLING_ADDRESS = "BILLING_ADDRESS"
        RISK_ADDRESS = "RISK_ADDRESS"
        REGISTRATION_OFFICE = "REGISTRATION_OFFICE"
        NEW_ADDRESS = "NEW_ADDRESS"
        OTHER_OFFICES = "OTHER_OFFICES"

        ADDRESS_TYPE_CHOICES = (
            (COMMUNICATION_ADDRESS, "Communication Address"),
            (PERMANENT_ADDRESS, "Permanent Address"),
            (BILLING_ADDRESS, "Billing address"),
            (RISK_ADDRESS, "Risk address"),
            (REGISTRATION_OFFICE, "Registered office"),
            (NEW_ADDRESS, "New address"),
            (OTHER_OFFICES, "Other offices"),
        )

    class Gender:
        MALE = "MALE"
        FEMALE = "FEMALE"

        GENDER_CHOICES = ((MALE, "Male"), (FEMALE, "Female"))
        TITLE_CHOICES = (
            ("MR.", "Mr."),
            ("MRS.", "Mrs."),
            ("MISS", "Miss"),
            ("DR", "Dr"),
            ("CAPTAIN", "Captain"),
            ("LT", "Lt"),
            ("MAJOR", "Major"),
            ("GENERAL", "General"),
            ("COLONEL", "Colonel"),
            ("BRIGADIER", "Brigadier"),
            ("JUDGE", "Judge"),
            ("PROF", "Prof"),
            ("SIR", "Sir"),
            ("FATHER", "Father"),
            ("MASTER", "Master"),
            ("MADAM", "Madam"),
        )

    class Vehicle:
        MAKE = "MANUFACTURER"
        MODEL = "MODEL"
        VARIANT = "VARIANT"

# TODO: Categorize below constants

POLICY_EXPIRED = "POLICY_EXPIRED"
INSPECTION_EXPIRED = "INSPECTION_EXPIRED"
POLICY_HAS_EXPIRED = "POLICY HAS EXPIRED"
INSPECTION_IS_REQUIRED = "INSPECTION IS REQUIRED"


