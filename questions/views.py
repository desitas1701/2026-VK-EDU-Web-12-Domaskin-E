from django.shortcuts import render

from django.views.generic import TemplateView, RedirectView
from django.urls import reverse

from common.context_processors import test_data
from common.paginator import Paginator

# Create your views here.


# ============================ Index =============================

class IndexView(RedirectView):
    pattern_name = 'questions'


# ========================== Questions ===========================

class QuestionsView(RedirectView):
    pattern_name = 'questions_newest'


class QuestionAskView(TemplateView):
    template_name = "pages/questions/ask.html"
    title = "Ask Question"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = self.title
        
        return context


class QuestionsHottestView(TemplateView):
    template_name = "pages/questions/hottest.html"
    title = "Hottest Questions"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page = self.request.GET.get('page', 1)
        
        all_questions = test_data.get_questions(key='votes', reverse=True)

        paginator = Paginator(all_questions)
        page_obj = paginator.get_page(page)

        context['title'] = self.title
        context['questions'] = page_obj.object_list
        context['page'] = page_obj
        
        return context


class QuestionsNewestView(TemplateView):
    template_name = "pages/questions/newest.html"
    title = "Newest Questions"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        page = self.request.GET.get('page', 1)
        
        all_questions = test_data.get_questions(key='created_at', reverse=True)
        
        paginator = Paginator(all_questions)
        page_obj = paginator.get_page(page)

        context['title'] = self.title
        context['questions'] = page_obj.object_list
        context['page'] = page_obj
        
        return context


class QuestionView(TemplateView):
    template_name = "pages/questions/id.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        question_id = self.kwargs.get('id')

        question = test_data.get_question_by_id(question_id)
        answers = test_data.get_answers_by_question(question, key='votes', reverse=True)

        context['title'] = question['title']
        context['question'] = question
        context['answers'] = answers

        return context


class QuestionDeleteView(RedirectView):
    pattern_name = 'index'

    def get_redirect_url(self, *args, **kwargs):
        if self.pattern_name is None:
            return None
        return reverse(self.pattern_name, args=args)


class QuestionEditView(TemplateView):
    template_name = "pages/questions/id/edit.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        question_id = self.kwargs.get('id')

        question = test_data.get_question_by_id(question_id)

        context['title'] = f"Edit: {question['title']}"
        context['question'] = question

        return context
