import csv
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse("bus_stations"))


def bus_stations(request):
    CONTENT = []
    with open(BUS_STATION_CSV, newline="", encoding="UTF-8") as csv_file:
        data = csv.DictReader(csv_file)
        for el in data:
            CONTENT.append(
                {"Name": el["Name"], "Street": el["Street"], "District": el["District"]}
            )
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(CONTENT, 2)
    page = paginator.get_page(page_number)
    context = {"bus_stations": page, "page": page}
    return render(request, "stations/index.html", context)
