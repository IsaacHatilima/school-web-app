from authentication.models import StaffProfile


def get_staff_id(request):
    profile = StaffProfile.objects.get(user=request.user.id)
    return profile
