import redis

def Test():
    r = redis.Redis(host='localhost', port=6379, db=0)
    aa = r.set('foo', 'bar')
    print(aa)
