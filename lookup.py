from flask import Flask,request, jsonify, render_template
import pika, json, uuid
app = Flask(__name__)


class cacheClient():
    def __init__(self):
        self.connection = pika.BlockingConnection()

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

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
        return json.loads(self.response)

    def insert(self, key, val):
        dic = {}
        dic[key] = val
        return self.call(dic, 'insert_queue')

    def get(self, key):
        dic = {}
        dic['key'] = key
        return self.call(dic, 'get_queue')

cache_client = cacheClient()

@app.route('/get/<_key>', methods=['GET'])
def home(_key):
    r = cache_client.get(_key)
    return jsonify(r)

@app.route('/insert', methods=['POST'])
def posyt_method():
    key = request.form['key']
    value = request.form['value']
    cache_client.insert(key, value)
    return 'done'

@app.route('/', methods=['GET'])
def basic_home():
    return render_template('Index.html')

if __name__ == '__main__':
    app.run()
