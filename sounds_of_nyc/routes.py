import requests
from sounds_of_nyc import sounds_of_nyc
from flask import render_template, request

@sounds_of_nyc.route('/')
def index():
    return render_template("index.html")

@sounds_of_nyc.route('/', methods=['POST'])
def index_post():
    img_url = str(request.form['link'])
    celeb_info = get_celeb_info(img_url)
    name = celeb_info['name']
    probability = celeb_info['confidence']
    if name != 'unknown':
        artist_id = get_artist_id(name)
        albums = get_albums_list(artist_id)
    else:
        albums = 'None'

    return render_template("albums.html",
        albums=albums,
        img_url=img_url,
        artist_name=name,
        confidence=probability)

@sounds_of_nyc.route('/res')
def search_res(search):
    res = [search]
    return res


# Classification stuff
token = 'BQA1-EvGmBLh4ftQO_Zs7KEwI5dc3Wq_PQSlF58fngUsdD-pfrvZalmgVPDCdR6rE4aWbNjcbAQn_MvQR9lETcnV4a5-wC13rvkvHpXvHCombRCpMiVu07_mWmroWPjIMEn3zTA0lxeBsw'

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
    'Authorization': 'Bearer ' + token,
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
    'Authorization': 'Bearer ' + token,
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