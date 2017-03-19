
import pika, json, uuid, redis

class Worker:
    '''
    Base class for all workers
    Pass the required queue name for worker to serve to
    Rpc = True enables RPC
    Otherwise, queue implements a basic worker queue - i.e. replies with basic ack
    '''
    def __init__(self, queue_name, no_workers=10):
        self.id = uuid.uuid1()
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
        connection = pika.BlockingConnection()
        channel = connection.channel()

        self.queue = channel.queue_declare(queue= queue_name, durable=True)
        # allow max n request per worker
        channel.basic_qos(prefetch_count=no_workers)

        channel.basic_consume(self.on_request, queue=queue_name)

        print " [.] Awaiting RPC requests : Queue : ", queue_name , " with ", self.id, "\n [.] Ctrl + C to exit"
        channel.start_consuming()



    def execute(self, body):
        print 'parent worker execute called'
        return None

    def on_request(self, ch, method, properties, body):
        response = {}
        try:
            print("\n [->] Received %r" % body)
            dict = json.loads(body)
            response = self.execute(dict)

        except Exception as e:
            response['result'] = False
            response['message'] = str(e)

        print '\n [<-] Response:', response
        ch.basic_publish(exchange='',
                             routing_key=properties.reply_to,
                             properties=pika.BasicProperties(correlation_id=properties.correlation_id),
                             body= json.dumps(response))
        ch.basic_ack(delivery_tag=method.delivery_tag)
