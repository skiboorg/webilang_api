import json

from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .services import create_random_string
from .serializers import *
from .models import *

from lesson.models import LessonPresence, Lesson
from rest_framework import generics
import requests

from random import choices
import string
from django.views.decorators.clickjacking import xframe_options_exempt

from django.core.mail import send_mail
from django.template.loader import render_to_string
import settings
import datetime

import paypalrestsdk

paypalrestsdk.configure({
  "mode": settings.PAY_PAL_MODE, # sandbox or live
  "client_id": settings.PAY_PAL_CLIENT_ID,
  "client_secret": settings.PAY_PAL_CLIENT_SECRET})

class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        print(json.loads(request.data['userData']))
        selected_avatar = None
        try:
            selected_avatar = json.loads(request.data['selected_avatar'])
        except:
            pass
        print(selected_avatar)
        serializer = UserSerializer(user, data=json.loads(request.data['userData']))
        if serializer.is_valid():
            serializer.save()
            for f in request.FILES.getlist('avatar'):
                user.avatar = f
                user.chosen_avatar = None
                user.save(update_fields=['avatar','chosen_avatar'])
            if selected_avatar:
                ava = Avatar.objects.get(id=selected_avatar)
                user.avatar = None
                user.chosen_avatar=ava
                user.save(update_fields=['avatar', 'chosen_avatar'])
            return Response(status=200)
        else:
            print(serializer.errors)
            return Response(status=400)


class GetUser(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserRecoverPassword(APIView):
    def post(self,request):
        user = None
        lang = request.data['lang']
        print(lang)
        try:
            user = User.objects.get(email=request.data['email'])
        except:
            user = None
        if user:
            password = create_random_string(digits=True, num=8)
            user.set_password(password)
            user.save()
            if lang=='ru':
                text = f'Ваш новый пароль на сайте Webilang : {password}'
                subject = 'Ваш новый пароль на сайте Webilang'
            else:
                text = f'Your new password on Webilang : {password}'
                subject = 'Your new password on Webilang'
            msg_html = render_to_string('notify.html', {
                'text': text,
            })
            print(password)
            send_mail(subject, None, settings.EMAIL_HOST_USER, [user.email],
                      fail_silently=False, html_message=msg_html)
            return Response({'result': True}, status=200)
        else:
            return Response({'result': False}, status=200)

class Dictionary(APIView):

    def get(self,request):
        queryset = None
        if request.GET.get('type') == 'all':
            queryset = Vocabulary.objects.filter(user=request.user)
        if request.GET.get('type') == 'last5':
            queryset = Vocabulary.objects.filter(user=request.user)[:5]
        serializer = DictionarySerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        action = request.data.get('action')
        id = request.data.get('id')
        item = None
        if id:
            item = Vocabulary.objects.get(id=id)
        if action == 'delete':
            item.delete()
        if action == 'add':
            Vocabulary.objects.create(user=request.user,
                                      word=request.data.get('word'),
                                      translate=request.data.get('translate'))
        if action == 'update':
            item.word = request.data.get('update_word')
            item.translate = request.data.get('update_translate')
            item.save()
        return Response(status=200)


class Notes(APIView):
    def get(self,request):
        queryset = None
        if request.GET.get('type') == 'all':
            queryset = Note.objects.filter(user=request.user)
        if request.GET.get('type') == 'last3':
            queryset = Note.objects.filter(user=request.user)[:3]
        serializer = NoteSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        print(request.data)
        action = request.data.get('action')
        id = request.data.get('id')
        item = None
        if id:
            item = Note.objects.get(id=id)
        if action == 'delete':
            item.delete()
        if action == 'add':
            Note.objects.create(user=request.user,
                                text=request.data.get('text'))
        if action == 'update':
            item.text = request.data.get('updated_text')
            item.save()
        return Response(status=200)


class SetTimeFormat(APIView):
    def post(self, request):
        print(request.data.get('format'))
        request.user.is_time_24h = request.data.get('format')
        request.user.save()
        return Response(status=200)


class LessonActivity(APIView):
    def post(self, request):
        data = request.data
        print(data)
        lesson = None
        for user in data['data']:
            if user['is_present']:
                lesson_presence, created = LessonPresence.objects.get_or_create(
                    lesson_id=data['lesson_id'],
                    user_id=user['id'])
                lesson = lesson_presence.lesson
                if created:
                    print('created')
            if user['selected_reward']:
                lesson = Lesson.objects.get(
                    id=data['lesson_id'],
                    )
                reward, created = UserReward.objects.get_or_create(
                    user_id=user['id'],
                    reward_id=user['selected_reward']['id'])
                if not created:
                    reward.count += 1
                    reward.save()

                UserNotification.objects.create(user_id=user['id'],
                                                is_reward=True,
                                                title='Вы получили новую награду',
                                                title_en='You have been given an award',
                                                text=f'Вы получили новую награду <strong>{reward.reward.label}</strong> за активность '
                                                     f'на уроке <strong>{lesson.theme}</strong> {datetime.date.today()}',
                                                text_en=f'You have been given an award <strong>{reward.reward.label_en}</strong> for your'
                                                        f' performance in lesson <strong>{lesson.theme}</strong> {datetime.date.today()}'
                                                )
        return Response(status=200)


class Notifications(APIView):
    def get(self,request):
        queryset = UserNotification.objects.filter(user=request.user)
        serializer = UserNotificationSerializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def post(self,request):
        print(request.data)
        action = request.data.get('action')
        if action == 'set_read':
            UserNotification.objects.filter(user=request.user, is_chat=False).update(is_new=False)
        if action == 'set_read_chat':
            UserNotification.objects.filter(user=request.user, is_chat=True).update(is_new=False)
        if action == 'delete':
            UserNotification.objects.filter(id__in=request.data.get('ids')).delete()
        return Response(status=200)


class Avatars(generics.ListAPIView):
    serializer_class = AvatarSerializer
    queryset = Avatar.objects.all()

class Rewards(generics.ListAPIView):
    serializer_class = RewardSerializer
    queryset = Reward.objects.all()

class CheckPromo(APIView):
    def post(self,request):

        promo_code = None
        used_promo = False
        try:
            promo_code = PromoCode.objects.get(code=request.data.get('code'))
        except:
            pass

        try:
            used_promo = UsedPromoCode.objects.get(user=request.user, promo=promo_code)

        except:
            pass
        if not used_promo:
            if promo_code:
                serializer = PromoCodeSerializer(promo_code)
                UsedPromoCode.objects.create(user=request.user, promo=promo_code)
                return Response(serializer.data,status=200)
            else:
                return Response(status=200)
        else:
            return Response({'status':False,'promo_used':True},status=200)




@xframe_options_exempt
def sber_payment_complete(request):
    sber_id = request.GET.get('orderId')
    payment = Payment.objects.get(sber_id=sber_id)
    print(payment)
    if not payment.is_pay:
        payment.is_pay = True
        payment.save()
        tariff = payment.tariff
        user = payment.user

        if tariff.is_personal:
            user.personal_lessons_left += tariff.lessons_count
        else:
            user.group_lessons_left += tariff.lessons_count

        if payment.promo_code:
            promo = PromoCode.objects.get(code=payment.promo_code)

            if promo.is_free_lessons:
                if tariff.is_personal:
                    user.personal_lessons_left += promo.free_lessons_count
                else:
                    user.group_lessons_left += promo.free_lessons_count

                user_who_has_promo = User.objects.get(promo=promo)
                if user_who_has_promo.personal_lessons_left > 0:
                    user_who_has_promo.personal_lessons_left += promo.free_lessons_count
                elif user_who_has_promo.group_lessons_left > 0:
                    user_who_has_promo.group_lessons_left += promo.free_lessons_count
                else:
                    user_who_has_promo.personal_lessons_left += promo.free_lessons_count

                user_who_has_promo.save(update_fields=['personal_lessons_left', 'group_lessons_left'])

        UserNotification.objects.create(user=user,
                                        title='Оплата',
                                        title_en='Payment',
                                        text='Ваш платеж поступил',
                                        text_en='Payment success',
                                        )

        user.save(update_fields=['personal_lessons_left', 'group_lessons_left'])

        msg_html = render_to_string('notify.html', {
            'text': f'Поступила оплата от {user.firstname} {user.lastname} {user.email} | Сумма {payment.amount}',
        })

        send_mail('Поступила оплата', None, settings.EMAIL_HOST_USER, [settings.ADMIN_EMAIL],
                  fail_silently=False, html_message=msg_html)
        print('return')
        return HttpResponseRedirect(f'{settings.RETURN_URL}/student/payment_complete')
    else:
        print('return payed')
        return HttpResponseRedirect(f'{settings.RETURN_URL}')


class SberPaymentCallback(APIView):
    def post(self,request):
        print('post')
        data = request.data
        print(data)
        return Response(status=200)
    def get(self,request):
        print('get')
        print(self.request.query_params)
        print(self.request)
        return Response(status=200)


class SberPayment(APIView):
    def post(self,request):
        data = request.data

        orderNumber = "".join(choices(string.ascii_uppercase, k=6))
        if data.get("language") == 'ru':
            language = 'ru'
            sign = 'руб'
            description = f'Оплата за обучение  {request.user.email}'
        else:
            language = 'en'
            sign = '$'
            description = f'Payment  {request.user.email}'
        response = requests.get(f'{settings.SBER_PAY_URL}'
                                f'amount={data.get("amount")}&'
                                f'currency=643&'
                                f'language={language}&'
                                f'orderNumber={orderNumber}&'
                                f'description={description}&'
                                f'dynamicCallbackUrl={settings.SBER_API_CALLBACK_URL}&'
                                f'password={settings.SBER_API_PASSWORD}&'
                                f'userName={settings.SBER_API_LOGIN}&'
                                f'returnUrl={settings.SBER_API_RETURN_URL}&'
                                f'failUrl={settings.SBER_API_FAIL_URL}&'
                                'pageView=DESKTOP&sessionTimeoutSecs=1200')
        response_data = json.loads(response.content)
        print(response_data)

        if response_data.get('errorCode'):
            result = {'success': False, 'message': response_data.get('errorMessage')}
        else:
            Payment.objects.create(sber_id=response_data.get('orderId'),
                                   user=request.user,
                                   tariff_id=data.get("tariff_id"),
                                   amount=f'{int(data.get("amount")) / 100} {sign}',
                                   promo_code=data.get("promo_code"),
                                   orderNumber=orderNumber
                                   )
            result = {'success': True, 'url': response_data.get('formUrl')}

        return Response(result, status=200)

class PayPalPayment(APIView):
    def post(self,request):
        data = request.data
        print(data)
        orderNumber = "".join(choices(string.ascii_uppercase, k=6))

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"},
            "redirect_urls": {
                "return_url": settings.PAY_PAL_RETURN_URL,
                "cancel_url": "http://localhost:3000/"},
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Order",
                        "sku": orderNumber,
                        "price": data.get('amount'),
                        "currency": "RUB",
                        "quantity": 1}]},
                "amount": {
                    "total": data.get('amount'),
                    "currency": "RUB"},
                "description": f'Payment  {request.user.email}'}]})

        if payment.create():
            payment_info = payment.to_dict()
            print(payment_info['links'][1]['href'])

            Payment.objects.create(pay_pal_id=payment_info['id'],
                                   user=request.user,
                                   tariff_id=data.get("tariff_id"),
                                   amount=f'{int(data.get("amount"))} USD',
                                   promo_code=data.get("promo_code"),
                                   orderNumber=orderNumber
                                   )

            result = {'success': True, 'url':payment_info['links'][1]['href'] }
        else:
            print(payment.error)
            result = {'success': False, 'message': payment.error}

        return Response(result, status=200)

def pay_pal_payment_complete(request):
    paymentId = request.GET.get('paymentId')
    payment = Payment.objects.get(pay_pal_id=paymentId)
    checkPayment(payment=payment)
    return HttpResponseRedirect(f'{settings.RETURN_URL}/student/payment_complete')

class Test(APIView):

    def get(self,request):
        from lesson.tasks import checkLessons
        checkLessons()

