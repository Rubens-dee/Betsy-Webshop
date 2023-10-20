# Models go here
import peewee

db = peewee.SqliteDatabase("betsy-webshop.db")

class User(peewee.Model):
    name = peewee.CharField(unique=True)
    address = peewee.CharField()
    zip_code = peewee.CharField()
    city = peewee.CharField()
    billing_info = peewee.CharField()
    

    class Meta:
        database = db

class Tag(peewee.Model):
    name = peewee.CharField(unique=True)

    class Meta:
        database = db

class Product(peewee.Model):
    name = peewee.CharField(index=True)
    description = peewee.CharField()
    price = peewee.DecimalField(decimal_places=2,auto_round=True)
    amount = peewee.SmallIntegerField()
    user = peewee.ForeignKeyField(User)
    tag = peewee.ManyToManyField(Tag)
    

    class Meta:
        database = db
    

class Buyer(peewee.Model):
    buyer = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)
    amount = peewee.SmallIntegerField()

    class Meta:
        database = db      

ProductTag = Product.tag.get_through_model()


