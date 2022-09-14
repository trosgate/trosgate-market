# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Notification

# @login_required
# def notifications(request):
#     goto = request.GET.get('goto', '')
#     # notification_id = request.GET.get('notification', 0)
#     notification_slug = request.GET.get('notification', '')
#     # extra_id = request.GET.get('extra_id', 0)

#     if goto != '':
#         notification = Notification.objects.get(slug=notification_slug)
#         notification.is_read = True
#         notification.save()

#         # if notification.notification_type == Notification.MESSAGE:
#         #     return redirect('application_detail', application_id=notification.extra_id)
#         if notification.notification_type == Notification.APPLICATION:
#             return redirect('application_detail', application_slug=notification.slug)
#     context = {

#     }
#     return render(request, 'notification/notifications.html', context)

