import streamlit as st
import pybase64
import pandas as pd
import numpy as np
from streamlit_option_menu import option_menu
import pickle
from PIL import Image
import plotly.graph_objects as go
import dash_map as dm
from prophet import Prophet
import randDataProvider as rd

#Create plot
def create_plot(df, x, y, y_lim, g0, g1, b0, b1, y0, y1, r0, r1, param):
    """
        The function creates a plot of the selected parameter and catchment area using the following arguments
        
        Inputs:
        df - dataframe
        area - Selected catchment area
        x - x_axis
        y - y_axis
        y_lim - upper limit of the y_axis
        g0 - lower y value of acceptable rectangle
        g1 - upper y value of acceptable rectangle
        b0 - lower y value of ideal rectangle
        b1 - upper y value of ideal rectangle
        y0 - lower y value of tolerable rectangle
        y1 - upper y value of tolerable rectangle
        r0 - lower y value of unacceptable rectangle
        r1 - upper y value of unacceptable rectangle
    
    """
    fig = go.Figure() 
    #Line chart
    fig.add_trace(go.Scatter(x=df[x], y=df[y], mode='lines',
            line=dict(color='black', width=3),
            connectgaps=True))
    #update axis
    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            tickangle=330),
        yaxis=dict(
            showgrid=False,
            zeroline=True,
            showline=True,
            showticklabels=True,
            title= f'{param} ',
            range=[0, y_lim]) )
    # Add shapes
    fig.add_hrect(y0=g0, y1=g1, 
                annotation_text="Acceptable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="green", opacity=0.2, line_width=0)
    fig.add_hrect(y0=b0, y1=b1, 
                annotation_text="Ideal", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="blue", opacity=0.2, line_width=0)
    fig.add_hrect(y0=y0, y1=y1, 
                annotation_text="Tolerable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="yellow", opacity=0.2, line_width=0)
    fig.add_hrect(y0=r0, y1=r1, 
                annotation_text="Unacceptable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="red", opacity=0.2, line_width=0)
    st.plotly_chart(fig)


def make_forecast(df, y, para ):
    df.reset_index(inplace=True)

    #Prepare data for forecast
    df['day-month'] = ''
    for i, qtr in enumerate(df.qtr):
        if qtr == 1:
            df['day-month'][i] = '31-03'
        elif qtr == 2:
            df['day-month'][i] = '30-06'
        elif qtr == 3:
            df['day-month'][i] = '30-09'
        else:
            df['day-month'][i] = '31-12'
        
    df['date'] = df['day-month'].astype(str) + ' ' + df['year'].astype(str)
    df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)

    # define the period for which we want a prediction
    future = pd.date_range('2022-06-30', periods=10, freq='Q').tolist()
    future = pd.DataFrame(future)
    future.columns = ['ds']
    future['ds']= pd.to_datetime(future['ds'], infer_datetime_format=True)

    
    # prepare expected column names
    data = pd.DataFrame(columns=['ds', 'y'])
    data['ds'] = df['date']
    data['y'] = df[y]
    data['ds']= pd.to_datetime(data['ds'], infer_datetime_format=True)

    # define the model
    model = Prophet()

    # fit the model
    model.fit(data)

    #save model as pickle file
    #pickle.dump(model, open("data/model.sav", 'wb'))

    # use the model to make a forecast
    #model = pickle.load(open("data/model.sav", 'rb'))
    forecast = model.predict(future)   

    #plot forecast
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat'],
    mode = 'lines',
    marker = {
        'color': '#3bbed7'
    },
    line = {
        'width': 1.5
    },
    name = 'Forecast',
    ))

    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat_lower'],
    marker = {
        'color': 'rgba(0,0,0,0)'
    },
    showlegend = False,
    hoverinfo = 'none',
    name = 'yhat_lower' ,
    ))

    fig.add_trace(go.Scatter(
    x = forecast['ds'],
    y = forecast['yhat_upper'],
    fill='tonexty',
    fillcolor = 'rgba(0,128,128,0.5)',
    name = 'Confidence',
    mode = 'none'
    ))

    fig.add_trace(go.Scatter(
    x = data['ds'],
    y = data['y'],
    mode = 'lines',
    line=dict(color='blue', width=2),
    connectgaps=True,
    name = 'Actual'
    ))

    # Add shapes
    fig.add_hrect(y0=70, y1=90, 
                annotation_text="Acceptable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="green", opacity=0.2, line_width=0)
    fig.add_hrect(y0=90, y1=100, 
                annotation_text="Ideal", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="blue", opacity=0.2, line_width=0)
    fig.add_hrect(y0=50, y1=70, 
                annotation_text="Tolerable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="yellow", opacity=0.2, line_width=0)
    fig.add_hrect(y0=0, y1=50, 
                annotation_text="Unacceptable", annotation_position="right",
                annotation=dict(font_size=10, font_family="Times New Roman"),
                fillcolor="red", opacity=0.2, line_width=0)

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='black',
            linewidth=0.7,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='black',
                        ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            title=para,
            linecolor='black',
            linewidth=0.7,
            ticks='outside',
            tickfont=dict(
                family='Arial',
                size=12,
                color='black',
            )
        ),
        
        showlegend = True,
    plot_bgcolor='#D3E2F7'
    ) 
    st.plotly_chart(fig)

def river_plot(id, df):

    df = df.loc[df['river_id'] == id]
    

    # Step: Sort column(s) year ascending (A-Z), qtr ascending (A-Z)
    df = df.sort_values(by=['year', 'qtr'], ascending=[True, True])


    # Step: Create new column 'date' from formula 'quarter + " " + year.astype(str)'
    df['date'] = df['quarter'] + " " + df['year'].astype(str)

    #create sidebar options for parameters
    if id == 2:
        parameters = ['Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P', 'Overall Compliance']

    else:
        parameters = ['COD', 'Conductivity','E.coli','Nitrate NO3 as N','pH','Phosphate PO4 as P', 'Overall Compliance']
   
    param = st.sidebar.selectbox("Choose Parameter", parameters)   

    if param == 'Overall Compliance':

        para = st.sidebar.radio('', ['Physical', 'Chemical', 'Overall'])

        
        
        if para == 'Physical':

            #create options for catchment area
            options = df['sample_pt_desc'].loc[df['physical_compliance_percentage'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)
           
            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]
            
            make_forecast(df, 'physical_compliance_percentage', para)

        if para == 'Chemical':

            #create options for catchment area
            options = df['sample_pt_desc'].loc[df['chemical_compliance_percentage'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]


            make_forecast(df, 'chemical_compliance_percentage', para)

        if para == 'Overall':

            #create options for catchment area
            options = df['sample_pt_desc'].loc[df['overall_compliance_percentage'] > 0].unique().tolist()
            area = st.sidebar.selectbox("Choose Catchment area", options)

            #filter by catchment area
            df = df.loc[df['sample_pt_desc'] == area]
            
            make_forecast(df, 'overall_compliance_percentage', para)

    if param == 'COD':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #create options for catchment area
        options = df['sample_pt_desc'].loc[df['cod'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #Filter data by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #Create plot
        create_plot(df = df, x='date', y = 'cod', y_lim = 60, g0 = 20, g1=35, b0=0, b1=19, y0=35, y1=55, r0=55, r1=60, param=param)


    if param == 'Conductivity':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #catchment area options
        options = df['sample_pt_desc'].loc[df['conductivity'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #filter by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #Create plot
        create_plot(df = df, x='date', y = 'conductivity', y_lim = 140, g0 = 18, g1=30, b0=0, b1=18, y0=30, y1=70, r0=70, r1=140, param=param)

    
    if param == 'pH':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #options for catchment area
        options = df['sample_pt_desc'].loc[df['pH'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #filter by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #Create plot
        fig = go.Figure() 

        #Line chart
        fig.add_trace(go.Scatter(x=df['date'], y=df['pH'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))

        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                tickangle=330),
            
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} ',
                range=[5, 11]) )

                    
        # Add shapes
        fig.add_hrect(y0=6.5, y1=7, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.2, line_width=0)
        
        fig.add_hrect(y0=8.4, y1=8.5,
                    fillcolor="green", opacity=0.2, line_width=0)

        fig.add_hrect(y0=7, y1=8.4, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.2, line_width=0)

        fig.add_hrect(y0=6, y1=6.5, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.2, line_width=0)
        
        fig.add_hrect(y0=8.5, y1=9, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.2, line_width=0)

        fig.add_hrect(y0=0, y1=6, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.2, line_width=0)
        fig.add_hrect(y0=9, y1=11, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.2, line_width=0)
        st.plotly_chart(fig)

    
    if param == 'E.coli':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #Catchment area options
        options = df['sample_pt_desc'].loc[df['e_coli'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #filter by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #Create plot
        fig = go.Figure() 
        #Line chart
        fig.add_trace(go.Scatter(x=df['date'], y=df['e_coli'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))
        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                tickangle=330 ),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (mg/l)',
                type='log',
                range=[0, 5]) )
        # Add shapes
        fig.add_hrect(y0=130, y1=200, 
                    annotation_text="Acceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="green", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0, y1=130, 
                    annotation_text="Ideal", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="blue", opacity=0.2, line_width=0)
        fig.add_hrect(y0=200, y1=400, 
                    annotation_text="Tolerable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="yellow", opacity=0.2, line_width=0)
        fig.add_hrect(y0=400, y1=100000, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="red", opacity=0.2, line_width=0)
        
        st.plotly_chart(fig)

    if param == 'Nitrate NO3 as N':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #options for catchment area
        options = df['sample_pt_desc'].loc[df['nitrate'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #filter by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #create plot
        create_plot(df = df, x='date', y = 'nitrate', y_lim = 8, g0 = 0.5, g1=3, b0=0, b1=0.5, y0=3, y1=6, r0=6, r1=8, param=param)
    
        
    if param == 'Phosphate PO4 as P':

        #create date slider
        year = [f'{i}' for i in range(2011, 2023) ]
        start, stop = st.select_slider('Select time frame', options=year, value=('2011', '2022'))

        #Catchment area options
        options = df['sample_pt_desc'].loc[df['phosphate'] > 0].unique().tolist()
        area = st.sidebar.selectbox("Choose Catchment area", options)

        #filter by catchment area
        df = df.loc[df['sample_pt_desc'] == area]

        #Filter data by year
        df = df.loc[(df['year'].astype(str) >= start) & (df['year'].astype(str) <= stop)]

        #Create plot
        fig = go.Figure() 
        
        fig.add_trace(go.Scatter(x=df['date'], y=df['phosphate'], mode='lines',
                line=dict(color='black', width=3),
                connectgaps=True))
        #update axis
        fig.update_layout(
            xaxis=dict(
                showline=True,
                showgrid=False,
                showticklabels=True,
                tickangle=330),
            yaxis=dict(
                showgrid=False,
                zeroline=True,
                showline=True,
                showticklabels=True,
                title= f'{param} (mg/l)',
                range=[0, 3]) )
        
        # Add shapes
        fig.add_hrect(y0=0, y1=0.03, 
                    fillcolor="green", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0, y1=0, 
                    fillcolor="blue", opacity=0.2, line_width=0)
        fig.add_hrect(y0=0.03, y1=0.05, 
                    fillcolor="yellow", opacity=0.2, line_width=0)

        fig.add_hrect(y0=0.05, y1=3, 
                    annotation_text="Unacceptable", annotation_position="right",
                    annotation=dict(font_size=10, font_family="Times New Roman"),
                    fillcolor="red",opacity=0.2, line_width=0)
        st.plotly_chart(fig)

# Load data from databricks function
@st.cache(suppress_st_warning=True)
def get_data_from_databricks(query):
    data = rd.get_data(query)
    data.fillna(0, inplace=True)
    #data.to_csv("data/df.csv", index=False)
    return data

def main():
    #load data from sql table
    query = '''

        SELECT sp.sample_pt_desc, ra.year, ra.qtr, ra.quarter, ra.cod, ra.conductivity, ra.e_coli,
                ra.pH, nitrate, phosphate, ra.physical_compliance_percentage, ra.chemical_compliance_percentage,
                ra.bacteriological_compliance_percentage, 
                ra.biological_compliance_percentage, ra.overall_compliance_percentage, ri.river_id

        FROM rand ra
        INNER JOIN sampling_points sp
        ON ra.sample_id = sp.sample_id
        INNER JOIN rivers ri
        ON ra.river_id = ri.river_id

        '''
    data = get_data_from_databricks(query)

    #Select river
    rivers = ['Vaal', 'Klip', 'Blesbokspruit']
    river = st.sidebar.selectbox("Select a river", rivers)

    if river == 'Vaal':
        river_plot(1, data)
            
        
    if river == 'Blesbokspruit':
        river_plot(2, data)

    if river == 'Klip':
        river_plot(3, data)
       