import models
import os
import difflib

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"


def search(term):
    '''
    By using difflib.SequenceMatcher a result is given, 
    if the comparison between the search term and name/description is above a certain value.
    '''

    for row in models.Product.select():
        if difflib.SequenceMatcher(None, row.name, term).ratio() >= 0.5 or difflib.SequenceMatcher(None, row.description, term).ratio() >= 0.4:
            print(row.name)


def list_user_products(user_id):
    product_list = []
    for row in models.Product.select().where(models.Product.user == (user_id)):
        product_list.append(row.name)
    print(product_list)


def list_products_per_tag(tag_id):
    tag_list = []
    for row in models.Product.select().join(models.ProductTag).join(models.Tag).where(models.Tag.name == (tag_id)):
        tag_list.append(row.name)
    print(tag_list)


def add_product_to_catalog(user_id, product):
    products = models.Product.create(
        name=product[0],
        description=product[1],
        price=product[2],
        amount=product[3],
        user=user_id,
        )
    products.tag.add(product[4])


def update_stock(product_id, new_quantity):
    row = models.Product.get(models.Product.id == product_id)
    print("old amount: {}".format(row.amount))
    row.amount = new_quantity
    print("new amount: {}".format(row.amount))
    row.save()


def purchase_product(product_id, buyer_id, quantity):
    models.Buyer.create(
        product=product_id,
        buyer=buyer_id,
        amount=quantity
    )


def remove_product(product_id):
    product = models.Product.get(models.Product.id == product_id)
    product.delete_instance()


def populate_test_database():
    """
    Delete the database.
    """
    cwd = os.getcwd()
    database_path = os.path.join(cwd, "betsy-webshop.db")
    if os.path.exists(database_path):
        os.remove(database_path)

    """
    Creates the database and fills it with data.
    """
    models.db.connect()
    models.db.create_tables(
        [
           models.User,
           models.Product,
           models.Tag,
           models.Buyer,
           models.ProductTag,
        ]
    )

    product_data = [
        ('koffiekopje', 'blauwe koffiekopjes van de Action', 0.50, 4, 1, [1]),
        ('campingstoel', 'grijze campingstoelen', 10, 2, 2, [2]),
        ('borden', 'blauwe borden van de Action', 0.75, 8, 1, [1]),
        ('tafel', 'bamboe campingtafel', 20, 1, 2, [2]),
        ('campingglazen', 'plastic campingglazen van een festival', 0.10, 10, 2, [1, 2])
    ]

    tag_data = [
        ('servies'),
        ('camping'),
    ]

    user_data = [
        ('Alfred Alfredson', 'Alfredslane 123', '1234 AB', 'Fredsville', 'IBAN123456789'),
        ('Bert Bertson', 'Bertslane 231', '2345 CD', 'Bertsville', 'ASNB123456789'),
        ('Candice Candicedottir', 'Candicelane 312', '3456 EF', 'Candiceville', 'INGB123456789')
    ]

    buyer_data = [
        (1, 1, 2),
    ]

    for user in user_data:
        models.User.create(
            name=user[0],
            address=user[1],
            zip_code=user[2],
            city=user[3],
            billing_info=user[4]
        )

    for product in product_data:
        products = models.Product.create(
            name=product[0],
            description=product[1],
            price=product[2],
            amount=product[3],
            user_id=product[4]
        )
        products.tag.add(product[5])

    for tag in tag_data:
        models.Tag.create(
            name=tag,
        )

    for buyer in buyer_data:
        models.Buyer.create(
            buyer_id=buyer[0],
            product_id=buyer[1],
            amount=buyer[2]
        )


if __name__ == "__main__":

    # search('Caming')
    # list_user_products(1)
    # list_products_per_tag('camping')
    # add_product_to_catalog(2, ('luifel', 'luifel voor vouwwagen', 50, 1, 2))
    # update_stock(3, 4)
    # purchase_product(5, 1, 5)
    # remove_product(2)
    populate_test_database()
