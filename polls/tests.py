import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_feature_questions(self):
        """was_published_recently returns False for questions whose pub_date in in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)