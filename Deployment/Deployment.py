import streamlit as st
import requests
from streamlit_lottie import st_lottie
import joblib
from sklearn.impute import KNNImputer
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from Encoders import encoding
from streamlit_modal import Modal
import pandas as pd
from PIL import Image
import numpy as np
pd.set_option('display.max_columns', None)


# ********************************* Loading Files ********************************************
polynomial_model = joblib.load(r'D:\Applai\Project\Deployment\poly_model.joblib')
linear_model = joblib.load(r'D:\Applai\Project\Deployment\linear_regressor.joblib')
polynomial_features = joblib.load(r'D:\Applai\Project\Deployment\poly_reg.joblib')
xgb_model = joblib.load(r'D:\Applai\Project\Deployment\xgb_regressor.joblib')

scaler = joblib.load(open(r"D:\Applai\Project\Deployment\scaler.joblib", 'rb'))
sale_type_encoder = joblib.load(open(r"D:\Applai\Project\Deployment\saletype_encoder.joblib", 'rb'))
neighbor_encoding = joblib.load(open(r"D:\Applai\Project\Deployment\neighbor_encoding.joblib", 'rb'))
foundation_encoder = joblib.load(open(r"D:\Applai\Project\Deployment\foundation_encoder.joblib", 'rb'))
exterior2_encoder = joblib.load(open(r"D:\Applai\Project\Deployment\exterior2_encoder.joblib", 'rb'))
exterior1_encoder = joblib.load(open(r"D:\Applai\Project\Deployment\exterior1_encoder.joblib", 'rb'))
knn_imputer = joblib.load(open(r"D:\Applai\Project\Deployment\imputer.joblib", 'rb'))


house_image = Image.open(r"D:\Applai\Project\Deployment\houseicon.jpg")

col1, col2 = st.columns([1, 0.5])  
col2.image(house_image, width=180) 
col1.title("Your Dream House")


available_features = [2,4,8,12,14,15,19,20,22,24,25,30,32,34,36,39,42,44,46,47,49,50,51,56]
numerical_features = ['Street Frontage', 'Year Built',
                      'Year Remodeled', 'Masonry Veneer Area',
                      'Total Basement SF', 'First Floor SF', 'Above Grade Living SF', 'Full Bathrooms', 'Kitchens Above Grade', 'Total Rooms Above Grade', 'Fireplaces', 'Garage Cars Capacity', 'Garage Area SF', 'Open Porch Area SF']
categorical_features = ['Lot Shape', 'Neighborhood', 'Foundation Type', 'Overall Quality','Exterior Quality'
                        'Basement Quality', 'Basement Exposure',
                        'Heating Quality and Condition', 'Garage Location', 'Garage Finish']

selected_scaling_params = scaler.scale_[available_features]
selected_min_values = scaler.min_[available_features]
selected_max_values = scaler.data_max_[available_features]

new_scaler = MinMaxScaler()
new_scaler.scale_ = selected_scaling_params
new_scaler.min_ = selected_min_values
new_scaler.data_max_ = selected_max_values



# Taking input data
with st.form(key="form1"):
    left_column,right_column = st.columns(2)
    with right_column:
        lot_shape = st.selectbox("Choose Lot Shape", ["Regular", "Slightly Irregular", "Moderately Irregular","Irregular"])
        neighborhood = st.selectbox("Choose The Neighborhood",
                                    ["Bloomington Heights", "Bluestem ", "Briardale", "Brookside", 'Clear Creek'
                                        , 'College Creek', 'Crawford', 'Edwards', 'Gilbert',
                                     'Iowa DOT and Rail Road', 'Meadow Village', 'Mitchell',
                                     'North Ames', 'Northridge', 'Northpark Villa', 'Northridge Heights',
                                     'Northwest Ames', 'Old Town',
                                     'South & West of Iowa State University', 'Sawyer', 'Sawyer West', 'Somerset',
                                     'Stone Brook',
                                     'Timberland', 'Veenker'])
        overall_cat_qual=st.select_slider("Choose The Overall Quality Of The Finish & Material",[1,2,3,4,5,6,7,8,9,10])
        exterior_qual=st.select_slider("Choose The Exterior Quality ",[0,1,2,3])
        foundation_type=st.selectbox("Choose The Foundation Type ",['Brick & Tile','Cinder Block','Poured Contrete','Slab','Stone','Wood'])
        basement_qual=st.selectbox("Choose Basement Quality ",['No Basement','Poor','Fair','Typical','Good','Excellent'])
        basement_exposure=st.selectbox("Choose Basement Exposure ",['No Basement','No Exposure','Mimimum Exposure','Average Exposure','Good Exposure'])
        heating_qual_cond = st.selectbox("Choose The Heating Quality and Condition ",[0,1,2,3,4])
        garage_location = st.selectbox("Choose The Garage Location ", ['2 Types', 'Attached To Home', 'Basement Garage', 'Built-In ','Car Port','Detached From Home','No Garage'])
        garage_finish = st.selectbox("Choose The Interior  Finish of The Garage ",['Finished', 'Rough Finished', 'Un finished', 'No Garage'])
        garage_area_sf = st.text_input(label="Enter The Garage Size in Square Feet")
        open_porch_area_sf = st.text_input(label="Enter The Size of the Open Porch Area in Square Feet")

    with left_column:
        street_frontage = st.text_input(label="Enter Street Frontage In Feet ")
        year_built = st.text_input(label="Enter The Year The House Was Built ")
        year_remodeled = st.text_input(label="Enter The Remodeled Year")
        masonary_veneer = st.text_input(label="Enter Masonary Veneer Area in Square Feet")
        total_basement_sf = st.text_input(label="Enter Total Basement Area in Square Feet")
        first_floor_sf = st.text_input(label="Enter The Area of The First Floor in Square Feet")
        above_grade_living_sf = st.text_input(label="Enter The Above grade (ground) Living Area in Square Feet")
        full_bathrooms = st.text_input(label="Enter The Number of Full Bathrooms ")
        kitchens_abv_grade = st.text_input(label="Enter The Number of Kitchen Above Grade ")
        total_rooms_abv_grade = st.text_input(label="Enter The Total Number of Rooms Above Grade ")
        fire_places = st.text_input(label="Enter The Number of Fire Places")
        garage_cars_capacity = st.text_input(label="Enter The Number of Cars Garage Can Have")

    submit_button = st.form_submit_button("Submit")

input_data=None
if submit_button:
   input_data = {
        "Lot Shape": lot_shape,
        "Neighborhood": neighborhood,
        "Overall Quality": overall_cat_qual,
        "Exterior Quality": exterior_qual,
        "FoundationType": foundation_type,
        "Basement Quality": basement_qual,
        "Basement Exposure": basement_exposure,
        "Heating Quality and Condition": heating_qual_cond,
        "Garage Location": garage_location,
        "Garage Finish": garage_finish,
        "Garage Area (Square Feet)": garage_area_sf,
        "Open Porch Area (Square Feet)": open_porch_area_sf,
        "Street Frontage": street_frontage,
        "Year Built": year_built,
        "Year Remodeled": year_remodeled,
        "Masonry Veneer Area (Square Feet)": masonary_veneer,
        "Total Basement Area (Square Feet)": total_basement_sf,
        "First Floor Area (Square Feet)": first_floor_sf,
        "Above Grade Living Area (Square Feet)": above_grade_living_sf,
        "Full Bathrooms": full_bathrooms,
        "Kitchens Above Grade": kitchens_abv_grade,
        "Total Rooms Above Grade": total_rooms_abv_grade,
        "Fireplaces": fire_places,
        "Garage Cars Capacity": garage_cars_capacity
      }

   input_df = pd.DataFrame([input_data])

   # Encoding
   encoder = encoding()
   input_df['Lot Shape']= encoder.lot_shape(input_df['Lot Shape'])
   input_df['Neighborhood']= encoder.neighborhood(neighbor_encoding,input_df['Neighborhood'])
   input_df['FoundationType']= encoder.foundation_type(foundation_encoder,input_df['FoundationType'])
   input_df['Basement Quality']= encoder.basement_quality(input_df['Basement Quality'])
   input_df['Basement Exposure']= encoder.basement_exposure(input_df['Basement Exposure'])
   input_df['Garage Location']= encoder.garage_location(input_df['Garage Location'])
   input_df['Garage Finish']= encoder.garage_finish(input_df['Garage Finish'])

   input_df['Masonry Veneer Area (Square Feet)'] = input_df['Masonry Veneer Area (Square Feet)'].astype(int)
   input_df['Total Basement Area (Square Feet)'] =input_df['Total Basement Area (Square Feet)'].astype(int)
   input_df['First Floor Area (Square Feet)'] = input_df['First Floor Area (Square Feet)'].astype(int)
   input_df['Above Grade Living Area (Square Feet)'] = input_df['Above Grade Living Area (Square Feet)'].astype(int)
   input_df['Total Rooms Above Grade'] =  input_df['Total Rooms Above Grade'].astype(int)
   input_df['Open Porch Area (Square Feet)'] =  input_df['Open Porch Area (Square Feet)'].astype(int)

   input_df['Masonry Veneer Area (Square Feet)'] = np.cbrt(input_df['Masonry Veneer Area (Square Feet)'])
   input_df['Total Basement Area (Square Feet)'] = np.cbrt(input_df['Total Basement Area (Square Feet)'])
   input_df['First Floor Area (Square Feet)'] = np.log(input_df['First Floor Area (Square Feet)'])
   input_df['Above Grade Living Area (Square Feet)'] = np.log(input_df['Above Grade Living Area (Square Feet)'])
   input_df['Total Rooms Above Grade'] = np.log1p(input_df['Total Rooms Above Grade'])
   input_df['Open Porch Area (Square Feet)'] = np.cbrt(input_df['Open Porch Area (Square Feet)'])


   # Scaling
   input_scaled = new_scaler.transform(input_df)

   # Models Prediction
   prediction = xgb_model.predict(input_scaled)

   prediction=np.round(prediction,0)
   average_prediction_str = f"{prediction} $"
   modal = Modal(
       key="demo-modal",
       title="The Price of your House is",

       # Optional
       padding=60,
       max_width=500
   )
   # Define the content of the modal
   with modal.container():
       # Display the content of the modal
       st.success(average_prediction_str)

       # Add a button at the bottom right to close the modal
       if st.button("OK", key="close-modal"):
           modal.toggle()








