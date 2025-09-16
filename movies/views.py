from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Like
from django.contrib.auth.decorators import login_required
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    liked_reviews = list(
    Like.objects.filter(user=request.user).values_list('review', flat=True)
)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    template_data['liked_reviews'] = liked_reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def like_review(request, id, review_id):
    try:
        like = Like.objects.get(user=request.user, review =Review.objects.get(id=review_id))
    except Like.DoesNotExist:
        like = None
    if like == None:
        newLike = Like()
        newLike.review = Review.objects.get(id=review_id)
        newLike.user = request.user
        newLike.save()
        newLike.review.likeCount = Like.objects.filter(review = Review.objects.get(id=review_id)).count()
        newLike.review.save()
        return redirect('movies.show', id=id)   
    else:
        review = like.review
        like.delete()
        review.likeCount = Like.objects.filter(review = Review.objects.get(id=review_id)).count()
        review.save()
        return redirect('movies.show', id=id)

    
