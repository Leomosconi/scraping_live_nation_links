import time
import requests


def api_livenation(artist_id: str, max_retries: int = 3, wait: int = 2) -> list:
    '''
    This function queries the Live Nation GraphQL API for a given artist ID and returns a list of event URLs.
    It automatically retries the request up to `max_retries` times in case of errors, waiting `wait` seconds between attempts.
    '''
    url = "https://api.livenation.com/graphql"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0",
        "Accept": "*/*",
        "Accept-Language": "pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3",
        "Referer": "https://www.livenation.com/",
        "x-api-key": "da2-jmvb5y2gjfcrrep3wzeumqwgaq",
        "x-amz-user-agent": "aws-amplify/6.13.1 api/1 framework/2",
        "content-type": "application/json; charset=UTF-8",
        "Origin": "https://www.livenation.com",
    }
    payload = {
        "query": "query PROMOTION_EVENTS($artist_id: String, $dedup: Boolean, $end_date_time: String, $include_genres: String, $market_id: Int, $offset: Int!, $promotion_id: String!, $start_date_time: String, $venue_id: String) {\n  getEvents(\n    filter: {artist_id: $artist_id, dedup: $dedup, end_date_time: $end_date_time, exclude_status_codes: [\"cancelled\", \"postponed\"], image_identifier: \"ARTIST_PAGE_3_2\", include_genres: $include_genres, market_id: $market_id, promotion_id: $promotion_id, start_date_time: $start_date_time, venue_id: $venue_id}\n    limit: 36\n    offset: $offset\n    order: \"ascending\"\n    sort_by: \"start_date\"\n  ) {\n    artists {\n      discovery_id\n      genre\n      name\n      slug\n      tm_id\n    }\n    discovery_id\n    event_date\n    event_date_timestamp_utc\n    event_end_date\n    event_end_date_timestamp_utc\n    event_end_time\n    event_status_code\n    event_time\n    event_timezone\n    genre\n    images {\n      fallback\n      image_url\n    }\n    links {\n      link\n      platform\n    }\n    name\n    presales {\n      end_date_time\n      is_ln_promoted\n      name\n      start_date_time\n    }\n    sales_end_date_time\n    sales_start_date_time\n    similar_event_count\n    slug\n    source\n    tm_id\n    type\n    url\n    venue {\n      discovery_id\n      is_livenation_owned\n      location {\n        address\n        city\n        country\n        state\n      }\n      market_ids\n      name\n      slug\n      tm_id\n      venue_type\n    }\n  }\n}\n",
        "variables": {
            "artist_id": f"{artist_id}",
            "dedup": False,
            "promotion_id": "tickettosummer",
            "offset": 0
        }
    }
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            events = data['data']['getEvents']
            urls = [event['url'] for event in events if 'url' in event]
            return urls
        except Exception as e:
            print(f"Attempt {attempt} failed for {artist_id}: {e}")
            if attempt < max_retries:
                time.sleep(wait)
            else:
                print(f"Failed to fetch events for {artist_id} after {max_retries} attempts.")
                return []