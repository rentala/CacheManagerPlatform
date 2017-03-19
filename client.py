
import pika, json, uuid



class cacheClient():
    def __init__(self):
        self.connection = pika.BlockingConnection()

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)
        self.id = uuid.uuid4()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, message, queue_name):
        message = json.dumps(message)
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange='',
                                   routing_key=queue_name,
                                   properties=pika.BasicProperties(
                                       reply_to=self.callback_queue,
                                       correlation_id=self.corr_id,
                                       delivery_mode=2,  # make message persistent
                                   ),
                                   body=message)
        print(" [.] Queue %r " % queue_name)
        print(" [.] Sent %r " % message)
        while self.response is None:
            self.connection.process_data_events()

        print(" [.] Recived %r " % self.response)
        return json.loads(self.response)

    def insert(self, key, val, exp=5000):
        '''
        Insert key value into the cache
        :param key: key - must be string
        :param val: any
        :param exp: int in milliseconds
        :return: boolean
        '''
        dic = {}
        dic['key'] = key
        dic['val'] = val
        dic['exp'] = exp
        return str(self.call(dic, 'insert_queue')['result'])

    def get(self, key):
        '''
        Gets the corresponding value
        :param key: key - must be string
        :return: value - object/primitive
        '''
        dic = {}
        dic['key'] = key
        return str(self.call(dic, 'get_queue')['result'])

