from datetime import datetime, date

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Invite, Subscriber
from .serializers import InviteSerializer


@api_view(['GET', 'POST'])
def invite_list(request):
    if request.method == 'GET':
        invites = Invite.objects.all()
        serializer = InviteSerializer(invites, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = InviteSerializer(data=request.data)
        if serializer.is_valid():
            sender = None
            receiver = None
            for key in request.data:
                if key == 'sender_subs_id':
                    sender = key
                if key == 'receiver_subs_id':
                    receiver = key
            # Select count(*) from invites where sender_subs_id = ?1 and start_date > {полночь}
            if Invite.objects.filter \
                        (sender_subs_id__in=[request.data[sender]], start_date__gte=date.today()).count() < 4:

                # Select count(*) from invites where sender_subs_id = ?1 and start_date > {месяц}
                year, month, day = str(date.today()).split('-')
                this_month = date(int(year), int(month), 1)
                if Invite.objects.filter \
                        (sender_subs_id__in=[request.data[sender]], start_date__gte=this_month).count() <= 29:

                    # Если абонент Б отключил возможность приглашения, то уведомить абонента А
                    if Subscriber.objects.filter(phone__in=[request.data[receiver]], active__in='1'):

                        # Если абонент Б уже активировал инвайт, то вернуть соответствующий ответ
                        if not Invite.objects.filter(receiver_subs_id__in=[request.data[receiver]], status__in='3'):

                            #Абонент А может приглашать абонента Б только раз в сутки
                            if Invite.objects.filter(sender_subs_id__in=[request.data[sender]], receiver_subs_id__in=[request.data[receiver]]).count() < 1:

                                # Если абонент Б был ранее приглашен, но не успел активировать инвайт,
                                # то предыдущий инвайт становится не активным.
                                # Каждый новый инвайт заменяет предыдущий

                                status_receiver = Invite.objects.filter(receiver_subs_id__in=[request.data[receiver]], status__in='1').update(status=2)

                                serializer.save()

                            else:
                                return Response(serializer.errors, status=status.HTTP_208_ALREADY_REPORTED)

                        else:
                            return Response(serializer.errors, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                    else:
                        return Response(serializer.errors, status.HTTP_423_LOCKED)
                else:
                    return Response(serializer.errors, status=status.HTTP_429_TOO_MANY_REQUESTS)
            else:
                return Response(serializer.errors, status=status.HTTP_429_TOO_MANY_REQUESTS)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)