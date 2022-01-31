from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹ "+str(number)


def stringToList(string):
    list=[]
    list[:0]=string
    return list

def listToString(s): 
    string= "" 
    for ele in s: 
        string += ele  
    return string 


@register.filter(name='inrcurrency')
def inrcurrency(number):
    num = str(number)
    list = stringToList(num)
    if len(list) <= 3:
        value = listToString(list)
        return value
    elif len(list) > 3 and len(list) < 5:
        list.insert(1, ",")
        value = listToString(list) # value = 1,000
        return value
    elif len(list) == 5:
        list.insert(2, ",")
        value = listToString(list) # value = 1,000
        return value  
    elif len(list) > 5 and len(list) <= 7:
        list.insert(1, ",")
        list.insert(4,",")
        value = listToString(list) # value = 1,00,000
        return value
    elif len(list) > 7 and len(list) <= 9:
        list.insert(1, ",")
        list.insert(4,",")
        list.insert(7,",")
        value = listToString(list) # value = 1,00,00,000
        return value
    else:
        value = listToString(list)
        return value
      


@register.filter(name='multiply')
def multiply(number , number1):
    return number * number1


@register.filter(name='discountedprice')
def discountedprice(price , discount):
    return int(price * (1 - discount/100))


@register.filter(name='cart_count')
def cart_count(cart):
    return len(cart)


