

def acestream_link(params):
   url3 = "https://pastebin.com/raw/E1yBvqHa"
   request_headers = []
   request_headers.append ( ["User-Agent" , "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0"] )
   read_url, response_headers = plugintools.read_body_and_headers ( url3 , headers = request_headers )
   url = read_url.strip ()
   matches = re.findall(r'(?s).*?<canal>(.*?)<canal>.*?<id>(.*?)<', url, re.DOTALL )
   for nombre_canal, id in matches:
       
        plugintools.add_item ( action = "resolve_acestream" , title = "[COLOR yellow][B]" + nombre_canal + "[/B][/COLOR]" , plot = id, url="", thumbnail = "https://i.imgur.com/pDh2Gmp.jpg"  , fanart = "https://i.imgur.com/pDh2Gmp.jpg" , folder = False , isPlayable = True )