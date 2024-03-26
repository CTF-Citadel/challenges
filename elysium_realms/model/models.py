from sqlalchemy import Column, ForeignKey, Integer, String
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
    credits = Column(Integer())

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

    itemname = Column(String(length=255), primary_key=True)
    quantity = Column(Integer())
    affiliation = Column(String(length=255), ForeignKey("users.username"))

class Tool(Base):

    __tablename__ = "tools"

    toolname = Column(String(length=255), primary_key=True)
    damage = Column(Integer())
    rank = Column(Integer()) # rank using numbers for minimal data
    affiliation = Column(String(length=255), ForeignKey("users.username"))

class Armor(Base):

    __tablename__ = "armor"

    armorname = Column(String(length=255), primary_key=True)
    protection = Column(Integer()) 
    affiliation = Column(String(length=255), ForeignKey("users.username"))

