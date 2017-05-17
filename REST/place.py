from twitter_client import get_twitter_oauth_api
api = get_twitter_oauth_api()

query = input('location: ')
places = api.geo_search(query=query, granularity="city")

place_id = places[0].id
print('id is: ', place_id)
