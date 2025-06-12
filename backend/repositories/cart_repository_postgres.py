from backend.interfaces.cart_repository_interface import ICartRepository




class CartRepositoryPostgres(ICartRepository):

    def show_my_cart(self,cursor,user_id):

        cursor.execute("""
                        select pro."name",pro.price,pro.description,ci.quantity  from products pro

                        join cart_items ci ON ci.product_id = pro.id
                        join cart c ON c.id = ci.cart_id
                        join users u ON u.id = c.user_id
                        Where u.id = %s                    
                        """,(user_id,))
        cart = cursor.fetchall()
        return cart


    def get_cart_id(self,cursor,user_id):

        id =cursor.execute("SELECT id FROM cart WHERE user_id = %s ",(user_id,))
        cursor.fetchone()
        return id
    def new_cart(self,cursor,user_id):

        cursor.execute("INSERT INTO cart (user_id) VALUES (%s) RETURNING id",(user_id,))
        cart_id = cursor.fetchone()
        return cart_id       

    def add_product(self,cursor, product,cart_id):

        cursor.execute("""INSERT INTO cart_items  (cart_id,product_id,quantity) VALUES (%s,%s,%s)
                        """,(cart_id,product.product_id,product.quantity))
        