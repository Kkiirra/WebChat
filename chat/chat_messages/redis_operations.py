import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


def save_channel_name(user_id, channel_name):
    redis_client.hset('user_channels', user_id, channel_name)


def get_channel_name(user_id):
    user_channel_name = redis_client.hget('user_channels', user_id)
    if user_channel_name is not None:
        return user_channel_name.decode('utf-8')
    else:
        return None


def delete_channel_name(user_id):
    return redis_client.hdel('user_channels', user_id)


def get_all_channel_names(user_channels):
    all_channels = redis_client.hgetall(user_channels)

    decoded_channels = {}
    for key, value in all_channels.items():
        decoded_key = key.decode('utf-8')
        decoded_value = value.decode('utf-8')
        decoded_channels[decoded_key] = decoded_value
    return decoded_channels


print(get_all_channel_names('user_channels'))
