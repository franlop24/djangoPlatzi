import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from polls.models import Question

# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_feature_questions(self):
        """was_published_recently returns False for questions whose pub_date in in the future"""

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_now_or_a_day_ago(self):
        """was_published_recently returns True for questions created now or a day ago"""

        now_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=timezone.now())
        self.assertTrue(now_question.was_published_recently())

    def test_was_published_earlier_than_a_day(self):
        """was_published_recently returns True for questions created earlier than a day"""

        time = timezone.now() - datetime.timedelta(days=1)
        now_question = Question(question_text="¿Quien es el mejor CD de Platzi?", pub_date=time)
        self.assertFalse(now_question.was_published_recently())

class QuestionIndexViewTests(TestCase):

    def test_no_questions(self):
        """If no questions exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_no_questions_in_the_future(self):
        """Question created in the future has not been included in latest_question_list"""
        Question(question_text="Question in the future?", pub_date=timezone.now() + timezone.timedelta(days=1)).save()
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_with_questions_in_the_past(self):
        """Question created in the past has been included in latest_question_list"""
        question = Question(question_text="Question in the Past?", pub_date=timezone.now() - timezone.timedelta(days=10)).save()
        response = self.client.get(reverse("polls:index"))
        #self.assertQueryNotEqual(response.context["latest_question_list"], [question])
        self.assertEquals(len(response.context["latest_question_list"]), 1)

    def test_future_question_and_past_question(self):
        """test with a question in the future and a question in the past, returns a latest_question_list with only a question"""
        Question(question_text="Question in the Past?", pub_date=timezone.now() - timezone.timedelta(days=10)).save()
        Question(question_text="Question in the Future?", pub_date=timezone.now() + timezone.timedelta(days=10)).save()
        response = self.client.get(reverse("polls:index"))
        self.assertEquals(len(response.context["latest_question_list"]), 1)

    def test_with_two_future_questions(self):
        """test with a question in the future and a question in the past, returns a latest_question_list with only a question"""
        Question(question_text="Question in the Past 1?", pub_date=timezone.now() - timezone.timedelta(days=10)).save()
        Question(question_text="Question in the Past 2?", pub_date=timezone.now() - timezone.timedelta(days=20)).save()
        response = self.client.get(reverse("polls:index"))
        self.assertEquals(len(response.context["latest_question_list"]), 2)