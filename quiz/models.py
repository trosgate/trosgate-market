from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.core.mail import send_mail
from uuid import uuid4
from django.utils.text import slugify
from teams.utilities import create_random_code


class Answer(models.Model):
	answer = models.CharField(_("Answer Option"), max_length=500)
	is_correct = models.BooleanField(default=False)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Quiz Master"), related_name="answers", on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.answer} ({self.is_correct})'


class Question(models.Model):
	question = models.CharField(_("Question"), max_length=500)
	answers = models.ManyToManyField(Answer, verbose_name=_("Answers"), related_name="questions",)
	marks = models.PositiveIntegerField(_("Marks"),)
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Quiz Master"), related_name="questions", on_delete=models.CASCADE)
	reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.question

	def save(self, *args, **kwargs):
		if self.reference is None:
			self.reference = create_random_code()
		self.slug = slugify({self.reference})
		super(Question, self).save(*args, **kwargs)


class Quizes(models.Model):
	title = models.CharField(_("title"), max_length=200)
	instruction = models.TextField(_("Instruction"),)
	created_at = models.DateTimeField(_("created On"), auto_now_add=True)
	attempts = models.PositiveIntegerField(_("Attempt"),)
	duration = models.PositiveIntegerField(_("Duration(Min)"))
	skills = models.ManyToManyField("general_settings.Skill", verbose_name=_("Required Skills"), related_name="quizskills")
	created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Quiz Master"), related_name="quizmaster", on_delete=models.CASCADE)
	questions = models.ManyToManyField(Question, verbose_name=_("questions"), related_name="quizes",)
	reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=100, blank=True, null=True)
	is_published = models.BooleanField(_("Status"), choices = ((False,'Private'), (True, 'Public')), default = False)
	
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.reference is None:
			self.reference = create_random_code()
		self.slug = slugify(f'{self.title}-{self.reference}')
		super(Quizes, self).save(*args, **kwargs)

	def get_quiz_detail_absolute_url(self):
			return reverse('quiz:quiz_detail', args=[self.slug])

	#a url route for the project update page
	def get_question_absolute_url(self):
		return reverse('quiz:questions', args=[self.slug])

	#a url route for the project update page
	def get_take_test_absolute_url(self):
		return reverse('quiz:take_test', args=[self.slug])

	#a url route for the archive project page
	def get_quiz_result_absolute_url(self):
		return reverse('quiz:quiz_result', args=[self.id])

	def get_modify_quiz_absolute_url(self):
		return reverse('quiz:modify_quiz', args=[self.slug])

	def get_quiz_participants_absolute_url(self):
		return reverse('quiz:quiz_participants', args=[self.slug])

	def get_question_detail_absolute_url(self):
		return reverse('quiz:question_detail', args=[self.slug])


class Participant(models.Model):
	quiz = models.ForeignKey(Quizes, verbose_name=_("Quiz Name"), related_name="participants", on_delete=models.CASCADE)
	score = models.PositiveIntegerField(_("Score"),)
	completed = models.DateTimeField(_("Completed On"), auto_now_add=True)
	participant = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_("Quiz Master"), related_name="myparticipants", on_delete=models.CASCADE)
	reference = models.CharField(unique=True, null=True, blank=True, max_length=100)
	slug = models.SlugField(max_length=100, blank=True, null=True)

	def __str__(self):
		return self.participant.short_name

	def save(self, *args, **kwargs):
		if self.reference is None:
			self.reference = create_random_code()
		self.slug = slugify(f'{self.quiz.title}-{self.reference}')
		super(Participant, self).save(*args, **kwargs)


class Attempt(models.Model):
	quiz = models.ForeignKey(Quizes, verbose_name=_("Quiz"), related_name="myattemptquiz", on_delete=models.CASCADE)
	participant = models.ForeignKey(Participant, verbose_name=_("Participant"), related_name="myattemptpaticipant", on_delete=models.CASCADE)
	question = models.ForeignKey(Question, verbose_name=_("Question"), related_name="myattemptquestion", on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, verbose_name=_("Answer"), related_name="myattemptanswer", on_delete=models.CASCADE)

	def __str__(self):
		return self.participant.quiz.title

