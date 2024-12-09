import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import pickle

# Streamlit Configuration
st.set_page_config(page_title='Real Estate Analytics', layout='wide')
st.title('Real Estate Analytics Dashboard')

# Load Data
new_df = pd.read_csv('datasets/data_viz1.csv')
feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))

# Sidebar for Navigation
st.sidebar.title("Navigation")
visualization_option = st.sidebar.selectbox(
    "Select Visualization",
    [
        "GeoMap: Sector Price per Sqft",
        "Features WordCloud",
        "Area vs Price",
        "BHK Pie Chart",
        "BHK Price Comparison",
        "Price Distribution by Property Type"
    ]
)

# GeoMap Visualization
if visualization_option == "GeoMap: Sector Price per Sqft":
    st.header("GeoMap: Sector-wise Price per Sqft")
    
    # Adding "Overall" option
    sector_options = ['Overall'] + new_df['sector'].unique().tolist()
    selected_sectors = st.sidebar.multiselect(
        "Select Sectors (select 'Overall' to include all)", sector_options, default=['Overall']
    )
    
    # Filtering data based on selection
    if 'Overall' in selected_sectors:
        filtered_df = new_df
    else:
        filtered_df = new_df[new_df['sector'].isin(selected_sectors)]
    
    # Group data for GeoMap
    group_df = filtered_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'Latitude', 'Longitude']].mean()
    
    # Create the GeoMap
    fig = px.scatter_mapbox(
        group_df,
        lat="Latitude",
        lon="Longitude",
        color="price_per_sqft",
        size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=10,
        mapbox_style="open-street-map",
        hover_name=group_df.index
    )
    
    # Display the GeoMap
    st.plotly_chart(fig, use_container_width=True)


# Features WordCloud
elif visualization_option == "Features WordCloud":
    st.header("Features WordCloud")
    wordcloud = WordCloud(
        width=800, height=800, background_color='white',
        stopwords=set(['s']), min_font_size=10
    ).generate(feature_text)
    
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    st.pyplot()

# Area vs Price Visualization
elif visualization_option == "Area vs Price":
    st.header("Area vs Price")
    property_type = st.selectbox("Select Property Type", ['flat', 'house'])
    
    filtered_data = new_df[new_df['property_type'] == property_type]
    fig1 = px.scatter(
        filtered_data, x="built_up_area", y="price",
        color="bedRoom", title=f"Area vs Price for {property_type.capitalize()}"
    )
    st.plotly_chart(fig1, use_container_width=True)

# BHK Pie Chart
elif visualization_option == "BHK Pie Chart":
    st.header("BHK Distribution")
    sector_option = st.selectbox("Select Sector", ['Overall'] + new_df['sector'].unique().tolist())
    
    if sector_option == "Overall":
        fig2 = px.pie(new_df, names='bedRoom', title="Overall BHK Distribution")
    else:
        fig2 = px.pie(new_df[new_df['sector'] == sector_option], names='bedRoom', title=f"BHK Distribution in {sector_option}")
    st.plotly_chart(fig2, use_container_width=True)

# BHK Price Comparison
elif visualization_option == "BHK Price Comparison":
    st.header("BHK Price Comparison")
    temp_df = new_df[new_df['bedRoom'] <= 4]
    fig3 = px.box(temp_df, x='bedRoom', y='price', title='Price Range by BHK')
    st.plotly_chart(fig3, use_container_width=True)

# Price Distribution by Property Type
elif visualization_option == "Price Distribution by Property Type":
    st.header("Price Distribution by Property Type")
    
    # Set Matplotlib backend
    matplotlib.use('Agg')
    
    fig4, ax = plt.subplots(figsize=(10, 6))
    sns.kdeplot(new_df[new_df['property_type'] == 'house']['price'], label='House', fill=True, ax=ax)
    sns.kdeplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', fill=True, ax=ax)
    
    ax.legend()
    ax.set_xlabel("Price")
    ax.set_ylabel("Density")
    ax.set_title("Price Distribution by Property Type")
    st.pyplot(fig4)
