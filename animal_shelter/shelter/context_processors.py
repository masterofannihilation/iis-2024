def logged_in_user(request):
    return {"logged_in_user": request.user}
