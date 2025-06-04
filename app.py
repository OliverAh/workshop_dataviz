import pandas as pd
import plotly.express as px
import streamlit as st

st.title('Interact with Gapminder Data')

df = pd.read_csv('Data/gapminder_tidy.csv')

metric_labels = {
    'gdpPercap': 'GDP per Capita',
    'lifeExp': 'Life Expectancy',
    'pop': 'Population'
}

def format_metric(metric_raw:str) -> str:
    return metric_labels[metric_raw]

continent_list = list(df['continent'].unique())
metric_list = list(df['metric'].unique())
countries_in_continent_dict = df.groupby('continent')['country'].unique().to_dict()
years_in_continent_dict = df.groupby('continent')['year'].unique().to_dict()

with st.sidebar:
    st.subheader('Configure the plot')
    continent = st.selectbox(label='Choose a continent',
                             options=continent_list)
    metric = st.selectbox(label='Choose a metric',
                          options=metric_list,
                          format_func=format_metric)
    countries = st.multiselect(
        label="What countries should be plotted?",
        options=countries_in_continent_dict[continent],
        default=countries_in_continent_dict[continent],
    )

    years = st.multiselect(
        label="What years should be plotted?",
        options=years_in_continent_dict[continent],
        default=years_in_continent_dict[continent],
    )

    is_show_dataframe = st.checkbox(label='Show DataFrame', value=True)

query = f'continent == "{continent}" & metric == "{metric}"'

df_filtered = df.query(query)


title = f'{metric_labels[metric]} for countries in {continent}'

fig = px.line(df_filtered, 
              x='year', 
              y='value', 
              color='country', 
              title=title, 
              labels={'value': metric_labels[metric], 'year': 'Year'}
)


st.markdown(
    """
    This line chart displays different metrics over time for countries in different continents, based on the Gapminder dataset.
    Use the legend to highlight specific countries and explore trends from year to year.
    """
)

st.plotly_chart(fig, use_container_width=True)

if is_show_dataframe:
    st.markdown(
        """
        The following Dataframe was used to generate the chart above.
        """
    )

    st.dataframe(df_filtered, use_container_width=True)
