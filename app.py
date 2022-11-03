import json
from flask import Flask, request
from redis import Redis

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

in_memory_datastore = {
   "1" : {"url":"https://www.tvmaze.com/episodes/1/under-the-dome-1x01-pilot","name":"Pilot","season":1,"number":1,"type":"regular","airdate":"2013-06-24","airtime":"22:00","airstamp":"2013-06-25T02:00:00+00:00","runtime":60,"rating":{"average":7.7},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_landscape/1/4388.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/1/4388.jpg"},"summary":"<p>When the residents of Chester's Mill find themselves trapped under a massive transparent dome with no way out, they struggle to survive as resources rapidly dwindle and panic quickly escalates.</p>","_links":{"self":{"href":"https://api.tvmaze.com/episodes/1"}}},
   "2" : {"url":"https://www.tvmaze.com/episodes/2/under-the-dome-1x02-the-fire","name":"The Fire","season":1,"number":2,"type":"regular","airdate":"2013-07-01","airtime":"22:00","airstamp":"2013-07-02T02:00:00+00:00","runtime":60,"rating":{"average":7.3},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_landscape/1/4389.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/1/4389.jpg"},"summary":"<p>While the residents of Chester's Mill face the uncertainty of life in the dome, panic is heightened when a house goes up in flames and their fire department is outside of the dome.</p>","_links":{"self":{"href":"https://api.tvmaze.com/episodes/2"}}},
   "3" : {"url":"https://www.tvmaze.com/episodes/3/under-the-dome-1x03-manhunt","name":"Manhunt","season":1,"number":3,"type":"regular","airdate":"2013-07-08","airtime":"22:00","airstamp":"2013-07-09T02:00:00+00:00","runtime":60,"rating":{"average":7.1},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_landscape/1/4390.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/1/4390.jpg"},"summary":"<p>When a former deputy goes rogue, Big Jim recruits Barbie to join the manhunt to keep the town safe. Meanwhile, Junior is determined to escape the dome by going underground.</p>","_links":{"self":{"href":"https://api.tvmaze.com/episodes/3"}}},
   "4" : {"url":"https://www.tvmaze.com/episodes/4/under-the-dome-1x04-outbreak","name":"Outbreak","season":1,"number":4,"type":"regular","airdate":"2013-07-15","airtime":"22:00","airstamp":"2013-07-16T02:00:00+00:00","runtime":60,"rating":{"average":7.3},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_landscape/1/4391.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/1/4391.jpg"},"summary":"<p>The people of Chester's Mill fall into a state of panic as an outbreak of meningitis strikes their community, threatening their already depleted medical supplies. Meanwhile, Julia continues to search for answers into her husband's disappearance.</p>","_links":{"self":{"href":"https://api.tvmaze.com/episodes/4"}}},
   "5" : {"url":"https://www.tvmaze.com/episodes/5/under-the-dome-1x05-blue-on-blue","name":"Blue on Blue","season":1,"number":5,"type":"regular","airdate":"2013-07-22","airtime":"22:00","airstamp":"2013-07-23T02:00:00+00:00","runtime":60,"rating":{"average":7.3},"image":{"medium":"https://static.tvmaze.com/uploads/images/medium_landscape/1/4392.jpg","original":"https://static.tvmaze.com/uploads/images/original_untouched/1/4392.jpg"},"summary":"<p>The Chester's Mill residents receive an unexpected visit from their loved ones on the other side. Meanwhile, the community braces for a threat from outside the Dome.</p>","_links":{"self":{"href":"https://api.tvmaze.com/episodes/5"}}},
}

def create_movie_entry(new_movie):
   movie_id = len(in_memory_datastore)
   in_memory_datastore[str(movie_id)] = new_movie
   return new_movie

def update_movie(movie_id, new_movie_attributes):
   lang_getting_update = in_memory_datastore[movie_id]
   lang_getting_update.update(new_movie_attributes)
   redis.set(str(movie_id), json.dumps(lang_getting_update)) 
   return lang_getting_update

# return specific movie by id while caching
# if id have been searched.updated, retrieve from redis
@app.route('/services/<m_id>')
def get_movie(m_id):
   movie_id = str(m_id)
   if redis.get(movie_id):
      redis_obj_as_bytes = redis.get(movie_id)
      redis_as_str = redis_obj_as_bytes.decode("utf-8")
      val = json.loads(redis_as_str)
   else:
      val = in_memory_datastore[m_id]
      redis.set(movie_id, json.dumps(val))  
   return {"status":200, "data": val, "message status": "success"}

# return specific movie using partial name
@app.get('/services')
def list_movies():
   mov_name = request.args.get('name')
   qualifying_data = list(
       filter(
           lambda mn: mov_name in mn['name'],
           in_memory_datastore.values()
       )
   )
   return {"status":200, "data": qualifying_data, "message status": "success"}

# update movie details and cache it to redis
@app.route('/services/<movie_id>', methods=['PUT'])
def movie_route(movie_id):
   if request.method == "PUT":
      return update_movie(movie_id, request.get_json(force=True))
    
   
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

