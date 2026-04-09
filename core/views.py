from django.shortcuts import render

from django.views.generic import TemplateView, RedirectView
from django.urls import reverse

from common.context_processors import test_data
from common.paginator import Paginator

# Create your views here.


# =========================== Answers ============================
   
class AnswerEditView(TemplateView):
    template_name = "pages/answers/id/edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        answer_id = self.kwargs.get('id')

        answer = test_data.get_answer_by_id(answer_id)

        context['title'] = "Edit Answer"
        context['answer'] = answer

        return context
    
# ============================ Search ============================

class SearchView(TemplateView):
    template_name = "pages/search.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        query = self.request.GET.get('q', '')
        page = self.request.GET.get('page', 1)

        all_questions = test_data.get_questions_by_query(query)
            
        paginator = Paginator(all_questions)
        page_obj = paginator.get_page(page)
        
        context['title'] = f"Search results for '{query}'"
        context['query'] = query
        context['questions'] = page_obj.object_list
        context['page'] = page_obj
        
        return context


# ============================= Tags =============================

class TagsView(RedirectView):
    pattern_name = 'index'


class TagView(TemplateView):
    template_name = "pages/tags/tag.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        tag_name = self.kwargs.get('tag')
        page = self.request.GET.get('page', 1)

        tag = test_data.get_tag_by_name(tag_name)
        all_questions = test_data.get_questions_by_tag(tag)

        paginator = Paginator(all_questions)
        page_obj = paginator.get_page(page)
        
        context['title'] = f"Tag: {tag_name}"
        context['questions'] = page_obj.object_list
        context['page'] = page_obj
        
        return context


# ============================ Users =============================

class UsersView(TemplateView):
    template_name = "pages/users.html"
    title = "All Users"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page', 1)
        
        all_users = test_data.get_users()

        paginator = Paginator(all_users)
        page_obj = paginator.get_page(page)
        
        context['title'] = self.title
        context['users'] = page_obj.object_list
        context['page'] = page_obj
        
        return context


class UserLoginView(TemplateView):
    template_name = "pages/users/login.html"
    title = "Login"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.title

        return context


class UserLogoutView(RedirectView):
    pattern_name ='index'


class UserSettingsView(TemplateView):
    template_name = "pages/users/settings.html"
    title = "Settings"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.title

        return context


class UserSignupView(TemplateView):
    template_name = "pages/users/signup.html"
    title = "Sign Up"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['title'] = self.title

        return context


class UserView(TemplateView):
    template_name = "pages/users/id.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user_id = self.kwargs.get('id')
        page = self.request.GET.get('page', 1)

        user = test_data.get_user_by_id(user_id)
        all_questions = test_data.get_questions_by_author(user)

        paginator = Paginator(all_questions)
        page_obj = paginator.get_page(page)
        
        context['title'] = f"User: {user['nickname']}"
        context['user'] = user
        context['questions'] = page_obj.object_list
        context['page'] = page_obj
        
        return context
    