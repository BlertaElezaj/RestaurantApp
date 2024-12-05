from enums import UserRole,UserFeatures
from admin_view import RestaurantManagerContentPanel,MenuManagerContentPanel,MenuItemManagerContentPanel,TableManagerContentPanel

class AuthorizationService:
    #class responsible for providing user feautures based on the user role
    def get_user_feature_by_user_role(self,user_role):

        if user_role == UserRole.ADMIN:
           return [UserFeatures.RESTAURANT_MANAGER ,UserFeatures.MENU_MANAGER ,UserFeatures.MENU_ITEM_MANAGER,UserFeatures.TABLE_MANAGER,UserFeatures.SIGN_OUT]
        elif user_role == UserRole.FINANCIAL_MANAGER:
           return [UserFeatures.ACCOUNTS,UserFeatures.FINANCIAL_REPORTS,UserFeatures.EXPENSE_TRACKING,UserFeatures.BILLING,UserFeatures.PAYROLLS,UserFeatures.SIGN_OUT]
        elif user_role == UserRole.WAITER:
            return [UserFeatures.BILLING,UserFeatures.TABLE_MANAGER ,UserFeatures.TAKE_ORDERS,UserFeatures.SIGN_OUT]
        elif user_role is None :
            raise RuntimeError("The provided user role" + user_role + "is not supported")
        
class UserFeatureLabelResolver:
    #class resposible for resolving user feature labels

    user_feature_label_dict = None

    @staticmethod

    def get_user_feature_label (user_feature):
        return UserFeatureLabelResolver.__get_user_features_label_dict().get(user_feature)
         

    @staticmethod
    def __get_user_features_label_dict():
        if UserFeatureLabelResolver.user_feature_label_dict is None:
            UserFeatureLabelResolver.user_feature_label_dict = {
               UserFeatures.EMPLOYEES: "Employees" ,
               UserFeatures.RESTAURANT_MANAGER: "Restaurant_manager",
               UserFeatures.MENU_MANAGER:"Menu_manager",
               UserFeatures.MENU_ITEM_MANAGER:"Menu_item_manager",
               UserFeatures.ACCOUNTS :"Accounts",
               UserFeatures.TABLE_MANAGER:"Table_manager",
               UserFeatures.FINANCIAL_REPORTS:"Financial_reprots",
               UserFeatures.EXPENSE_TRACKING:"Expense_tracking",
               UserFeatures.PAYROLLS:"Payrolls",
               UserFeatures.BILLING:"Billing",
               UserFeatures.FINANCIAL_REPORTS:"Financial_reports",
               UserFeatures.CUSTOMER_SERVICE:"Customer_service",
               UserFeatures.TAKE_ORDERS:"Take_orders",
               UserFeatures.SIGN_OUT :"Sign_out"
        
            }        

        return UserFeatureLabelResolver.user_feature_label_dict
    


class UserFeatureContentPanelResolver:
    user_feature_content_panel_map = None

    @staticmethod
    def get_user_feature_panel(user_feature):
        return UserFeatureContentPanelResolver.get_user_feature_content_panel_map().get(user_feature)

    @staticmethod
    def get_user_feature_content_panel_map():
        if UserFeatureContentPanelResolver.user_feature_content_panel_map is None:
            UserFeatureContentPanelResolver.user_feature_content_panel_map = {
                "Restaurant_manager": RestaurantManagerContentPanel(),
                "Menu_item_manager":MenuItemManagerContentPanel(),
                "Menu_manager":MenuManagerContentPanel(),
                "Table_manager":TableManagerContentPanel(),
              
                # Add more mappings here if needed
            }

        return UserFeatureContentPanelResolver.user_feature_content_panel_map

