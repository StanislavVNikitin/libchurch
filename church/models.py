from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.

from church.singleton import SingletonModel

class SocialNet(models.Model):
    SOCIALNET_CHOICES = [
        ("fa-telegram", "Telegram"),
        ("fa-whatsapp", "Whatsapp"),
        ("fa-vk", "VK"),
        ("fa-facebook", "Facebook"),
        ("fa-linkedin-in", "LinkedIn"),
        ("fa-odnoklassniki", "OK"),
        ("fa-google-plus-g", "Google+"),
        ("fa-instagram", "Instagram"),
        ("fa-github", "GitHub"),
        ("fa-twitter", "Twitter/X"),
    ]
    social_net = models.CharField(max_length=17, choices=SOCIALNET_CHOICES, blank=True , verbose_name=_('Social network'))
    title =  models.CharField( blank=True,verbose_name=_('Title'), max_length=256)
    url = models.URLField(verbose_name=_('Website url'), blank=True, max_length=256)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Social network')
        verbose_name_plural = _('Social networks')

class SiteSettings(SingletonModel):
    site_url = models.URLField(verbose_name=_('Website url'),blank=True, max_length=256)
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    top_biblia_citation = models.CharField(verbose_name=_('Biblia citation'),blank=True, max_length=256)
    hero_section_image = models.ImageField(upload_to="herosection", blank=True, verbose_name=_('Image hero section'))
    hero_section_title = models.CharField(verbose_name=_('Title hero section'),blank=True, max_length=256)
    hero_scripture_quote = models.CharField(verbose_name=_('Scripture quote'),blank=True, max_length=256)
    upcoming_event_enable = models.BooleanField(default=False, verbose_name=_('About section enable'))
    about_section_enable = models.BooleanField(default=False, verbose_name=_('Upcoming event section enable'))
    about_section_title = models.CharField(verbose_name=_('Title hero section'),blank=True, max_length=256)
    about_section_content = models.TextField(blank=True, verbose_name=_('Content about section'))
    about_section_image = models.ImageField(upload_to="aboutsection", blank=True, verbose_name=_('Image about section'))
    advantage_section_enable = models.BooleanField(default=False, verbose_name=_('Advantage section enable'))
    advantage_max_count = models.IntegerField(default=3,verbose_name=_('Advantage post count'),validators=[MinValueValidator(0), MaxValueValidator(3)])
    sermon_section_enable = models.BooleanField(default=False, verbose_name=_('Sermon section enable'))
    event_section_enable = models.BooleanField(default=False, verbose_name=_('Event section enable'))
    event_max_count = models.IntegerField(default=3,verbose_name=_('Event count'),validators=[MinValueValidator(0), MaxValueValidator(3)])
    donate_section_enable = models.BooleanField(default=False, verbose_name=_('Donate section enable'))
    news_section_enable = models.BooleanField(default=False, verbose_name=_('News section enable'))
    news_post_max_count = models.IntegerField(default=3,verbose_name=_('News post max count'),validators=[MinValueValidator(0), MaxValueValidator(3)])
    contact_section_content = models.TextField(blank=True, verbose_name=_('Contact us content section'))
    google_map_url = models.URLField(verbose_name=_('Google map'),blank=True, max_length=256)
    social_net_link = models.ManyToManyField("SocialNet", blank=True, related_name="sitesettings", verbose_name=_('Social Network'))
    subscribe_section_enable = models.BooleanField(default=True, verbose_name=_('Subscribe section enable'))


    def __str__(self):
        return 'Configuration'

    class Meta:
        verbose_name = _('Configuration')
        verbose_name_plural = _('Configurations')


class Image(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    file = models.ImageField(upload_to="image/%Y/%m/%d/", blank=True, verbose_name=_('Photo'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:image", kwargs={"pk": self.pk})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
        ordering = ["title"]


class Advantage(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    class_name = models.CharField(max_length=50, verbose_name=_('Class name'))
    content = models.TextField(blank=True, verbose_name=_('Content'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:advantage", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Advantage')
        verbose_name_plural = _('Advantages')
        ordering = ["title"]


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ["title"]


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Title'))
    slug = models.SlugField(max_length=50, verbose_name=_('Slug'), unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:tag", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ["title"]

class Pastor(models.Model):
    fullname = models.CharField(max_length=255, verbose_name=_('Full name'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    title_pastor = models.CharField(blank=True,max_length=255, verbose_name=_('Tilte pastor'))
    biography = models.TextField(blank=True, verbose_name=_('Biography'))
    photo = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="pastor",verbose_name=_('Photo'))

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("church:pastor", kwargs={"slug": self.slug})


    class Meta:
        verbose_name = _('Pastor')
        verbose_name_plural = _('Pastors')
        ordering = ["fullname"]


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    author = models.CharField(max_length=150,blank=True, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    photo = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="posts",verbose_name=_('Photo'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name=_('Category'))
    tags = models.ManyToManyField("Tag", blank=True, related_name="posts", verbose_name=_('Tag'))
    gallery = models.ForeignKey("Gallery",blank=True, null=True, on_delete=models.PROTECT, related_name="posts", verbose_name=_('Gallery'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("church:post", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural =  _('Posts')
        ordering = ["-created_at"]

class Sermon(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    author = models.CharField(max_length=150, verbose_name="Автор")
    pastor = models.ForeignKey('Pastor', on_delete=models.CASCADE, related_name="sermons",verbose_name=_('Pastor'))
    content = models.TextField(blank=True, verbose_name=_('Content'))
    data_sermon = models.DateField(verbose_name=_('Date'))
    web_url_sermon = models.URLField(verbose_name=_('Website url'), blank=True, max_length=256)
    file_sermon = models.FileField(upload_to="sermons/%Y/%m/%d/",verbose_name=_('Upload File'))
    photo = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="sermons",verbose_name=_('Photo'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="sermons", verbose_name=_('Category'))
    tags = models.ManyToManyField("Tag", blank=True, related_name="sermons", verbose_name=_('Tag'))
    pin = models.BooleanField(default=False, verbose_name=_('Pin'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:sermon", kwargs={"slug": self.slug})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Sermon')
        verbose_name_plural = _('Sermons')
        ordering = ["title"]

class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    author = models.CharField(max_length=100, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name=_('Content'))
    place_event = models.CharField(max_length=255, verbose_name=_('Place of event'))
    datatime_event = models.DateTimeField(verbose_name=_('DateTime'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    photo = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="events", verbose_name=_('Photo'))
    views = models.IntegerField(default=0, verbose_name=_('Views'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:event", kwargs={"slug": self.slug})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
        ordering = ["title"]


class Gallery(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    image = models.ManyToManyField("Image", blank=True, related_name="galleries", verbose_name=_('Image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:gallery", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')
        ordering = ["title"]

class Donate(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    slug = models.SlugField(max_length=255, verbose_name=_('Slug'), unique=True)
    author = models.CharField(blank=True,max_length=100, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name=_('Content'))
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="donates", verbose_name=_('Category'))
    enddate_donate = models.DateTimeField(blank=True,verbose_name=_('DateTime'))
    donate_sum = models.IntegerField(blank=True,default=0,verbose_name=_('Donate sum'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Publication date'))
    photo = models.ForeignKey('Image', on_delete=models.CASCADE, related_name="donates", verbose_name=_('Photo'))
    deleted = models.BooleanField(default=False, verbose_name=_('Deleted'))

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("church:donate", kwargs={"slug": self.slug})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = _('Donate')
        verbose_name_plural = _('Donates')
        ordering = ["title"]


class MenuTop(models.Model):
    name = models.CharField(verbose_name=_('Name'),max_length=50, unique=True)
    url = models.CharField(verbose_name=_('Url'), max_length=255)
    position = models.PositiveIntegerField(verbose_name=_('Position'), default=1)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name = _('Menu')
        verbose_name_plural = _('Menu')
        ordering = ('position',)