import streamlit as st
from datetime import datetime, timedelta, date
from search_term_fetch import search_term_fetch  # Ensure this function accepts start and end dates
from produce_sentiment import produce_sentiment
from plots import violin_plot, likes_post, word_plot

def main():
    st.title("YouTube Comment Sentiment Analysis")

    search_term = st.text_input("Enter a search term:", "")

    # Add date input for start date
    start_date = st.date_input("Start date", date.today() - timedelta(days=7))
    # Add date input for end date
    end_date = st.date_input("End date", date.today())

    if st.button("Analyze"):
        if not search_term:  # Check if the search term is empty after the button is pressed
            st.error("Please enter a valid search term.")
        elif start_date > end_date:
            st.error("Error: End date must fall after start date.")
        else:
            with st.spinner('Fetching YouTube data and analyzing sentiment...'):
                try:
                    # Assuming the search_term_fetch function now properly uses start_date and end_date
                    # Convert start_date and end_date to the required format within search_term_fetch if necessary
                    search_term_fetch(search_term, start_date, end_date)
                    results_df = produce_sentiment(search_term)  # Ensure this function is implemented correctly
                    
                    # Display plots
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
                    
                    st.write(f"Dataframe results for '{search_term}':")
                    st.dataframe(results_df)

                except Exception as e:
                    st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
