from .models import Option, CartItemOption
from django.core.exceptions import ValidationError
from django.db.models import Q
from shop.models.cartmodel import CartItem
from shop.models.productmodel import Product
from shop.util.cart import get_or_create_cart
from shop.views.cart import CartDetails
from shop_simplevariations.models import TextOption, CartItemTextOption, OptionGroup
from util import (
    parse_option_group_name,
    prefix as option_group_name_prefix,
    store_error,
    render_errors_response
)

class SimplevariationCartDetails(CartDetails):
    """Cart view that answers GET and POSTS request."""

    def post(self, *args, **kwargs):
        # get a copy of POST so it is mutable
        post = self.request.POST.copy()
        
        #it starts similar to the original post method
        product_id = post['add_item_id']
        product_quantity = post.get('add_item_quantity')
        if not product_quantity:
            product_quantity = 1
        product = Product.objects.get(pk=product_id)
        cart_object = get_or_create_cart(self.request, save=True)

        #now we need to find out which options have been chosen by the user
        option_ids = []
        text_option_ids = {} # A dict of {TextOption.id:CartItemTextOption.text}
        
        errors = {}
        for key in post.keys():
            if key.startswith(option_group_name_prefix):
                pk = post[key]
                if pk:
                    option_ids.append(pk)
                else:
                    # verify the option isn't required
                    data = parse_option_group_name(key)
                    og = OptionGroup.objects.get(pk=data["pk"])
                    if og.required:
                        choose_count = og.get_choose_count()
                        ek = u"%s%s" % (
                            og,
                            u" (%d of %d)" % (
                                data["choice"],
                                choose_count
                            ) if 1 < choose_count else ""
                        )
                        store_error(errors, ek, "Required", "You must make a selection")
            elif key.startswith('add_item_text_option_'):
                pk = key.split('add_item_text_option_')[1]
                txtopt = TextOption.objects.get(pk=pk)
                txt = post[key]
                if txt:
                    text_option_ids.update({pk:txt})
                    
                    # verify text meets max_length requirements
                    if txtopt.max_length and txtopt.max_length < len(txt):
                        store_error(errors, txtopt.name, "Max Length", "Field Is Too Long")
                else:
                    # verify the option isn't required
                    if txtopt.required:
                        store_error(errors, txtopt.name, "Required", "Field Is Required")
        
        if errors:
            return render_errors_response(
                request = self.request,
                template_name = "shop/cart_validation_errors.html",
                errors = errors
            )
        
        #now we need to find out if there are any cart items that have the exact
        #same set of options
        qs = CartItem.objects.filter(cart=cart_object).filter(product=product)
        found_cartitem_id = None
        merge = False
        for cartitem in qs:
            # for each CartItem in the Cart, get it's options and text options
            cartitemoptions = CartItemOption.objects.filter(
                cartitem=cartitem, option__in=option_ids
                )
                
            cartitemtxtoptions = CartItemTextOption.objects.filter(
                text_option__in=text_option_ids.keys(),
                text__in=text_option_ids.values()
                )
            
            if len(cartitemoptions) + len(cartitemtxtoptions) == (len(option_ids) + len(text_option_ids)):
                found_cartitem_id = cartitem.id
                merge = True
                break

        #if we found a CartItem object that has the same options, we need
        #to select this one instead of just any CartItem that belongs to this
        #cart and this product.
        if found_cartitem_id:
            qs = CartItem.objects.filter(pk=found_cartitem_id)

        cart_item = cart_object.add_product(
            product, product_quantity, merge=merge, queryset=qs)
        cart_object.save()
        return self.post_success(product, cart_item)

    def post_success(self, product, cart_item, post=None):
        super(SimplevariationCartDetails, self).post_success(product, cart_item)
        #if this cart item already has an option set we don't need to do
        #anything because an existing option set will never change. if we got a
        #set of different options, that would become a new CartItem.
        if cart_item.cartitemoption_set.exists():
            return self.success()

        post = self.request.POST
        for key in post.keys():
            if key.startswith(option_group_name_prefix):
                pk = post[key]
                if not pk:
                    # blank option group was already validated
                    # and allowed by the time this point
                    # is reached, so just skip it
                    continue
                data = parse_option_group_name(key)
                group = OptionGroup.objects.get(pk=data["pk"])
                option = Option.objects.get(pk=pk)
                cartitem_option = CartItemOption()
                cartitem_option.cartitem = cart_item
                cartitem_option.option = option
                cartitem_option.group = group
                cartitem_option.choice = data["choice"]
                cartitem_option.save()
            elif key.startswith('add_item_text_option_'):
                txt = post[key]
                if not txt:
                    # blank text option was already validated
                    # and allowed by the time this point
                    # is reached, so just skip it
                    continue
                pk = key.split('add_item_text_option_')[1]
                txt_opt = TextOption.objects.get(pk=pk)
                cito = CartItemTextOption()
                cito.text_option = txt_opt
                cito.text = txt
                cito.cartitem = cart_item
                cito.save()
                
        return self.success()
