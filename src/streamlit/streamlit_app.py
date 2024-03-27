import streamlit as st
import plotly.express as px
from search_term_fetch import search_term_fetch
from produce_sentiment import produce_sentiment
from plots import violin_plot, likes_post, word_plot




def main():
    st.title("YouTube Comment Sentiment Analysis")

    search_term = st.text_input("Enter a search term:", "")
    # Add a number input widget to get the number of weeks
    num_weeks = st.number_input('Enter the search timeline in weeks from today:', min_value=1, value=1)

    if st.button("Analyze"):
        if search_term:
            with st.spinner('Fetching YouTube data and analysing sentiment...'):
                try:
                    search_term_fetch(search_term, num_weeks)
                    results_df = produce_sentiment(search_term)

                    # Display Plots
                    try:
                        fig1 = violin_plot(results_df, search_term)
                        st.plotly_chart(fig1)  # Use st.pyplot(fig) if it's a matplotlib figure
                    except Exception as e:
                        st.error(f"An error occurred while generating the violin plot: {e}")

                    try:
                        fig2 = likes_post(results_df, search_term)
                        st.plotly_chart(fig2)  # Adjust accordingly if not a plotly figure
                    except Exception as e:
                        st.error(f"An error occurred while generating the likes per comment plot: {e}")
                        
                    try:
                        fig3 = word_plot(results_df, search_term)
                        st.plotly_chart(fig3)  # Adjust accordingly if not a plotly figure
                    except Exception as e:
                        st.error(f"An error occurred while generating the word plot: {e}")
                    
                    st.write(f"Sentiment analysis results for '{search_term}':")
                    st.dataframe(results_df)

                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a valid search term.")

if __name__ == "__main__":
    main()