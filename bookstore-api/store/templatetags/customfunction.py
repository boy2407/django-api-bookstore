import locale

from django.utils.safestring import mark_safe
from django import template

register = template.Library()

shippingConst = 100_000


@register.filter(name='text_short')
def text_short(value):
    temp = value[0:50]
    return temp


@register.filter(name='formatcurrency')
def formatcurrency(value):
    # Thiết lập ngôn ngữ là tiếng Việt và đơn vị tiền tệ là VND
    # locale.setlocale(locale.LC_ALL, 'vi_VN.utf8')
    # return locale.currency(value, grouping=True)
    return "{:,.0f}".format(float(value))



@register.filter(name='shipping')
def shipping(value):
    return shippingConst


@register.filter(name='payabletotal')
def payabletotal(value, discount):
    return (value + shippingConst) - discount

@register.filter(name='averagerating')
def averagerating(value, args):
    temp = value / args
    if int(temp + 0.5) > int(temp):
        temp = int(temp + 0.5)
    else:
        temp = int(temp)

    if temp > 5:
        temp = 5

    if temp == 1:
        temp1 = ("<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>")
    elif temp == 2:
        temp1 = ("<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>")

    elif temp == 3:
        temp1 = ("<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>")
    elif temp == 4:
        temp1 = ("<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb '><i class='fa-solid fa-star'></i></button>")
    else:
        temp1 = ("<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>"
                 "<button class='star-fb default-star'><i class='fa-solid fa-star'></i></button>")

    return mark_safe(temp1)


@register.filter(name='subtotal')
def subtotal(value, args):
    return value * args
