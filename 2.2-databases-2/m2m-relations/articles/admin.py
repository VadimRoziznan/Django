from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope



class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tag_name = []
        is_main_count = 0
        for form in self.forms:
            form.cleaned_data
            if form.cleaned_data.get('tag') in tag_name and form.cleaned_data.get('tag') is not None:
                raise ValidationError('Имена тегов не должны повторяться.')
            else:
                tag_name.append(form.cleaned_data.get('tag'))
            if form.cleaned_data.get('is_main'):
                is_main_count += 1
            if is_main_count == 2:
                raise ValidationError('Количество избранных тегов не должно быть больше одного.')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
