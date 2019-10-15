import datetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
from django.views import View
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
        try:
            request.session.pop('start_test_time')
            request.session.pop('test')
        except KeyError:
            pass
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
            user = models.Profile.objects.all().filter(username=data['username'][0].upper()).first()
            if user is None:
                messages.error(request, 'Такого пользователя не существует')
            else:
                if user.check_password(user.username):
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
        try:
            request.session.pop('start_test_time')
            request.session.pop('test')
        except KeyError:
            pass
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
        request.session['start_test_time'] = str(datetime.datetime.now())
        request.session['test'] = str(test.id)
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
            max_points = 0
            points = 0
            full_correct = 0
            non_full_correct = 0
            for key in dictionary.keys():
                current_question = models.Question.objects.filter(id=key).first()
                max_points += current_question.score
                maxtrue = len(dictionary[key])
                try:
                    if maxtrue > 1:
                        count = 0
                        for element in dictionary[key]:
                            if element in data[key]:
                                count += 1
                        if maxtrue == count:
                            points += current_question.score
                            full_correct += 1
                        elif count > 0:
                            non_full_correct += 1
                            points += test.points
                    elif dictionary[key] == data[key]:
                        points += current_question.score
                        full_correct += 1
                except KeyError:
                    continue
            if request.user.is_authenticated:
                if test.logged:
                    result = models.Result.objects.filter(user=request.user, test=test).first()
                    result.score = points
                    result.full_correct = full_correct
                    result.non_full_correct = non_full_correct
                    result.end_test_date = datetime.datetime.now()
                    result.save()
                    msg = 'Тест завершен.'
                    return HttpResponse(msg, content_type='text/plain')
            msg = 'Тест завершен.\nНабрано баллов %d из %d\nПолных ответов: %d\nНеполных ответов: %d' % \
                  (points, max_points, full_correct, non_full_correct)
            return HttpResponse(msg, content_type='text/plain')


class SyncTime(View):
    def post(self, request, **kwargs):
        if request.POST:
            data_response = {'min': '0', 'sec': '0'}
            start_test_time = request.session.get('start_test_time')
            if start_test_time is None:
                return HttpResponse(JsonResponse(data_response), content_type="application/json")
            then = datetime.datetime.strptime(start_test_time, '%Y-%m-%d %H:%M:%S.%f')
            now = datetime.datetime.now()
            delta_now = now - then
            test_id = request.session.get('test')
            if test_id is None:
                return HttpResponse(JsonResponse(data_response), content_type="application/json")
            test = models.Test.objects.filter(id=test_id).first()
            if test is None:
                return HttpResponse(JsonResponse(data_response), content_type="application/json")
            over_time = datetime.timedelta(minutes=test.time)
            delta = over_time - delta_now
            total_seconds = delta.total_seconds()
            data_response = {'min': total_seconds // 60, 'sec': int(total_seconds % 60)}
            return HttpResponse(JsonResponse(data_response), content_type="application/json")
