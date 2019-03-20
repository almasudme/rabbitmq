from pyrabbit.api import Client

cl = Client('100.200.250.255:15672', 'user', 'password',5)
cl.is_alive()


print(f"queue depth for queue_name :\t {cl.get_queue_depth('vhost', 'queue_name')}") 
