import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
from . import models
from django.views.generic import ListView, DetailView


# Create your views here.

class DepartamentListView(ListView):
    model = models.Departament
    context_object_name = 'departament'
    template_name = 'testing/departament_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(self, request, *args, **kwargs)


class TestNameView(DetailView):
    model = models.Departament
    template_name = 'testing/test_list.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(self, request, *args, **kwargs)


class Login(DetailView):
    model = models.Departament
    template_name = 'testing/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, **kwargs):
        if request.POST:
            data = dict(request.POST)
            user = models.Profile.objects.all().filter(username=data['username'][0]).first()
            if user is None:
                messages.error(request, 'Такого пользователя не существует')
            else:
                if user.check_password(data['username'][0]):
                    login(request, user)
                    return redirect(reverse('testing:auth_test_list', kwargs=kwargs))
                else:
                    messages.error(request, 'Такого пользователя не существует')
            return redirect(reverse('testing:login', kwargs=kwargs))


class AuthTestListView(DetailView):
    model = models.Departament
    template_name = 'testing/auth_test_list.html'
    pk_url_kwarg = 'pk'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('testing:login', kwargs=kwargs))
        else:
            departament = models.Departament.objects.filter(id=kwargs['pk']).first()
            if departament in request.user.departament.all():
                return super().get(self, request, *args, **kwargs)
            else:
                messages.error(request, 'Вы не можете решать данные тестовые задания')
                return redirect(reverse('testing:login', kwargs=kwargs))


class TestBaseView(DetailView):
    model = models.Test
    template_name = 'testing/test_base.html'

    def get_context_data(self, **kwargs):
        context = super(TestBaseView, self).get_context_data(**kwargs)
        context['questions'] = models.Question.objects.filter(answers__correct=True, test=kwargs['object']).distinct()
        return context

    def get(self, request, *args, **kwargs):
        test_id = kwargs['pk']
        test = models.Test.objects.all().filter(id=test_id).first()
        if request.user.is_authenticated:
            if models.Result.objects.filter(user=request.user, test=test_id).first() is None:
                result = models.Result(user=request.user, test=test)
                result.save()
            else:
                messages.error(request, 'Вы уже прошли задание - %s' % test.name)
                return redirect(reverse('testing:auth_test_list', kwargs=kwargs))
        else:
            if test.logged is True:
                messages.error(request, 'Вы не можете решать тестовые задания без авторизации')
                return redirect(reverse('testing:test_list', kwargs=kwargs))
        return super().get(self, request, *args, **kwargs)

    def post(self, request, **kwargs):
        if request.POST:
            data = dict(request.POST)
            questions = models.Question.objects.all().filter(test_id=kwargs['pk'])
            dictionary = {}
            for question in questions:
                dictionary[str(question.id)] = []
                answers = models.Answer.objects.all().filter(question_id=question.id)
                for answer in answers:
                    if answer.correct:
                        dictionary[str(question.id)].append(str(answer.id))
                if len(dictionary[str(question.id)]) < 1:
                    del dictionary[str(question.id)]
            over = len(dictionary)
            test = models.Test.objects.all().filter(id=kwargs['pk']).first()
            summ = 0
            correct = 0
            for key in dictionary.keys():
                maxtrue = len(dictionary[key])
                try:
                    if maxtrue > 1:
                        count = 0
                        for element in dictionary[key]:
                            if element in data[key]:
                                count += 1
                        if maxtrue == count:
                            summ += models.Question.objects.filter(id=key).first().score
                            correct += 1
                        else:
                            summ += test.points
                    elif dictionary[key] == data[key]:
                        summ += models.Question.objects.filter(id=key).first().score
                        correct += 1
                except KeyError:
                    continue
            if request.user.is_authenticated:
                if test.logged:
                    result = models.Result.objects.filter(user=request.user, test=test).first()
                    result.score = summ
                    result.end_test_date = datetime.datetime.now()
                    result.save()
                    msg = 'Тест завершен.'
                else:
                    msg = 'Тест завершен.\nВы набрали баллов: %d\nПравильно отвеченных вопросов: %d из %d' % \
                          (summ, correct, over)
            else:
                msg = 'Тест завершен.\nВы набрали баллов: %d\nПравильно отвеченных вопросов: %d из %d' % \
                      (summ, correct, over)
            return HttpResponse(msg, content_type='text/plain')
