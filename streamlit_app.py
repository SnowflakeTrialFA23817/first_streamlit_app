import streamlit
import pandas
import requests
import snowflake.connector

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
#User input to determine what fruit to get advice about
fruity_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered',fruity_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruity_choice)

streamlit.header('Fruityvice Fruit Advice!')

#take the response json and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#output the normalized json on screen as a table
streamlit.dataframe(fruityvice_normalized)

#Snowflake connection information and display
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)
