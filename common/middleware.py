class AuthenticationEmulatorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        as_user = request.GET.get('as_user')

        if as_user:
            try:
                user_id = int(as_user)
            except ValueError:
                user_id = 0

            request.session['user_id'] = user_id
            
        response = self.get_response(request)

        return response
