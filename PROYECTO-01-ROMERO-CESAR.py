#!/usr/bin/env python
# coding: utf-8


import lifestore_file as ls  #import file of lists provided 


#renaming lists
searches, sales, products = ls.lifestore_searches, ls.lifestore_sales,ls.lifestore_products


# ## 1. Productos más vendidos y productos rezagados

# ### *1.1 Top best sales*


#Getting just id of products sold
total_sales = []
for index in range(len(sales)):
    total_sales.append(sales[index][1]) 


#Getting total sales per index
sales_by_index = {}  #Declare empty dictionary

#Verify the quantity of sales a product had 
for id_product in range(len(products)):
    if id_product in total_sales:
        sales_by_index[id_product] = total_sales.count(id_product)  # .count specifies the quantity



# Changing id_products to their product_names 
sales_by_names = {}
for id_product,quantity_sold in sales_by_index.items():
    sales_by_names[products[id_product-1][1]] = quantity_sold   # id_product-1 indicates index on product list, since it starts at 0



#Sorting products by quantity_sold (using lambda functiom)
top_sales = sorted(sales_by_names.items(), key=lambda x: x[1], reverse=True)



#Verify the stock available for products which were sold
stock_of_sold_products = {}
for id_product,name,price,category,stock in products:
    if id_product in sales_by_index.keys():
        stock_of_sold_products[id_product] = stock


        
# ### *1.2 Products without  sales*

#Products not sold and their stock 
not_sold_products = {}
for id_product,name,price,category,stock in products:
    if id_product not in sales_by_index.keys():     
        not_sold_products[products[id_product-1][1]] = stock       #Dict keys and values = products_names and stocks respectively
    
#This is the list of products with not sales sort by their stock     
lagging_products= sorted(not_sold_products.items(), key=lambda x: x[1], reverse=True)    



# ### *1.3 Searches by products*


#Getting total product searches
total_searches = []
searches_by_index = {}

for id_search,id_product in searches: total_searches.append(id_product) 
#Verifying number of searches by product
for id_product in range(1,len(products)+1): # products from 1 to 96
    if id_product in total_searches: 
        searches_by_index[id_product] = total_searches.count(id_product) # .count inicates total number of searches



#Converting id_products to their respective names
searches_by_names = {}
for id_product,number_of_searches in searches_by_index.items():
    searches_by_names[products[id_product-1][1]] = number_of_searches



#Gettin the top of products most searched (sorted using lambda function)
top_searches = sorted(searches_by_names.items(), key=lambda x: x[1], reverse=True)



# ### *1.4 Sales and Searches by categories*


#Getting list of products which belong to each category (there are 8 categories)
total_categories = {}
for id_product, name, price, category, stock in products:
    if category not in total_categories.keys():
        total_categories[category] = [id_product]
    else: 
        total_categories[category].append(id_product)



#Getting lists of searches of each product belonging to each category
searches_by_categories = {}
for category,list_products in total_categories.items():
    searches_by_categories[category] = []
    for id_product,searches in searches_by_index.items():
        if id_product in list_products:
            searches_by_categories[category].append((id_product,searches))
            
#Sorting, for each category, their products considering num of searches.
for category,lists in searches_by_categories.items():
    searches_by_categories[category] = sorted(lists, key=lambda x: x[1], reverse=True)


#Top searches per categories
top_categories_searches = list(searches_by_categories.items())


#Getting sales to each category 
sales_by_categories = {}
for category,list_products in total_categories.items():
    sales_by_categories[category] = []
    for id_product,num_sales in sales_by_index.items():
        if id_product in list_products:
            sales_by_categories[category].append((id_product,num_sales))

#Sorting products of each category considering quantity sold
for category,lists in sales_by_categories.items():
    sales_by_categories[category] = sorted(lists, key=lambda x: x[1], reverse=True)


#top products sales for each category 
top_categories_sales = list(sales_by_categories.items())



# ## 2.Productos por reseña en el servicio


#Generating list of products by score
best_rated = {}
for id_sale,id_product,rate,date,refund in sales:
    if rate not in best_rated.keys():
        best_rated[rate] = [id_product]
    else: best_rated[rate].append(id_product)


#To each score_rate, sort id_products considering rates given and refund
top_best_rated = {}
for rate, products_list in best_rated.items():
    top_best_rated[rate] = []
    for id_product in range(len(products)):
        if id_product in products_list:
            top_best_rated[rate].append((id_product,products_list.count(id_product)))
        else: continue
#Sorting using lambda function
for rate,products_list in top_best_rated.items():
    top_best_rated[rate] = sorted(products_list, key=lambda x: x[1], reverse=True)


#Verifying which products were sold and then returned to the store
refunds = []
total_refunds = {}
#Get product names and the number of times they were returned 
for id_sale,id_product,rate,date,refund in sales:
    if refund == 1: refunds.append(products[id_product-1][1])
for product in refunds:
    if product not in total_refunds.keys(): total_refunds[product] = refunds.count(product)
    else: continue


#Getting list of products based on the number of times they were returned
products_refunded = sorted(total_refunds.items(), key=lambda x: x[1], reverse=True)



# ## 3. Total de ingresos y ventas promedio mensuales

# ### *3.1 Total_incomes*


#Getting incomes per each product
incomes = []
for product in total_sales:
        incomes.append(products[product-1][2])


#Total income
total_income = sum(incomes)


# ### *3.2 Incomes per months and year*


import datetime  #To mmodify dates

#Changing format of the dates to datetime
#Generatin list of sales by date
sales_date = []
for id_sales,id_product,rate,date,refund in sales:
    new_date = datetime.datetime.strptime(date, '%d/%m/%Y').date()
    sales_date.append((id_product,new_date))


#Generating lists of months per year
months_2019 = []
months_2020 = []
for id_product,date in sales_date:
    if date.year == 2020:
        months_2020.append(date.month)
    elif date.year == 2019: months_2019.append(date.month)
        
#Generatin a dict of dicts, to each year, show the quantity of sales by months registered
monthly_sales = {}
monthly_sales[2019]={}
monthly_sales[2020]={}
for month in range(1,13):
    if month in months_2019:
        monthly_sales[2019][month] = months_2019.count(month)
    elif month in months_2020:
        monthly_sales[2020][month] = months_2020.count(month)   
       

month_names = ["Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]


#Total incomes per year
incomes_per_year = {}
for year in monthly_sales.keys():
    year_income = 0
    for months in monthly_sales[year].keys():
        for dates,price in zip(sales_date,incomes):
            if dates[1].year == year:
                if dates[1].month == months:
                    year_income += price
    incomes_per_year[year] = year_income


#Total incomes per month
incomes_per_month = {}
#Considering all months (both 2019 and 2020)
for months in list(monthly_sales[2020].keys())+list(monthly_sales[2019].keys()):
    q_income = 0
    for dates,price in zip(sales_date,incomes):
        if dates[1].month == months:
            q_income += price
        else: continue
    incomes_per_month[months] = (month_names[months-1],q_income)


#Sort months by the income generated
top_month_incomes = sorted(list(incomes_per_month.items()),key= lambda x: x[1][1], reverse=True)


# ## 4. Menu

#This is the interactive menu made

print("\n^^^^^^^^^^^^^^^^^^^^^/ Bienvenido a LifeStore \^^^^^^^^^^^^^^^^^^^^^\n")
print("Ingresar como:\n 1.Administrador\n 2.Usuario")

#Login selection 
valid_option = False
while valid_option == False:
    try:
        login = int(input("Número de elección:"))
        if login !=1 and login !=2: print(" ¡¡OPCIÓN NO VÁLIDA!!. Inténtalo de nuevo...")
        else: valid_option = True
    except:
        print(" ¡¡OPCIÓN NO VÁLIDA!!. Sólo números, Inténtalo de nuevo...")

#Menu for administrators
if login == 1:
    name = input("Nombre: ")
    print("\n¡Genial! {} as accedido como administrador, estas son tus opciones:\n".format(name))
    print('\\\\\\\\\\\\\\\\\\\ Menú ////////////\n')
    print(' 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
    valid_options = [1,2,3,4,5,6,7,8,9,10]
    option = None
    while option not in valid_options:
        try:
            option = int(input("Selecciona una: "))
            if option not in valid_options: print("OPCIÓN NO VÁLIDA!!. Solo números del 1 al 10...")
        except:
            print(" ¡¡OPCIÓN NO VÁLIDA!!. Solo números del 1 al 10...")
    
    while option in valid_options:
        
        if option ==1:
            print("\n>>> //PRODUCTOS MÁS VENDIDOS\\ <<<")
            print("\n|Top|____________________________________________|Producto|_____________________________________|Piezas vendidas|\n")
            count = 1
            for name,amount in top_sales:
                print(count ,"º | ", name, "| ",amount, "pzs\n")
                count+=1
            
            print("\n\n**!PRODUCTOS SIN O CON POCO STOCK DISPONIBLE!**")
            print("\n|Producto|______________________________________________________________________________________|Stock actual|\n")
            for id_product,q_stock in stock_of_sold_products.items():
                if q_stock < 3:
                    print(products[id_product][1]," | ",q_stock,"pzs\n")
            print("\n¡CONSIDERE SURTIR ESTOS PRODUCTOS PRONTO!")
                
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
        
        
        elif option == 2:
            print("\n>>> //PRODUCTOS REZAGADOS\\ <<<")
            print("\n|Top|___________________________________________|Producto|_____________________________________|Stock disponible|\n")
            count = 1
            for names,stock in lagging_products:
                print(count ,"º | ", names, "| ",stock, "pzs\n")
                count+=1
                
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
                
        elif option == 3: 
            print("\n>>> //VENTAS POR CATEGORÍA\\ <<<")
            for categories,lists in top_categories_sales:
                print("\n|xx ",categories,"xx|\n")
                print("\n|Top|____________________________________________|Producto|_____________________________________|Piezas vendidas|\n")
                count = 1
                for id_product,quant_sold in lists:
                    print(count ,"º |",products[id_product-1][1], " | ",quant_sold,"pzs\n")
                    count+=1
            
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                    
                    
        elif option == 4:
            print("\n>>> //PRODUCTOS MÁS BUSCADOS\\ <<<")
            print("\n|Top|_________________________________________|Producto|_____________________________________|Total de búsquedas|\n")
            count = 1
            for names,num_searches in top_searches:
                print(count ,"º |", names, "| ",num_searches, "\n")
                count+=1
                if count > 25: break
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
    
    
        elif option == 5:
            print("\n>>> //PRODUCTOS MENOS BUSCADOS\\ <<<")
            print("\n|Top|_________________________________________|Producto|_____________________________________|Total de búsquedas|\n")
            count = 1
            for names,num_searches in top_searches[::-1]:
                print(count ,"º |", names, "| ",num_searches, "\n")
                count+=1
                if count > 25: break
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
    
    
        elif option ==6:
            print("\n>>> //BÚSQUEDAS POR CATEGORÍA\\ <<<")
            for categories,lists in top_categories_searches:
                print("\n|xx",categories,"xx|\n")
                print("\n|Top|_________________________________________|Producto|_____________________________________|Total de búsquedas|\n")
                count = 1
                for id_product,num_searches in lists:
                    print(count ,"º |",products[id_product-1][1], " | ",num_searches,"\n")
                    count+=1
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
    
        elif option==7:
            print("\n>>> //PRODUCTOS MEJOR CALIFICADOS\\ <<<")
            print("\n|Top|____________________________|Producto|________________________|Total de Reseñas|__________|Calificación|\n")
            count = 1
            for id_product,num_rates in top_best_rated[5]:
                print(count ,"º |",products[id_product-1][1], " |  ",num_rates,"  | ","*"*5,"\n")
                count+=1
                if count > 20: break
            
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
            
        elif option==8:
            print("\n>>> //PRODUCTOS PEOR CALIFICADOS\\ <<<")
            print("\n|Top|____________________________|Producto|________________________|Total de Reseñas|__________|Calificación|\n")
            count = 1
            for rates,lists in list(top_best_rated.items())[::-1]:
                for id_product,num_rates in lists:
                    print(count ,"º |",products[id_product-1][1], " |  ",num_rates,"  | ","*"*rates,"\n")
                    count+=1
                if count > 20: break
            
            print("\n**PRODUCTOS REEMBOLSADOS!**")
            print("\n|Product|_______________________________________________________________|Total de reembolsos|\n")
            for product_names,num_refunds in products_refunded:
                print(product_names," | ",num_refunds,"pzs\n")
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
                    
        elif option==9:
            print("\n>>> //REPORTE DE INGRESOS\\\ <<<")
            print("\n ·o \Ingresos totales/ : $",total_income)
            print("\n\n ·o \Ingresos anuales/")
            for year,y_income in incomes_per_year.items():
                print("    ",year,": $",y_income)
            print("\n\n ·o \Promedio de ingresos mensuales/ : $", "%.2f" % (total_income/12))
            print("\n\n ·o \Ingresos mensuales/")
            for year,lists in monthly_sales.items():
                print("\n\n    ~",year,"~\n")
                print("    ·Promedio de ventas mensuales: ",(sum(monthly_sales[year].values())/len(monthly_sales[year].values())))
                print("\n Top|______|Mes|______|Total de ventas|_____|Ingresos totales")
                count = 1
                for month_id,month_income in top_month_incomes:
                    if month_id in lists:
                        print("  \n",count ,"º |  ",month_income[0],"  |   ",lists[month_id],"  |   $",month_income[1])
                        count+=1
                        
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n 1: Productos más vendidos\n 2: Productos rezagados\n 3: Ventas por categoría\n 4: Productos más buscados\n 5: Productos menos buscados\n 6: Búsquedas por categoría\n 7: Productos mejor calificados\n 8: Productos peor calificados\n 9: Reporte de ingresos\n 10:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
        
        elif option == 10:
            print("\nGracias por su visita :)")
            option = None
        
                
        
#Menu for users            
elif login == 2: 
    name = input("Nombre: ")
    print("\n¡Genial! {} as accedido como usuario, estas son tus opciones:\n".format(name))
    print('\\\\\\\\\\\\\\\\\\\ Menú ////////////\n')
    print(' 1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
    valid_options = [1,2,3,4,5,6]
    option = None
    while option not in valid_options:
        try:
            option = int(input("Selecciona una: "))
            if option not in valid_options: print("OPCIÓN NO VÁLIDA!!. Solo números del 1 al 6...")
        except:
            print(" ¡¡OPCIÓN NO VÁLIDA!!. Solo números del 1 al 6...")
    
    while option in valid_options:
        
        if option ==1:
            print("\n>>> //PRODUCTOS MÁS VENDIDOS\\ <<<")
            print("\n|Top|____________________________________________|Producto|_____________________________________|Piezas vendidas|\n")
            count = 1
            for name,amount in top_sales:
                print(count ,"º | ", name, "| ",amount, "pzs\n")
                count+=1
                
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
        
                
                
        elif option == 2: 
            print("\n>>> //MÁS VENDIDOS POR CATEGORÍA\\ <<<")
            for categories,lists in top_categories_sales:
                print("\n|xx ",categories,"xx|\n")
                print("\n|Top|____________________________________________|Producto|_____________________________________|Piezas vendidas|\n")
                count = 1
                for id_product,quant_sold in lists:
                    print(count ,"º |",products[id_product-1][1], " | ",quant_sold,"pzs\n")
                    count+=1
            
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                    
                    
        elif option == 3:
            print("\n>>> //PRODUCTOS MÁS BUSCADOS\\ <<<")
            print("\n|Top|_________________________________________|Producto|_____________________________________|Total de búsquedas|\n")
            count = 1
            for names,num_searches in top_searches:
                print(count ,"º |", names, "| ",num_searches, "\n")
                count+=1
                if count > 25: break
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
    

    
        elif option ==4:
            print("\n>>> //MÁS BUSCADOS POR CATEGORÍA\\ <<<")
            for categories,lists in top_categories_searches:
                print("\n|xx",categories,"xx|\n")
                print("\n|Top|_________________________________________|Producto|_____________________________________|Total de búsquedas|\n")
                count = 1
                for id_product,num_searches in lists:
                    print(count ,"º |",products[id_product-1][1], " | ",num_searches,"\n")
                    count+=1
                    
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
    
        elif option==5:
            print("\n>>> //PRODUCTOS MEJOR CALIFICADOS\\ <<<")
            print("\n|Top|____________________________|Producto|________________________|Total de Reseñas|__________|Calificación|\n")
            count = 1
            for id_product,num_rates in top_best_rated[5]:
                print(count ,"º |",products[id_product-1][1], " |  ",num_rates,"  | ","*"*5,"\n")
                count+=1
                if count > 20: break
            
            ans = input("\nDeseas seleccionar otra opción (Si/No):")
            if ans == 'Si' or ans == 'si' or ans =='SI':
                option = 0
                while option not in valid_options:
                    try:
                        print('\n1: Productos más vendidos\n 2: Más vendidos por categoría\n 3: Productos más buscados\n 4: Más búscados por categoría\n 5: Productos mejor calificados\n 6:Salir')
                        option = int(input("Selecciona una: "))
                        if option not in valid_options: print("\nOPCIÓN NO VÁLIDA!. Intenta de nuevo..")
                    except:
                        print("\nOPCIÓN NO VÁLIDA! Intenta de nuevo...")
            else:
                print("Gracias por su visita :)")
                option = None
                
        
        elif option == 6:
            print("\nGracias por su visita :)")
            option = None
        

