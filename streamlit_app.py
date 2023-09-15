import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('my parents new healthy dinner')
streamlit.header('Breakfast Favourites')
streamlit.text('🥣 omega 3 & blueberry oatmeal')
streamlit.text('🥗 kale, spincacj & rocket smoothie')
streamlit.text('🐔 hard-boiled gree-reange egg')
streamlit.text('🥑🍞 advocado toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)


#create repeatable block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

#new section to display api response
streamlit.header('Fuityvice Fruite Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
    
    # format inot a new table
    #streamlit.dataframe(fruityvice_normalized)
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
#snowflake related fiunctions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return  my_cur.fetchall()

#add button
if streamlit.button('get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_row)

# dont run anything past here
streamlit.stop()

  



 #streamlit.write('The user entered ', fruit_choice)
#streamlit.text(fruityvice_response.json())
# write your own comment -what does the next line do? 


#my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text("Hello from Snowflake:")
#streamlit.text(my_data_row)





# my_data_row = my_cur.fetchone()
my_data_row = my_cur.fetchall()
#streamlit.header("The fruit load list contains:")


add_my_fruit = streamlit.text_input('What fruit would you like add','jackfruit')
# streamlit.text("thanks fort adding :" + add_my_fruit )
my_cur.execute("insert into FRUIT_LOAD_LIST values ('from streamlit')")
