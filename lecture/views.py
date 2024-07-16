from django.shortcuts import render, get_object_or_404, redirect
from .models import Lecture, Review
from .forms import ReviewForm
from django.db.models import Q

def lecture_room(request):
    query = request.GET.get('q')
    if query:
        lectures = Lecture.objects.filter(
            Q(course_name__icontains=query) | Q(professor__icontains=query)
        )
    else:
        lectures = Lecture.objects.all()
    context = {'lectures': lectures}
    return render(request, 'lecture/lecture_room.html', context)

def lecture_detail(request, lecture_id):
    lecture = get_object_or_404(Lecture, id=lecture_id)
    reviews = Review.objects.filter(lecture=lecture)
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