import xlwt
from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Q
from django.http import HttpResponse

from testing.models import Test, Question, Answer, Departament, Result, Profile, TestResult
import nested_admin


class MyAdminSite(AdminSite):
    site_header = 'Система тестирования'
    site_url = None


test_admin = MyAdminSite(name='myadmin')


class BaseNestedModel(nested_admin.NestedModelAdmin):
    view_on_site = False


class BaseAdminModel(admin.ModelAdmin):
    view_on_site = False


class DepartamentAdmin(BaseAdminModel):
    list_display = ['name', ]
    fields = ('name', ('description_open', 'description_close', ), )

    # Выводит список отделов,
    # в которых состоит данный администратор
    def get_queryset(self, request):
        qs = super(DepartamentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return request.user.departament.all()

    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


test_admin.register(Departament, DepartamentAdmin)


class AnswerInLine(nested_admin.NestedTabularInline):
    model = Answer
    fields = ('correct', 'text',)
    extra = 0
    min_num = 2


class QuestionInLine(nested_admin.NestedTabularInline):
    model = Question
    extra = 0
    min_num = 2
    inlines = [
        AnswerInLine
    ]
    fields = ('text', ('image', 'icon'), 'score', )
    readonly_fields = ['icon', ]


class TestAdmin(BaseNestedModel):
    save_on_top = True
    list_display = ['name', 'logged', 'enabled']
    inlines = [
        QuestionInLine
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # При создании теста заполняет поле внешнего ключа отделами
        # из списка, в который входит данный администратор
        user = request.user
        if user.is_superuser is False:
            if db_field.name == "departament":
                kwargs["queryset"] = user.departament.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        # Выводит список тестов, принадлежащих
        # отделам данного администратора
        qs = super(TestAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(departament__in=request.user.departament.all())


test_admin.register(Test, TestAdmin)


class ProfileAdmin(BaseAdminModel):
    list_display = ['username', 'is_staff', 'public', 'dep']

    def set_fields(self, request, obj=None, **kwargs):
        self.fields.append('public')
        self.fields.append('departament')
        form = super(ProfileAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['departament'].widget = forms.CheckboxSelectMultiple()
        return form

    def get_form(self, request, obj=None, **kwargs):
        # Разграничивает доступность полей для
        # суперпользователей и администраторов
        self.fields = ['username']
        if request.user.is_superuser:
            self.fields.append('password')
            self.fields.append('is_staff')
        if obj is None:
            return self.set_fields(request, obj, **kwargs)
        else:
            if obj.is_superuser is not True:
                return self.set_fields(request, obj, **kwargs)
        return super(ProfileAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # При создании обычного пользователя заполняет поле м2м отделов,
        # изображенное чекбоксами, из списка, в который входит данный администратор,
        # а также, в которых состоит сам пользователь.
        user = request.user
        if user.is_superuser is False:
            if db_field.name == "departament":
                if 'object_id' in request.resolver_match.kwargs:
                    kwargs["queryset"] = Departament.objects.filter(
                        Q(id__in=user.departament.all()) |
                        Q(id__in=Profile.objects.filter(
                            id=request.resolver_match.kwargs['object_id']).first().departament.all()
                          )
                    )
                else:
                    kwargs["queryset"] = Departament.objects.filter(id__in=user.departament.all())
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def get_queryset(self, request):
        # Метод выводит список общедоступных и закрепленных
        # за отделами администратора пользователей
        qs = super(ProfileAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(id__in=Profile.objects.filter(departament__in=request.user.departament.all())) |
                         Q(public=True)).filter(is_staff=False)

    def dep(self, obj):
        # Метод для поля "dep", выводит отделы
        # в которых состоит пользователь
        deps = obj.departament.all()
        return ', '.join([dep.name for dep in deps])

    dep.short_description = "Отдел"

    def is_staff(self, obj):
        # Метод для поля "is_admin", отображает,
        # является ли пользователь администратором
        return obj.is_staff

    is_staff.short_description = "Администратор"

    class Media:
        js = ("admin/js/check_first.js",)


test_admin.register(Profile, ProfileAdmin)


def get_time(obj):
    import datetime
    # Метод для поля "time", подсчитывающий количество
    # минут и секунд, за которые пройден тест
    if obj.end_test_date is None:
        return 'Тест не завершен. \n Начат %s' % obj.start_test_date.strftime('%Y.%m.%d %T')
    delta = obj.end_test_date - obj.start_test_date
    minutes = delta.seconds // 60
    seconds = delta.seconds % 60
    test_time = datetime.timedelta(minutes=obj.test.time)
    if delta >= test_time:
        return '%d мин. 0 сек. \n Время истекло' % obj.test.time
    return '%d мин. %d сек.' % (minutes, seconds)


class ResultInLine(admin.TabularInline):
    model = Result
    readonly_fields = ['user', 'score', 'full_correct', 'non_full_correct', 'time']
    extra = 0

    def time(self, obj):
        return get_time(obj)

    time.short_description = "Затрачено времени"

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


class TestResultAdmin(BaseAdminModel):
    fields = []
    exclude = ['description', 'time', 'logged', ]
    readonly_fields = ['name', 'departament']
    list_display = ['name', 'tested', 'departament']
    inlines = [
        ResultInLine,
    ]
    actions = ['remove_results', 'export_as_xls']

    def remove_results(self, request, queryset):
        # Метод очистки всех результатов
        # для выбранных тестов
        for element in queryset:
            results = Result.objects.filter(test=element)
            for result in results:
                result.delete()

    remove_results.short_description = "Очистить результаты"

    def export_as_xls(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="results.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        for element in queryset:
            ws = wb.add_sheet(element.name)
            results = Result.objects.filter(test=element)
            rows = list(results.values_list('user__username', 'score', 'full_correct', 'non_full_correct', ))[:]
            row_num = 0

            font_style = xlwt.XFStyle()
            font_style.font.bold = True

            columns = ['Тестируемый', 'Баллы', 'Полных ответов', 'Частичных ответов', 'Время']
            widthes = [35, 7, 20, 20, 15]  # Примерные длины столбцов
            for col_num in range(len(columns)):
                ws.col(col_num).width = 256 * widthes[col_num]
                ws.write(row_num, col_num, columns[col_num], font_style)
            font_style = xlwt.XFStyle()
            for row in rows:
                row_num += 1
                tmp = row + (get_time(results.filter(user__username=row[0]).first()),)
                for col_num in range(len(tmp)):
                    ws.write(row_num, col_num, tmp[col_num], font_style)
        wb.save(response)
        return response

    export_as_xls.short_description = "Экспорт в xls"

    def tested(self, obj):
        # Метод поля, подсчитывающий количество
        # пользователей прошедших тест
        results = Result.objects.filter(test=obj)
        return len(results)

    tested.short_description = "Количество результатов"

    def get_queryset(self, request):
        # Выводит список тестов, а также
        # дополнительную информацию
        qs = super(TestResultAdmin, self).get_queryset(request)
        self.list_filter = []
        if request.user.is_superuser:
            return qs
        return qs.filter(departament__in=request.user.departament.all())

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


test_admin.register(TestResult, TestResultAdmin)
