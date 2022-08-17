from dateutil.relativedelta import relativedelta
from django.utils import timezone
from .models import Question, Attempt, Participant


def one_month():
    return (timezone.now() + relativedelta(months = 1))


class QuizMaster():
    """
    This is the base class for controlling Quiz
    """
    def __init__(self, request, quiz):
        self.user = request.user
        self.quiz = quiz

    def num_of_attempt_avail(self):
        '''
        Getting numbler of attempts for a single quiz query
        '''
        return self.quiz.attempts

    # def num_of_attempt_avail(self):
    #     '''
    #     Looping through queryset for available attempt
    #     '''
    #     num_of_attempts = 1
    #     for attempt in self.quiz:
    #         num_of_attempts = attempt.attempts
    #     return num_of_attempts


    def num_of_attempt_remaining(self, participant):
        participant = Participant.objects.filter(quiz=self.quiz, participant=participant).count()
        print('attempted::', participant)
        return self.num_of_attempt_avail() - participant

    def can_attempt_again(self, participant):
        participant = Participant.objects.filter(quiz=self.quiz, participant=participant).count()
        return self.quiz.attempts > participant

    def total_quiz_questions(self):
        return len(self.quiz.questions.all())
    
    def total_marks_for_quiz_questions(self):
        return sum((question.marks) for question in self.quiz.questions.all())
    
        # question = Question.objects.filter(self.quiz)
    # def total_correct_marks_per_quiz(self, participant):

        # attempts = Attempt.objects.filter(quiz=self.quiz, participant__id=participant.id)
        # participant = Participant.objects.filter(quiz=self.quiz, participant=participant)
        # if participant > 0:
        #     participants = participant.last()  


        # for attempt in participant:
        #     print(attempt.score)
        # return correct





# num_of_attempt_avail, num_of_attempt_remaining, 
# can_attempt_again, total_marks_gotten,total_quiz_questions, 
# total_marks_for_quiz_questions,single_quiz_attempt_avail 




























































