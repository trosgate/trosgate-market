# from projects.models import Project
# # from general_settings.models import PaymentGateway


# class ApplicationBox():
#     """
#     This is the base class for project application and hiring sessions
#     """
#     def __init__(self, request):
#         self.session = request.session
#         hiring_box = self.session.get('proposal_box')
#         if 'proposal_box' not in request.session:
#             hiring_box = self.session['proposal_box'] = {}
#         self.hiring_box = hiring_box