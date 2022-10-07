from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from quiz.views import (
    QuestionDetail,
    QuestionList,
    QuizDetail,
    QuizList,
    AnswerFormView,
    LogoutUser,
    )
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'main'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('list/', QuizList.as_view(), name="quiz_list"),
    path('quiz-<int:pk>', QuizDetail.as_view(), name="quiz_detail"),
    path('quiz-<int:number>/questions/', AnswerFormView.as_view(), name="questions_list"),
    path('logout/', LogoutUser.as_view(), name="logout"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


