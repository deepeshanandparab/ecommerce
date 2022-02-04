from store.models import Order
import datetime

def generate_product_sku(name, type, category):
    i = 0
    j = 0
    k = 0
    sku = []
    sku_number = ''
    
    while i<=2:
        sku.append(str(name)[i])
        i += 1
            
    while k<=2:
        sku.append(str(type)[k])
        k += 1

    while j<=2:
        sku.append(str(category)[j])
        j += 1

    for n in sku: 
        sku_number += n  

    return sku_number 


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
    return lastMonth.strftime("%B, %Y")
