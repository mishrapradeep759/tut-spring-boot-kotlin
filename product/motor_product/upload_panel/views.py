from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .forms import UploadFileForm
from motor_product import parser_utils
from motor_product.general_codes import mmain


@csrf_protect
# @login_required
# @utils.profile_type_only("MOTOR_MASTER_ADMIN")
def dashboard(request):
    context = {}
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            response = {}
            print("<<<<<<<<<<<<<<<<<<<<<<<<<")
            _file = request.FILES["file"]
            file_row_gen = parser_utils.parse_xlsx(_file, row_dict=True)
            mappings = mmain(file_row_gen)
            context["file"] = mappings
    else:
        form = UploadFileForm()
        context["form"] = form
    return render(request, "motor_product/dashboard.html", context)