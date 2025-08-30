import streamlit as st
import requests 
import pandas as pd

st.set_page_config(page_title="Weather App", layout='wide')

st.title("🌤️" 'Live Weather App')


api_key = 'a9fc986668504355b03105930252908'

base_url ='http://api.weatherapi.com/v1/current.json'


st.sidebar.header("⚙️" 'Settings')

unit = st.sidebar.selectbox("Temperature Unit :", ['Celsius', 'Fehrenheit'])

days = st.sidebar.slider("📅" 'Forecast days', min_value= 1, max_value= 7, value = 3)

show_wind = st.sidebar.checkbox('Show Wind speed', value = False)

show_humidity = st.sidebar.checkbox('Show Humidity', value = False)

city = st.text_input("🏙️"'Enter City Name:')

if st.button(" 🔍 "'Get Weather') and city:

    url = f'{base_url}/forecast.json?key={api_key}&q={city}&days={days}&aqi=no'
    

    r = requests.get(url)

    if r.status_code == 200:

        data = r.json()

        loc = data['location']['name']
        country = data['location']['country']
        temp = data['current']['temp_c'] 
        cond = data['current']['condition']['text']
        icon = 'https:'+ data['current']['condition']['icon']
        humidity = data['current']['humidity']
        wind = data['current']['wind_kph']

        if unit == "Celsius":
            temp = data['current']['temp_c']
        else:
            temp = data['current']['temp_f']

        st.subheader(f'{loc}, {country}')
        st.image(icon,width=90)

        col1,col2 = st.columns(2)

        with col1:
            st.write(f'🌡️  temperature:{temp} {unit[0]}')

        with col2:
            st.write(f' ⛅Condition: {cond}')


        if show_humidity:
            st.write(f'💧Humidity: {humidity}%')

        if show_wind:
            st.write(f'💨 Wind Speed: {wind} kph')

        st.markdown('-----')

        st.header(f'📅 {days} Days Forecast')

        forecast_day = data['forecast']['forecastday']

        # Collect report data
        report_data = []

        for day in forecast_day:
            date = day['date']
            if unit == 'Celsius':
                min_temp = day['day']['mintemp_c']
                max_temp = day['day']['maxtemp_c']

            else:
                min_temp = day['day']['mintemp_f']
                max_temp = day['day']['maxtemp_f']

            condition = day['day']['condition']['text']
            icon_url = 'http:' + day['day']['condition']['icon']


            col1,col2,col3,col4 = st.columns([2,2,2,2])

            with col1:
             st.write(f'📆  {date}')

            with col2:
             st.image(icon_url, width = 50)

            with col3:
             st.write(f'🌡️ Min:{min_temp} {unit[0]}')

            with col4:
             st.write(f'🔥  Max:{max_temp} {unit[0]}')

            st.write(f'🌦️ {condition}')

            st.markdown('-----')

              # Append to report data
            report_data.append({
                "Date": date,
                "Min Temp": f"{min_temp} {unit[0]}",
                "Max Temp": f"{max_temp} {unit[0]}",
                "Condition": condition
            })

        # Convert report to DataFrame
        df_report = pd.DataFrame(report_data)

        # Save as CSV
        csv = df_report.to_csv(index=False).encode('utf-8')

        # Download button
        st.download_button(
            label="⬇️ Download Forecast Report (CSV)",
            data=csv,
            file_name=f"{city}_forecast_report.csv",
            mime="text/csv"
        )

        


