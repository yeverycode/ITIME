from django.shortcuts import render, get_object_or_404, redirect
from .models import Lecture, Review
from .forms import ReviewForm
from django.db.models import Avg

def lecture_room(request):
    lectures = Lecture.objects.annotate(avg_rating=Avg('reviews__rating'))
    return render(request, 'lecture/lecture_room.html', {'lectures': lectures})

def lecture_detail(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    reviews = lecture.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0  # 평균 평점 계산
    return render(request, 'lecture/lecture_detail.html', {'lecture': lecture, 'reviews': reviews, 'avg_rating': avg_rating})

def add_review(request, pk):
    lecture = get_object_or_404(Lecture, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.lecture = lecture
            review.save()
            return redirect('lecture_detail', pk=lecture.pk)
    else:
        form = ReviewForm()
    return render(request, 'lecture/add_review.html', {'form': form, 'lecture': lecture})
