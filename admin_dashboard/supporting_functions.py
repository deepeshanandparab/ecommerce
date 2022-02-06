from store.models import Order, ProductCategory
import datetime

def generate_custom_string(param1, param2, param3):
    i = 0
    j = 0
    k = 0
    list = []
    custom_string = ''
    
    while i<=2:
        list.append(str(param1)[i])
        i += 1
            
    while k<=2:
        list.append(str(param2)[k])
        k += 1

    while j<=2:
        list.append(str(param3)[j])
        j += 1

    for n in list: 
        custom_string += n  

    return custom_string.upper() 


def get_sale_count(month):

    orders_list_present_month = Order.objects.filter(date__month=month)
    orders_list_last_month = Order.objects.filter(date__month=month-1)

    count = len(orders_list_present_month) - len(orders_list_last_month)
    percentage = (count/len(orders_list_last_month))*100
    return int(percentage)

def get_previous_month():
    today = datetime.date.today()
    first = today.replace(day=1)
    lastMonth = first - datetime.timedelta(days=1)
    return lastMonth.strftime("%b, %Y")


def get_product_category(product_type_list):
    products_category_list = []
    i = 0
    for type in product_type_list:
        products_category = ProductCategory.objects.filter(type=type.id)
        products_category_list.append(products_category)
        print(products_category_list)
    
    return products_category_list
