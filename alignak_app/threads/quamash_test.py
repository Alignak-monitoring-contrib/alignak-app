#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json


from alignak_backend_client.client import Backend

backend = Backend('http://demo.alignak.net:6000')
backend.login('admin', 'admin')

endpoints = [
    'host',
    'service',
    'user',
    'history'
]

@asyncio.coroutine
def event_handler(endpoint, stop=False):
    print('Running on endpoint %s' % endpoint)
    params = {
        'projection': json.dumps({'_id': 1})
    }
    data = backend.get_all(endpoint, params=params)
    print("Collected data: (%d) %s" % (len(data['_items']), data['_items']))

    # Close app
    # if stop:
    #     print('stopping the loop')
    #     loop.stop()


# if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    #
    #
    # try:
    #     for endpoint in endpoints:
    #         loop.call_soon(event_handler, loop, endpoint, loop)
    #         print('starting event loop')
    #         # loop.call_soon(functools.partial(event_handler, endpoint, loop, stop=True))
    #
    #         loop.run_forever()
    # finally:
    #     print('closing event loop')
    #     loop.close()

if __name__ == '__main__':
    my_event_loop = asyncio.get_event_loop()
    try:
        for endpoint in endpoints:
            print('task creation started')
            task_obj = my_event_loop.create_task(event_handler(endpoint))
            my_event_loop.run_until_complete(task_obj)
    finally:
        my_event_loop.close()

    # print("The task's result was: {}".format(task_obj.result()))