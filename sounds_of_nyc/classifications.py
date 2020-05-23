import requests

def get_celeb_info(img_url):
  resp = requests.post(
    "https://api.deepai.org/api/celebrity-recognition",
    data={'image': img_url,},
    headers={'api-key': 'c99d825a-1248-48ac-9ed9-035bc6c0ad69'}
  )
  
  resp_json = resp.json()
  info = {
    'confidence': resp_json['output']['celebrities'][0]['confidence'],
    'name': resp_json['output']['celebrities'][0]['name']}
  return info


def get_artist_id(artist_name):
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQDiV6JXLr-wTQ5SWXI4eYJQw19Z_tyOn_GjSzYhjlPc20U22VrOZSsPXShsycbQqcEZIaYIIVCCoGPL-Rf1zp80buvr4SOfpDzNrQc4qap0x_YwTwIpHqRGcdt-gtNf1Efhw2exSkTBzw',
  }
  params = (
      ('q', artist_name),
      ('type', 'artist'),
  )
  response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)
  return response.json()['artists']['items'][0]['id']


def get_albums_list(artist_id):
  headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQDiV6JXLr-wTQ5SWXI4eYJQw19Z_tyOn_GjSzYhjlPc20U22VrOZSsPXShsycbQqcEZIaYIIVCCoGPL-Rf1zp80buvr4SOfpDzNrQc4qap0x_YwTwIpHqRGcdt-gtNf1Efhw2exSkTBzw',
  }
  params = (
      ('include_groups', 'single,appears_on'),
      ('market', 'ES'),
      ('limit', '20'),
      ('offset', '5'),
  )
  response = requests.get('https://api.spotify.com/v1/artists/' + artist_id + '/albums', headers=headers, params=params).json()
  albums = []
  for item in response['items']:
    albums.append(item['name'])
  return ', '.join(albums)
  

def get_albums_list_str(img_url):
  celeb_info = get_celeb_info(img_url)
  if celeb_info['name'] != 'unknown':
    artist_id = get_artist_id(celeb_info['name'])
    return get_albums_list(artist_id)
  else:
    return 'unknown'