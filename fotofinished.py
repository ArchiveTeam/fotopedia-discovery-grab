'''Get fotopedia.com URLs.'''
import io
import itertools
import re
import requests
import sys


USER_ARTICLE_CONTRIB = 'http://www.fotopedia.com/users/{0}/best_contributed_articles/query'
USER_PHOTOS = 'http://www.fotopedia.com/users/{0}/last_photos/query'
USER_FOLLOWERS = 'http://www.fotopedia.com/users/{0}/all_followers/query'
USER_FOLLOWING = 'http://www.fotopedia.com/users/{0}/all_following/query'
USER_ALBUMS = 'http://www.fotopedia.com/users/{0}/all_albums/query'
USER_DRAFTS = 'http://www.fotopedia.com/apps/reporter/users/{0}/drafts/query?sort=date'
USER_STORIES = 'http://www.fotopedia.com/apps/reporter/users/{0}/published/query?sort=date'


default_headers = {'User-Agent': 'ArchiveTeam'}


def main():
    username = sys.argv[1]
    output_filename = sys.argv[2]
    print('Username:', username)

    items = itertools.chain(
        paginate_user(USER_ARTICLE_CONTRIB, username),
        paginate_user(USER_PHOTOS, username),
        paginate_user(USER_FOLLOWERS, username),
        paginate_user(USER_FOLLOWING, username),
        paginate_user(USER_ALBUMS, username),
        paginate_user(USER_DRAFTS, username),
        paginate_user(USER_STORIES, username),
    )

    with io.open(output_filename, 'w', encoding='utf8') as f:
        for item in sorted(items):
            f.write(u'{0}|{1}\n'.format(item[0], item[1]))


def paginate_user(template, username):
    print('Grabbing', template, username)

    for offset in itertools.count(step=100):
        print('Offset:', offset)

        response = requests.get(
            template.format(username),
            headers=default_headers,
            params={'offset': offset, 'limit': 100}
            )

        doc = response.json()

        if not doc['items']:
            break

        for item in doc['items']:
            if not item:
                continue

            yield item['_klass'], item['_id']

        remain = doc['totalNumberOfItems'] - offset
        print('Remain:', remain)

if __name__ == '__main__':
    main()
