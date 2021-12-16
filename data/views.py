from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings
class CreateCallback(generics.ListAPIView):
    def post(self, request):
        name = request.data.get('name')
        phone = request.data.get('phone')
        course = request.data.get('course')

        Callback.objects.create(
            name=name,
            phone=phone,
            course=course
            )
        msg_html = render_to_string('callback.html', {
            'name': name,
            'phone': phone,
            'course': course,
        })
        send_mail('Форма обратной связи с сайта Webilang', None, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL],
                  fail_silently=False, html_message=msg_html)
        return Response(status=200)


class Email_Subscribe(generics.ListAPIView):
    def post(self,request):
        print(request.data)
        try:
            EmailSubscribe.objects.get(email=request.data.get('email'))
        except:
            EmailSubscribe.objects.create(email=request.data.get('email'))
            print('created')
        return Response(status=200)

class Teachers(generics.ListAPIView):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()


class GetTariff(generics.ListAPIView):
    serializer_class = TariffCategorySerializer
    queryset = TariffCategory.objects.all()

class GetFB(generics.ListAPIView):
    serializer_class = FeedbackSerializer
    queryset = Feedback.objects.all()