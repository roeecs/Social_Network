import json
import random
import requests

BASE_URL = "http://localhost:8000/"
USERS_URL = BASE_URL + "users/"
LOGIN_URL = BASE_URL + "api/token/"
RFRSH_URL = LOGIN_URL + "refresh/"
POST_UP_URL = BASE_URL + "post/"
LIKE_URL = BASE_URL + "like/"


class Bot:

    def __init__(self, path):
        with open(path, 'r') as config_file:
            cfg = json.loads(config_file.read())

        self.number_of_users = cfg['number_of_users']
        self.max_post_per_user = cfg['max_posts_per_user']
        self.max_likes_per_user = cfg['max_likes_per_user']
        self.username_prefix = cfg['username_prefix']
        self.password_prefix = cfg['password_prefix']
        self.users = []

    def run(self):
        self.users_signup()
        self.users_upload_posts()
        self.likes_manager()

    def users_signup(self):
        for i in range(self.number_of_users):
            user_fields = {"username": self.username_prefix+str(i),
                           "password": self.password_prefix+str(i)}
            requests.post(USERS_URL, data=user_fields)
            self.users.append(user_fields)

    def users_upload_posts(self):
        for i in range(self.number_of_users):
            r = random.randint(0, self.max_post_per_user)
            self.users[i]['num_posts'] = r
            self.users[i]['num_of_0_likes_post'] = r
            self.users[i]['posts'] = []
            ac_tk, rf_tk = self.login(i)
            for j in range(r):
                content = f"this is post #{j+1} made by {self.users[i]['username']}."
                post_id, ac_tk, rf_tk = self.logged_in_action({'content': content},
                                                           ac_tk, rf_tk, True)
                self.users[i]['posts'].append([post_id, 0])   # the zero indicates the current num of likes

    def login(self, i):
        user_fields =  {"username": self.users[i]['username'],
                        "password": self.users[i]['password']}
        resp = requests.post(LOGIN_URL, data=user_fields)
        tokens = json.loads(resp.content)
        return tokens['access'], tokens['refresh']

    def logged_in_action(self, data, ac_tk, rf_tk, is_post):
        url = POST_UP_URL if is_post else LIKE_URL
        headers = {"Authorization": "Bearer " + ac_tk}
        resp = requests.post(url, headers=headers, data=data)
        resp_body = json.loads(resp.content)

        if "code" in resp_body:
            if resp_body["code"] == "token_not_valid":
                resp = requests.post(RFRSH_URL, data={"refresh": rf_tk})
                resp_body = json.loads(resp.content)
                ac_tk = resp_body['access']
                return self.logged_in_action(data, ac_tk, rf_tk, is_post)

        if "post_id" in resp_body:
            return resp_body["post_id"], ac_tk, rf_tk

    def likes_manager(self):
        self.users = sorted(self.users, key=lambda k: k['num_posts'], reverse=True)
        likeable_users_lst = [j for j in range(self.number_of_users) if self.users[j]['num_posts'] != 0]
        for i in range(self.number_of_users):
            if i in likeable_users_lst:
                likeable_users_lst.remove(i)

            ac_tk, rf_tk = self.login(i)
            i_user_likes = []   #   to make sure no post is liked twice by the Ith user
            while len(i_user_likes) < self.max_likes_per_user and likeable_users_lst:
                j = likeable_users_lst[random.randint(0,len(likeable_users_lst)-1)]
                t = random.randint(0, len(self.users[j]['posts'])-1)
                p = self.users[j]['posts'][t]
                if (j, p[0]) in i_user_likes:
                    continue
                self.logged_in_action({'post_id': p[0]}, ac_tk, rf_tk, False)
                if p[1] == 0:
                    self.users[j]['num_of_0_likes_post'] -= 1
                    if self.users[j]['num_of_0_likes_post'] == 0:
                        likeable_users_lst.remove(j)
                self.users[j]['posts'][t][1] += 1
                i_user_likes.append((j, p[0]))

            if self.users[i]['num_of_0_likes_post'] != 0:
                likeable_users_lst.append(i)


if __name__ == '__main__':
    bot = Bot('bot_config.json')
    bot.run()

