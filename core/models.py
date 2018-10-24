from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser, PermissionsMixin
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance


STATUS_CHOICES = (
    ('WT', 'Waiting'),
    ('CO', 'Completed'),
    ('IP', 'In Progress'),
    # ('SR', 'Senior'),
)

# BAZAR_CHOICES = ()


class MyProfileManager(BaseUserManager):
    def create_user(self, mobile, password=None):
        """
        Creates and saves a User with the given mobile.
        """
        if not mobile:
            raise ValueError('Users must have mobile')

        user = self.model(
            mobile=mobile,
            password=password,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            mobile=mobile,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Date(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Profile(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=15, unique=True)
    # name =
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'mobile'
    objects = MyProfileManager()


class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Request(Date):
    title = models.CharField(max_length=70)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    dscr = models.CharField(max_length=200)
    # bazar = models.CharField(max_length=50)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='WT')
    # count = models.IntegerField()
    # price = models.IntegerField()
    # deadline = models.DateField()
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    def __str__(self):
        return self.title

    # def sum(self):
    #     return self.price*self.count


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

# class MPTTMeta:

# class Image(models.Model):
#     req = models.ForeignKey(Request, on_delete=models.CASCADE)
#
# class Message(models.Model):
#     req = models.ForeignKey(Request, on_delete=models.CASCADE)

# class Bazar(models.Model):
#     name = models.CharField(max_length=30)

class Seller(models.Model):
    name = models.CharField(max_length=50, unique=True)
    rating = models.IntegerField(default=0)
    feedbacks_number = models.IntegerField(default=0)
    # shop = models.IntegerField()
    # bazar =
    # subscription =
    # billing history =
    # payment information =
    # points =
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)
    # photo =
    tag = models.ManyToManyField(Tag)

    def get_rating(self):
        return self.rating/self.feedbacks_number

    def rate(self, score):
        self.rating += score
        self.feedbacks_number += 1

    def __str__(self):
        return  self.name
    # def set_photo(self):


class Feedback(models.Model):
    message = models.TextField(max_length=500)
    # media =
    score = models.IntegerField()
    sender = models.ForeignKey('User', on_delete=models.CASCADE)
    receiver = models.ForeignKey('Seller',  on_delete=models.CASCADE)


class User(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    # photo =
    # rating = models.DecimalField()

    def __str__(self):
        return self.name



