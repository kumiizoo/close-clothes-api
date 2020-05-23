from app.model.role import Role
from app.model.user import User
from app.module.mongodb.mongo_client import MongoDBClient
from app.module.redis.redis_client import RedisClient


def __fetch_api(request_path, request_method):
    mongodb_db = MongoDBClient().get_mongodb()
    mongodb_api = mongodb_db.apis.find_one({'$and': [{'api': request_path}, {'method': request_method}]})
    return mongodb_api


def index():
    redis = RedisClient().get_redis_client()
    redis.incr('hits')
    return 'Hello World! I have been seen %s times.' % redis.get('hits')


def add_user(user_name, role_name):
    user = User(user_name, role_name)
    user_id = user.add_user()
    user.user_id = user_id
    return user


def fetch_user(user_id):
    user = User()
    mongodb_user = user.fetch_user(user_id)
    user.user_id = mongodb_user['user_id']
    user.user_name = mongodb_user['user_name']
    user.role_name = mongodb_user['role_name']
    return user


def add_role(role_name, role_policies):
    role = Role(role_name, role_policies)
    role.add_role()


def fetch_roles():
    role = Role()
    roles = role.fetch_roles()
    return roles


def validate_request_path(request_path, request_method, user_id):
    user = fetch_user(user_id)
    role = Role()
    mongodb_role = role.fetch_role(user.role_name)
    role.role_policies = mongodb_role['role_policies']
    mongodb_api = __fetch_api(request_path, request_method)
    return role.authorize(mongodb_api['role_policy'])
