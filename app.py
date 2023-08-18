import os
import json
import streamlit as st
import modal
# import time

episodesPath = "episodes/"

def fetch_from_modal(rss_url):
    f = modal.Function.lookup("corise-podcast-project", "process_podcast")
    output = f.call(rss_url, '/content/podcast/')
    # For local testing without fetching from modal
    # output = {
    #   "podcast_details": {
    #     "podcast_title": "Lorem Title",
    #     "episode_title": "Lorem episode",
    #     "episode_image": "https://megaphone.imgix.net/podcasts/35230150-ee98-11eb-ad1a-b38cbabcd053/image/TWIML_AI_Podcast_Official_Cover_Art_1400px.png?ixlib=rails-4.3.1&max-w=3000&max-h=3000&fit=crop&auto=format,compress",
    #     "episode_transcript": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
    #   },
    #   "podcast_summary": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
    #   "podcast_guest": "Not Available",
    #   "podcast_highlights": "",
    #   "podcast_hashtags": "#htg1 #htg1 #htg1 #htg1 #htg1"
    # }
    # time.sleep(5)
    return output


def get_podcast_title_from_file(file_name):
    """Helper function to extract podcast title from a given JSON file."""
    with open(episodesPath+file_name, 'r') as file:
        podcast_data = json.load(file)
    return podcast_data['podcast_details']['podcast_title']


def display_podcast_info_final(podcast_data):
    """Function to display selected podcast information with adjusted design for highlights."""
    # Display podcast and episode titles
    st.header(podcast_data['podcast_details']['podcast_title'])
    st.subheader(podcast_data['podcast_details']['episode_title'])

    # Two columns for displaying podcast details
    col1, col2 = st.columns([0.25, 0.75])

    # Left column
    with col1:
        st.image(podcast_data['podcast_details']
                 ['episode_image'], use_column_width=True)
        # Display hashtags with box styling
        for hashtag in podcast_data['podcast_hashtags'].split():
            st.markdown(
                f"<div style='display: inline-block; padding: 4px 8px; background-color: #f0f0f0; border-radius: 4px; font-size: 12px; color: black;'>{hashtag}</div>", unsafe_allow_html=True)

    # Right column
    with col2:
        st.write("**Summary:**", podcast_data['podcast_summary'])
        st.write("**Guest:**", podcast_data['podcast_guest'])
        # Display highlights as a list
        st.write("**Highlights:**")
        highlights = podcast_data['podcast_highlights'].split(
            '\n\n')  # Splitting based on the provided separator
        for highlight in highlights:
            st.markdown(f"- {highlight.strip()}")

def main():
    st.title("Podcast Episode Information")

    # New Podcast Form Section
    st.subheader("Add a New Podcast")
    with st.expander("Click to expand and add a new podcast"):
        rss_url = st.text_input(
            "Enter RSS URL of a podcast episode (for episodes not yet processed):")
        submit_button = st.button("Submit")

        if rss_url and submit_button:
            # Inform the user to wait
            with st.spinner(f"Fetching {rss_url}. This can take up to 5 minutes..."):
                podcast_data = fetch_from_modal(rss_url)

                # Save the received data to a new JSON file
                filename = f"podcast-{len(os.listdir(episodesPath)) + 1}.json"
                with open(episodesPath+filename, 'w') as file:
                    json.dump(podcast_data, file)

    # Separate section for selected podcast info
    st.write("---")
    st.subheader("Selected Podcast Info")

    # List all available podcast JSON files from root directory and extract titles
    podcast_files = [f for f in os.listdir(episodesPath)]
    podcast_titles = [get_podcast_title_from_file(f) for f in podcast_files]
    selected_podcast_title = st.selectbox(
        "Select a podcast episode:", podcast_titles, index=0)
    selected_podcast_file = podcast_files[podcast_titles.index(
        selected_podcast_title)]

    # Display podcast information when a title is selected
    if selected_podcast_file:
        with open(episodesPath+selected_podcast_file, 'r') as file:
            podcast_data = json.load(file)
            display_podcast_info_final(podcast_data)


if __name__ == "__main__":
    main()
