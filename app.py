import asyncio
import base64
import streamlit as st
from datetime import datetime
from pathlib import Path
from PIL import Image

# Set the page title and icon and set layout to "wide" to minimise margains
st.set_page_config(page_title="Grand Tourney", page_icon=":medal:")

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )

async def countdown(container: st.delta_generator.DeltaGenerator):
    # Function to do a running countdown until a given date, and output results to a container

    # :param container: The container to output the time to
    # :type container: st.delta_generator.DeltaGenerator

    # Run infinitely
    while True:
        # Calculate the timedelta between a given date, and now.
        time_diff = datetime.strptime("11/18/25 09:00:00", '%m/%d/%y %H:%M:%S') - datetime.now()
        # Find the total number of seconds until the given date
        total_seconds = int(time_diff.seconds)
        # Calculate how many hours there are, and how many seconds are left
        hours, remainder = divmod(total_seconds, 3600)
        # Calculate the number of minutes, and the remaining seconds
        minutes, seconds = divmod(remainder,60)

        # Create markdown for the container
        container.markdown(
            f"""
            <p class="time">
                {time_diff.days}:{hours}:{minutes}:{seconds}
            </p>
            """, unsafe_allow_html=True)
        # Wait for one second to update
        r = await asyncio.sleep(1)

# Add styling to the countdown
st.markdown(
    """
    <style>
    .time {
        font-size: 60px !important;
        font-weight: 500 !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

img_path = Path(__file__).parents[0]
logo_img = Image.open(f"{img_path}/Images/Logo.jpg")
add_bg_from_local(f"{img_path}/bg.jpg")

def main():
    with st.sidebar:
        st.subheader("Submit Results!")

        name = st.selectbox(
            "Who are you?",
            ("Khorne", "Nurgle", "Tzeentch", "Slaanesh", "The Great Horned Rat"),
        )

        result = st.radio(
            "What was your result?",
            ("Victory", "Defeat"),
        )

        vp = st.text_input(
            "How many victory points did you score?"
        )



    with st.container():
        st.subheader("Welcome one and all to")
        st.title("Grand Tourney of Chaos Divided!")
        st.image(logo_img)

    st.markdown("<h2 style='text-align: center;'>Day:Hours:Minutes:Seconds until the clash!</h2>", unsafe_allow_html=True)
    # Create a container to store the timer
    countdown_container = st.empty()

    asyncio.run(countdown(countdown_container))

if __name__ == "__main__":
    main()