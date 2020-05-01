from random import randrange


class colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


class Person:
    def __init__(self, name, hp, mp, attack, magic, ):
        self.maximum_hp = hp
        self.maximum_mp = mp
        self.hp = hp
        self.name = name
        self.mp = mp
        self.attack_low = attack - 5
        self.attack_high = attack + 20
        self.magic = magic
        self.actions = ['Attack', 'Magic']

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

    def choose_action(self, act=1):
        print(colors.HEADER + colors.GREEN + colors.BOLD + "Actions" + colors.END)

        for item in self.actions:
            print("{0} : {1}".format(act, item))
            act += 1

    def choose_magic(self, i=1):
        print(colors.BLUE + colors.BOLD + "Magic" + colors.END)

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

player = Person(input("Enter Player name : ").capitalize(), 1000, 65, 60,
                [fire, blizzard, thunder, meteor, quake, cure, coral])
enemy = Person("Enemy", 2000, 0, 100, [])
print(colors.FAIL + colors.BOLD + "AN ENEMY ATTACK GAME" + colors.END, "\n====================")
print(
    f"\nWelcome! {colors.GREEN + colors.BOLD + player.name + colors.END}  \n"
    f"Maximum Hp of {player.name} : {player.maximum_hp}\nMaximum Hp of Enemy {enemy.maximum_hp}")
levels = ["Easy", "Medium", "Hard"]
print("---------------------\nDifficulty Levels\n")
for i in enumerate(levels):
    print(f"{i[0] + 1} : {i[1]}")
levels = int(input("Choose Difficulty level : ")) - 1
level_points = {1: 30, 0: 50, 2: 10}
while True:
    player.choose_action()
    try:
        choice_action = int(input("Choose Action : ")) - 1
        if choice_action == 0:
            Attack_damage = player.generate_damage() + level_points[levels]
            enemy.take_damage(Attack_damage)
            print(f"{colors.BOLD}You attack for {Attack_damage} points of damage")
            enemy_damage = enemy.generate_damage() - level_points[levels]
            player.take_damage(enemy_damage)
            print(f"Enemy attack for {enemy_damage} points of damage\n")
        elif choice_action == 1:
            player.choose_magic()
            choice_magic = int(input("Choose Action : ")) - 1
            spell = player.magic[choice_magic]
            magic_damage = spell.generate_damage()

            current_mp = player.get_mp()
            if spell.cost > current_mp:
                print(colors.FAIL + "\nNot Enough Magic Points" + colors.END)
                continue
            player.reduce_magic_point(spell.cost)
            if spell.mode == "White":
                player.heal(magic_damage)
                print(f"player is healed with {magic_damage} Hp")
            else:
                enemy.take_damage(magic_damage)
                print(f"{colors.BLUE} \n{spell.name} deals {magic_damage} Points of damage {colors.END}\n")
                enemy_damage = enemy.generate_damage() - level_points[levels]
                player.take_damage(enemy_damage)
                print(f"Enemy attack for {enemy_damage} points of damage")

    except (IndexError, ValueError):
        print("Wrong Input!!!  \n")
        continue
    if enemy.get_hp() == 0:
        print(colors.GREEN + colors.BOLD + "\nYou Win".upper() + colors.END)
        break
    elif player.get_hp() == 0:
        print(colors.FAIL + colors.BOLD + " \nGame Over!\n you have been defeated".upper() + colors.END)
        break
    print("\n---------------------------------------------------------------------------------------------")
    print(f"{colors.BOLD}Enemy Hp : {colors.GREEN}{enemy.get_hp()}/{enemy.get_maximum_hp()}")
    print(
        f"{colors.END}\n{player.name} Hp : {colors.FAIL + colors.BOLD}{player.get_hp()}/{player.get_maximum_hp()}")
    print(
        f"{colors.END}\n{player.name} Mp "
        f": {colors.BLUE + colors.BOLD}{player.get_mp()}/{player.get_maximum_mp()}{colors.END}")
