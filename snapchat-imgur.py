from argparse import ArgumentParser
from datetime import datetime

from imgurpython import ImgurClient
from snapchat_bots import SnapchatBot


class ImgurBot(SnapchatBot):
    def __init__(self, username, password, imgur_id, imgur_secret, callback):
        SnapchatBot.__init__(self, username, password)
        self.callback = callback
        self.imgclient = ImgurClient(imgur_id, imgur_secret)

    def on_snap(self, sender, snap):
        """ Upload snaps anonymously to imgur, and pass the response to callback """
        config = {
                'title': 'Snap from {0}'.format(sender),
                'description': 'Sent on {0}'.format(datetime.now()),
        }
        image = self.imgclient.upload_from_path(snap.file.name, config=config, anon=True)
        self.callback(sender, image)

    def on_friend_add(self, friend):
        """ Add anyone who adds me """
        self.add_friend(friend)

    def on_friend_delete(self, friend):
        """ Delete anyone who deletes me """
        self.delete_friend(friend)

if __name__ == '__main__':
    parser = ArgumentParser("Imgur Bot")
    parser.add_argument(
            '-u', '--username', required=True, type=str,
            help="Snapchat username to run the bot on")
    parser.add_argument(
            '-p', '--password', required=True, type=str,
            help="Snapchat password")
    parser.add_argument(
            '-i', '--imgurid', required=True, type=str,
            help="Imgur client ID")
    parser.add_argument(
            '-s', '--imgursecret', required=True, type=str,
            help="Imgur client secret")

    args = parser.parse_args()

    def print_url(sender, image):
        print('Uploaded snap from {0} to {1}.'.format(sender, image['link']))

    bot = ImgurBot(args.username, args.password,
                   args.imgurid, args.imgursecret,
                   print_url)

    bot.listen(timeout=5)
