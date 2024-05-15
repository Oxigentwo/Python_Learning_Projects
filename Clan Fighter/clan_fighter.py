import random

from names import exotic_names as names


def get_integer_input(prompt):
    while True:
        try:
            user_input = int(input(prompt))
            return user_input
        except ValueError:
            print("Invalid input. Please enter an integer.")


class ClanMember:
    def __init__(self, clan, member_id):
        self.member_id = member_id
        self.name = random.choice(names)
        self.age = random.randint(18, 100)
        self.clan = clan
        self.strength = random.randint(1, 5)
        self.constitution = random.randint(1, 5)
        self.dexterity = random.randint(1, 5)
        self.wisdom = random.randint(1, 5)

    def calculate_health(self):
        return 10 + self.constitution - (round(self.age, -1) / 10)


class Fighter(ClanMember):
    def __init__(self, clan, member_id):
        super().__init__(clan, member_id)
        self.strength = self.strength + 2
        self.constitution = self.constitution + 2
        self.health = self.calculate_health()

    def deal_dmg(self):
        return float(self.strength)

    def print_data(self):
        return (f"Fighter: {self.name} {self.clan}, Age: {self.age}, Strength: {self.strength}, "
                f"Constitution: {self.constitution}, Dexterity: {self.dexterity}, Wisdom: {self.wisdom}, "
                f"Health: {self.health}")


class Ranger(ClanMember):
    def __init__(self, clan, member_id):
        super().__init__(clan, member_id)
        self.dexterity = self.dexterity + 2
        self.constitution = self.constitution + 1
        self.health = self.calculate_health()

    def deal_dmg(self):
        return round(self.dexterity * 1.2, 1)

    def print_data(self):
        return (f"Ranger: {self.name} {self.clan}, Age: {self.age}, Strength: {self.strength}, "
                f"Constitution: {self.constitution}, Dexterity: {self.dexterity}, Wisdom: {self.wisdom}, "
                f"Health: {self.health}")


class Mage(ClanMember):
    def __init__(self, clan, member_id):
        super().__init__(clan, member_id)
        self.wisdom = self.wisdom + 2
        self.health = self.calculate_health()

    def deal_dmg(self):
        return round(self.wisdom * 2, 1)

    def print_data(self):
        return (f"Mage: {self.name} {self.clan}, Age: {self.age}, Strength: {self.strength}, "
                f"Constitution: {self.constitution}, Dexterity: {self.dexterity}, Wisdom: {self.wisdom}, "
                f"Health: {self.health}")


clans = []
clan_names = []


def clan_generator():
    num_clans = get_integer_input("Enter the number of clans: ")
    for _ in range(num_clans):
        while True:
            clan_name = input("Enter the name of the clan: ")
            if clan_name not in clan_names:
                break
            overwrite = input(f"Clan '{clan_name}' already exists. Do you want to overwrite it? (YES/NO): ").upper()
            if overwrite == 'NO':
                continue
            elif overwrite == 'YES':
                break
            else:
                print("Invalid input. Please enter 'YES' or 'NO'.")
        clans.append({})
        clan_names.append(clan_name)
        population = get_integer_input(f"Number of people in clan {clan_name}: ")
        for x in range(population):
            class_roll = random.randint(1, 3)
            if class_roll == 1:
                clans[-1][x] = Fighter(clan_name, x)
            elif class_roll == 2:
                clans[-1][x] = Ranger(clan_name, x)
            else:
                clans[-1][x] = Mage(clan_name, x)


def clan_fight():
    while len(clans) > 1:
        # Choose the first attacker and defender
        choose_clan = random.choice(clans)
        attacker = random.choice(list(choose_clan.values()))
        choose_clan2 = random.choice(clans)
        while choose_clan2 == choose_clan:
            choose_clan2 = random.choice(clans)
        defender = random.choice(list(choose_clan2.values()))

        while True:
            damage = attacker.deal_dmg()
            defender.health -= damage
            print(
                f'{attacker.name} {attacker.clan} ATTACKS {defender.name} {defender.clan}, dealing {damage} DAMAGE and leaving them with {defender.health:.1f} HEALTH.')

            if defender.health <= 0:
                print(f'{defender.name} {defender.clan} is SLAIN in combat.\n')
                loser_id = defender.member_id
                if loser_id in choose_clan2:
                    del choose_clan2[loser_id]
                else:
                    pass

                # Check if the defender's clan is empty
                if not choose_clan2:
                    # Remove the entire clan from the list of clans
                    clans.remove(choose_clan2)
                break  # Exit the combat loop if the defender is defeated
            else:
                # Swap attacker and defender for the next round of combat
                attacker, defender = defender, attacker
                choose_clan, choose_clan2 = choose_clan2, choose_clan

    print(f'\nClan {clan_names[-1]} stands VICTORIOUS. Surviving members:')
    for clan in clans:
        for member in clan.values():
            print(member.print_data())  # Print an empty line between clans


def main():
    clan_generator()
    for i in range(len(clans)):
        print(f"\nClan {clan_names[i]} consists of:\n")
        for member in clans[i].values():
            print(member.print_data())  # Print an empty line between clans
    print('\n')
    clan_fight()
    return


main()
