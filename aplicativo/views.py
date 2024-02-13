import json
import random
import urllib.parse
from datetime import datetime
from django.db import connection
from django.db.models import Count
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Specialities, Subjects, SubjecstMap, Questions, ExamConstrainst, Exam, ExamType, User, Hyerarchies, SubjectToc, get_password


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('provas:index')
        else:
            # messages.error(request, f'Falha ao realizar login!')
            return render(request, 'login.html')

    return render(request, 'login.html')


@login_required
def index(request):
    easyQuestions   = Questions.objects.filter(facility__gte=80, status=0)
    hardQuestions   = Questions.objects.filter(facility__lte=20, status=0)
    mediumQuestions = Questions.objects.filter(facility__gt=20, facility__lt=80, status=0)

    # Passar os dados para o template
    return render(request, 'index.html', {'user': request.user, 'image_questionsByFacility': ''}) 


@login_required
def course_view(request):
    if request.user.showCourses == 1:
        status = request.GET.get('status', None)
        course = Course.objects.all()
        return render(request, 'courses.html', {'courses': course, 'status': status})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')
    

@login_required
def savecourse_view(request):
    if request.user.editCourse == 1:
        if request.method == 'POST':  
            sigla = request.POST.get('sigla')
            descricao = request.POST.get('descricao')
            serie = request.POST.get('serie')

            # Verificar se o curso já existe
            course = Course.objects.filter(id=sigla).first()

            # Se o curso já existe, redirecione com status de erro
            if course is not None:
                course.caption = descricao
                course.numberOfSeries = serie
            else:
                course = Course(id=sigla, caption=descricao, numberOfSeries=serie) 
            try:
                course.save()
                messages.success(request, 'Curso salvo com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar curso: {str(e)}')

        return redirect('provas:courses')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:courses')


@login_required
def deletecourse_view(request, courseId):
    if request.user.removeCourse == 1:
        courseId = urllib.parse.unquote(courseId)
        course = get_object_or_404(Course, id=courseId)
        try:
            course.delete()
            messages.success(request, 'Curso deletado com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao deletar curso: {str(e)}')

        # Se o método não for POST, redirecione com status de erro
        return redirect('provas:courses')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:courses')


@login_required
def specialty_view(request):
    if request.user.showSpecialities == 1:
        specialities = Specialities.objects.all()
        # Mapeia especialidade - Série - Matérias
        especialidades_data = []
        for especialidade in specialities:
            especialidade_dict = {especialidade: {}}
            for subjects in SubjecstMap.objects.filter(specialityId=especialidade).values('subjectId__id', 'subjectId__caption', 'specialityId', 'serie').order_by('serie'):
                if subjects['serie'] not in especialidade_dict[especialidade]:
                    especialidade_dict[especialidade][subjects['serie']] = []
                
                especialidade_dict[especialidade][subjects['serie']].append({'subjectId': subjects['subjectId__id'], 'subjectName': subjects['subjectId__caption']})
            especialidades_data.append(especialidade_dict)

        course = Course.objects.all()
        return render(request, 'specialities.html', {'specialities': especialidades_data, 'courses': course})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def saveSpecialty_view(request):
    if request.user.editSpeciality == 1:
        if request.method == 'POST':  
            data = json.loads(request.body)
            courseId = data.get('curso_id')
            name = data.get('espec_id')
            description = data.get('descricao')
            subjectsBySeries = data.get('subjectsBySeries', [])
            specialtyId = f"{courseId}_{name}"

            # Verificar se o curso já existe
            specialty = Specialities.objects.filter(id=specialtyId).first()

            # Se o curso já existe, redirecione com status de erro
            if specialty is not None:
                specialty.description = description
                with connection.cursor() as cursor:
                    sql = "DELETE FROM subjectsmap WHERE specialityId = %s"
                    cursor.execute(sql, [specialtyId])
            else:
                specialty = Specialities(id=specialtyId,name=name,courseId=courseId,caption=description) 

            for i in range(1, len(subjectsBySeries)+1, 1):
                subjects = subjectsBySeries[i-1][str(i)]
                for subject in subjects:
                    subjectId   = get_object_or_404(Subjects, id=subject)
                    subject_map = SubjecstMap(specialityId=specialty,subjectId=subjectId,serie=i) 
                    subject_map.save()

            try:
                specialty.save()
                messages.success(request, 'Especialidade salva com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar especialidade: {str(e)}')

        return JsonResponse({})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return JsonResponse({})


@login_required
def series_view(request):
    espec_id = request.POST.get('espec_id')
    curso_id = request.POST.get('curso_id')
    course = get_object_or_404(Course, id=curso_id)
    subjects = Subjects.objects.all()
    subject_data = [{'id': subject.id, 'caption': subject.caption} for subject in subjects]

    select_subjects = {}
    for subjects in SubjecstMap.objects.filter(specialityId=f'{curso_id}_{espec_id}').values('subjectId__id', 'subjectId__caption', 'specialityId', 'serie').order_by('serie'):
        if subjects['serie'] not in select_subjects:
            select_subjects[subjects['serie']] = []
        
        select_subjects[subjects['serie']].append({'subjectId': subjects['subjectId__id'], 'subjectName': subjects['subjectId__caption']})

    return JsonResponse({'series': course.numberOfSeries, 'subjects': subject_data, 'selectSubjects': select_subjects})


@login_required
def deleteSpecialty_view(request, specialtyId):
    if request.user.removeSpeciality == 1:
        specialtyId = urllib.parse.unquote(specialtyId)
        specialty = get_object_or_404(Specialities, id=specialtyId)
        try:
            specialty.delete()
            messages.success(request, 'Especialidade deletada com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao deletar especialidade: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
    
    return redirect('provas:specialties')


@login_required
def subjects_view(request):
    if request.user.showSubjects == 1:
        subjects = Subjects.objects.all()
        return render(request, 'subjects.html', {'subjects': subjects})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def savesubject_view(request):
    if request.user.editSubject == 1:
        if request.method == 'POST':  
            sigla = request.POST.get('sigla')
            descricao = request.POST.get('descricao')
            cod_area = request.POST.get('cod_area')

            # Verificar se o curso já existe
            subject = Subjects.objects.filter(id=sigla).first()

            # Se o curso já existe, redirecione com status de erro
            if subject is not None:
                subject.caption = descricao
                subject.eearNo = cod_area
            else:
                subject = Subjects(id=sigla, caption=descricao, eearNo=cod_area) 

            try:
                subject.save()
                messages.success(request, 'Disciplina salva com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar disciplina: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')

    return redirect('provas:subjects')


@login_required
def deletesubject_view(request, subjectId):
    if request.user.removeSubject == 1:
        subjectId = urllib.parse.unquote(subjectId)
        subject = get_object_or_404(Subjects, id=subjectId)
        try:
            subject.delete()
            messages.success(request, 'Disciplina deletada com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao deletar disciplina: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')

    return redirect('provas:subjects')


@login_required
def questions_view(request):
    if request.user.showQuestions == 1:
        sql = """ select count(questions.id) as 'numberOfQuestions', questions.subjectId, subjects.caption as 'subjectCaption', specialities.caption, subjectsmap.serie
        from questions
        join subjects on questions.subjectId = subjects.id
        join subjectsmap on subjectsmap.subjectId = subjects.id
        join specialities on specialities.id = subjectsmap.specialityId
        group by questions.subjectId, subjects.caption, specialities.caption, subjectsmap.serie """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()

        questions = []
        for row in result:
            questions.append({
                'url': urllib.parse.quote(row[1], safe=''),
                'id': row[1],
                'caption': row[2],
                'num_questions': row[0],
                'data_tooltip': 'Série: ' + str(row[4]) + ' - Especialidade: ' + row[3]
            })
        # Select da soma de questões por disciplina
        # for question in Subjects.objects.annotate(num_questions=Count('subjectsQuestions')):
        #     for subjectMap in SubjecstMap.objects.filter(subjectId=question).values('specialityId__name', 'serie'):
        #         questions.append({
        #             'url': urllib.parse.quote(question.id, safe=''),
        #             'id': question.id,
        #             'caption': question.caption,
        #             'num_questions': question.num_questions,
        #             'data_tooltip': 'Série: ' + str(subjectMap['serie']) + ' - Especialidade: ' + subjectMap['specialityId__name']
        #         })
        return render(request, 'questions.html', {'questions': questions})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def subunit_view(request, subjectId):
    if request.user.showQuestions == 1:
        subjectId = urllib.parse.unquote(subjectId)
        sql = f"""
            select count(questions.id) as 'qtd_questoes', subjecttoc.unit, subjecttoc.subunit, subjecttoc.caption,
            subjecttoc.CH, subjecttoc.multiplicador, subjecttoc.ch * subjecttoc.multiplicador as 'numberMinQuestions'
            from questions
            join subjecttoc on questions.subjectId = subjecttoc.subjectId
            where questions.subjectId = '{subjectId}' 
            group by subjecttoc.unit, subjecttoc.subunit, subjecttoc.caption, subjecttoc.CH, subjecttoc.multiplicador, 'numberMinQuestions'
            order by subjecttoc.unit, subjecttoc.subunit;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
        subunits = []
        for r in result:
            subunits.append({
                "unit": r[1],
                "subunit": r[2],
                "caption": r[3],
                "qtd_questoes": r[0],
                "ch": r[4],
                "multiplicador": r[5],
                "numberMinQuestions": r[6],
            })
        return render(request, 'subunit.html', {'subunits': subunits, 'subjectId': subjectId})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def chSave_view(request, subjectId):
    if request.user.editSubjectCH == 1:
        if request.method == 'POST':  
            unidade = request.POST.get('unidade')
            subunidade = request.POST.get('subunidade')
            ch = request.POST.get('ch')
            caption = request.POST.get('caption')
            multiplicador = request.POST.get('multiplicador')

            sql = f"""Update subjecttoc set ch = {ch}, caption = '{caption}', multiplicador = {multiplicador} 
                    where subjectId = '{subjectId}' and unit = '{unidade}' and subunit = '{subunidade}';"""
            try:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                messages.success(request, 'Carga horária salva com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar carga horária: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')

    return redirect('provas:subUnit', subjectId)


@login_required
def questionDetails_view(request, subjectId):
    if request.user.showQuestions == 1:
        subjectId = urllib.parse.unquote(subjectId)
        questions = Questions.objects.filter(subjectId=subjectId).order_by('id')
        return render(request, 'questionsDetails.html', {'questions': questions, 'subjectId': subjectId})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def questionOpen_view(request, subjectId, questionId):
    if request.user.previewQuestion == 1:
        question = get_object_or_404(Questions, id=questionId)
        bodyImage = str(question.bodyImage).split('assets/')[-1]
        answer1Image = str(question.answer1Image).split('assets/')[-1]
        answer2Image = str(question.answer2Image).split('assets/')[-1]
        answer3Image = str(question.answer3Image).split('assets/')[-1]
        answer4Image = str(question.answer4Image).split('assets/')[-1]
        return render(request, 'questionOpen.html', {"question": question, 'bodyImage': bodyImage, 'answer1Image': answer1Image, 
                                                     'answer2Image': answer2Image, 'answer3Image': answer3Image, 'answer4Image': answer4Image, 'subjectId': subjectId})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:questions') 
    

@login_required
def questionEdit_view(request, subjectId=None, questionId=None):
    if request.user.editQuestion == 1:
        question = {}
        bodyImage = ''
        answer1Image = ''
        answer2Image = ''
        answer3Image = ''
        answer4Image = ''
        mode = 'insert'
        if questionId is not None:
            question = get_object_or_404(Questions, id=questionId)
            mode = 'edit'

            if question.bodyImage is not None:
                bodyImage = str(question.bodyImage).split('assets/')[-1]
            if question.answer1Image is not None:
                answer1Image = str(question.answer1Image).split('assets/')[-1]
            if question.answer2Image is not None:
                answer2Image = str(question.answer2Image).split('assets/')[-1]
            if question.answer3Image is not None:
                answer3Image = str(question.answer3Image).split('assets/')[-1]
            if question.answer4Image is not None:
                answer4Image = str(question.answer4Image).split('assets/')[-1]

        subjects = Subjects.objects.all()

        context = {"question": question, 'bodyImage': bodyImage, 'answer1Image': answer1Image, 'answer2Image': answer2Image, 'answer3Image': answer3Image, 'answer4Image': answer4Image, 
                   'subjectId': subjectId, 'subjects': subjects, 'mode': mode, 'author': request.user.realName, "creation": datetime.now().date()}
        return render(request, 'questionEdit.html', context)
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:questions')


def handle_uploaded_image(image):
    from django.core.files.uploadedfile import InMemoryUploadedFile
    from io import BytesIO
    from PIL import Image
    import uuid

    # Função para lidar com o upload de imagem
    image = Image.open(image)

    # Gere um nome de arquivo único para a imagem
    filename = f"{uuid.uuid4().hex}.png"

    # Salve a imagem em BytesIO
    image_io = BytesIO()
    image.save(image_io, format='PNG')  # Pode ajustar o formato conforme necessário

    # Crie um novo InMemoryUploadedFile
    image_file = InMemoryUploadedFile(image_io, None, filename, 'image/png', image_io.tell(), None)

    return image_file


@login_required
def questionSave_view(request, subjectId=None, questionId=None):
    if request.user.editQuestion == 1:
        if request.method == 'POST':  
            subjectId = request.POST.get('subject')
            subject = get_object_or_404(Subjects, id=subjectId)
            author = request.POST.get('author')
            # creationDate = request.POST.get('creation_date')
            facility = request.POST.get('facility')
            unit = request.POST.get('unit')
            subunit = request.POST.get('subunit')
            reference = request.POST.get('reference')
            body = request.POST.get('body')
            bodyImage = request.FILES.get('bodyImage', None)
            answer1 = request.POST.get('answer1')
            answer1Image = request.FILES.get('answer1Image', None)
            answer2 = request.POST.get('answer2')
            answer2Image = request.FILES.get('answer2Image', None)
            answer3 = request.POST.get('answer3')
            answer3Image = request.FILES.get('answer3Image', None)
            answer4 = request.POST.get('answer4')
            answer4Image = request.FILES.get('answer4Image', None)
            correctAnswer = request.POST.get('correct-answer')

            if questionId is not None:
                mode = 'edit'
                question_tosave = Questions.objects.filter(id=questionId).first()
                question_tosave.subjectId = subject
                question_tosave.author = author
                question_tosave.facility = facility
                question_tosave.unit = unit
                question_tosave.subUnit = subunit
                question_tosave.reference = reference
                question_tosave.body = body
                if bodyImage is not None:
                    question_tosave.bodyImage = handle_uploaded_image(bodyImage)
                question_tosave.answer1 = answer1
                question_tosave.answer2 = answer2
                question_tosave.answer3 = answer3
                question_tosave.answer4 = answer4
                if correctAnswer is not None:
                    question_tosave.rightAnswer = correctAnswer
                if answer1Image is not None:
                    question_tosave.answer1Image = handle_uploaded_image(answer1Image)
                if answer2Image is not None:
                    question_tosave.answer2Image = handle_uploaded_image(answer2Image)
                if answer3Image is not None:
                    question_tosave.answer3Image = handle_uploaded_image(answer3Image)
                if answer4Image is not None:
                    question_tosave.answer4Image = handle_uploaded_image(answer4Image)
            else:
                mode = 'insert'
                question_tosave=Questions(subjectId=subject,author=author,facility=facility,initialFacility=facility,unit=unit,subUnit=subunit,reference=reference,
                body=body,answer1=answer1,answer2=answer2,answer3=answer3,answer4=answer4,rightAnswer=correctAnswer,questionType=0,creation=datetime.now().date())
            
            question_tosave.bodyImage = handle_uploaded_image(bodyImage) if bodyImage is not None else ''
            question_tosave.answer1Image = handle_uploaded_image(answer1Image) if answer1Image is not None else ''
            question_tosave.answer2Image = handle_uploaded_image(answer2Image) if answer2Image is not None else ''
            question_tosave.answer3Image = handle_uploaded_image(answer3Image) if answer3Image is not None else ''
            question_tosave.answer4Image = handle_uploaded_image(answer4Image) if answer4Image is not None else ''
            try:
                question_tosave.save()
                questionId = question_tosave.id
                messages.success(request, 'Questão salva com sucesso.')

                with connection.cursor() as cursor:
                    cursor.execute(f"SELECT * FROM SUBJECTTOC WHERE UNIT = '{question_tosave.unit}' AND SUBUNIT = {question_tosave.subUnit} AND SUBJECTID = '{question_tosave.subjectId.id}';")
                    subjecttoc = cursor.fetchone()
                    if subjecttoc is None:
                        cursor.execute(f"INSERT INTO SUBJECTTOC (UNIT, SUBUNIT, SUBJECTID, CH, MULTIPLICADOR) VALUES ('{question_tosave.unit}', '{question_tosave.subUnit}', '{question_tosave.subjectId.id}', 3, 6);")
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar questão: {str(e)}')

            return redirect('provas:openQuestion', subjectId=subjectId, questionId=questionId)
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:questions')


@login_required
def questionDelete_view(request, questionId):
    question = get_object_or_404(Questions, id=questionId)
    subjectId = question.subjectId.id

    if request.user.deleteQuestion == 1:
        question.status = 1
        try:
            question.save()
            messages.success(request, 'Questão inativada com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao inativar questão: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')

    return redirect('provas:questionDetails', subjectId)


@login_required
def exams_view(request):
    if request.user.showExams == 1:
        exams = ExamConstrainst.objects.exclude(numberOfQuestions=0).order_by('-applyDate')
        courses = Course.objects.all()
        examTypes = ExamType.objects.all()
        return render(request, 'exams.html', {'exams': exams, 'courses': courses, 'examTypes': examTypes})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def examDetails_view(request, examId):
    if request.user.showExamDetails == 1:
        examDetails = Exam.objects.filter(examId=examId).order_by('classId', 'questionNumber')
        return render(request, 'examDetails.html', {'examDetails': examDetails, 'examId': examId})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:exams')
    

@login_required
def examsSpecialties_view(request, courseId):
    numberOfSeries = get_object_or_404(Course, id=courseId)
    specialities_data = []
    specialities = Specialities.objects.filter(courseId=courseId)
    specialities_data = [{'id': spec.name, 'caption': spec.caption} for spec in specialities]
    return JsonResponse({'numberOfSeries': numberOfSeries.numberOfSeries, 'specialities': specialities_data})


@login_required
def examsSubjects_view(request, courseId, specialtyId, serie):
    subjects_data = []
    speciality    = Specialities.objects.filter(name=specialtyId).first()
    subjects_map  = SubjecstMap.objects.filter(specialityId=speciality, serie=serie).values('subjectId__id', 'subjectId__caption')

    subjects_data = [{'id': subject['subjectId__id'], 'caption': subject['subjectId__caption']} for subject in subjects_map]
    return JsonResponse({'subjects': subjects_data})


@login_required
def examsQuestions_view(request, courseId, specialtyId, serie, subjectId):

    return ''


@login_required
def examSave_view(request):
    if request.user.createExam == 1:
        if request.method == 'POST':  
            courseId = request.POST.get('courseId') + "/" + request.POST.get('examType')
            specialityId = request.POST.get('specialityId')
            serie = request.POST.get('serie')
            subjectId = request.POST.get('subjectId')
            examType = request.POST.get('examType')
            examTypeObj = ExamType.objects.filter(id=examType).first()
            numberOfQuestions = request.POST.get('numberOfQuestions')
            applyDate = request.POST.get('applyDate')
            unit1 = 1 if request.POST.get('unit1') == 'on' else 0
            unit2 = 2 if request.POST.get('unit2') == 'on' else 0
            unit3 = 3 if request.POST.get('unit3') == 'on' else 0
            unit4 = 4 if request.POST.get('unit4') == 'on' else 0

            exam = None
            if exam is not None:
                pass
            else:
                exam = ExamConstrainst(login=request.user.username,courseId=courseId,specialityId=specialityId,subjectId=subjectId,serie=serie,
                                    examType=examTypeObj,creation=datetime.now().date(),readDate=datetime.now().date(),applyDate=applyDate,numberOfQuestions=numberOfQuestions)
            try:
                exam.save()
                question_list = generateExamQuestions(request, exam, unit1, unit2, unit3, unit4)
                generateExamStruct(request, exam, request.user)
                generateExamUniverse(request, exam.id, request.user, question_list)
                messages.success(request, 'Exame salvo com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar exame: {str(e)}')
        return redirect('provas:examLoad', exam.id, 'X0')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:exams')


@login_required
def generateExamQuestions(request, exam: ExamConstrainst, unit1, unit2, unit3, unit4):
    dificulty = {
        'facil': 30,
        'media': 50,
        'dificil': 20
    }
    qtd_questions = {
        'facil': int(exam.numberOfQuestions) * dificulty['facil'] / 100,
        'media': int(exam.numberOfQuestions) * dificulty['media'] / 100,
        'dificil': int(exam.numberOfQuestions) * dificulty['dificil'] / 100
    }

    subjectId = Subjects.objects.get(id=exam.subjectId)

    easyQuestions   = Questions.objects.filter(facility__gte=80, subjectId=subjectId, status=0, unit__in=[unit1, unit2, unit3, unit4])
    hardQuestions   = Questions.objects.filter(facility__lte=20, subjectId=subjectId, status=0, unit__in=[unit1, unit2, unit3, unit4])
    mediumQuestions = Questions.objects.filter(facility__gt=20, facility__lt=80, subjectId=subjectId, status=0, unit__in=[unit1, unit2, unit3, unit4])

    # Seleciona aleatoriamente 10 objetos de cada categoria
    easy_questions_random = random.sample(list(easyQuestions), min(int(qtd_questions['facil']), len(easyQuestions)))
    hard_questions_random = random.sample(list(hardQuestions), min(int(qtd_questions['dificil']), len(hardQuestions)))
    medium_questions_random = random.sample(list(mediumQuestions), min(int(qtd_questions['media']), len(mediumQuestions)))

    question_list = easy_questions_random + medium_questions_random + hard_questions_random

    exam_question = ""
    for i in range(2):
        random.shuffle(question_list)
        counter = 0
        classId = 'X0' if i == 0 else 'X9'
        for question in question_list:
            counter += 1
            exam_question += f"""INSERT INTO exams (id, class, questionNumber, questionId, globalFacility, localFacility, A, B, C, D, counterA, counterB, counterC, counterD) VALUES ({exam.id}, '{classId}', {counter}, {question.id}, {question.facility}, 0, {1 if question.rightAnswer == 'A' else 0}, {1 if question.rightAnswer == 'B' else 0}, {1 if question.rightAnswer == 'C' else 0}, {1 if question.rightAnswer == 'D' else 0}, 0, 0, 0, 0);"""

    # Executa o SQL
    with connection.cursor() as cursor:
        cursor.execute(exam_question)

    # Certifique-se de chamar commit para salvar as alterações no banco de dados
    connection.commit()

    return question_list


@login_required
def generateExamStruct(request, exam: ExamConstrainst, user):
    sql = f"""select exams.id, questions.unit, questions.subunit, count(exams.questionId) as count from exams
                join questions on questions.id = exams.questionId
                where exams.id = {exam.id} and exams.class = 'X0'
                group by exams.id, questions.unit, questions.subunit;"""
    
    # Executa a consulta SQL
    with connection.cursor() as cursor:
        cursor.execute(sql)
        result = cursor.fetchall()

    insert_sql = ''
    # 'result' conterá os resultados da consulta
    for row in result:
        exam_id, unit, subunit, count = row
        # Substitua este SQL pelo SQL que você deseja executar para inserção
        insert_sql += f"""
            INSERT INTO examstructure (examConstraintsId, login, unit, subunit, ch, numberOfQuestions, questionsAvailable)
            VALUES ({exam_id}, '{user.username}', '{unit}', '{subunit}', 0, {count}, 0);
        """

        # Executa o SQL para inserção
        with connection.cursor() as cursor:
            cursor.execute(insert_sql)

        # Certifique-se de chamar commit para salvar as alterações no banco de dados
        connection.commit()


@login_required
def generateExamUniverse(request, examId, user, questions):
    sql = ''
    for question in questions:
        sql += f"""Insert into examuniverse values ({examId}, '{user.username}', {question.id}, '{question.rightAnswer}', {question.facility}, '{question.lastUsed}', {question.status}, {question.unit}, {question.subUnit}); """
    
    # Executa o SQL para inserção
    with connection.cursor() as cursor:
        cursor.execute(sql)

    # Certifique-se de chamar commit para salvar as alterações no banco de dados
    connection.commit()


@login_required
def examLoad_view(request, examId, type):
    exam_code_map = {
        "PrU": {"X0": "10", "X9": "19"},
        "PrP1": {"X0": "10", "X9": "19"},
        "PrP2": {"X0": "20", "X9": "29"},
        "PrP2": {"X0": "30", "X9": "39"},
        "PrFi": {"X0": "60", "X9": "69"},
        "Pr2E": {"X0": "70", "X9": "72"},
        "Pr2C": {"X0": "10/20/30", "X9": "10/20/30"},
    }
    exam_details  = ExamConstrainst.objects.filter(id=examId).first()
    exam_code = exam_code_map.get(exam_details.examType.id, {}).get(type, "")
    question_list = Exam.objects.filter(examId=examId, classId=type).order_by('questionNumber')
    images_dict = {}
    for question in question_list:
        images_dict[question.questionNumber] = {
            "bodyImage": str(question.questionId.bodyImage).split('assets/')[-1],
            "answer1Image": str(question.questionId.answer1Image).split('assets/')[-1],
            "answer2Image": str(question.questionId.answer2Image).split('assets/')[-1],
            "answer3Image": str(question.questionId.answer3Image).split('assets/')[-1],
            "answer4Image": str(question.questionId.answer4Image).split('assets/')[-1]
        }

    return render(request, 'examLoad.html', {'exam': exam_details, 'questions': question_list, "exam_code": exam_code, 'images_dict': images_dict})


@login_required
def examDelete_view(request, examId):
    if request.user.removeExam == 1:
        examId = urllib.parse.unquote(examId)
        exam = get_object_or_404(ExamConstrainst, id=examId)

        sql = f"Delete from exams where id = {examId}; Delete from examuniverse where examConstraintsId = {examId}; Delete from examstructure where examConstraintsId = {examId}"
        try:
            exam.delete()
            # Executa o SQL para inserção
            with connection.cursor() as cursor:
                cursor.execute(sql)

            # Certifique-se de chamar commit para salvar as alterações no banco de dados
            connection.commit()
            messages.success(request, 'Prova deletada com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao deletar prova: {str(e)}')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')

    return redirect('provas:exams')


@login_required
def users_view(request):
    if request.user.removeExam == 1:
        users = User.objects.all()
        hyerarchies = Hyerarchies.objects.all()
        access_map = {
            "1": {"id": "showCourses", "caption": "Ver Cursos"},
            "2": {"id": "editCourse", "caption": "Editar Cursos"},
            "3": {"id": "mapCourse", "caption": "Mapear Cursos"},
            "4": {"id": "removeCourse", "caption": "Remover Cursos"},
            "5": {"id": "showSpecialities", "caption": "Ver Especialidades"},
            "6": {"id": "editSpeciality", "caption": "Editar Especialidades"},
            "7": {"id": "mapSpeciality", "caption": "Mapear Especialidades"},
            "8": {"id": "removeSpeciality", "caption": "Remover Especialidades"},
            "9": {"id": "showSubjects", "caption": "Ver Matérias"},
            "10": {"id": "editSubject", "caption": "Editar Matérias"},
            "11": {"id": "removeSubject", "caption": "Remover Matérias"},
            "12": {"id": "showQuestions", "caption": "Ver Questões"},
            "13": {"id": "editQuestion", "caption": "Editar Questões"},
            "14": {"id": "previewQuestion", "caption": "Preview Questões"},
            "15": {"id": "deleteQuestion", "caption": "Deletar Questões"},
            "16": {"id": "showExams", "caption": "Ver Provas"},
            "17": {"id": "showExamDetails", "caption": "Ver Detalhes da Prova"},
            "18": {"id": "createExam", "caption": "Criar Prova"},
            "19": {"id": "correctExam", "caption": "Corrigir Prova"},
            "20": {"id": "removeExam", "caption": "Remover Prova"},
            "21": {"id": "adminUsers", "caption": "Administrar Usuários"},
            "22": {"id": "showLogs", "caption": "Ver Logs"},
            "23": {"id": "editSubjectCH", "caption": "Editar Matérias CH"},
            "24": {"id": "revisionOkQuestion", "caption": "Revisar Questões"},
            "25": {"id": "backupFull", "caption": "Backup Total"},
            "27": {"id": "backupPartial", "caption": "Backup Parcial"}
        }
        return render(request, 'users.html', {'users': users, 'hyerarchies': hyerarchies, 'access_map': access_map})
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def userSave_view(request):
    if request.user.removeExam == 1:
        if request.method == 'POST':  
            hyerarchy = request.POST.get('hyerarchy')
            hyerarchyObj = get_object_or_404(Hyerarchies, hyerarchy=hyerarchy)
            username = request.POST.get('username')
            realName = request.POST.get('realName')
            showCourses = 1 if request.POST.get('showCourses') == 'on' else 0
            editCourse = 1 if request.POST.get('editCourse') == 'on' else 0
            mapCourse = 1 if request.POST.get('mapCourse') == 'on' else 0
            removeCourse = 1 if request.POST.get('removeCourse') == 'on' else 0
            showSpecialities = 1 if request.POST.get('showSpecialities') == 'on' else 0
            editSpeciality = 1 if request.POST.get('editSpeciality') == 'on' else 0
            mapSpeciality = 1 if request.POST.get('mapSpeciality') == 'on' else 0
            removeSpeciality = 1 if request.POST.get('removeSpeciality') == 'on' else 0
            showSubjects = 1 if request.POST.get('showSubjects') == 'on' else 0
            editSubject = 1 if request.POST.get('editSubject') == 'on' else 0
            removeSubject = 1 if request.POST.get('removeSubject') == 'on' else 0
            showQuestions = 1 if request.POST.get('showQuestions') == 'on' else 0
            editQuestion = 1 if request.POST.get('editQuestion') == 'on' else 0
            previewQuestion = 1 if request.POST.get('previewQuestion') == 'on' else 0
            showExams = 1 if request.POST.get('showExams') == 'on' else 0
            showExamDetails = 1 if request.POST.get('showExamDetails') == 'on' else 0
            createExam = 1 if request.POST.get('createExam') == 'on' else 0
            correctExam = 1 if request.POST.get('correctExam') == 'on' else 0
            removeExam = 1 if request.POST.get('removeExam') == 'on' else 0
            adminUsers = 1 if request.POST.get('adminUsers') == 'on' else 0
            showLogs = 1 if request.POST.get('showLogs') == 'on' else 0
            editSubjectCH = 1 if request.POST.get('editSubjectCH') == 'on' else 0
            revisionOkQuestion = 1 if request.POST.get('revisionOkQuestion') == 'on' else 0
            backupFull = 1 if request.POST.get('backupFull') == 'on' else 0
            backupPartial = 1 if request.POST.get('backupPartial') == 'on' else 0

            password = get_password(request.POST.get('senha-atual'))
            new_password = request.POST.get('senha-nova')
            confirm_password = request.POST.get('senha-confirmacao')

            user = User.objects.filter(username=username).first()

            # Se o curso já existe
            if user is not None:
                if user.password != password:
                    messages.error(request, f'A senha atual não está correta')   
                    return redirect('provas:users')  
    
                if new_password != confirm_password:
                    messages.error(request, f'A nova senha não coincide')   
                    return redirect('provas:users')

                user.realName=realName
                user.password=get_password(new_password)
                user.showCourses=showCourses
                user.editCourse=editCourse
                user.mapCourse=mapCourse
                user.removeCourse=removeCourse
                user.showSpecialities=showSpecialities
                user.editSpeciality=editSpeciality
                user.mapSpeciality=mapSpeciality
                user.removeSpeciality=removeSpeciality
                user.showSubjects=showSubjects
                user.editSubject=editSubject
                user.removeSubject=removeSubject
                user.showQuestions=showQuestions
                user.editQuestion=editQuestion
                user.previewQuestion=previewQuestion
                user.showExams=showExams
                user.showExamDetails=showExamDetails
                user.createExam=createExam
                user.correctExam=correctExam
                user.removeExam=removeExam
                user.adminUsers=adminUsers
                user.showLogs=showLogs
                user.editSubjectCH=editSubjectCH
                user.hyerarchy=hyerarchyObj
                user.revisionOkQuestion=revisionOkQuestion
                user.backupFull=backupFull
                user.backupPartial=backupPartial
            else:
                user=User(username=username,realName=realName,password=password,accessLevel=0,showCourses=showCourses,editCourse=editCourse,mapCourse=mapCourse,
                        removeCourse=removeCourse,showSpecialities=showSpecialities,editSpeciality=editSpeciality,mapSpeciality=mapSpeciality,
                        removeSpeciality=removeSpeciality,showSubjects=showSubjects,editSubject=editSubject,removeSubject=removeSubject,
                        showQuestions=showQuestions,editQuestion=editQuestion,previewQuestion=previewQuestion,showExams=showExams,showExamDetails=showExamDetails,
                        createExam=createExam,correctExam=correctExam,removeExam=removeExam,adminUsers=adminUsers,showLogs=showLogs,editSubjectCH=editSubjectCH,
                        hyerarchy=hyerarchyObj,revisionOkQuestion=revisionOkQuestion,backupFull=backupFull,backupPartial=backupPartial)
            try:
                user.save()
                messages.success(request, 'Usuário salvo com sucesso.')
            except Exception as e:
                print(e)
                messages.error(request, f'Erro ao salvar usuário: {str(e)}')

        return redirect('provas:users')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def userDelete_view(request, username):
    if request.user.removeExam == 1:
        user = get_object_or_404(User, username=username)
        try:
            user.delete()
            messages.success(request, 'Usuário deletado com sucesso.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao deletar usuário questão: {str(e)}')

        return redirect('provas:users')
    else:
        messages.error(request, f'O usuário não possui acessos suficientes para acessar essa view!')
        return redirect('provas:index')


@login_required
def userChangePassword_view(request, username):
    if request.method == 'POST':  
        senhaAtual = get_password(request.POST.get('senha-atual'))
        senhaNova = request.POST.get('senha-nova')
        senhaConfirmacao = request.POST.get('senha-confirmacao')

        user = get_object_or_404(User, username=username)

        if user.password != senhaAtual:
            messages.error(request, f'Erro ao trocar senha: a senha atual está incorreta')     
            return redirect('provas:users')
        
        if senhaNova != senhaConfirmacao:
            messages.error(request, f'Erro ao trocar senha: as senhas não coincidem')     
            return redirect('provas:users')

        try:
            user.password = get_password(senhaNova)
            user.save()
            messages.success(request, 'Senha trocada com sucesso!.')
        except Exception as e:
            print(e)
            messages.error(request, f'Erro ao trocar senha: {str(e)}')

        return redirect('provas:users')


def logout_view(request):
    logout(request)
    return redirect('provas:login')