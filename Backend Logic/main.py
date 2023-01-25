import random
import time

rarity = ['common', 'uncommon', 'rare', 'epic', 'legendary']
species = ['Fish', 'Mammal', 'Reptile', 'Amphibian']
fish_names = ["Salmon", "Tuna", "Grouper", "Herring", "Carp", "Cod", "Catfish", "Hammerhead Shark", "Great White Shark", "Megalodon"]
mammal_names = ["Walrus", "Sea Otter", "Seal", "Sea Lion", "Orca", "Sperm Whale", "Humpback Whale"]
reptile_names = ["Sea Turtle", "Alligator", "Crocodile"]
amphibian_names = ["Frog", "Toad", "Salamander", "Newt"]

class Animal:
    def __init__(self, rarity):
        # Date of birth is the time the animal was created
        self.dob = time.time()
        self.rarity = rarity
        # Species of the animal can be [Fish, Mammal, Reptile, Amphibian]
        animal_type = random.choice(species)
        self.species = animal_type
        
        match animal_type:
            case 'Fish':
                self.name = random.choice(fish_names)
            case 'Mammal':
                self.name = random.choice(mammal_names)
            case 'Reptile':
                self.name = random.choice(reptile_names)
            case 'Amphibian':
                self.name = random.choice(amphibian_names)
            case _:
                self.name = "Unknown"

        self.set_yield()
        self.coins_yielded = 0

    def set_yield(self):
        # Yield is the amount of coins made per hour by the coin, and is based on the rarity of the animal
        # It will be based on the probability of getting each rarity, added with a random number from 0 to 10
        # The probability of getting each rarity is 50%, 30%, 15%, 4%, 1% respectively
        match self.rarity:
            case 'common':
                self.coin_yield = random.randint(0, 10) + 50/50 * 20
            case 'uncommon':
                self.coin_yield = random.randint(0, 20) + 50/30 * 20
            case 'rare':
                self.coin_yield = random.randint(0, 30) + 50/15 * 20
            case 'epic':
                self.coin_yield = random.randint(0, 40) + 50/4 * 20
            case 'legendary':
                self.coin_yield = random.randint(0, 50) + 50/1 * 20

    def update_yielded_coins(self):
        # Get current time
        current_time = time.time()
        # Get the time difference between current time and date of birth
        time_diff = current_time - self.dob
        # Get the number of hours passed since the animal was created
        hours_passed = time_diff / 3600
        # Get the number of coins yielded by the animal
        self.coins_yielded = self.coin_yield * hours_passed

    def burn(self):
        # burning the animal destroys it and gives the user the coins yielded by the animal
        self.update_yielded_coins()
        return self.coins_yielded
        

    def get_rarity(self):
        return self.rarity
    
    def get_species(self):
        return self.species

    def get_name(self):
        return self.name

    def print(self):
        print("Rarity: " + self.rarity)
        print("Species: " + self.species)
        print("Name: " + self.name)
        print("Yield: " + str(self.coin_yield))
        print("Coins Yielded: " + str(self.coins_yielded))


class Egg:
    def __init__(self):
        # Rarity of the egg can be from [common, uncommon, rare, epic, legendary]
        # The spawn rate of each rarity is 50%, 30%, 15%, 4%, 1% respectively
        self.rarity = random.choices(['common', 'uncommon', 'rare', 'epic', 'legendary'], weights=[50, 30, 15, 4, 1])[0]
        self.cost = 20

    def get_rarity(self):
        return self.rarity

    def get_cost(self):
        return self.cost

    def hatch(self):
        return Animal(self.rarity)

test = Egg()
test = test.hatch()
test.print()