from django_filters import rest_framework as filters

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = filters.DateFromToRangeFilter()
    status = filters.ChoiceFilter(
        choices=[
            ("OPEN", "Открыто"),
            ("CLOSED", "Закрыто"),
            ("DRAFT", "Черновик"),
        ]
    )

    class Meta:
        model = Advertisement
        fields = ["created_at", "status"]
