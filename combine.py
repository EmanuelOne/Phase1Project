from random import randrange


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, attack, defence, magic, ):
        self.maximum_hp = hp
        self.maximum_mp = mp
        self.hp = hp
        self.name = name
        self.defence = defence
        self.mp = mp
        self.attack_low = attack - 5
        self.attack_high = attack + 20
        self.magic = magic
        self.actions = ['Attack', 'Magic']
        # self.item = item

    def generate_damage(self):
        return randrange(self.attack_low, self.attack_high)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def get_hp(self):
        return self.hp

    def get_maximum_hp(self):
        return self.maximum_hp

    def get_mp(self):
        return self.mp

    def get_maximum_mp(self):
        return self.maximum_mp

    def reduce_magic_point(self, cost):
        self.mp -= cost

    def choose_action(self):
        print(bcolors.HEADER + bcolors.OKGREEN + bcolors.BOLD + "Actions" + bcolors.ENDC)
        i = 1
        for item in self.actions:
            print("{0} : {1}".format(i, item))
            i += 1

    def choose_magic(self):
        print(bcolors.OKBLUE + bcolors.BOLD + "Magic" + bcolors.ENDC)
        i = 1
        for spell in self.magic:
            print(f"{i} : {spell.name}  (cost : {spell.cost})")
            i += 1

    def heal(self, hp):
        self.hp += hp
        if self.hp > self.maximum_hp:
            self.hp = self.maximum_hp


class Magic:
    def __init__(self, name, cost, damage, mode):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.mode = mode

    def generate_damage(self):
        low = self.damage - 15
        high = self.damage + 15
        return randrange(low, high)


fire = Magic("Fire", 8, 100, 'Black')
blizzard = Magic("Blizzard", 12, 150, 'Black')
thunder = Magic("Thunder", 10, 120, 'Black')
meteor = Magic("Meteor", 15, 160, 'Black')
quake = Magic("Quake", 20, 250, 'Black')
cure = Magic("Cure", 12, 120, "White")
coral = Magic("Coral", 18, 200, "White")

player = Person(input("Enter Player name : ").capitalize(), 1000, 65, 60, 34,
                [fire, blizzard, thunder, meteor, quake, cure, coral])
enemy = Person("Enemy", 2000, 65, 45, 25, [])
print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACK GAME" + bcolors.ENDC, "\n====================")
print(
    f"\nWelcome! {bcolors.OKGREEN + bcolors.BOLD + player.name + bcolors.ENDC}  \n\nMaximum Hp of {player.name} : {player.maximum_hp}\nMaximum Hp of Enemy {enemy.maximum_hp}")
levels = ["Easy", "Medium", "Hard"]
print("---------------------\nDifficulty Levels\n")
for i in enumerate(levels):
    print(f"{i[0] + 1} : {i[1]}")
levels = int(input("Choose Difficulty level : ")) - 1
level_points = {1: 10, 0: 30, 2: 5}
while True:
    player.choose_action()
    try:
        choice_action = int(input("Choose Action : ")) - 1
        if choice_action == 0:
            Attack_damage = player.generate_damage() + level_points[levels]
            enemy.take_damage(Attack_damage)
            print(f"{bcolors.BOLD}You attack for {Attack_damage} points of damage")
            enemy_damage = enemy.generate_damage() - level_points[levels] + 10
            player.take_damage(enemy_damage)
            print(f"Enemy attack for {enemy_damage} points of damage\n")
        elif choice_action == 1:
            player.choose_magic()
            choice_magic = int(input("Choose Action : ")) - 1
            spell = player.magic[choice_magic]
            magic_damage = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot Enough Magic Points" + bcolors.ENDC)
                continue
            player.reduce_magic_point(spell.cost)
            if spell.mode == "White":
                player.heal(magic_damage)
                print(f"player is healed with {magic_damage} Hp")
            else:
                enemy.take_damage(magic_damage)
                print(f"{bcolors.OKBLUE} \n{spell.name} deals {magic_damage} Points of damage {bcolors.ENDC}\n")
                enemy_damage = enemy.generate_damage() - level_points[levels]
                player.take_damage(enemy_damage)
                print(f"Enemy attack for {enemy_damage} points of damage")

    except (IndexError, ValueError):
        print("Wrong Input!!!  \n")
        continue
    if enemy.get_hp() == 0:
        print(bcolors.OKGREEN + bcolors.BOLD + "\nYou Win".upper() + bcolors.ENDC)
        break
    elif player.get_hp() == 0:
        print(bcolors.FAIL + bcolors.BOLD + " \nGame Over!\n you have been defeated".upper() + bcolors.ENDC)
        break
    print("\n-------------------------------------------------------------------------------------")
    print(f"{bcolors.BOLD}Enemy Hp : {bcolors.OKGREEN}{enemy.get_hp()}/{enemy.get_maximum_hp()}")
    print(
        f"{bcolors.ENDC}\n{player.name} Hp : {bcolors.FAIL + bcolors.BOLD}{player.get_hp()}/{player.get_maximum_hp()}")
    print(
        f"{bcolors.ENDC}\n{player.name} Mp : {bcolors.OKBLUE + bcolors.BOLD}{player.get_mp()}/{player.get_maximum_mp()}{bcolors.ENDC}")
