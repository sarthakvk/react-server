from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from users.models import *
from multimedia.models import *
from channels.models import *
from random import randint, choice, sample

fake = Faker()

_users = User.objects.all()
_channels = Channel.objects.all()


def populate_users(populate=50):
    for i in range(populate):
        email = fake.email()
        user = User(
            email=email,
            username=email,
        )
        user.set_password(fake.password())
        user.save()


def populate_channels(populate=50):
    global _users
    for i in range(populate):
        user = choice(_users)
        subscribers = sample(list(_users), randint(1, len(_users)))

        channel = Channel.objects.create(
            owner=user,
            about=fake.text(),
            profile_pic=fake.file_path(),
            name=fake.company(),
        )
        channel.subscribers.set(subscribers)
        channel.save()


def populate_multimedia(populate=100):
    global _channels
    for i in range(populate):
        channel = choice(_channels)
        type = choice(("video", "audio", "picture", "article"))
        model = eval(type.capitalize())
        if type == "video":
            ext = fake.file_path(extension="mp4")
        elif type == "audio":
            ext = fake.file_path(extension="mp3")
        else:
            ext = fake.file_path(extension="png")
        media_obj = model(
            title=fake.text(max_nb_chars=15),
            description=fake.text(),
            channel=channel,
            thumbnail=fake.file_path(extension="png"),
            content=ext,
        )
        if type == "article":
            media_obj.body = fake.text(max_nb_chars=500)
        media_obj.save()


def populate_comments(populate=10):
    global _users
    type = ("video", "audio", "picture", "article")
    for t in type:
        model = eval(t.capitalize())
        _media = model.objects.all()
        for i in _media:
            for j in range(randint(0, populate)):
                user = choice(_users)
                try:
                    reply_to = eval(
                        "choice([choice(Comments.objects.filter({}=i)), None])".format(
                            t
                        )
                    )
                except:
                    reply_to = None
                comment = Comments.objects.create(
                    user=user,
                    message=fake.text(max_nb_chars=randint(10, 30)),
                    reply_to=reply_to,
                )
                if reply_to is None:
                    eval("comment.{}.add(i)".format(t))
                comment.save()


def populate_likes():
    global _users
    type = ("video", "audio", "picture", "article")
    for t in type:
        model = eval(t.capitalize())
        _media = model.objects.all()
        for user in _users:
            like = Likes.objects.create(user=user, val=True)
            eval(
                "like.{}.add(*sample(list(_media), randint(0, len(_media))))".format(t)
            )
            like.save()
            dislike = Likes.objects.create(user=user, val=False)
            eval(
                "dislike.{model}.add(*_media.difference(like.{model}.all()))".format(
                    model=t
                )
            )
            dislike.save()


def populate_saved(populate=10):
    global _users
    type = ("video", "audio", "picture", "article")
    for t in type:
        model = eval(t.capitalize())
        inter = eval("Saved{}".format(t.capitalize()))
        _media = model.objects.all()
        for user in _users:
            if choice([True, False, True]):
                continue
            saved = SavedMedia.objects.create(
                user=user,
            )
            eval("saved.{}.add(*sample(list(_media), randint(0, populate)))".format(t))
            saved.save()
            bulk = []
            for m in eval("saved.{}.all()".format(t)):
                bulk.append(eval("inter({t}=m,saved_to=saved)".format(t=t)))
            inter.objects.bulk_create(bulk)


def populate_tags(N=20):
    try:
        for i in range(N):
            Tags.objects.create(name=fake.word())
    except:
        pass
    type = ("video", "audio", "picture", "article")
    for t in type:
        model = eval(t.capitalize())
        _media = model.objects.all()
        all_tags = list(Tags.objects.all())
        media = list(_media)
        for a in all_tags:
            eval("a.{}.set(sample(media, randint(1, len(media)-1)))".format(t))
            a.save()


def populate_views():
    global _users
    type = ("video", "audio", "picture", "article")
    for t in type:
        model = eval(t.capitalize())
        _media = model.objects.all()
        media = list(_media)
        for user in _users:
            view = Views(user=user)
            view.save()
            eval("view.{}.set(sample(media, randint(1, len(media))))".format(t))
            view.save()


def populate_data(
    default=True,
    users=None,
    channels=None,
    multimedia=None,
    max_comments=None,
    max_saved=None,
):
    if default:
        print("This will take some time")
        confirm = input("Proceed (y/N) ")
        if confirm not in ("y", "Y"):
            return
        print("Creating Users...")
        populate_users()
        print("Creating Channels...")
        populate_channels()
        print("Creating Media...")
        populate_multimedia()
        print("Generating Comments...")
        populate_comments()
        print("Liking Videos...")
        populate_likes()
        print("Adding saved videos...")
        populate_saved()
        print("popolating Tags...")
        populate_tags()
        print("populateing views...")
        populate_views()
    else:
        populate_users(populate=users)
        populate_channels(populate=channels)
        populate_multimedia(populate=multimedia)
        populate_comments(populate=max_comments)
        populate_likes()
        populate_saved(populate=max_saved)
        populate_tags()


class Command(BaseCommand):
    help = "Generate Fake Data"

    def add_arguments(self, parser):
        parser.add_argument("-u", "--users", help="number of users", type=int)
        parser.add_argument("-c", "--channel", help="number of channels", type=int)
        parser.add_argument("-m", "--multimedia", help="number of multimedia", type=int)
        parser.add_argument(
            "-mc", "--max-comment", help="max comments per media", type=int
        )
        parser.add_argument(
            "-ms", "--max-saved", help="max saved medial per user", type=int
        )

    def handle(self, *args, **options):
        try:
            populate_data()
        except:
            raise ValueError
        self.stdout.write(self.style.SUCCESS("Successfully generated fake data"))
