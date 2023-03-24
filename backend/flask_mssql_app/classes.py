# ! COPIED HERE COS IDK HOW to IMPORT
import random
import time
import requests
# from .config import image_api_key
import os

rarity = ['common', 'uncommon', 'rare', 'epic', 'legendary']
species = ['Fish', 'Mammal', 'Reptile', 'Amphibian']
fish_names = ["Salmon", "Tuna", "Grouper", "Herring", "Carp", "Cod", "Catfish", "Hammerhead Shark", "Great White Shark", "Megalodon"]
mammal_names = ["Walrus", "Sea Otter", "Seal", "Sea Lion", "Orca", "Sperm Whale", "Humpback Whale", "Dolphin", "Porpoise", "Beluga Whale", "Gray Whale"]
reptile_names = ["Sea Turtle", "Alligator", "Crocodile", "Spectacled Caiman", "Green Anaconda", "Saltwater Crocodile"]
amphibian_names = ["Frog", "Toad", "Salamander", "Newt", "Caecilian", "Axolotl", "Fire-bellied toad"]

# ? Animal class is used to create an animal hatched from an egg
class Animal:
    # Static
    num_animals = 0

    # Dynamic
    def __init__(self, *args):

        self.dob = time.time()
        if len(args) == 1:
            # Date of birth is the time the animal was created
            self.rarity = args[0]
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
        else:
            # args should be [rarity, species, name, yield]
            self.rarity = args[0]
            self.species = args[1]
            self.name = args[2]
            self.coin_yield = args[3]

        self.coins_yielded = 0
        self.id = Animal.num_animals + 1
        Animal.num_animals += 1
        self.image = self.create_image()
    
    def __del__(self):
        print("Animal " + str(self.id) + " deleted from memory")


    def set_yield(self):
        # Yield is the amount of coins made per hour by the coin, and is based on the rarity of the animal
        # It will be based on the probability of getting each rarity, added with a random number from 0 to 10
        # The probability of getting each rarity is 50%, 30%, 15%, 4%, 1% respectively
        match self.rarity:
            case 'common':
                self.coin_yield = random.randint(0, 10) + 50/50 * 5
            case 'uncommon':
                self.coin_yield = random.randint(0, 20) + 40/30 * 10
            case 'rare':
                self.coin_yield = random.randint(0, 30) + 30/15 * 12.5
            case 'epic':
                self.coin_yield = random.randint(0, 40) + 20/4 * 17.5
            case 'legendary':
                self.coin_yield = random.randint(0, 50) + 10/1 * 20

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
        # remove from memory
        to_return = self.coins_yielded
        del self
        return to_return
    
    def create_image(self):
        # Create an image of the animal
        prompt = f"{self.rarity} {self.species} called {self.name}"
        try:
            api_key  = os.environ.get('IMAGE_API_KEY')
            res = requests.post(
                "https://api.deepai.org/api/text2img",
                data={
                    'text': prompt,
                    'grid_size': '1',
                },
                headers={'api-key': api_key}
            )
            url = res.json()['output_url']
        except:
            url = "https://www.gannett-cdn.com/presto/2022/10/24/USAT/6253d26d-8894-4a38-87ee-6c2f37b1c0d2-7._Miroslav-Srb_Hello-everyone_00001567.jpg?crop=2999,1687,x0,y300&width=1600&height=800&format=pjpg&auto=webp"
        return url

        

    def get_rarity(self):
        return self.rarity
    
    def get_species(self):
        return self.species

    def get_name(self):
        return self.name

    def get_yield(self):
        return self.coin_yield

    def get_id(self):
        return self.id
    
    def get_image(self):
        return self.image

    def print(self):
        print("ID: " + str(self.id))
        print("Image: " + self.image)
        print("Rarity: " + self.rarity)
        print("Species: " + self.species)
        print("Name: " + self.name)
        print("Yield: " + str(self.coin_yield))
        print("Coins Yielded: " + str(self.coins_yielded))

# ? Egg class is used to create an egg, which can be hatched to create an animal. Can be bought by user if they pay the cost
class Egg:
    def __init__(self, *args):
        # Rarity of the egg can be from [common, uncommon, rare, epic, legendary]
        # The spawn rate of each rarity is 50%, 30%, 15%, 4%, 1% respectively
        if len(args) < 2:
            self.rarity = random.choices(['common', 'uncommon', 'rare', 'epic', 'legendary'], weights=[50, 30, 15, 4, 1])[0]
            self.cost = 20
        else:
            self.rarity = args[0]
            self.cost = args[1]

    def get_rarity(self):
        return self.rarity

    def get_cost(self):
        return self.cost

    def hatch(self):
        return Animal(self.rarity)

    def return_json(self):
        return {"rarity": self.rarity, "cost": self.cost}

# ? Breeder class is used to combine two animals to create a new animal
class Breeder:
    def __init__(self, username):
        self.username = username
        self.inventory = []

    def add_animal(self, animal):
        # Add an animal to the breeder's inventory
        self.inventory.append(animal)

    def print_inventory(self):
        # Print the breeder's inventory
        for animal in self.inventory:
            animal.print()

    def get_inventory(self):
        return self.inventory

    # takes in two animal ids
    def breed(self, id_1, id_2):
        # first check if both animals are in the breeder's inventory
        if id_1 == id_2:
            return "Cannot breed the same animal"

        animal_1, animal_2 = None, None
        for animal in self.inventory:
            if animal.id == id_1:
                animal_1 = animal
            elif animal.id == id_2:
                animal_2 = animal

        if animal_1 == None or animal_2 == None:
            return "One or more of the animals are not in the breeder's inventory"
        
        # breeding logic
        # if the two animals are the same species, the new animal will be the same species
        # if the two animals are different species, the new animal will be a random species
        # the rarity of the new animal will be the rarity of the animal with the higher rarity
        # add a 1 % chance of upgrading the rarity of the new animal by 1
        # yield will be a random mix of the two animals' yields
        # name will be a random mix of the two animals' names

        # get the rarity of the new animal
        rarity_1 = animal_1.get_rarity()
        rarity_2 = animal_2.get_rarity()
        rarity_1_index = rarity.index(rarity_1)
        rarity_2_index = rarity.index(rarity_2)
        rarity_index = max(rarity_1_index, rarity_2_index)
        if random.randint(0, 100) == 1:
            rarity_index += 1
        rarity_index = min(rarity_index, 4)
        new_rarity = rarity[rarity_index]

        # get the species of the new animal
        species_1 = animal_1.get_species()
        species_2 = animal_2.get_species()
        if species_1 == species_2:
            new_species = species_1
        else:
            new_species = random.choice(species)
        
        # get the name of the new animal
        name_1 = animal_1.get_name()
        name_2 = animal_2.get_name()
        new_name = name_1 + " " + name_2

        # get the yield of the new animal
        yield_1 = animal_1.get_yield()
        yield_2 = animal_2.get_yield()

        yield_1 = random.randint(int(-yield_1/2), int(yield_1/2)) + yield_1
        yield_2 = random.randint(int(-yield_2/2), int(yield_2/2)) + yield_2
        weight = random.randint(0, 100)
        new_yield = (weight * yield_1 + (100 - weight) * yield_2) / 100

        # create the new animal
        new_animal = Animal(new_rarity, new_species, new_name, new_yield)

        # burn the two animals
        self.inventory.remove(animal_1)
        self.inventory.remove(animal_2)
        animal_1.burn()
        animal_2.burn()

        return new_animal

    