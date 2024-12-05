from dataprovider import DataProvider

class RestaurantPointApp:
  def start(self):
    self.restaurant_list=[]
    self.data_provider = DataProvider()
    self.restaurant_list=self.data_provider.restaurant_list

    #loop through each restaurant
    for restaurant in self.restaurant_list:
      print("================================")
      print("List of menus in the " + restaurant.name +"restaurant")
      print ("====================================")
      #loop through each menu in the restaurant
      for menu in restaurant.menu_list:
        print (menu.name +", "+str(menu.menu_id) )
        print("-------------------------------------")

        for menu_item in menu.menu_item_list:
          print(menu_item.name +" "+str(menu_item.price)+ " "+ menu_item.description )
          print("--------------------------------------")



restaurant_point_app=RestaurantPointApp()
restaurant_point_app.start()



        
        