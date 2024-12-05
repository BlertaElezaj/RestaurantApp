from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager

from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from login_controller import LoginController
from utils import AuthorizationService, UserFeatureLabelResolver,UserFeatureContentPanelResolver
import sys



class TwoPanelLayoutApp(MDApp):

    def build(self):
        Window.size = (900, 500)
        screen = Screen()
        screen.add_widget(self._create_split_layout_panel())
        return screen
    
    def _create_split_layout_panel(self):
        self.split_layout_panel = GridLayout(cols = 2)
        self.split_layout_panel.add_widget(self._create_navigation_bar_panel())
        self.split_layout_panel.add_widget(self._create_content_panel())
        return self.split_layout_panel
  
    def __create_navigation_bar_buttons(self):
        self.button_list = []
        user_role = LoginController.get_logged_in_user().user_role
        authorization_service = AuthorizationService()
        self.user_featuers = authorization_service.get_user_feature_by_user_role(user_role)
        for feature in self.user_featuers:
                button = Button(text= UserFeatureLabelResolver.get_user_feature_label(feature)  ,  background_color=(0, 1, 1, 1), 
                            color=(1, 1, 1, 1), 
                            font_size=18, 
                            size_hint=(1, None))
                button.size = (300,60)
                self.button_list.append(button)
        return self.button_list
    
    def _create_navigation_bar_panel(self):
        navigation_bar_panel = GridLayout(cols = 1, spacing = 20)
        navigation_bar_panel.size_hint_x = None
        navigation_bar_panel.width = 300
        button_list = self.__create_navigation_bar_buttons()
        for button in button_list:
            if button.text != "Sign out":
                button.bind(on_press=self._change_content_panel_label)
            else:
                button.bind(on_press=self._sign_out)
            navigation_bar_panel.add_widget(button)
        return navigation_bar_panel

    def _create_content_panel(self):
        self.content_panel = GridLayout(cols = 1, spacing = 20)
        self.content_panel.size_hint_x = None
        self.content_panel.width = 900
        self.content_panel_content =Label(
            text = "WELCOME", color =(64,181,173)
        )
        self.content_panel.add_widget(self.content_panel_content)
        return self.content_panel
    
    def _change_content_panel_label(self, instance):
        self.split_layout_panel.clear_widgets()
        self.split_layout_panel.add_widget(self._create_navigation_bar_panel())

        user_feature_panel_creator = UserFeatureContentPanelResolver.get_user_feature_panel(instance.text)

        if user_feature_panel_creator is not None:
            self.content_panel = user_feature_panel_creator.create_content_panel()
            self.split_layout_panel.add_widget(self.content_panel)
        else:
            # Handle the case where user_feature_panel_creator is None
            print("Error: User feature panel creator is None.")

        for button in self.button_list:
            if button.text == instance.text:
                button.background_color = (0, 0, 0, 1)
            else:
                button.background_color = (0, 1, 1, 1)


    def _sign_out(self, instance):
        sys.exit(0)




class LoginApp(MDApp):
    username_input = None
    password_input = None

    def build(self):
        Window.size = (500, 600)
        screen_manager = ScreenManager()
        screen = Screen()
        screen.add_widget(self._create_login_components())
        screen_manager.add_widget(screen)
        self.screen = screen
        self.screen_manager = screen_manager
        return screen_manager

    def _create_login_components(self):
        layout = GridLayout(cols=1, padding=150, spacing=30)

        restaurant_label = MDLabel(text="LOGIN FORM", font_size="50sp", halign="center")
        layout.add_widget(restaurant_label)

        self._create_username_component()
        layout.add_widget(self.username_input)

        self._create_password_components()
        layout.add_widget(self.password_input)

        view_password_button = MDIconButton(
            icon="eye-off", on_release=self.toggle_password_visibility
        )
        layout.add_widget(view_password_button)

        login_button = self._create_button_component()
        layout.add_widget(login_button)

        return layout

    def _create_username_component(self):
        self.username_input = MDTextField(hint_text="Username")

    def _create_password_components(self):
        self.password_input = MDTextField(password=True, hint_text="Password")
        self.password_input.bind(
            on_text_validate=self.login_with_provided_user_credentials
        )

    def toggle_password_visibility(self, instance):
        if self.password_input.password:
            self.password_input.password = False
            instance.icon = "eye"
        else:
            self.password_input.password = True
            instance.icon = "eye-off"

    def _create_button_component(self):
        login_button = Button(
            text="Login",
            size_hint=(None, None),
            size=(100, 50),
            background_color=(0, 0.7, 0.9, 1),
        )
        login_button.bind(on_press=self.login_with_provided_user_credentials)
        return login_button

    def login_with_provided_user_credentials(self, instance):
        username = self.username_input.text
        password = self.password_input.text

        if self.is_credentials_provided(username, password):
            LoginController.login_user( username, password)
            user = LoginController.get_logged_in_user()
            if user is None:
                popup = Popup(
                    title="Login failed",
                    content=Label(text="Invalid username or password."),
                    size_hint=(None, None),
                    size=(400, 200),
                )
                self.username_input.text = ""
                self.password_input.text = ""
                popup.open()
            else:
                two_panel_layout_screen = TwoPanelLayoutApp().build()
                self.screen_manager.remove_widget(self.screen)
                self.screen_manager.add_widget(two_panel_layout_screen)

    def is_credentials_provided(self, username, password):
        if LoginController.is_string_none_or_blank(username):
            popup = Popup(
                title="Credentials missing ",
                content=Label(text="Please provide your username."),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()
            return False
        elif LoginController.is_string_none_or_blank(password):
            popup = Popup(
                title="Credentials missing ",
                content=Label(text="Please provide your password."),
                size_hint=(None, None),
                size=(400, 200),
            )
            popup.open()
            return False
        return True

LoginApp().run()