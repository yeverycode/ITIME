from django.shortcuts import render, get_object_or_404, redirect
from .models import Lecture, Review
from .forms import ReviewForm
from django.db.models import Q, Avg

# lecture/views.py
from django.shortcuts import render
from .models import Lecture


def lecture_room(request):
    query = request.GET.get('q')
    if query:
        lectures = Lecture.objects.filter(course_name__icontains=query) | Lecture.objects.filter(
            professor__icontains=query)
    else:
        lectures = Lecture.objects.all()

    return render(request, 'lecture/lecture_room.html', {'lectures': lectures})


def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    lecture.average_rating = average_rating
    lecture.save()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lecture = lecture
            review.save()
            return redirect('lecture_detail', lecture_id=lecture.id)
    else:
        form = ReviewForm()
    context = {
        'lecture': lecture,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'lecture/lecture_detail.html', context)


def add_review(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lecture = lecture
            review.save()
            return redirect('lecture_detail', lecture_id=lecture.id)
    else:
        form = ReviewForm()
    context = {
        'lecture': lecture,
        'form': form,
    }
    return render(request, 'lecture/add_review.html', context)


def submit_review(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        lecture = get_object_or_404(Lecture, id=lecture_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')  # 기본값 추가
        homework = request.POST.get('homework', 'N/A')  # 기본값 추가
        groupwork = request.POST.get('groupwork', 'N/A')  # 기본값 추가
        grading = request.POST.get('grading', 'N/A')  # 기본값 추가
        attendance = request.POST.get('attendance', 'N/A')  # 기본값 추가
        exams = request.POST.get('exams', 'N/A')  # 기본값 추가

        Review.objects.create(
            lecture=lecture,
            rating=rating,
            comment=comment,
            homework=homework,
            groupwork=groupwork,
            grading=grading,
            attendance=attendance,
            exams=exams
        )

        return redirect('lecture_detail', lecture_id=lecture.id)
    return redirect('lecture_room')


from django.shortcuts import render, get_object_or_404, redirect
from .models import Lecture, Review
from django.db.models import Count, Avg
from django.http import HttpResponseBadRequest


def calculate_percentage(count, total):
    return (count / total) * 100 if total > 0 else 0


def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)

    total_reviews = reviews.count()
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    star_counts = reviews.values('rating').annotate(count=Count('rating')).order_by('-rating')
    star_percentages = {item['rating']: calculate_percentage(item['count'], total_reviews) for item in star_counts}

    homework_stats = reviews.values('homework').annotate(count=Count('homework'))
    groupwork_stats = reviews.values('groupwork').annotate(count=Count('groupwork'))
    grading_stats = reviews.values('grading').annotate(count=Count('grading'))
    attendance_stats = reviews.values('attendance').annotate(count=Count('attendance'))
    exams_stats = reviews.values('exams').annotate(count=Count('exams'))

    homework_percentages = {item['homework']: calculate_percentage(item['count'], total_reviews) for item in
                            homework_stats}
    groupwork_percentages = {item['groupwork']: calculate_percentage(item['count'], total_reviews) for item in
                             groupwork_stats}
    grading_percentages = {item['grading']: calculate_percentage(item['count'], total_reviews) for item in
                           grading_stats}
    attendance_percentages = {item['attendance']: calculate_percentage(item['count'], total_reviews) for item in
                              attendance_stats}
    exams_percentages = {item['exams']: calculate_percentage(item['count'], total_reviews) for item in exams_stats}

    context = {
        'lecture': lecture,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'average_rating': average_rating,
        'star_percentages': star_percentages,
        'homework_percentages': homework_percentages,
        'groupwork_percentages': groupwork_percentages,
        'grading_percentages': grading_percentages,
        'attendance_percentages': attendance_percentages,
        'exams_percentages': exams_percentages,
    }

    return render(request, 'lecture/lecture_detail.html', context)


def submit_review(request):
    if request.method == 'POST':
        lecture_id = request.POST.get('lecture_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        homework = request.POST.get('homework')
        groupwork = request.POST.get('groupwork')
        grading = request.POST.get('grading')
        attendance = request.POST.get('attendance')
        exams = request.POST.get('exams')

        if not (lecture_id and rating):
            return HttpResponseBadRequest("Lecture ID and rating are required.")

        lecture = get_object_or_404(Lecture, id=lecture_id)

        review = Review(
            lecture=lecture,
            rating=rating,
            comment=comment,
            homework=homework,
            groupwork=groupwork,
            grading=grading,
            attendance=attendance,
            exams=exams
        )
        review.save()

        return redirect('lecture_detail', lecture_id=lecture.id)
    return HttpResponseBadRequest("Invalid request method.")
