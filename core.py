from ConfigParser import SafeConfigParser
config = SafeConfigParser()
config.read('discuss.conf')

from redis import Redis
import simplejson as json
class Cache(object):
    def __init__(self):
        self._db = Redis(host=config.get('db', 'host'),
                         port=config.getint('db', 'port'))
    def get(self, k, t=str):
        r = self._db.get(k)
        return t(r) if r!=None else None
    def set(self, k, v):
        return self._db.set(k, v)
    def delete(self, k):
        return self._db.delete(k)
    def set_add(self, k, v):
        return self._db.sadd(k, v)
    def set_remove(self, k, v):
        return self._db.srem(k, v)
    def set_pop(self, k, v):
        return self._db.spop(k, v)
    def set_exist(self, k, v):
        return self._db.sismember(k, v)
    def set_all(self, k):
        return self._db.smembers(k)
_cache = Cache()

class Discuss(object):
    def __init__(self, id, post_id, title, author, email, content, create_time):
        self._id = id
        self._post_id = post_id
        self._title = title
        self._author = author
        self._email = email
        self._content = content
        self._create_time = create_time
    @property
    def id(self):
        return self._id
    @property
    def post_id(self):
        return self._post_id
    @property
    def title(self):
        return self._title
    @property
    def author(self):
        return self._author
    @property
    def email(self):
        return self._email
    @property
    def content(self):
        return self._content
    @property
    def create_time(self):
        return self._create_time

    def to_json(self):
        return json.dumps(
            {'id': self._id,
             'post_id': self._post_id,
             'title': self._title,
             'author': self._author,
             'email': self._email,
             'content': self._content,
             'create_time': self._create_time,
             })

    def serialize(self):
        discuss_header = "discuss:%s:" % self.id
        post_header = "post:%s:" % self.post_id

        _cache.set_add("discuss:ids", self.id)
        _cache.set_add("post:ids", self.post_id)
        _cache.set_add(post_header+"discuss_ids", self.id)
        _cache.set(discuss_header+"post_id", self.post_id)
        _cache.set(discuss_header+"title", self.title)
        _cache.set(discuss_header+"author", self.author)
        _cache.set(discuss_header+"email", self.email)
        _cache.set(discuss_header+"content", self.content)
        _cache.set(discuss_header+"create_time", self.create_time)

    def __exit__(self):
        self.serialize()

    def delete(self, id):
        discuss_header = "discuss:%s:" % self.id
        post_header = "post:%s:" % self.post_id

        _cache.set_remove("discuss:ids", self.id)
        _cache.set_remove("post:ids", self.post_id)
        _cache.set_remove(post_header+"discuss_ids", self.id)
        _cache.delete(discuss_header+"post_id", self.post_id)
        _cache.delete(discuss_header+"title", self.title)
        _cache.delete(discuss_header+"author", self.author)
        _cache.delete(discuss_header+"email", self.email)
        _cache.delete(discuss_header+"content", self.content)
        _cache.delete(discuss_header+"create_time", self.create_time)

    @classmethod
    def create(cls, id, post_id, title, author, email, content, create_time):
        discuss = Discuss(id, post_id, title, author, email, content, create_time)
        discuss.serialize()
        return discuss

    @classmethod
    def ids(cls):
        return _cache.set_all("discuss:ids")

    @classmethod
    def get(cls, id):
        if not _cache.set_exist("discuss:ids", id):
            return None

        return cls(id,
                   _cache.get("discuss:%s:post_id" % id),
                   _cache.get("discuss:%s:title" % id),
                   _cache.get("discuss:%s:author" % id),
                   _cache.get("discuss:%s:email" % id),
                   _cache.get("discuss:%s:content" % id),
                   _cache.get("discuss:%s:create_time" % id))

    @classmethod
    def get_by_post_id(cls, post_id):
        if not _cache.set_exist("post:%s:discuss_ids" % post_id):
            return None
        return map(cls.get, _cache.set_all("post:%s:discuss_ids" % post_id))
   
from flask import Flask, request, Response
from uuid import uuid4
from time import time as now
app = Flask(__name__)

uuidgen = lambda: str(uuid4())

@app.route("/api/hello")
def api_hello():
    return "hello,world"

@app.route("/api/discuss", methods=["POST"])
def api_discuss_post():
    js = request.json
    return _api_discuss_post(js['post_id'],
                             js['title'],
                             js['author'],
                             js['email'],
                             js['content'])

def _api_discuss_post(post_id, title, author, email, content):
    discuss = Discuss.create(uuidgen(), post_id, title, author, email, content, now())
    response = Response(discuss.to_json(), status=200, mimetype="application/json")
    return response

@app.route("/api/discuss/ids", methods=["GET"])
def api_discuss_get_ids():
    ret = _api_discuss_get_ids()
    return Response(json.dumps(_api_discuss_get_ids()), 
                    status=200, 
                    mimetype="application/json")

def _api_discuss_get_ids():
    return [x for x in iter(Discuss.ids())]


@app.route("/api/discuss/<id>", methods=["GET"])
def api_discuss_get(id):
    return _api_discuss_get(id)

def _api_discuss_get(id):
    discuss = Discuss.get(id)
    if discuss == None:
        ret = json.dumps({})
    else:
        ret = discuss.to_json()

    response = Response(ret, status=200, mimetype="application/json")
    return response

@app.route("/api/discuss/post/<id>", methods=["GET"])
def api_discuss_get_by_post_id(id):
    import pdb; pdb.set_trace();
    return Response(json.dumps(_api_discuss_get_by_post_id(id)),
                    status=200,
                    mimetype="application/json")

def _api_discuss_get_by_post_id(id):
    return Discuss.get_by_post_id(id)
