import time 
from web import get_info_web
from api_livenation import api_livenation

def main():
    # URL of the Live Nation promotion page with all artists
    url = "https://www.livenation.com/promotion/tickettosummer/artists?locationmode=default-all"
    links = get_info_web(url)

    '''Extract artist IDs from the links'''
    ids_list = []
    for _, link in links:
        link = link.replace("https://www.livenation.com/promotion/tickettosummer/artist/", "")
        ids_list.append(link.strip())

    '''Fetch event URLs for each artist'''
    event_link_list = []
    for id_artist in ids_list:
        print(f"Searching events for the artist: {id_artist}")
        link_events = api_livenation(id_artist)
        event_link_list.extend(link_events)
        time.sleep(1) # Avoid hitting the API too quickly

    '''Save the event links to a file named "links.txt".'''
    with open("links.txt", "w", encoding="utf-8") as f:
        for link in event_link_list:
            f.write(link + "\n")



if __name__ == "__main__":
    main()