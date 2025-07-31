import streamlit as st

# -----------------------

st.set_page_config(page_title="About", layout="centered")
st.title("About")
st.markdown("""
            This application is designed to help you find the nearest petrol station to your chosen location,
            and compare the prices around you so that you can make a more informed decision!

            The application takes in your selected location, radius, desired fuel type, fuel consumption, and
            litres to fill in order to find you the best deals. The app takes things a step further by finding 
            the petrol stations within your chosen radius, and then calculating the distance between your location
            and the petrol station to take into account how much fuel is used to travel to each petrol station - 
            this is then factored into the final decision!
            """)

st.subheader("Why did I make this app?")
st.markdown("""
           One day I was sitting with my parents in George, who were visiting for my
            sister's 30th birthday. We were sitting in a Vida at Garden Route mall, trying to figure out where to fill
            petrol. None of us were particularly familiar with George (this was all our first time visting), so we 
            didn't quite know the lay of the land just yet. 

            My dad commented that different petrol stations they had been to while in George (and even around Cape Town)
            had dispalyed different prices for their fuel, and he didn't know which line of petrol stations had the
            best prices. It got me to thinking - surely there should be some sort of application that can identify
            petrol stations around you (similar to how Google Maps or Apple Maps would), with the added advantage of 
            factoring in petrol prices for each fuel type, as well as how much fuel you'd use travelling there.

            This is all just a long-winded way to say, a random conversation and a bored mind led to this.
            """)


st.subheader("So what about the additional shops aspect?")
st.markdown("""
           That was also borne of this trip to George. Since we went by car, it was about a 4-5 hour drive to and
            from Cape Town - meaning, we needed to stop along the way. 

            It's surprisingly difficult to find information on where the larger petrol stations with food places attached
            (such as Engen 1stops or Shell Ultra Cities) are along the main roads such as the N1 or N2. That, or we just took
            a really bad route. I spent a lot of time on Google and Apple Maps trying to figure out where would be best to
            stop along our route home for lunch. Some information is outdated, some just simply is non-existent. I had
            to rely plently on looking at street view and hoping that the images were somewhat still representative of
            the way we'd find the petrol station.

            I figured, again, an app that includes this kind of information about petrol stations might be useful for
            travellers planning road trips.
            """)
