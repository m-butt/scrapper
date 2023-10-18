
import mysql.connector as db
def setup_connection_with_db():
    db_host = "zdp-dev-private-subnet-mariadb.mariadb.database.azure.com"
    db_user = "mariadbadmin@zdp-dev-private-subnet-mariadb"
    db_pass = "DAeROzAza847UfTd"
    db_port = "3306"
    db_name = "cdw_products"

    connection = db.connect(user=db_user, password=db_pass, database=db_name, host=db_host, port=db_port)
    print(f"**Connection successfully established with \"{db_host}\"**")
    return connection


def save_products_info_to_db(db_connection, prod_dict):

    cursor = db_connection.cursor(buffered= True)
    query = f"INSERT INTO cdw_products.products_information (product_name, manufacturer_part_no, price) " \
            f"VALUES (%(product_name)s, %(manufacturer_part_no)s, %(price)s)"
    try:
        cursor.execute(query, prod_dict)
        db_connection.commit()
        print("data inserted successfully!")

    except:
        print(cursor.statement)
        print("could not execute query!")

    cursor.close()
    # db_connection.close()


# db_connection = setup_connection_with_db()
# prod_dict = {
#              'product_name': 'Apple MacBook Pro - 16" - M2 Pro - 32 GB RAM - 1 TB SSD Space Gray',
#              'manufacturer_part_no': 'Z174-2002180539',
#              'price': '$3,125.99'
#              }
# save_products_info_to_db(db_connection, prod_dict)
