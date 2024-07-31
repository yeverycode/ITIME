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

from django.shortcuts import render, get_object_or_404
from .models import Lecture, Review

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, pk=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)

    total_reviews = reviews.count()

    def calculate_percentage(count):
        return (count / total_reviews) * 100 if total_reviews > 0 else 0

    context = {
        'lecture': lecture,
        'total_reviews': total_reviews,
        'no_homework_percentage': calculate_percentage(reviews.filter(homework='없음').count()),
        'average_homework_percentage': calculate_percentage(reviews.filter(homework='보통').count()),
        'many_homework_percentage': calculate_percentage(reviews.filter(homework='많음').count()),
        'no_groupwork_percentage': calculate_percentage(reviews.filter(groupwork='없음').count()),
        'average_groupwork_percentage': calculate_percentage(reviews.filter(groupwork='보통').count()),
        'many_groupwork_percentage': calculate_percentage(reviews.filter(groupwork='많음').count()),
        'generous_grading_percentage': calculate_percentage(reviews.filter(grading='너그러움').count()),
        'average_grading_percentage': calculate_percentage(reviews.filter(grading='보통').count()),
        'strict_grading_percentage': calculate_percentage(reviews.filter(grading='깐깐함').count()),
        'complex_attendance_percentage': calculate_percentage(reviews.filter(attendance='복합적').count()),
        'direct_attendance_percentage': calculate_percentage(reviews.filter(attendance='직접호명').count()),
        'designated_seating_percentage': calculate_percentage(reviews.filter(attendance='지정좌석').count()),
        'electronic_attendance_percentage': calculate_percentage(reviews.filter(attendance='전자출결').count()),
        'no_attendance_percentage': calculate_percentage(reviews.filter(attendance='반영안함').count()),
        'four_or_more_exams_percentage': calculate_percentage(reviews.filter(exams='네 번 이상').count()),
        'three_exams_percentage': calculate_percentage(reviews.filter(exams='세 번').count()),
        'two_exams_percentage': calculate_percentage(reviews.filter(exams='두 번').count()),
        'one_exam_percentage': calculate_percentage(reviews.filter(exams='한 번').count()),
        'no_exams_percentage': calculate_percentage(reviews.filter(exams='없음').count()),
        'reviews': reviews,
    }

    return render(request, 'lecture/lecture_detail.html', context)
