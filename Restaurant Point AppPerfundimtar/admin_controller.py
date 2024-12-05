from model import Restaurant,Menu,Menu_Item

class RestaurantManagerController:

    def add_restaurant(self, restaurant_list, restaurant_data):
        if len(restaurant_data) < 2:
            print("Error: Insufficient data provided to create a restaurant.")
            return

        new_restaurant = Restaurant(restaurant_data[0], restaurant_data[1], [])
        restaurant_list.append(new_restaurant)

    def delete_restaurant(self, restaurant_list, restaurant_name):
        for restaurant in restaurant_list:
            if restaurant.name == restaurant_name:
                restaurant_list.remove(restaurant)
                break

    def update_restaurant(self, restaurant_list, old_restaurant_name, new_restaurant_data):
        for restaurant in restaurant_list:
            if restaurant.name == old_restaurant_name:
                restaurant.name = new_restaurant_data[0]
                restaurant.address = new_restaurant_data[1]
                break




class MenuItemManagerController:
    
    def add_menu_item(self, menu, menu_item_data):
        # Get the menu item list of the specified menu
        menu_items = menu.menu_item_list
        # Create a new MenuItem object with the provided data
        new_menu_item = Menu_Item(
            menu_item_data[0],  # ID
            menu_item_data[1],  # Name
            menu_item_data[2],  # Price
            menu_item_data[3],  # Description
            menu_item_data[4]   # Priority
        )
        # Add the new menu item to the menu's menu item list
        menu_items.append(new_menu_item)

    def delete_menu_item(self, menu, menu_item_name):
        menu_item_list = menu.menu_item_list
        # Iterate over the menu item list to find the menu item to be deleted
        for menu_item in menu_item_list:
            if menu_item.name == menu_item_name:
                # Remove the menu item from the menu item list
                menu_item_list.remove(menu_item)
                menu.menu_item_list = menu_item_list
                break  # Exit the loop once the menu item is deleted

    def update_menu_item(self, old_menu_item_name, new_menu_item_data,menu):
        menu_item_list = menu.menu_item_list
        # Iterate over the menu list to find the menu item to be updated
        for menu_item in menu_item_list:
            
            if menu_item.name == old_menu_item_name:
                # Update the menu item's data
                menu_item.id = new_menu_item_data[0]
                menu_item.name = new_menu_item_data[1]
                menu_item.price = new_menu_item_data[2]
                menu_item.description =new_menu_item_data[3]
                menu_item.priority =new_menu_item_data[4]
                break  # Exit the loop once the menu item is updated




class MenuManagerController:

    def add_Menu(self, restaurant, menu_data):
        menus = restaurant.menu_list
        new_menu = Menu(menu_data[0], menu_data[1], [])
        menus.append(new_menu)
        restaurant.menu_list = menus

    def delete_Menu(self, restaurant, menu_data):
        menu_list = restaurant.menu_list

        for menu in menu_list:
            if menu.menu_id == menu_data[0]:  # Updated to match on menu_id
                menu_list.remove(menu)
                break

    def update_Menu(self, old_menu_name, new_menu_data, restaurant):
        menu_list = restaurant.menu_list

        for menu in menu_list:
            if menu.menu_name == old_menu_name[0]:
                menu.menu_id = new_menu_data[0]
                menu.name = new_menu_data[1]
                break

 

class TableManagerController:

    def add_Table(self, restaurant, table_data):
        tables= restaurant.seats_list
        new_table = Menu(table_data[0], table_data[1],[])
        tables.append(new_table)
        restaurant.seats_list =tables

    def delete_Table(self, restaurant, table_data):

        table_list=restaurant.seats_list

        for table in table_list:
            if table.name == table_data[0]:
                
               table_list.remove(table)


    def update_row(self, old_table_data, new_table_data, restaurant):

        table_list = restaurant.table_list

        for table in table_list:
            if table.name == old_table_data[0]:
                table.id =new_table_data[0]
                table.name = new_table_data[1]
                break