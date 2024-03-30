import streamlit as st
from datetime import datetime, timedelta, date
from search_term_fetch import search_term_fetch  # Ensure this function accepts start and end dates
from produce_sentiment import produce_sentiment
from plots import violin_plot, likes_post, word_plot, preprocess_and_plot,timeline_plot, country_share


def main():
    st.title("YouTube Comment Sentiment Analysis")

    search_term = st.text_input("Enter a search term:", "")
    start_date = st.date_input("Start date", date.today() - timedelta(days=7))
    end_date = st.date_input("End date", date.today())

    if st.button("Analyse"):
        if not search_term:
            st.error("Please enter a valid search term.")
        elif start_date > end_date:
            st.error("Error: End date must fall after start date.")
        else:
            with st.spinner('Fetching YouTube data and analyzing sentiment...'):
                try:
                    search_term_fetch(search_term, start_date, end_date)
                    results_df = produce_sentiment(search_term)

                    
                    # Display existing plots
                    try:
                        fig1 = violin_plot(results_df, search_term)
                        st.plotly_chart(fig1)
                    except Exception as e:
                        st.error(f"An error occurred while generating the violin plot: {e}")
                    
                    try:
                        fig2 = likes_post(results_df, search_term)
                        st.plotly_chart(fig2)
                    except Exception as e:
                        st.error(f"An error occurred while generating the likes per comment plot: {e}")
                        
                    try:
                        fig3 = word_plot(results_df, search_term)
                        st.plotly_chart(fig3)
                    except Exception as e:
                        st.error(f"An error occurred while generating the word plot: {e}")

                    # Generate and display the world map plot
                    try:
                        world_map_fig = preprocess_and_plot(results_df, search_term)
                        st.plotly_chart(world_map_fig)
                    except Exception as e:
                        st.error(f"An error occurred while generating the world map plot: {e}")
                    
                    try:
                        fig5 = country_share(results_df)
                        st.plotly_chart(fig5)
                    except Exception as e:
                        st.error(f"An error occurred while generating the world map plot: {e}")
                    
                    try:
                        fig4 = timeline_plot(results_df, search_term)
                        st.plotly_chart(fig4)
                    except Exception as e:
                        st.error(f"An error occurred while generating the word plot: {e}")

                    st.write(f"Dataframe results for '{search_term}':")
                    st.dataframe(results_df)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
