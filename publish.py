from mastodon import Mastodon

m = Mastodon(client_secret='put secret here', access_token='put access token here', api_base_url='https://mastodon.example.com')


pic = m.media_post(media_file="co2.png")

m.status_post("Here is a 24 hour reading of the CO2 levels", media_ids=pic)
