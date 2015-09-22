import sqlite3


class WKDDb:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    def get_all(self, query="SELECT * FROM stock"):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def update_stock(self, values):
        # print values
        self.cursor.execute("UPDATE stock SET drug_name = ?, quantity = ?, "
                            "price = ?, total = ?, expiring_date = ?, category = ? WHERE rowid = ?", values)
        self.conn.commit()

    def delete_all_stock(self):
        self.cursor.execute('DELETE FROM stock')
        self.conn.commit()

    def delete_drug(self, drug_id):
        item_id = (drug_id,)
        self.cursor.execute("DELETE FROM stock WHERE rowid = ?", item_id)
        self.conn.commit()

    def insert_drug(self, new_drug):
        self.cursor.execute('INSERT INTO stock VALUES (?,?,?,?,?,?)', new_drug)
        self.conn.commit()

    def query_drug(self, drug):
        # print (drug)
        self.cursor.execute("SELECT drug_name, price FROM stock WHERE drug_name like '%"+drug+"%'")
        return self.cursor.fetchall()

    def query_drug_names_for_autocomplete(self):
        self.cursor.execute("SELECT drug_name FROM stock")
        return self.cursor.fetchall()

    def query_drugs_for_checkout(self, drug_names):
        self.cursor.execute("SELECT quantity FROM stock WHERE drug_name = ?", drug_names)
        return self.cursor.fetchall()

    def update_quantity_after_checkout(self, value):
        # print values
        self.cursor.execute("UPDATE stock SET quantity = ? WHERE drug_name = ?", value)
        self.conn.commit()

    def query_for_expiring_drugs(self):
        self.cursor.execute("SELECT drug_name, expiring_date FROM stock WHERE expiring_date <= date('now', '+90 days')")
        return self.cursor.fetchall()

session = WKDDb(sqlite3.connect('db/wkd_healthcare.sqlite3'))
