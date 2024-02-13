from django.urls import path

from . import views

app_name = 'provas'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.index, name='index'),

    path('courses/', views.course_view, name='courses'),
    path('courses/save/', views.savecourse_view, name='saveCourse'),
    path('courses/<str:courseId>/delete/', views.deletecourse_view, name='deleteCourse'),

    path('specialties/', views.specialty_view, name='specialties'),
    path('specialties/save/', views.saveSpecialty_view, name='saveSpecialty'),
    path('specialties/<str:specialtyId>/delete/', views.deleteSpecialty_view, name='deleteSpecialty'),
    path('series/', views.series_view, name='series'),

    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/save/', views.savesubject_view, name='saveSubject'),
    path('subjects/<str:subjectId>/delete/', views.deletesubject_view, name='deleteSubject'),

    path('questions/', views.questions_view, name='questions'),
    path('questions/insert/', views.questionEdit_view, name='insertQuestion'),
    path('questions/insert/save/', views.questionSave_view, name='saveInsertQuestion'),
    path('questions/<str:subjectId>/subunit/', views.subunit_view, name='subUnit'),
    path('questions/<str:subjectId>/subunit/ch', views.chSave_view, name='saveCh'),
    path('questions/<str:subjectId>/details/', views.questionDetails_view, name='questionDetails'),
    path('questions/<str:questionId>/delete/', views.questionDelete_view, name='deleteQuestion'),
    path('questions/<str:subjectId>/<str:questionId>/', views.questionOpen_view, name='openQuestion'),
    path('questions/<str:subjectId>/<str:questionId>/edit/', views.questionEdit_view, name='editQuestion'),
    path('questions/<str:subjectId>/<str:questionId>/save/', views.questionSave_view, name='saveEditQuestion'),

    path('exams/', views.exams_view, name='exams'),
    path('exams/courses/<str:courseId>/specialties/', views.examsSpecialties_view, name='examsSpecialties'),
    path('exams/courses/<str:courseId>/specialties/<str:specialtyId>/series/<int:serie>/subjects/', views.examsSubjects_view, name='examsSubjects'),
    path('exams/courses/<str:courseId>/specialties/<str:specialtyId>/series/<int:serie>/subjects/<str:subjectId>/questions/', views.examsQuestions_view, name='examsQuestions'),
    path('exams/save/', views.examSave_view, name='examSave'),
    path('exams/<str:examId>/delete/', views.examDelete_view, name='examDelete'),
    path('exams/<int:examId>/details/', views.examDetails_view, name='examDetails'),
    path('exams/<int:examId>/load/<str:type>', views.examLoad_view, name='examLoad'),

    path('users/', views.users_view, name='users'),
    path('users/save', views.userSave_view, name='userSave'),
    path('users/<str:username>/delete/', views.userDelete_view, name='userDelete'),
    path('users/<str:username>/changePassword/', views.userChangePassword_view, name='userChangePassWord'),
    path('logout/', views.logout_view, name='logout'),
]