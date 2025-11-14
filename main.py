import random
import time

"""Basik class"""

class Character:
    def __init__(self, name, hp, attack):
        self._name = name
        self._hp = hp
        self._max_hp = hp
        self._attack = attack

    def is_alive(self):
        return self._hp > 0

    def take_damage(self, amount):
        self._hp -= amount
        if self._hp < 0:
            self._hp = 0

    def heal(self, amount):
        self._hp += amount
        if self._hp > self._max_hp:
            self._hp = self._max_hp

    def get_info(self):
        return f"{self._name}: {self._hp}/{self._max_hp} HP"


"""Heroies"""

class Hero(Character):
    def attack_enemy(self, enemy):
        pass


class Warrior(Hero):
    def attack_enemy(self, enemy):
        damage = self._attack
        print(f"{self._name} рубит мечом и наносит {damage} урона!")
        enemy.take_damage(damage)


class Mage(Hero):
    def attack_enemy(self, enemy):
        bonus = random.choice([0, 5, 10])
        damage = self._attack + bonus
        print(f"{self._name} колдует и наносит {damage} урона!")
        enemy.take_damage(damage)


class Archer(Hero):
    def attack_enemy(self, enemy):
        if random.random() < 0.2:
            print(f"{self._name} промахнулся!")
        else:
            damage = self._attack
            print(f"{self._name} стреляет и наносит {damage} урона!")
            enemy.take_damage(damage)


"""New character Berserker"""

class Berserker(Hero):
    def __init__(self, name, hp, attack):
        super().__init__(name, hp, attack)
        self._rage = 0

    def take_damage(self, amount):
        super().take_damage(amount)
        if self.is_alive():
            self._rage += 5
            print(f"{self._name} впадает в ярость! Ярость увеличивается до {self._rage}")

    def attack_enemy(self, enemy):
        bonus = self._rage // 2
        damage = self._attack + bonus

        if random.random() < 0.1:
            damage *= 2
            print(f"Критический удар! {self._name} наносит {damage} урон !")
        else:
            print(f"Берсерк {self._name} атакует в ярости! Урон: {damage}")

        enemy.take_damage(damage)
        self._rage = max(0, self._rage - 3)


"""Class potion"""

class Potion:
    def __init__(self, name, heal_amount):
        self.name = name
        self.heal_amount = heal_amount

    def use(self, hero):
        if not hero.is_alive():
            return
        before = hero._hp
        hero.heal(self.heal_amount)
        healed = hero._hp - before
        print(f"{hero._name} использует {self.name} и восстанавливает {healed} HP.")


"""Boss"""

class Boss(Character):
    def attack_enemy(self, heroes):
        alive_heroes = [h for h in heroes if h.is_alive()]
        if not alive_heroes:
            return
        
        target = random.choice(alive_heroes)
        damage = self._attack
        print(f"Босс атакует {target._name} и наносит {damage} урона!")
        target.take_damage(damage)


"""Game progress"""

def battle():
    warrior = Warrior("Арагорн", 100, 20)
    mage = Mage("Гэндальф", 70, 15)
    archer = Archer("Леголас", 80, 18)
    berserker = Berserker("Конан", 120, 25)

    heroes = [warrior, mage, archer, berserker]

    healing_potion = Potion("Зелье лечения", 30)
    big_potion = Potion("Большое зелье", 60)

    hero_potions = {
        warrior: healing_potion,
        mage: healing_potion,
        archer: big_potion,
        berserker: big_potion
    }

    boss = Boss("Саурон", 400, 40)

    round_num = 1
    print("Добро пожаловать в битву героев и босса Саурона!")

    while boss.is_alive() and any(h.is_alive() for h in heroes):
        print(f"\n===== Раунд {round_num} =====")

        for hero in heroes:
            if hero.is_alive():
                hero.attack_enemy(boss)
                time.sleep(0.5)

        print(f"\n{boss.get_info()}")

        if not boss.is_alive():
            print("\nГерои победили! Мир спасён!")
            break 

        boss.attack_enemy(heroes)
        time.sleep(0.5)

        for hero in heroes:
            print(hero.get_info())
        
        round_num  +=1
        time.sleep(1)

    if not any(h.is_alive() for h in heroes):
        print("\n Босс победил! Герои пали в бою...")

if __name__ == "__main__":
    battle()