from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Permission


class Departament(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название отдела",)
    description_open = models.TextField(blank=True, default='', max_length=256,
                                        verbose_name="Описание для открытой части", )
    description_close = models.TextField(blank=True, default='', max_length=256,
                                         verbose_name="Описание для закрытой части", )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("testing:detail", kwargs={'pk': self.pk})

    class Meta:
        verbose_name = _("Отдел")
        verbose_name_plural = _("Отделы")


class ProfileManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.password = password
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=255, blank=False, verbose_name="ФИО")
    password = models.CharField(_('password'), max_length=128, default='', blank=True)
    is_staff = models.BooleanField(default=False, verbose_name="Администратор",)
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    public = models.BooleanField(default=False, verbose_name="Общедоступный",
                                 help_text=_('Данный пользователь будет доступен '
                                             'администраторам других отделов.'))
    departament = models.ManyToManyField(Departament, blank=False, verbose_name="Отделы",
                                         help_text=_('Данный пользователь сможет проходить '
                                                     'закрытые тесты выбранных здесь групп.'))
    objects = ProfileManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return '{username}'.format(username=self.username)

    def get_name(self):
        return self.username

    class Meta:
        verbose_name = _("Пользователь")
        verbose_name_plural = _("Пользователи")


@receiver(signal=pre_save, sender=Profile)
def save_profile(sender, instance, signal, **kwargs):
    user = Profile.objects.filter(username=instance.username).first()

    if user is None:
        if instance.password == '':
            instance.set_password(instance.username)
            instance.is_staff = False
        else:
            instance.set_password(instance.password)
    else:
        if instance.password == '':
            instance.set_password(instance.username)
            instance.is_staff = False
        else:
            if user.password == instance.password:
                pass
            else:
                instance.set_password(instance.password)


@receiver(signal=post_save, sender=Profile)
def psave_profile(sender, instance, signal, **kwargs):
    if instance.is_superuser is False:
        perms = ['add_profile', 'delete_profile', 'change_profile', 'view_profile',
                 'add_departament', 'delete_departament', 'change_departament', 'view_departament',
                 'add_test', 'delete_test', 'change_test', 'view_test',
                 'add_question', 'delete_question', 'change_question', 'view_question',
                 'add_answer', 'delete_answer', 'change_answer', 'view_answer',
                 'add_testresult', 'delete_testresult', 'change_testresult', 'view_testresult',
                 'add_result', 'delete_result', 'change_result', 'view_result', ]
        if instance.is_staff:
            for perm in perms:
                permission = Permission.objects.get(codename=perm)
                instance.user_permissions.add(permission)
        else:
            for perm in perms:
                permission = Permission.objects.get(codename=perm)
                instance.user_permissions.remove(permission)


class Test(models.Model):
    name = models.CharField(max_length=256, verbose_name="Название теста",)
    description = models.TextField(verbose_name="Описание теста",)
    time = models.PositiveIntegerField(default="1", verbose_name="Время на тест", )
    logged = models.BooleanField(default=False, verbose_name="Для авторизированных пользователей",)
    departament = models.ForeignKey(Departament, related_name='tests', on_delete=models.SET_DEFAULT,
                                    default="1", verbose_name="Отдел", )
    points = models.PositiveIntegerField(default="1", verbose_name="Очки за частично правильные ответы", )

    def get_absolute_url(self):
        return reverse("testing:test", kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Тест")
        verbose_name_plural = _("Тесты")


class TestResult(Test):
    class Meta:
        verbose_name = _("Результаты теста")
        verbose_name_plural = _("Результаты тестов")
        proxy = True


class Question(models.Model):
    text = models.TextField(verbose_name="Вопрос",)
    image = models.ImageField(upload_to='', blank=True)
    score = models.PositiveIntegerField(default="1", verbose_name="Количестово баллов")
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE, verbose_name="Название теста",)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Вопрос")
        verbose_name_plural = _("Вопросы")


class Answer(models.Model):
    text = models.CharField(max_length=256, verbose_name="Ответ")
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE,
                                 verbose_name="Название вопроса",)
    correct = models.BooleanField(default=False, verbose_name="Верный ответ",)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("Ответ")
        verbose_name_plural = _("Ответы")


class Result(models.Model):
    user = models.ForeignKey(Profile, related_name='user', verbose_name="Тестируемый",
                             on_delete=models.CASCADE, editable=False, blank=False)
    test = models.ForeignKey(Test, related_name='test', verbose_name="тест",
                             on_delete=models.CASCADE, editable=False, blank=False)
    score = models.PositiveIntegerField(default="0", verbose_name="Количестово баллов",
                                        editable=False, blank=True)
    start_test_date = models.DateTimeField(auto_now_add=True, editable=False,
                                           verbose_name="Тест начат", blank=False)
    end_test_date = models.DateTimeField(editable=False, verbose_name="Тест завершен", null=True)

    def __str__(self):
        return ''

    class Meta:
        verbose_name = _("Результат тестирования")
        verbose_name_plural = _("Результаты тестирования")
