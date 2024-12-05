from model import User, Restaurant, Menu, Menu_Item, Table, Seats
from enums import UserRole, Priority

class UserDataProvider:
    def __init__(self):
        self.__user_list = []
        self._create_user_list()

    def _create_user_list(self):
        user1 = User("1", "1", UserRole.ADMIN)
        user2 = User("2", "2", UserRole.WAITER)
        user3 = User("3", "3", UserRole.FINANCIAL_MANAGER)
        user4 = User("4", "4", UserRole.WAITER)
        self.__user_list.extend([user1, user2, user3, user4])

    @property
    def user_list(self):
        return self.__user_list

class DataProvider:
    def __init__(self):
        self.__restaurants = []
        self._create_restaurant_list()

    def _create_restaurant_list(self):
        # Create Menu for restaurant 1
        restaurant1_menu_list = self._create_restaurant1_menu()
        restaurant1_seats_list = self._create_restaurant1_seats_list()
        restaurant1 = Restaurant("Tirana_Restaurant", "Rruga Tr", restaurant1_menu_list, restaurant1_seats_list)

        # Create Menu for restaurant 2
        restaurant2_menu_list = self._create_restaurant2_menu()
        restaurant2_seats_list = self._create_restaurant2_seats_list()
        restaurant2 = Restaurant("Prishtina_Restaurant", "Rruga Pr", restaurant2_menu_list, restaurant2_seats_list)

        # Create Menu for restaurant 3
        restaurant3_menu_list = self._create_restaurant3_menu()
        restaurant3_seats_list = self._create_restaurant3_seats_list()
        restaurant3 = Restaurant("Kukes_Restaurant", "Rruga Kukes", restaurant3_menu_list, restaurant3_seats_list)

        # Add restaurants to the list
        self.__restaurants.extend([restaurant1, restaurant2, restaurant3])

    def _create_restaurant1_seats_list(self):
        table_list = [
            Table("101", "Table 1", self._seats_list_for_table1()),
            Table("102", "Table 2", self._seats_list_for_table2()),
            Table("103", "Table 3", self._seats_list_for_table3()),
        ]
        return table_list

    def _create_restaurant2_seats_list(self):
        table_list = [
            Table("201", "Table 1", self._seats_list_for_table1()),
            Table("202", "Table 2", self._seats_list_for_table2()),
            Table("203", "Table 3", self._seats_list_for_table3()),
        ]
        return table_list

    def _create_restaurant3_seats_list(self):
        table_list = [
            Table("301", "Table 1", self._seats_list_for_table1()),
            Table("302", "Table 2", self._seats_list_for_table2()),
            Table("303", "Table 3", self._seats_list_for_table3()),
        ]
        return table_list

    def _seats_list_for_table1(self):
        seats_list = [
            Seats("101", "5"),
            Seats("102", "6"),
            Seats("103", "8"),
        ]
        return seats_list

    def _seats_list_for_table2(self):
        seats_list = [
            Seats("201", "5"),
            Seats("202", "6"),
            Seats("203", "8"),
        ]
        return seats_list

    def _seats_list_for_table3(self):
        seats_list = [
            Seats("301", "5"),
            Seats("302", "6"),
            Seats("303", "8"),
        ]
        return seats_list

    def _create_restaurant1_menu(self):
        menu_list = [
            Menu("Tirane menu_1", 1, self._menu_items_for_menu1()),
            Menu("Tirane menu_2", 2, self._menu_items_for_menu2()),
            Menu("Tirane menu_3", 3, self._menu_items_for_menu3()),
        ]
        return menu_list

    def _create_restaurant2_menu(self):
        menu_list = [
            Menu("Prishtina menu_1", 1, self._menu_items_for_menu1()),
            Menu("Prishtina menu_2", 2, self._menu_items_for_menu2()),
            Menu("Prishtina menu_3", 3, self._menu_items_for_menu3()),
        ]
        return menu_list

    def _create_restaurant3_menu(self):
        menu_list = [
            Menu("Kukes menu_1", 1, self._menu_items_for_menu1()),
            Menu("Kukes menu_2", 2, self._menu_items_for_menu2()),
            Menu("Kukes menu_3", 3, self._menu_items_for_menu3()),
        ]
        return menu_list

    def _menu_items_for_menu1(self):
        menu_items = [
            Menu_Item(100, "Supe perime", 2.5, "Description1", Priority.MEAL),
            Menu_Item(101, "Brinje Qingji", 6.0, "Description1", Priority.MEAL),
            Menu_Item(102, "Sallate Cezar", 4.5, "Description1", Priority.MEAL),
            Menu_Item(103, "Pica", 5.5, "Description1", Priority.MEAL),
        ]
        return menu_items

    def _menu_items_for_menu2(self):
        menu_items = [
            Menu_Item(200, "Supe pule", 3.0, "Description1", Priority.MEAL),
            Menu_Item(201, "Brinje Qingji", 6.5, "Description1", Priority.MEAL),
            Menu_Item(202, "Sallate Cezar", 3.5, "Description1", Priority.MEAL),
            Menu_Item(203, "Pica", 1.5, "Description1", Priority.MEAL),
        ]
        return menu_items

    def _menu_items_for_menu3(self):
        menu_items = [
            Menu_Item(300, "Supe peshe", 6.0, "Description1", Priority.MEAL),
            Menu_Item(301, "Brinje Qingji", 6.5, "Description1", Priority.MEAL),
            Menu_Item(302, "Sallate ruse", 3.5, "Description1", Priority.MEAL),
            Menu_Item(303, "Pica", 1.5, "Description1", Priority.MEAL),
        ]
        return menu_items

    @property
    def restaurant_list(self):
        return self.__restaurants
