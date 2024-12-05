from dataprovider import DataProvider
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from kivy.uix.button import Button
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from model import Restaurant
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from admin_controller import RestaurantManagerController,MenuItemManagerController,MenuManagerController,TableManagerController
from model import Restaurant,Menu_Item,Menu,Table,Seats
from enums import Priority


class RestaurantManagerContentPanel:
    selected_row = -1
    restaurant_list = DataProvider().restaurant_list
    restaurant_manager_controller = RestaurantManagerController()

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_restaurant_input_data_panel())
        split_layout_panel.add_widget(self._create_restaurant_management_panel())
        return split_layout_panel

    def _create_restaurant_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        self.name_input = MDTextField(multiline=True, font_size='18sp', hint_text='Name')
        self.address_input = MDTextField(multiline=True, font_size='18sp', hint_text='Address')
        input_data_component_panel.add_widget(self.name_input)
        input_data_component_panel.add_widget(self.address_input)
        input_data_component_panel.add_widget(self._create_buttons_component_panel())

        return input_data_component_panel

    def _create_restaurant_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing=10)

        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_release=self._add_restaurant)
        update_button = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        update_button.bind(on_release=self._update_restaurant)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        delete_button.bind(on_release=self._delete_restaurant)

        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_button)
        button_component_panel.add_widget(delete_button)

        return button_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols=1, spacing=0)
        self.restaurant_table = self._create_table()
        self.restaurant_table.bind(on_check_press=self._checked)
        self.restaurant_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.restaurant_table)
        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
        button.bind(on_release=self.show_restaurant_list)
        return button

    def _create_table(self):
        table_row_data = []
        for restaurant in self.restaurant_list:
            table_row_data.append((restaurant.name, restaurant.address))

        self.restaurant_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            use_pagination=True,
            check=True,
            rows_num=10,
            column_data=[
                ('Name', dp(40)),
                ('Address', dp(40))
            ],
            row_data=table_row_data
        )
        return self.restaurant_table

    def show_restaurant_list(self, button):
        menu_items = []
        for restaurant in self.restaurant_list:
            menu_items.append({
                "viewclass": "OneLineListItem",
                "text": restaurant.name,
                "on_release": lambda r=restaurant: self.update_selected_restaurant(r),
            })

        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )
        self.dropdown.open()

    def update_selected_restaurant(self, restaurant):
        self.name_input.text = restaurant.name
        self.address_input.text = restaurant.address
        self.dropdown.dismiss()

    def _checked(self, instance_table, current_row):
        if len(current_row) < 2:
            print("Error: Insufficient data in current_row.")
            return

        selected_restaurant = Restaurant(current_row[0], current_row[1], [])
        self.name_input.text = str(selected_restaurant.name)
        self.address_input.text = str(selected_restaurant.address)

    def _update_data_table(self, restaurant_list):
        table_row_data = []
        for restaurant in restaurant_list:
            table_row_data.append((restaurant.name, restaurant.address))

        self.restaurant_table.row_data = table_row_data

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))

    def _add_restaurant(self, instance):
        name = self.name_input.text.strip()
        address = self.address_input.text.strip()

        if name and address:
            restaurant_data = [name, address]
            self.restaurant_manager_controller.add_restaurant(self.restaurant_list, restaurant_data)
            self.restaurant_table.row_data.append((name, address))
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid data", "Provide mandatory data to add a new restaurant")

    def _update_restaurant(self, instance):
        if self.selected_row != -1:
            name = self.name_input.text.strip()
            address = self.address_input.text.strip()

            if name and address:
                restaurant_data = [name, address]
                old_restaurant_name = self.restaurant_table.row_data[self.selected_row][0]
                self.restaurant_manager_controller.update_restaurant(self.restaurant_list, old_restaurant_name, restaurant_data)
                self.restaurant_table.row_data[self.selected_row] = (name, address)
                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to update the restaurant")
        else:
            self._show_error_popup("Invalid data", "Select any row to update")

    def _delete_restaurant(self, instance):
        if self.selected_row != -1:
            restaurant_to_remove = self.restaurant_table.row_data[self.selected_row]
            self.restaurant_manager_controller.delete_restaurant(self.restaurant_list, restaurant_to_remove[0])
            del self.restaurant_table.row_data[self.selected_row]
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid data", "Select any row to delete")

    def _clear_input_text_fields(self):
        self.name_input.text = ""
        self.address_input.text = ""
        self.selected_row = -1

    def _show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 200),
        )
        popup.open()

    
class MenuItemManagerContentPanel:
    def __init__(self):
        self.menu_item_manager_controller = MenuItemManagerController()
        self.restaurant_list = DataProvider().restaurant_list
        self.restaurant = self.restaurant_list[0]
        self.menu = self.restaurant.menu_list[0]  # Initialize self.menu here
        self.selected_menu = None
        self.selected_row = -1

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel

    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        self.id_input = MDTextField(multiline=True, font_size='18sp', hint_text='Id')
        input_data_component_panel.add_widget(self.id_input)
        self.name_input = MDTextField(multiline=False, font_size='18sp', hint_text='Name')
        input_data_component_panel.add_widget(self.name_input)
        self.price_input = MDTextField(multiline=False, font_size='18sp', hint_text='Price')
        input_data_component_panel.add_widget(self.price_input)
        self.description_input = MDTextField(multiline=False, font_size='18sp', hint_text='Description')
        input_data_component_panel.add_widget(self.description_input)

        input_data_component_panel.add_widget(self._create_priority_input_panel())
        input_data_component_panel.add_widget(self._create_buttons_component_panel())

        return input_data_component_panel

    def _create_priority_input_panel(self):
        priority_input_panel = GridLayout(cols=2, spacing=20)
        priority_options = ["Drink", "Meal"]
        for priority in priority_options:
            checkbox = CheckBox(group='priority', active=False, color=(0, 0, 0, 1))
            checkbox_label = Label(text=priority, color=(0, 0, 0, 1))
            priority_input_panel.add_widget(checkbox)
            priority_input_panel.add_widget(checkbox_label)
        self.priority_input_panel = priority_input_panel
        return priority_input_panel

    def _get_selected_priority(self):
        for index, child in enumerate(self.priority_input_panel.children):
            if isinstance(child, CheckBox) and child.active:
                label_index = index - 1
                if label_index < len(self.priority_input_panel.children):
                    label = self.priority_input_panel.children[label_index]
                    priority_text = label.text.lower()
                    return Priority[priority_text.upper()]
        return None

    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.size_hint_x = None
        content_panel.width = 800
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.add_widget(self._create_menu_selector())
        content_panel.add_widget(self._create_menu_table(self.menu))
        return content_panel

    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        buttons = [
            ("Add", self._add_menu_item),
            ("Update", self._update_menu_item),
            ("Delete", self._delete_menu_item)
        ]
        for text, callback in buttons:
            button = Button(text=text, size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
            button.bind(on_release=callback)
            button_component_panel.add_widget(button)
        return button_component_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
        button.bind(on_release=self.show_restaurant_list)
        self.restaurant_selector = button
        return button

    def show_restaurant_list(self, button):
        menu_items = [
            {"viewclass": "OneLineListItem", "text": restaurant.name,
             "on_release": lambda r=restaurant: self.update_selected_restaurant(r)}
            for restaurant in self.restaurant_list
        ]
        self.dropdown = MDDropdownMenu(caller=button, items=menu_items, width_mult=5, max_height=dp(150))
        self.dropdown.open()

    def update_selected_restaurant(self, restaurant):
        if self.restaurant_selector:
            self.restaurant_selector.text = restaurant.name
            self.update_menu_list(restaurant)
        else:
            print("Restaurant selector is not initialized properly.")
        self.dropdown.dismiss()

    def _create_menu_selector(self):
        button = Button(text='Select a menu', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
        button.bind(on_release=self.show_menu_list)
        self.menu_selector = button
        return button

    def show_menu_list(self, button):
        menu_items = [
            {'viewclass': "OneLineListItem", "text": menu.name, "on_release": lambda m=menu: self.update_data_table(m)}
            for menu in self.restaurant.menu_list
        ]
        self.dropdown = MDDropdownMenu(caller=button, items=menu_items, width_mult=5, max_height=dp(150))
        self.dropdown.open()

    def _create_menu_table(self, menu):
        table_row_data = [(menu_item.id, menu_item.name, menu_item.price, menu_item.description, menu_item.priority.value)
                          for menu_item in menu.menu_item_list]

        self.menu_item_table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ("Id", dp(40)),
                ("Name", dp(50)),
                ("Price", dp(40)),
                ("Description", dp(40)),
                ("Priority", dp(40))
            ],
            row_data=table_row_data
        )
        self.menu_item_table.bind(on_check_press=self._checked)
        self.menu_item_table.bind(on_row_press=self._on_row_press)
        return self.menu_item_table

    def _checked(self, instance_table, current_row):
        priority_value = current_row[4]  # Extract the priority value from the row
        priority_value = priority_value.split('.')[-1]  # Remove any prefix like "Priority."
        self.selected_menu_item = Menu_Item(
            current_row[0], current_row[1], current_row[2], current_row[3], Priority[priority_value.upper()]
        )
        self.id_input.text = str(self.selected_menu_item.id)
        self.name_input.text = str(self.selected_menu_item.name)
        self.price_input.text = str(self.selected_menu_item.price)
        self.description_input.text = str(self.selected_menu_item.description)

        if self.selected_menu_item.priority == Priority.MEAL:
            self.priority_input_panel.children[3].active = True
        elif self.selected_menu_item.priority == Priority.DRINK:
            self.priority_input_panel.children[1].active = True

    def _on_row_press(self, instance, row):
        self.selected_row = int(row.index / len(instance.column_data))

    def _clear_input_text_fields(self):
        self.id_input.text = ""
        self.name_input.text = ""
        self.price_input.text = ""
        self.description_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, menu_item_data):
        return all(menu_item_data)

    def _add_menu_item(self, instance):
        try:
            id = self.id_input.text
            name = self.name_input.text
            price = float(self.price_input.text)
            description = self.description_input.text
            priority = self._get_selected_priority()
            menu_item_data = [id, name, price, description, priority]

            if self._is_data_valid(menu_item_data):
                self.menu_item_manager_controller.add_menu_item(self.menu, menu_item_data)
                self.menu_item_table.row_data.append([id, name, price, description, priority])
                self._clear_input_text_fields()
            else:
                self._show_error_popup("Invalid data", "Provide mandatory data to add a new menu item")
        except ValueError:
            self._show_error_popup("Invalid data", "Price must be a number")

    def _update_menu_item(self, instance):
        if self.selected_row != -1:
            try:
                id = self.id_input.text
                name = self.name_input.text
                price = float(self.price_input.text)
                description = self.description_input.text
                priority = self._get_selected_priority()
                menu_item_data = [id, name, price, description, priority]

                if self._is_data_valid(menu_item_data):
                    # Remove the old menu item from the table
                    menu_item_to_remove = self.menu_item_table.row_data.pop(self.selected_row)

                    # Update the menu item using the controller
                    self.menu_item_manager_controller.update_menu_item(menu_item_to_remove[0], menu_item_data, self.menu)

                    # Add the updated menu item to the table
                    self.menu_item_table.row_data.append([id, name, price, description, priority])
                    self._clear_input_text_fields()
                else:
                    self._show_error_popup("Invalid data", "Provide mandatory data to update the menu item")
            except ValueError:
                self._show_error_popup("Invalid data", "Price must be a number")
        else:
            self._show_error_popup("Invalid data", "Select any row to update")

    def _delete_menu_item(self, instance):
        if self.selected_row != -1:
            menu_item_to_remove = self.menu_item_table.row_data[self.selected_row]

            del self.menu_item_table.row_data[self.selected_row]
            self.menu_item_manager_controller.delete_menu_item(self.menu, menu_item_to_remove[0])
            self._clear_input_text_fields()
        else:
            self._show_error_popup("Invalid", "Select any row to delete")

    def _show_error_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(None, None),
            size=(400, 300),
        )
        popup.open()

    def update_menu_list(self, restaurant):
        self.restaurant = restaurant
        self.menu = self.restaurant.menu_list[0]  # Update self.menu when restaurant changes
        self.selected_menu = None
        menu_items = [
            {'viewclass': "OneLineListItem", "text": menu.name, "on_release": lambda m=menu: self.update_data_table(m)}
            for menu in restaurant.menu_list
        ]
        self.menu_selector.items = menu_items
        self.menu_selector.text = 'Select a menu'
        self.dropdown.dismiss()

    def update_data_table(self, menu):
        self.menu = menu
        self.selected_menu = menu
        table_row_data = [
            (menu_item.id, menu_item.name, menu_item.price, menu_item.description, menu_item.priority.value)
            for menu_item in menu.menu_item_list
        ]
        self.menu_item_table.row_data = table_row_data
        self.dropdown.dismiss()


        
class MenuManagerContentPanel:
    selected_row = -1
    restaurant_list = DataProvider().restaurant_list
    menu_manager_controller = MenuManagerController()

    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_menu_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel

    def _create_menu_input_data_panel(self):
        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        self.menu_id_input = MDTextField(multiline=True, font_size='18sp', hint_text='Menu_id')
        self.name_input = MDTextField(multiline=True, font_size='18sp', hint_text='Name')

        input_data_component_panel.add_widget(self.menu_id_input)
        input_data_component_panel.add_widget(self.name_input)
        input_data_component_panel.add_widget(self._create_buttons_component_panel())

        return input_data_component_panel

    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())

        return content_panel

    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_release=self._add_menu)
        update_button = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        update_button.bind(on_release=self._update_menu)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        delete_button.bind(on_release=self._delete_menu)

        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_button)
        button_component_panel.add_widget(delete_button)

        return button_component_panel

    def _create_table_panel(self):
        table_panel = GridLayout(cols=1, spacing=0)
        self.menu_table = self.create_table()
        self.menu_table.bind(on_check_press=self._checked)
        self.menu_table.bind(on_row_press=self._on_row_press)
        table_panel.add_widget(self.menu_table)

        return table_panel

    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
        button.bind(on_release=self.show_restaurant_list)

        return button

    def create_table(self):
        table_row_data = []
        self.restaurant = self.restaurant_list[0]
        menus = self.restaurant.menu_list

        for menu in menus:
            table_row_data.append(
                (menu.menu_id, menu.name)
            )

        self.menu_table = MDDataTable(
            pos_hint={'center_x': 0.5, "center_y": 0.5},
            background_color_header="#7393B3",
            background_color_cell="#F0FFFF",
            background_color_selected_cell="#ADD8E6",
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ('Menu_id', dp(40)),
                ('Name', dp(40)),
            ],
            row_data=table_row_data
        )

        return self.menu_table

    def show_restaurant_list(self, button):
        menu_items = []
        restaurant_list = self.restaurant_list

        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem",
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r)})

        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )
        self.dropdown.open()

    def _checked(self, instance_table, current_row):
        self.selected_menu = Menu(
            current_row[0], current_row[1], []
        )
        self.menu_id_input.text = str(self.selected_menu.menu_id)
        self.name_input.text = str(self.selected_menu.name)

    def _update_data_table(self, restaurant):
        self.restaurant = restaurant

        # Get menu data for the selected restaurant
        table_row_data = []
        menus = restaurant.menu_list
        for menu in menus:
            table_row_data.append(
                (menu.menu_id, menu.name)
            )

        # Update the menu table with the new data
        self.menu_table.row_data = table_row_data

    def _add_menu(self, instance):
        menu_id = self.menu_id_input.text
        name = self.name_input.text

        menu_data = [menu_id, name]

        if self._is_data_valid(menu_data):
            self.menu_manager_controller.add_Menu(self.restaurant, menu_data)
            self.menu_table.row_data.append((menu_id, name))
            self.menu_table.row_data = self.menu_table.row_data  # Refresh the table view
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Provide mandatory data to add a new Menu"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    def _on_row_press(self, instance, row):
        # Set the row index to delete when the row is pressed
        self.selected_row = int(row.index / len(instance.column_data))

    def _update_menu(self, instance):
        if self.selected_row != -1:
            # Get the updated menu data from the input fields
            menu_id = self.menu_id_input.text
            name = self.name_input.text

            menu_data = [menu_id, name]

            if self._is_data_valid(menu_data):
                menu_to_remove = self.menu_table.row_data[self.selected_row]

                del self.menu_table.row_data[self.selected_row]
                self.menu_manager_controller.delete_Menu(
                    self.restaurant, menu_to_remove
                )
                self.menu_manager_controller.add_Menu(
                    self.restaurant, menu_data
                )
                self.menu_table.row_data.append((menu_id, name))
                self.menu_table.row_data = self.menu_table.row_data  # Refresh the table view
                self._clear_input_text_fields()
            else:
                popup = Popup(
                    title="Invalid data",
                    content=Label(text="Provide mandatory data to update the Menu"),
                    size_hint=(None, None),
                    size=(400, 200),
                )
                popup.open()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to update"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    def _delete_menu(self, instance):
        if self.selected_row != -1:
            menu_to_remove = self.menu_table.row_data[self.selected_row]
            del self.menu_table.row_data[self.selected_row]
            self.menu_manager_controller.delete_Menu(
                self.restaurant, menu_to_remove
            )
            self.menu_table.row_data = self.menu_table.row_data  # Refresh the table view
            self._clear_input_text_fields()
        else:
            popup = Popup(
                title="Invalid data",
                content=Label(text="Select any row to delete"),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()

    def _clear_input_text_fields(self):
        # Clear the input fields by setting their text to empty strings
        self.menu_id_input.text = ""
        self.name_input.text = ""
        self.selected_row = -1

    def _is_data_valid(self, menu_data):
        # Check if menu data is valid (all fields are filled)
        return (
            menu_data[0] != "" and
            menu_data[1] != ""
        )

class TableManagerContentPanel:

    selected_row = -1
    restaurant_list = DataProvider().restaurant_list
    table_manager_controller = TableManagerController()


    def create_content_panel(self):
        split_layout_panel = GridLayout(cols=2)
        split_layout_panel.add_widget(self._create_table_input_data_panel())
        split_layout_panel.add_widget(self._create_management_panel())
        return split_layout_panel

    def _create_table_input_data_panel(self):

        input_data_component_panel = GridLayout(cols=1, padding=30, spacing=20)
        input_data_component_panel.size_hint_x = None
        input_data_component_panel.width = 400

        self.table_id_input =MDTextField(multiline=True, font_size='18sp', hint_text='Table_id')
        self.seats_input = MDTextField(multiline=True, font_size='18sp', hint_text='Seats')

        input_data_component_panel.add_widget(self.table_id_input)
        input_data_component_panel.add_widget(self.seats_input)
     

        input_data_component_panel.add_widget(self._create_buttons_component_panel())
        return input_data_component_panel

    def _create_management_panel(self):
        content_panel = GridLayout(cols=1, spacing=10)
        content_panel.add_widget(self._create_restaurant_selector())
        content_panel.size_hint_x = None
        content_panel.width = 1200
        content_panel.add_widget(self._create_table_panel())
        return content_panel

    def _create_buttons_component_panel(self):
        button_component_panel = GridLayout(cols=3, padding=0, spacing=10)
        add_button = Button(text='Add', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        add_button.bind(on_release=self._add_table)
        update_button = Button(text='Update', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        update_button.bind(on_release=self._update_table)
        delete_button = Button(text='Delete', size_hint=(None, None), size=(100, 40), background_color=(0, 1, 1, 1))
        delete_button.bind(on_release=self._delete_table)

        button_component_panel.add_widget(add_button)
        button_component_panel.add_widget(update_button)
        button_component_panel.add_widget(delete_button)

        return button_component_panel
    
    def _create_table_panel(self):
        table_panel=GridLayout(cols=1,spacing=0)
        self.table_table = self.create_table()
        self.table_table.bind(on_check_press=self._checked)
        self.table_table.bind(on_row_press = self._on_row_press)
        table_panel.add_widget(self.table_table)
        return table_panel
    
    def _create_restaurant_selector(self):
        button = Button(text='Select a restaurant', size_hint=(1, 0.1), background_color=(0, 1, 1, 1))
        button.bind(on_release=self.show_restaurant_list)
        return button
    
    def create_table(self):

        table_row_data=[]
        self.restaurant =self.restaurant_list[0]
        tables =self.restaurant.seats_list

        for table in tables:
            table_row_data.append(
                (table.id,table.name)
            )
        self.table_table = MDDataTable(
            pos_hint={'center_x': 0.5, "center_y": 0.5},
            background_color_header="#7393B3",
            background_color_cell="F0FFFF",
            background_color_selected_cell="ADD8E6",  # Corrected attribute name
            check=True,
            use_pagination=True,
            rows_num=10,
            column_data=[
                ('Table_id', dp(40)),
                ('Name', dp(40)),
               
            ],
            row_data=table_row_data
        )
        return self.table_table
    
    def show_restaurant_list(self, button):
        menu_items = []
        restaurant_list =self.restaurant_list

        for restaurant in restaurant_list:
            menu_items.append({"viewclass": "OneLineListItem",
                               "text": restaurant.name,
                               "on_release": lambda r=restaurant: self._update_data_table(r)})

        self.dropdown = MDDropdownMenu(
            caller=button,
            items=menu_items,
            width_mult=5,
            max_height=dp(150),
        )
        self.dropdown.open()

    
   
    def _checked(self, instance_table, current_row):
        self.selected_table = Table(
            current_row[0], current_row[1] ,[]
        )
        self.table_id_input.text = str(self.selected_table.id)
        self.seats_input.text = str(self.selected_table.name)

   
    def _update_data_table(self,restaurant):
        
        self.restaurant = restaurant

        #get employee data for the selected department 
        table_row_data =[]
        tables= restaurant.seats_list
        for table in tables:
            table_row_data.append(
                (table.id,table.name)

            )
            #update the employee table with the data
            self.table_table.row_data = table_row_data

    def _add_table(self, instance):
        table_id =self.table_id_input.text
        seats = self.seats_input.text
        
        table_data = [table_id,seats]

        if self._is_data_valid(table_data):
            self.table_manager_controller.add_Table(self.restaurant, table_data)
            self.table_table.row_data.append((table_id,seats))
            self._clear_input_text_fields()
        else:

            popup = Popup(
                title = "Invalid data",
                content = Label(text="Provide manatory data to add a new Table"),
                size_hint =(None,None),
                size =(400,200),
  
            )
            popup.open()

    def _on_row_press(self,instance,row):
        #Set the row index to delete when the row is pressed 
        self.selected_row = int (row.index / len(instance.column_data))
    

    def _update_table(self,instance):
        if self.selected_row !=-1 :
            #Get the updated employee data from the input fields 
            table_id =self.table_id_input.text
            seats= self.seats_input.text
          

            table_data = []
            table_data.append(table_id)
            table_data.append(seats)

            if self._is_data_valid(table_data):

                table_to_remove = self.table_table.row_data[self.selected_row]
                
                del self.table_table.row_data[self.selected_row]
                self.table_manager_controller.delete_Table(
                    self.restaurant,table_to_remove
                )
                self.table_manager_controller.add_Table(
                    self.restaurant ,table_data

                )
                self.table_table.row_data.append([table_id,seats])
                self._clear_input_text_fields()
            else :
                popup = Popup (
                    title ="Invalid data",
                    content = Label(text ="Provide mandatory data to updat the Table"),
                    size_hint =(None,None),
                    size=(400,200),

                )
                popup.open()
        else:
            popup = Popup(
                title= "Invalid data",
                content =Label(text="Selectany row to update "),
                size_hint =(None,None),
                size =(400,200),

            )
            popup.open()

    def _delete_table(self,instance):
        if self.selected_row !=-1:
            table_to_remove = self.table_table.row_data[self.selected_row]
            del self.table_table.row_data[self.selected_row]
            self.table_manager_controller.delete_Table(
                self.restaurant,table_to_remove
            )
            self._clear_input_text_fields()

        else:
            popup =Popup(
                title ="Invalid data",
                content=Label(text="Selected any row to delete"),
                size_hint=(None,None),
                size=(400,200),
            )


            popup.open()

    def _clear_input_text_fields(self):
        #Clear the input fields by setting their text to empty strings
        self.table_id_input.text =""
        self.seats_input.text =""
        self.selected_row = -1

    def _is_data_valid(self,table_data):
        #Check if empl;oyee data is valid (all fields are filles)
        return(
            table_data[0] !=""
            and table_data[1] !=""
          

        )     
    
    

    