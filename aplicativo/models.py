from django.db import models
from django.db import connection


def get_password(password):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT CONCAT('*', UPPER(SHA1(UNHEX(SHA1('{password}')))));")
        raw_password = cursor.fetchone()

    return raw_password[0]


class Hyerarchies(models.Model):
    hyerarchy = models.CharField(max_length=3, primary_key=True, unique=True)
    levelNo = models.IntegerField()
    caption = models.CharField(max_length=255)

    class Meta:
        db_table = 'hyerarchies'


class User(models.Model):
    username = models.CharField(max_length=50, primary_key=True, unique=True, db_column='login')
    realName = models.CharField(max_length=255)
    password = models.CharField(max_length=50)
    accessLevel = models.IntegerField()
    last_login = models.DateTimeField(auto_now_add=True, db_column='lastAccess')
    lastAccessAddress = models.CharField(max_length=100)
    showCourses = models.IntegerField()
    editCourse = models.IntegerField()
    mapCourse = models.IntegerField() # o que faz?
    removeCourse = models.IntegerField()
    showSpecialities = models.IntegerField()
    editSpeciality = models.IntegerField()
    mapSpeciality = models.IntegerField() # o que faz?
    removeSpeciality = models.IntegerField()
    showSubjects = models.IntegerField()
    editSubject = models.IntegerField()
    removeSubject = models.IntegerField()
    showQuestions = models.IntegerField()
    editQuestion = models.IntegerField() 
    deleteQuestion = models.IntegerField()
    previewQuestion = models.IntegerField()
    showExams = models.IntegerField()
    showExamDetails = models.IntegerField()
    createExam = models.IntegerField()
    correctExam = models.IntegerField() # o que faz?
    removeExam = models.IntegerField()
    adminUsers = models.IntegerField()
    showLogs = models.IntegerField() # o que faz?
    editSubjectCH = models.IntegerField() 
    hyerarchy = models.ForeignKey(Hyerarchies, db_column='hyerarchy', on_delete=models.CASCADE)
    revisionOkQuestion = models.IntegerField() # o que faz?
    backupFull = models.IntegerField() # o que faz?
    backupPartial = models.IntegerField() # o que faz?
    is_active = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=False)
    is_authenticated = models.BooleanField(default=False)

    REQUIRED_FIELDS = [
        'login',
        'realName',
        'password',
        'showCourses',
        'editCourse',
        'mapCourse',
        'removeCourse',
        'showSpecialities',
        'editSpeciality',
        'mapSpeciality',
        'removeSpeciality',
        'showSubjects',
        'editSubject',
        'removeSubject',
        'showQuestions',
        'editQuestion',
        'previewQuestion',
        'showExams',
        'showExamDetails',
        'createExam',
        'correctExam',
        'removeExam',
        'adminUsers',
        'showLogs',
        'editSubjectCH',
        'hyerarchy',
        'revisionOkQuestion',
        'backupFull',
        'backupPartial',
        'is_active',
        'is_anonymous',
        'is_authenticated',
    ] 
    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'users'

    

    def check_password(self, raw_password):
        return get_password(raw_password) == self.password
    
    def has_perm(self, perm, obj=None):
        # Handle permissions logic here
        return True  # For simplicity, always return True

    def has_module_perms(self, app_label):
        # Handle module permissions logic here
        return True  # For simplicity, always return True
    
    def get_username(self):
        return self.username


class Course(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    caption = models.CharField(max_length=100)
    numberOfSeries = models.IntegerField()

    class Meta:
        db_table = 'courses'


class Specialities(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    caption = models.CharField(max_length=100)
    courseId = models.CharField(max_length=20)
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        db_table = 'specialities'


class Series(models.Model):
    courseId = models.CharField(max_length=100)
    examClasses = models.IntegerField()
    exposureClasses = models.IntegerField()
    finalExams = models.IntegerField()
    id = models.IntegerField(primary_key=True, unique=True)
    partialExams = models.IntegerField()
    practiceClasses = models.IntegerField()
    practiceExams = models.IntegerField()
    serie = models.IntegerField()
    # specialtyId = models.CharField(max_length=20)
    # specialityId = models.ForeignKey(Specialities, on_delete=models.CASCADE, to_field='name', db_column='specialityId')
    subjectId = models.IntegerField()

    class Meta:
        db_table = 'series'


class Subjects(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    caption = models.CharField(max_length=100)
    eearNo = models.IntegerField()

    class Meta:
        db_table = 'subjects'


class SubjecstMap(models.Model):
    # subjectId = models.CharField(max_length=20, primary_key=True, unique=True)
    subjectId = models.OneToOneField(Subjects, related_name='subjects', on_delete=models.CASCADE, db_column='subjectId')
    # specialtyId = models.CharField(max_length=20)
    specialityId = models.OneToOneField(Specialities, related_name='subjectsMap', on_delete=models.CASCADE, db_column='specialityId')
    serie = models.IntegerField()

    class Meta:
        unique_together = ('subjectId', 'specialityId', 'serie')
        managed = False
        db_table = 'subjectsmap'


class Questions(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    # subjectId = models.CharField(max_length=20)
    subjectId = models.ForeignKey(Subjects, related_name='subjectsQuestions', on_delete=models.CASCADE, db_column='subjectId')
    author = models.CharField(max_length=255)
    initialFacility = models.IntegerField()
    facility = models.IntegerField()
    unit = models.IntegerField()
    subUnit = models.IntegerField()
    rightAnswer = models.CharField(max_length=1)
    body = models.TextField()
    bodyImage = models.ImageField(upload_to='aplicativo/static/assets/questions/', null=True, blank=True)
    answer1 = models.TextField()
    answer1Image = models.ImageField(upload_to='aplicativo/static/assets/questions/', null=True, blank=True)
    answer2 = models.TextField()
    answer2Image = models.ImageField(upload_to='aplicativo/static/assets/questions/', null=True, blank=True)
    answer3 = models.TextField()
    answer3Image = models.ImageField(upload_to='aplicativo/static/assets/questions/', null=True, blank=True)
    answer4 = models.TextField()
    answer4Image = models.ImageField(upload_to='aplicativo/static/assets/questions/', null=True, blank=True)
    reference = models.CharField(max_length=250)
    lastUsed = models.DateField()
    creation = models.DateField()
    questionType = models.IntegerField()
    revision = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    counterA = models.IntegerField(default=0)
    counterB = models.IntegerField(default=0)
    counterC = models.IntegerField(default=0)
    counterD = models.IntegerField(default=0)
    status = models.IntegerField(default=0)
    numberAtSU = models.IntegerField(default=0)

    class Meta:
        db_table = 'questions'


class SubjectToc(models.Model):
    subjectId = models.ForeignKey(Subjects, related_name='subjectsToc', on_delete=models.CASCADE, db_column='subjectId')
    unit = models.IntegerField()
    subunit = models.IntegerField()
    caption = models.CharField(max_length=100)
    ch = models.IntegerField()
    multiplicador = models.IntegerField(default=1)

    class Meta:
        db_table = 'subjecttoc'


class ExamType(models.Model):
    id = models.CharField(max_length=20, primary_key=True, unique=True)
    description = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'examtype'


class ExamConstrainst(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    login = models.CharField(max_length=50)
    done = models.IntegerField(default=0)
    courseId = models.CharField(max_length=20)
    specialityId = models.CharField(max_length=20)
    subjectId = models.CharField(max_length=20)
    serie = models.IntegerField()
    examType = models.ForeignKey(ExamType, db_column='examType', on_delete=models.CASCADE)
    size1 = models.IntegerField(default=0)
    bFacility1 = models.IntegerField(default=0)
    eFacility1 = models.IntegerField(default=0)
    size2 = models.IntegerField(default=0)
    bFacility2 = models.IntegerField(default=0)
    eFacility2 = models.IntegerField(default=0)
    size3 = models.IntegerField(default=0)
    bFacility3 = models.IntegerField(default=0)
    eFacility3 = models.IntegerField(default=0)
    creation = models.DateField()
    readDate = models.DateField()
    counterX0 = models.IntegerField(default=0)
    counterX9 = models.IntegerField(default=0)
    counterWarning = models.IntegerField(default=0)
    numberOfQuestions = models.IntegerField(default=0)
    applyDate = models.DateField()
    monthsFromLastUse = models.IntegerField(default=24)

    class Meta:
        db_table = 'examconstraints'


class Exam(models.Model):
    examId = models.IntegerField(db_column='id', primary_key=True, unique=False)
    classId = models.CharField(max_length=3, db_column='class')
    questionNumber = models.IntegerField()
    questionId = models.ForeignKey(Questions, db_column='questionId', on_delete=models.CASCADE)
    # models.IntegerField()
    globalFacility = models.IntegerField()
    localFacility = models.IntegerField(default=0)
    A = models.IntegerField(default=0)
    B = models.IntegerField(default=0)
    C = models.IntegerField(default=0)
    D = models.IntegerField(default=0)
    counterA = models.IntegerField(default=0)
    counterB = models.IntegerField(default=0)
    counterC = models.IntegerField(default=0)
    counterD = models.IntegerField(default=0)

    class Meta:
        db_table = 'exams'
        unique_together = ('examId', 'questionId', 'classId')


class ExamUniverse(models.Model):
    examConstraintsId = models.IntegerField(primary_key=True, unique=True)
    login = models.CharField(max_length=50)
    questionId = models.IntegerField()
    rightAnswer = models.CharField(max_length=1)
    facility = models.IntegerField()
    lastUsed = models.IntegerField()
    status = models.IntegerField(default=0)
    unit = models.IntegerField()
    subUnit = models.IntegerField()

    class Meta:
        db_table = 'examuniverse'


class ExamsStruct(models.Model):
    examConstraintsId = models.IntegerField()
    login = models.CharField(max_length=50)
    unit = models.IntegerField()
    subunit = models.IntegerField()
    ch = models.IntegerField()
    numberOfQuestions = models.IntegerField()
    questionsAvailable = models.IntegerField()

    class Meta:
        db_table = 'examstructure'
