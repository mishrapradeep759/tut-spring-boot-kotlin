import csv
import re
import os
from fuzzywuzzy import fuzz


from motor_product.constants import Constants

INSURER_SLUG = ""
VEHICLE_TYPE = Constants.VehicleType.FOURWHEELER
FILE_TO_UPLOAD = "Car_To_Upload.xlsx"

# TODO: """this is just for testing purpose. Once done need to correct with absolute/relative path"""
local_path = os.path.join('C:\\working\\python\\projects\\tut-spring-boot-kotlin\\product', FILE_TO_UPLOAD)


def clean_string(str):
    return re.sub("\s+", " ", re.sub("[^a-zA-Z0-9 \n\.]", "", str)) if str else ""


# eg. format of VehicleMaster
vehicle_master = {
    "Tata Motors Ltd.": [
        {"id": 1, "model": "Indigo", "variant": "eGS EMAX GLX"},
        {"id": 2, "model": "Indigo", "variant": "eGS EMAX GLS"},
        {"id": 3, "model": "Indigo", "variant": "eGS EMAX GLH"},
        {"id": 4, "model": "Indigo", "variant": "eGS EMAX CLI"}
    ],
    "Honda": [
        {"id": 1, "model": "Accord", "variant": "li"},
        {"id": 2, "model": "Accord", "variant": "hi"}
    ]
}


def match_str(str1, str2):
    exact_ration = fuzz.ratio(clean_string(str1), clean_string(str2))
    partial_ratio = fuzz.partial_ratio(clean_string(str1), clean_string(str2))
    return exact_ration


def get_vehicle_variant_match(insurer_vehicle_model, master_model_variants, insurer_vehicle_variant):
    if not (insurer_vehicle_model or master_model_variants or insurer_vehicle_model):
        return 0, 0
    id_percent_matches = []

    for master_model_variant in master_model_variants:
        if clean_string(insurer_vehicle_model.lower()) == clean_string(master_model_variant.get("model", "").lower()):
            variant_percent_matches = match_str(
                master_model_variant.get("variant", ""),
                insurer_vehicle_variant
            )  # return how much it is matched
            if variant_percent_matches > 60:
                id_model_variant_dict = {
                    "id": master_model_variant.get("id"),
                    "model_variant": f'{master_model_variant["model"]} {master_model_variant["variant"]}',
                    "matching_percentage": variant_percent_matches
                }
                id_percent_matches.append(id_model_variant_dict)
    return id_percent_matches


def set_insurerer_vehicle_masterId(data, insurer_vehicle_model, master_model_variants, insurer_vehicle_variant):
    masterId_percent_matches = get_vehicle_variant_match(
        insurer_vehicle_model,
        master_model_variants, insurer_vehicle_variant
    )
    data["matches"] = masterId_percent_matches


def map_vehicles_with_master(raw_data):
    """
    This method will compare the combination of insurer vehicles make, model, variant with master vehicle
    and if it found matches range (65%-99%), it should be reviewed,
    100% matches should be automatically mapped (and masterId to Insurer vehicle)

    :type raw_data: it is list of insurer vehicles data (dictionary) provided by insurer (xlsx)
    """
    vehicles = []
    for data in raw_data:
        insurer_vehicle_make = clean_string(data.get(Constants.Vehicle.MAKE, ""))
        insurer_vehicle_model = clean_string(data.get(Constants.Vehicle.MODEL, ""))
        insurer_vehicle_variant = clean_string(data.get(Constants.Vehicle.VARIANT, ""))

        master_model_variants = vehicle_master.get(insurer_vehicle_make)
        if master_model_variants and insurer_vehicle_model and insurer_vehicle_variant:
            set_insurerer_vehicle_masterId(
                data,
                insurer_vehicle_model,
                master_model_variants,
                insurer_vehicle_variant
            )
        elif master_model_variants and insurer_vehicle_model:
            model_variant = insurer_vehicle_model.split()
            if len(model_variant) == 2:
                model, variant = clean_string(model_variant[0]), clean_string(model_variant[1])
                set_insurerer_vehicle_masterId(
                    data,
                    model,
                    master_model_variants,
                    variant
                )
            elif len(model_variant) > 2:
                count = len(model_variant)
                inc = 0
                masterId_variant_percent_match_mapping = []
                while count > 1:
                    variant_matching_percentage = get_vehicle_variant_match(
                        model_variant[inc],
                        master_model_variants, " ".join(model_variant[inc+1:])
                    )
                    print(variant_matching_percentage)
                    if variant_matching_percentage:
                        masterId_variant_percent_match_mapping.extend(variant_matching_percentage)
                    count -= 1
                    inc += 1
                data["matches"] = masterId_variant_percent_match_mapping
        data["matches"] = data.get("matches", {})
        vehicles.append(data)
    return vehicles


def set_master_make_model():
    pass


def mmain(raw_data):
    # raw_data = parser_utils.parse_xlsx(local_path, row_dict=True)
    mappings = map_vehicles_with_master(raw_data)
    return mappings
    # keys = mappings[0].keys()
    # with open('C:\\working\\InsData\\vehicle_mapping\output.csv', 'w') as output:
    #     dict_writer = csv.DictWriter(output, keys)
    #     dict_writer.writeheader()
    #     dict_writer.writerows(mappings)

#
# if __name__ == "__main__":
#     main()


def make_final_key():
    # TODO: run this function on each vehicle upload excel,
    #  it should be able to fix all the make, model, variant key
    #  and make it final
    pass
