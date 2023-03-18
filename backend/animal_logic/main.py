import classes

username = "kiriketsuki"
breeder = classes.Breeder(username)

# get two eggs
egg1 = classes.Egg()
egg2 = classes.Egg()

# hatch the eggs
animal1 = egg1.hatch()
animal2 = egg2.hatch()

# add the animals to the breeder's inventory
breeder.add_animal(animal1)
breeder.add_animal(animal2)

# print the breeder's inventory
breeder.print_inventory()

new_animal = breeder.breed(1, 2)
new_animal.print()
