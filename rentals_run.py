from rentals import Rentals
print("choose filters you want. use numbers as your answers.")
print("your answer has to be in numbers. for example if you want filters 1,2 and 4 your answer has to be: 124 , order doesn't matter")
print("the min price has to be atleast 0 and the max price has to be atmost 1,000,000")
print("locations wanted to find has to be in range of 1 to 50.")
print("you can choose not to have any filters for each part by writing 'no'. ")
locations_wanted_to_find = input('how many locations do you want to get the average prive from ?: ')
target = input("which city is your target ? (1=Toronto , 2=Vancouver , 3=Richmond hill)(default is Toronto): ")
beds = input("how many beds ? (0=Studio , 1=1bed , 2=2beds , 3=3beds , 4=+4beds): ")
baths = input("how many baths ? (1=1bath , 2=2baths , 3=3baths , 4=4baths , 5=+5baths): ")
min_price = input("what's the min price ? (atleast 0): ")
max_price = input("what's the max price ? (atmost 10000): ")
type_of_the_location = input("what type ? (1=Apartment , 2=Condo , 3=House , 4=Room , 5=Townhouse , 6=Other): ")
pets = input("do you have pets ? (1=dog , 2=cat): ")
availability = input("be available ? (1=only if it is available): ")
laundry = input("laundry ? (1=In unit , 2=In building): ")
AC = input("AC ? (1=only if it has AC): ")
dishW = input("dish washer ? (1=only if it has dish washer): ")
garage_parking = input("garage/parking ? (1=only if it has garage/parking): ")
print('___________________________')
instance = Rentals(
    locations_wanted_to_find,
    beds,
    baths,
    min_price,
    max_price,
    type_of_the_location,
    pets,
    availability,
    laundry,
    AC,
    dishW,
    garage_parking,
    target
    )
price_list = instance.get_price_list()
average = instance.get_average(price_list)
print(price_list)
print(average)