import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

streamlit.title('My Mums Healthy New Diner')

streamlit.header('Breakfast Favourites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Adding a picklist for the fruits they want in the smoothie
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Displaying the fruit list in a table
streamlit.dataframe(fruits_to_show)

#New Section to display Fruityvice API response
streamlit.header('Fruityvice Fruit Advice!')
try:
  #User input to determine what fruit to get advice about
  fruity_choice = streamlit.text_input('What fruit would you like information about?')
  
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruity_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #take the response json and normalize it
    streamlit.dataframe(fruityvice_normalized)  #output the normalized json on screen as a table
    
  except URLError as e:
    streamlit.error()
  
streamlit.stop() #No code running from here onwards while testing fixes

#Snowflake connection information and display
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

#User input box to add fruit to list
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')  #input box with default entry jackfruit
streamlit.write('Thanks for adding ',add_my_fruit) #displays input value from input box

#writeback to Snowflake - currently using test value rather than variable
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
