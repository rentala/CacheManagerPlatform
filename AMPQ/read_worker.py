import worker

class read_worker(worker.Worker):
    def __init__(self):
        worker.Worker.__init__(self, "get_queue")

    def execute(self, body):
        response = {}
        print body
        response['result'] = self.redis.get(body['key'])
        return response


readworker = read_worker()