# -*- coding: utf-8 -*-
from django.core.validators import MinValueValidator
from django.db import models
from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.fields import CurrencyField

#===============================================================================
# Text options
#===============================================================================

class TextOption(models.Model):
    """
    This part of the option is selected by the merchant - it lets him/her "flag"
    a product as being able to receive some text as an option, and sets its
    price.
    """
    name = models.CharField(max_length=255, help_text="A name for this option - this will be displayed to the user")
    description = models.CharField(max_length=255, null=True, blank=True, help_text='A longer description for this option')
    price = CurrencyField(help_text='The price for this custom text') # The price
    max_length = models.PositiveIntegerField(default=0, help_text='Limit the amount of text allowed.  A value of 0 means unlimited')
    products = models.ManyToManyField(Product, related_name='text_options')
    required = models.BooleanField(default=True, blank=True)
    
    
    def __unicode__(self):
        return self.name

class CartItemTextOption(models.Model):
    """
    An option representing a bit of custom text a customer can define, i.e.
    for engraving or custom printing etc...
    The text is stored on the cart item because we assume we will not engrave or
    print many times the same bit of text. 
    
    If your use case is different, you should probably make a "text bit" Model
    """
    text = models.TextField() # The actual text the client input
    
    text_option = models.ForeignKey(TextOption)
    cartitem = models.ForeignKey(CartItem, related_name='text_option')
    
    def __unicode__(self):
        return self.text

#===============================================================================
# Multiple choice options
#===============================================================================
class GroupDefaultOptionThrough(models.Model):
    class Meta:
        ordering = ["order"]
    
    group = models.ForeignKey("OptionGroup")
    option = models.ForeignKey("Option")
    order = models.FloatField(default=0)

class GroupProductThrough(models.Model):
    class Meta:
        ordering = ["order"]
        unique_together = ("group", "product")
        
    group = models.ForeignKey("OptionGroup")
    product = models.ForeignKey(Product)
    order = models.FloatField(default=0)

class OptionGroup(models.Model):
    '''
    A logical group of options
    Example:

    "Colors"
    '''
    name = models.CharField(max_length=255)
    slug = models.SlugField() # Used in forms for example
    description = models.CharField(max_length=255, blank=True, null=True)
    products = models.ManyToManyField(Product, through=GroupProductThrough,
                                      blank=True, null=True)
    subgroup = models.ForeignKey('self', blank=True, null=True)
    choose_count = models.PositiveSmallIntegerField(default=0)
    required = models.BooleanField(default=True, blank=True)
    defaults = models.ManyToManyField("Option", through=GroupDefaultOptionThrough, null=True, blank=True)

    def __unicode__(self):
        return self.name

    def get_options(self):
        '''
        A helper method to retrieve a list of options in this OptionGroup
        '''
        group = self
        groups = []
        while group:
            groups.append(group)
            group = group.subgroup
            if group in groups:
                break
        return Option.objects.filter(group__in=groups)
    
    def get_defaults(self):
        '''
        A helper method to retrieve the default options.  If "defaults" is not set and
        subgroup is set, attempt to traverse the subgroup tree until defaults are found.
        '''
        ogos = GroupDefaultOptionThrough.objects.filter(group=self)
        defaults = [ogo.option for ogo in ogos]
        if not defaults and self.subgroup:
            defaults = self.subgroup.get_defaults()
        return defaults 
        
    def get_choose_count(self, groups=None):
        '''
        A helper method to retrieve the choose_count.  If choose_count is zero
        and subgroup is set, use the subgroup's choose_count.  If the final
        choose_count is zero, return 1 because a choose_count of zero
        does not make sense.
        '''
        choose_count = self.choose_count
        if not choose_count and self.subgroup:
            if groups is None:
                groups = []
            if self not in groups:
                groups.append(self)
                choose_count = self.subgroup.get_choose_count(groups=groups)
        if not choose_count:
            choose_count = 1
        return choose_count 

class Option(models.Model):
    '''
    A product option. Examples:

    "Red": 10$
    "Blue": 5$
    ...
    '''
    name = models.CharField(max_length=255)
    price = CurrencyField() # Can be negative
    group = models.ForeignKey(OptionGroup)

    def __unicode__(self):
        return self.name

class CartItemOption(models.Model):
    '''
    This holds the relation to product options from the cart item.
    It allows to know which options where selected for what cartItem.

    Generally, this is used by
    shop.cart.modifiers.product_options.ProductOptionsModifier
    '''
    class Meta:
        ordering = ('group', 'choice')
        
    cartitem = models.ForeignKey(CartItem)
    option = models.ForeignKey(Option)
    group = models.ForeignKey(OptionGroup)
    choice = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0)])

