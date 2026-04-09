from common.utils import TestDataGenerator


test_data = TestDataGenerator()


def global_context(request):
    if request.session['user_id']:
        user_id = request.session['user_id']

        if not (0 <= user_id and user_id <= test_data.users_count):
            user_id = 0

        if user_id == 0:
            user = dict()
            user['is_authenticated'] = False
        else:
            user = test_data.get_user_by_id(user_id=user_id)
            user['is_authenticated'] = True
    else:
        from django.contrib.auth.models import AnonymousUser

        user = AnonymousUser()

    return {
        'title': "",
        'user': user,
        'tags': test_data.get_tags_by_questions_count(limit=20),
        'members': test_data.get_users_by_answers_count(limit=10),
    }
