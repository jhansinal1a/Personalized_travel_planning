import streamlit as st
import pickle
from dependency import FINAL
import pandas as pd
import streamlit.components.v1 as components
#import psycopg2
import folium

streamlit_style = """
			<style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;1,100&display=swap');

    .hotel-bold {
        font-weight: 600;
        color: green; /* Updated color for bold text */
    }

    .hotel-font {
        font-size: 20px;
        background-color: #f0e6ff; /* Light purple background */
        color: #3e2c41; /* Darker text color for contrast */
    }

    label.css-1p2iens.effi0qh3 {
        font-size: 18px;
        color: #4b3f4e; /* Updated label color */
    }

    p, li {
        font-size: 18px;
        color: #60AE9E; /* Updated paragraph and list item color */
    }

    #MainMenu {
        visibility: hidden;
    }

    button.css-135zi6y.edgvbvh9 {
        font-size: 18px;
        font-weight: 600;
        background-color: yellow; /* Updated button background color */
        color: #fff; /* White text for the button */
        border: 1px solid #867399; /* Border color for the button */
    }
</style>



			"""
st.markdown(streamlit_style, unsafe_allow_html=True)




#import streamlit_folium 
from streamlit_folium import folium_static


# Initialize connection.
# Uses st.experimental_singleton to only run once.
# @st.experimental_singleton
# def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])

# conn = init_connection()



st.image('./data/Cover-Img.png')
st.title('Refining Travel Suggestions Through Machine Learning ')

pickle_in = open("lol.pkl","rb")
load_lol=pickle.load(pickle_in)


def welcome():
    return "Welcome All"

def output_main(Type,Duration,Budget,TYPE,Ques):
    
    """Let's Authenticate the Banks Note 
    This is using docstrings for specifications.
    ---
    parameters:  
      - name: Type
        in: query
        type: string
        required: true
      - name: Duration
        in: query
        type: number
        required: true
      - name: Budget
        in: query
        type: number
        required: true
      - name: Ques
        in: query
        type: string
        required: true
      - name: .
        in: query
        type: number
        required: true
    responses:
        200:
            description: The output values
        
    """
   
    #prediction=classifier.predict([[variance,skewness,curtosis,entropy]])
    #print(load_lol)
    output,info, map = FINAL(Type,Duration,Budget,TYPE,Ques) 
    print(output)
    return [output,info,map]


def main():

    @st.cache(allow_output_mutation=True)
    def get_data():
      return []

    lis1 = ['Adventure and Outdoors','Spiritual','City Life', 'Cultural','Relaxing']
    lis2 = ['Family','Friends','Individual']

    Type = st.multiselect("Vacation type according to priority:",lis1)

    Duration = st.slider("Duration (days)",min_value=1,max_value=40)
    Duration = int(Duration)
    
    Budget = st.slider("Budget (INR)",min_value=200,max_value=150000,step=500)
    Budget = int(Budget)

    col1, col2 = st.columns(2)
    
    TYPE = col1.selectbox("Who are you travelling with?",lis2) ## already filled change
    Ques = col2.radio("Is covering maximum places a priority?",['Yes',"No"])

    ## Condition-Error
    cutoff = Budget/Duration

    result=""
    st.write(' ')
    if st.button("What do you recommend?"):

        try:
          RESULT = output_main(Type,Duration,Budget,TYPE,Ques)
        except:
          if(cutoff<260):
            st.subheader("Irrational. Try increasing your Budget or scaling down the Duration") # FORMAAT
          else:
            st.subheader("Please check your Console")
          return

        
        get_data().append({"Type": Type, "Duration": Duration,
                           "Budget": Budget, "TYPE": TYPE, "Ques": Ques})
        
        FINAL_DATA = pd.DataFrame(get_data()) #####
        FINAL_DATA.to_csv('data/FinalData.csv') #####

        Output = RESULT[0]
        Info = RESULT[1]
        Map = RESULT[2]

        st.subheader('Your Inputs')
        st.write('{}'.format(Info[0]))
        col3, col4 = st.columns(2)
        len(Info)
        for i in range(1,len(Info)-5):
            try: 
                col3.write('{}'.format(Info[i]))
            except:
                continue
        for i in range(4,len(Info)-2):
            try: 
                col4.write('{}'.format(Info[i]))
            except:
                continue
        st.write('{}'.format(Info[-2]))
        
        st.header('Suggested Itinerary')
        st.markdown('<p class="hotel-font"><span class="hotel-bold">Suggested Hotel/Accomodation:</span> {}<p>'.format(Info[-1]),unsafe_allow_html=True)
        st.write(' ')
        for i in range(0,len(Output)):
          st.write('{}'.format(Output[i])) ## 

        st_map = folium_static(Map)
        #st.markdown(st_map)
        
    # if st.button("Store data"):

    #   Before_df = pd.read_csv("data/MAIN_Data.csv")
    #   This_time_df = pd.read_csv('data/FinalData.csv')

    #   Before_df.append(This_time_df)
    #   Before_df.to_csv("data/MAIN_Data.csv",index=False)

    
    
if __name__=='__main__':
    main()


