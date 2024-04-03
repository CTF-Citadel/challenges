from sqlalchemy import Column, ForeignKey, Integer, String, BigInteger, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ = "users"

    username = Column(String(length=255), primary_key=True)
    password_hash = Column(String(length=255))
    level = Column(Integer())
    affiliation = Column(String(length=255), ForeignKey("guilds.title"))
    spawnpoint = Column(String(length=255))
    current_place = Column(String(length=255))
    credits = Column(BigInteger())

    def __repr__(self):
        return f'User(username={self.username}, password_hash={self.password_hash}, level={self.level}, affiliation={self.affiliation}, spawnpoint={self.spawnpoint}, current_place={self.current_place}, credits={self.credits})'

class Guild(Base):

    __tablename__ = "guilds"

    title = Column(String(length=255), primary_key=True)
    level = Column(Integer())

    def __repr__(self):
        return f'Guild(title={self.title}, level={self.level})'

class Item(Base):

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    itemname = Column(String(length=255))
    description = Column(String(length=255))
    quantity = Column(Integer())
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Item(id={self.id}, itemname={self.itemname}, description={self.description}, quantity={self.quantity}, price={self.price}, affiliation={self.affiliation})'

class Tool(Base):

    __tablename__ = "tools"

    id = Column(Integer, primary_key=True, autoincrement=True)
    toolname = Column(String(length=255))
    description = Column(String(length=255))
    durability = Column(Float())
    efficiency = Column(Float())
    rank = Column(String(length=255)) 
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Tool(id={self.id}, toolname={self.toolname}, description={self.description}, durability={self.durability}, efficiency={self.efficiency}, rank={self.rank}, type={self.type}, price={self.price}, affiliation={self.affiliation})'

class Weapon(Base):

    __tablename__ = "weapons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    weaponname = Column(String(length=255))
    description = Column(String(length=255))
    damage = Column(Float())
    attack_speed = Column(Float())
    durability = Column(Float())
    rank = Column(String(length=255)) 
    type = Column(String(length=20))
    price = Column(BigInteger())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

    def __repr__(self):
        return f'Weapon(id={self.id}, weaponname={self.weaponname}, description={self.description}, damage={self.damage}, attack_speed={self.attack_speed}, durability={self.durability}, rank={self.rank}, type={self.type}, price={self.price}, affiliation={self.affiliation})'