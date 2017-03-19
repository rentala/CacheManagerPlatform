import worker


class write_worker(worker.Worker):
    def __init__(self):
        worker.Worker.__init__(self, "insert_queue", 1)

    def execute(self, body):
        print body

        self.redis.set(body['key'], body['val'])
        response = {}
        response['result'] = True
        return response

writeworker = write_worker()