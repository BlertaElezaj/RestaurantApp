# Restaurant App

## Description
The **Restaurant App** is a Kivy-based application with Material Design components that allows users to log in, navigate through features, and interact with a two-panel layout. The app adapts to the user's role, displaying relevant features via dynamically generated buttons in the navigation panel.

### Key Features:
- **Login Form**: Users can log in with their username and password.
- **Two-Panel Layout**: A split layout consisting of a navigation panel on the left and a content panel on the right.
- **Role-based Navigation**: Navigation buttons are dynamically generated based on the user's role and the features available to them.
- **Dynamic Content Panel**: The content panel updates based on the selected feature from the navigation bar.
- **Sign Out**: Allows users to sign out from the application.
- **Password Visibility Toggle**: Provides a button to toggle the visibility of the password input field.

## Installation

### Prerequisites
- Python 3.x
- Kivy
- Kivymd

Install the required dependencies:

pip install kivy kivymd

Run the application:
python main.py

Usage
Login: Open the app and enter your username and password to log in.
Navigation: Once logged in, you’ll be presented with a two-panel layout. The left panel contains a dynamic navigation bar that updates based on your role and available features.
Content: The content panel on the right will display the relevant content based on the selected feature from the navigation panel.
Sign Out: You can sign out from the app by selecting the "Sign out" button in the navigation bar.
Components
LoginApp: Manages the login screen and the user authentication process. After a successful login, it transitions to the main two-panel layout.
TwoPanelLayoutApp: Controls the layout after logging in. It includes a navigation panel on the left and a content panel on the right.
Navigation Panel: The left panel dynamically generates navigation buttons based on the user role and available features.
Content Panel: Displays content dynamically based on the selected feature from the navigation panel.
Password Visibility Toggle: Allows users to toggle the visibility of the password during login.
