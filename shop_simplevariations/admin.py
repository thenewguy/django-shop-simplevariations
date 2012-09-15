#-*- coding: utf-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.admin.options import TabularInline, ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.urlresolvers import resolve
from django.utils.translation import ugettext_lazy as _
from shop_simplevariations.models import Option, OptionGroup, TextOption, OptionGroupOption

class OptionGroupOptionInline(TabularInline):
    model = OptionGroupOption
    verbose_name = "default option"
    verbose_name_plural = u"%ss" % verbose_name
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "option":
            # limit defaults to valid options of the OptionGroup
            match = resolve(request.get_full_path())
            if len(match.args) == 1:
                object_id = match.args[0]
            if object_id:
                og = OptionGroup.objects.get(pk=object_id)
                option_pks = og.get_options().values_list('pk', flat=True)
                kwargs.setdefault('queryset', Option.objects.filter(pk__in=option_pks))
        
        return super(OptionGroupOptionInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

class OptionInline(TabularInline):
    model = Option

class OptionGroupAdmin(ModelAdmin):
    inlines = [OptionInline, OptionGroupOptionInline]
    prepopulated_fields = {"slug": ("name",)}
    
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name=_('products'),
            is_stacked=False
        )},
    }

admin.site.register(OptionGroup, OptionGroupAdmin)

class TextOptionAdmin(ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name=_('products'),
            is_stacked=False
            )},
    }

admin.site.register(TextOption, TextOptionAdmin)
