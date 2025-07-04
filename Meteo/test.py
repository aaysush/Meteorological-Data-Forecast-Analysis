import streamlit as st
import pandas as pd
import numpy as np

# Tabs
Current ,Forecast, Weekly_Analysis = st.tabs(['Current','Forecast', ' Weekly-Analysis'])


    # Define the data
data = {
    "Original Columns": [
        "datetime", "temperature_2m", "dewpoint_2m", "apparent_temperature",
        "wind_speed_10m", "wind_direction", "cloud_cover_avg", "surface_pressure", 
        "sealevel_pressure", "rainfall", "snowfall", "relative_humidity_2m",
        "visibility", "uv_index", "chance_of_rain", "weather_condition",
        "vapour_pressure_deficit"
    ],
    "User-Friendly Names": [
        "Datetime", "Temperature (2m above surface)", "Dew Point (2m above surface)", "Feels Like Temperature",
        "Wind Speed (10m above surface)", "Wind Direction", "Cloud Cover (Avg)", "Surface Pressure",
        "Sea Level Pressure", "Rainfall", "Snowfall", "Relative Humidity (2m)",
        "Visibility", "UV Index", "Chance of Rain", "Weather Condition",
        "Vapour Pressure Deficit"
    ],
    "Units": [
        "ISO 8601 Datetime", "°C", "°C", "°C",
        "km/h", "Degrees", "%", "hPa",
        "hPa", "mm", "mm", "%",
        "km", "Index", "%", "Text",
        "kPa"
    ]
}

# Create the DataFrame
show = pd.DataFrame(data)
show.set_index("Original Columns", inplace=True)

#-----------------------------------------------------
# WEEKLY ANALYSIS
with Weekly_Analysis:
    st.title("WEEKLY ANALYSIS")
    st.divider()
    

    # Load data from CSV
    df = pd.read_csv(r'ml_code\df_final_filled.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Get last row
    last_row = df.iloc[-1]

    # Filter columns
    weather_columns = [col for col in last_row.index if col.startswith("weather")]
    no_show_colmns = [col for col in last_row.index if col.endswith('h')]
    other_columns = ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
    non_weather_columns = weather_columns + no_show_colmns + other_columns

    # Drop non-weather columns
    df_droped = df.drop(columns=non_weather_columns, errors="ignore")

    # Plotting UI
    st.title("Plotting and Column Details")
    columns_to_plot = [col for col in df_droped.columns if col != "datetime"]
    selected_column = st.selectbox("Select a column to plot:", columns_to_plot)

    if selected_column:
        st.write(f"Plotting datetime against **{selected_column}**")
        st.line_chart(data=df_droped.set_index('datetime')[selected_column])

    # Display cards
    st.write("Details of Other Columns:")
    for col in df.columns:
        if col not in non_weather_columns and pd.api.types.is_numeric_dtype(df[col]):
            value = np.mean(df[col])
            if col in show.index:
                user_friendly_name = show.loc[col, 'User-Friendly Names']
                unit_aaociated = show.loc[col, 'Units']
            else:
                user_friendly_name = col
                unit_aaociated = ""

            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px; background-color: #f9f9f9;">
                <h4 style="margin: 0;">{user_friendly_name}</h4>
                <p style="margin: 0;">Mean Value: <strong>{value:.2f} {unit_aaociated}</strong></p>
            </div>
            """, unsafe_allow_html=True)


from datetime import timedelta


#---------------------------------------------------------------------
# CURRENT AND FORECAST


with Forecast:


    df_forecast_weather = df.iloc[-1]

    for col in weather_columns:
     if df_forecast_weather[col] ==1:
        st.write(col) 

    # Filter columns
    weather_columns = [col for col in last_row.index if col.startswith("weather")]
    no_show_colmns = [col for col in last_row.index if col.endswith('h')]
    other_columns = ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
    non_weather_columns = weather_columns + no_show_colmns + other_columns

    df_forecast = df_forecast_weather.drop(non_weather_columns)

    st.header(" Hourly Forecast:")
    #st.divider()
    

    st.subheader("Temperature 🌤️")
    # Container for Temperature
    with st.container(border = True):
        
        pred1, pred2, pred3, pred4, pred5 = st.columns(5)

        with pred1:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=1))
            st.divider()
            st.subheader(f"{df_forecast_weather['temperature_2m_1h'].round(1)} °C")

        with pred2:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=2))
            st.divider()
            st.subheader(f"{df_forecast_weather['temperature_2m_2h'].round(1)} °C")

        with pred3:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=3))
            st.divider()
            st.subheader(f"{df_forecast_weather['temperature_2m_3h'].round(1)} °C")

        with pred4:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=4))
            st.divider()
            st.subheader(f"{df_forecast_weather['temperature_2m_4h'].round(1)} °C")

        with pred5:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=5))
            st.divider()
            st.subheader(f"{df_forecast_weather['temperature_2m_5h'].round(1)} °C")

    # Container for Relative Humidity
    st.subheader("Relative Humidity ☁️")
    st.write(' water vapor is in the air compared to the maximum amount of water vapor the air can hold at a specific temperature.')
    with st.container(border=True):
        
        pred1, pred2, pred3, pred4, pred5 = st.columns(5)

        with pred1:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=1))
            st.divider()
            st.subheader(f"{df_forecast_weather['relative_humidity_2m_1h'].round(1)} %")

        with pred2:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=2))
            st.divider()
            st.subheader(f"{df_forecast_weather['relative_humidity_2m_2h'].round(1)} %")

        with pred3:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=3))
            st.divider()
            st.subheader(f"{df_forecast_weather['relative_humidity_2m_3h'].round(1)} %")

        with pred4:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=4))
            st.divider()
            st.subheader(f"{df_forecast_weather['relative_humidity_2m_4h'].round(1)} %")

        with pred5:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=5))
            st.divider()
            st.subheader(f"{df_forecast_weather['relative_humidity_2m_5h'].round(1)} %")

    # Container for Chance of Rain
    st.subheader("Chance of Rain 🌧️")
    with st.container(border = True):
        
        pred1, pred2, pred3, pred4, pred5 = st.columns(5)

        with pred1:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=1))
            st.divider()
            st.subheader(f"{df_forecast_weather['chance_of_rain_1h'].round(1)} %")

        with pred2:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=2))
            st.divider()
            st.subheader(f"{df_forecast_weather['chance_of_rain_2h'].round(1)} %")

        with pred3:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=3))
            st.divider()
            st.subheader(f"{df_forecast_weather['chance_of_rain_3h'].round(1)} %")

        with pred4:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=4))
            st.divider()
            st.subheader(f"{df_forecast_weather['chance_of_rain_4h'].round(1)} %")

        with pred5:
            st.subheader(df_forecast_weather['datetime'] + timedelta(hours=5))
            st.divider()
            st.subheader(f"{df_forecast_weather['chance_of_rain_5h'].round(1)} %")



#-----------------------------------------------------------
#Current 
with Current:
    # Extract the last row for forecast weather data
    df_forecast_weather = df.iloc[-1]

    # Identify columns to exclude
    weather_columns = [col for col in df_forecast_weather.index if col.startswith("weather")]
    no_show_colmns = [col for col in df_forecast_weather.index if col.endswith('h')]
    other_columns = ['wind_degrees', 'hour_sin', 'hour_cos', 'wind_x', 'wind_y']
    non_weather_columns = weather_columns + no_show_colmns + other_columns

    # Drop the excluded columns from the row
    df_forecast = df_forecast_weather.drop(non_weather_columns)
    row_data = df_forecast

    # Streamlit UI
    st.title("Grid Display for Weather Forecast")

    # Define the number of columns per row
    columns_per_row = 4

    # Map original column names to user-friendly names and retrieve units using the `show` DataFrame
    keys = [
        f"{show.loc[col, 'User-Friendly Names']} ({show.loc[col, 'Units']})"
        if col in show.index else col
        for col in row_data.index
    ]
    values = list(row_data.values)  # Extract values

    for i in range(0, len(keys), columns_per_row):
        cols = st.columns(columns_per_row)

        for j, col in enumerate(cols):
            if i + j < len(keys):
                key = keys[i + j]
                value = values[i + j]
                background_color = "#f9f9f9" if (i // columns_per_row) % 2 == 0 else "#e8e8e8"

                with col:
                    st.markdown(
                        f"""
                        <div style="border-radius: 10px; padding: 10px; margin: 5px; background-color: {background_color}; text-align: center;">
                            <h4 style="margin: 0; color: #333;">{key}</h4>
                            <p style="font-size: 20px; margin: 5px 0; color: #555;"><strong>{value}</strong></p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
