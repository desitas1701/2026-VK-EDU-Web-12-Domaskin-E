import random
from datetime import datetime, timedelta


class TestDataGenerator:
    def __init__(self, users_count=100, questions_count=100, tags_count=20, answers_per_question=5):
        self.users_count = users_count
        self.questions_count = questions_count
        self.tags_count = tags_count
        self.answers_per_question = answers_per_question
        
        self._users = self._generate_users()
        self._tags = self._generate_tags()
        self._questions = self._generate_questions()
        self._answers = self._generate_answers()
    
    # ============================ Users =============================
    
    def _generate_users(self):
        nicknames = [
            "Dr. Pepper", "John Doe", "Jane Smith", "CodeMaster", 
            "StackOverflower", "Pythonista", "JavaGuru", "RustLover",
            "WebWizard", "DataNinja", "AIEnthusiast", "DevOpsGod",
            "BugHunter", "FeatureFan", "TestDriven", "CleanCoder"
        ]
        
        users = []

        for i in range(self.users_count):
            users.append({
                'id': i + 1,
                'login': f"user{i + 1}",
                'email': f"user{i + 1}@example.com",
                'nickname': f"{random.choice(nicknames)} #{i + 1}",
                'avatar_url': f"images/default_avatar.png",
            })
        
        return users
    
    def get_users(self, limit=None):
        if limit:
            return self._users[:limit]
        return self._users
    
    def get_users_by_answers_count(self, limit=None):
        users_with_counts = []

        for user in self._users:
            answer_count = len([a for a in self._answers if a['author']['id'] == user['id']])
            users_with_counts.append({
                **user,
                'answer_count': answer_count
            })
        
        users_with_counts = sorted(users_with_counts, key=lambda u: u['answer_count'], reverse=True)
        
        if limit:
            users_with_counts = users_with_counts[:limit]
        
        return users_with_counts
    
    def get_user_by_id(self, user_id):
        for user in self._users:
            if user['id'] == user_id:
                return user
        return None
    
    def get_random_user(self):
        return random.choice(self._users)
    
    # ============================= Tags =============================
    
    def _generate_tags(self):
        names = [
            'python', 'javascript', 'django', 'react', 'vue', 'angular',
            'html', 'css', 'sql', 'postgres', 'mongodb', 'redis',
            'docker', 'kubernetes', 'aws', 'azure', 'linux', 'git',
            'algorithms', 'data-structures', 'machine-learning', 'ai',
            'backend', 'frontend', 'fullstack', 'devops', 'security',
            'testing', 'debugging', 'performance', 'optimization'
        ]
        
        tags = []

        for i in range(self.tags_count):
            tags.append({
                'id': i + 1,
                'name': f"{random.choice(names)}{i + 1}",
            })
        
        return tags
    
    def get_tags(self, limit=None):
        if limit:
            return self._tags[:limit]
        return self._tags
    
    def get_tag_by_id(self, tag_id):
        for tag in self._tags:
            if tag['id'] == tag_id:
                return tag
        return None
    
    def get_tag_by_name(self, name):
        for tag in self._tags:
            if tag['name'] == name:
                return tag
        return None
    
    def get_tags_by_questions_count(self, limit=None):
        tags_with_counts = []

        for tag in self._tags:
            question_count = len([q for q in self._questions if any(t['id'] == tag['id'] for t in q['tags'])])
            tags_with_counts.append({
                **tag,
                'questions_count': question_count
            })
        
        tags_with_counts = sorted(tags_with_counts, key=lambda t: t['questions_count'], reverse=True)
        
        if limit:
            tags_with_counts = tags_with_counts[:limit]
        
        return tags_with_counts
    
    # ========================== Questions ===========================
    
    def _generate_questions(self):
        titles = [
            "How to build a moon park?",
            "Why is my code not working?",
            "Best practices for Django views?",
            "How to optimize SQL queries?",
            "What's the difference between GET and POST?",
            "How to deploy Django application?",
            "Docker vs Virtual Machines?",
            "React hooks explained?",
            "How to handle authentication in Django?",
            "What is the best way to learn programming?",
        ]

        questions = []
        
        for i in range(self.questions_count):
            author_id = random.randint(1, self.users_count)
            author = self.get_user_by_id(author_id)
            
            num_tags = random.randint(2, 4)
            tag_ids = [random.randint(1, self.tags_count) for i in range(num_tags)]
            tags = [self.get_tag_by_id(tag_id) for tag_id in tag_ids]

            stats = {
                'votes': random.randint(-self.users_count, self.users_count),
                'answers': 0,
            }
            
            questions.append({
                'id': i + 1,
                'author': author,
                'title': f"{random.choice(titles)} #{i + 1}",
                'text': f"I have a problem with something.\nCan anyone help me figure this out?\n\nDetails: Issue #{i + 1}",
                'tags': tags,
                'is_solved': False,
                'stats': stats,
                'created_at': datetime.now() - timedelta(days=random.randint(0, 30)),
            })
        
        return questions
    
    def get_questions(self, key=None, reverse=False, limit=None):
        questions = self._questions.copy()
        
        if key:
            if key == 'created_at':
                key_func = lambda q: q['created_at']
            elif key == 'votes':
                key_func = lambda q: q['stats']['votes']
            else:
                key_func = lambda q: q['id']
            
            if key_func:
                questions = sorted(questions, key=key_func, reverse=reverse)
        
        if limit:
            questions = questions[:limit]
        
        return questions
    
    def get_question_by_id(self, question_id):
        for question in self._questions:
            if question['id'] == question_id:
                return question
        return None
    
    def get_questions_by_query(self, query):
        if not query:
            return self.get_questions()

        questions = []
        
        query_lower = query.lower()
        for question in self._questions:
            title = question.get('title', '')
            text = question.get('text', '')
            
            if query_lower in title.lower() or query_lower in text.lower():
                questions.append(question)

        return questions
    
    def get_questions_by_tag(self, tag, limit=None):
        questions = [q for q in self._questions if any(t['id'] == tag['id'] for t in q['tags'])]
        if limit:
            questions = questions[:limit]
        return questions
    
    def get_questions_by_author(self, author, limit=None):
        questions = [q for q in self._questions if q['author']['id'] == author['id']]
        if limit:
            questions = questions[:limit]
        return questions
    
    # =========================== Answers ============================
    
    def _generate_answers(self):
        answers = []

        answer_id = 1
        for question in self._questions:
            num_answers = random.randint(0, self.answers_per_question)
            
            for j in range(num_answers):
                author_id = random.randint(1, self.users_count)
                author = self.get_user_by_id(author_id)
                
                answers.append({
                    'id': answer_id,
                    'question_id': question['id'],
                    'author': author,
                    'text': f"Here's my answer to question #{question['id']}.\n\nI think you should try this approach...\n\nAnswer #{answer_id}",
                    'status': random.randint(0, 2),  # 0 - Unknown, 1 - Correct, 2 - Incorrect
                    'votes': random.randint(-self.users_count, self.users_count),
                    'created_at': question['created_at'] + timedelta(hours=random.randint(1, 48)),
                })

                question['stats']['answers'] += 1
                question['is_solved'] |= (answers[-1]['status'] == 1)

                answer_id += 1
        
        return answers
    
    def get_answers(self, limit=None):
        if limit:
            return self._answers[:limit]
        return self._answers
    
    def get_answer_by_id(self, answer_id):
        for answer in self._answers:
            if answer['id'] == answer_id:
                return answer
        return None
    
    def get_answers_by_question(self, question, key=None, reverse=False, limit=None):
        answers = [a for a in self._answers if a['question_id'] == question['id']]
        
        if key:
            if key == 'created_at':
                key_func = lambda a: a['created_at']
            elif key == 'votes':
                key_func = lambda a: a['votes']
            elif key == 'status':
                key_func = lambda a: a['status']
            else:
                key_func = lambda a: a['id']
            
            if key_func:
                answers = sorted(answers, key=key_func, reverse=reverse)
        
        if limit:
            answers = answers[:limit]
        
        return answers
    
    def get_answers_by_author(self, author_id, limit=None):
        answers = [a for a in self._answers if a['author']['id'] == author_id]
        if limit:
            answers = answers[:limit]
        return answers
    