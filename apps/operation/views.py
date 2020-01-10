import datetime
import random

from django.shortcuts import render
from .models import MovieInfo
# Create your views here.
from django.views import View

from operation.models import Default5Recommend, Top5Recommend
from django.forms.models import model_to_dict

def recommendForUser(request):
    """
        向用户进行top5推荐
            如果用户已经登陆， 从default和top中进行混合随机推荐
            如果用户没有登陆， 从default中进行推荐
    :param request:
    :return:
    """
    user = request.user
    user_recommend_movies = None
    default_recommend_movies = list(map(lambda x: x.movie
                                        , list(Default5Recommend.objects.filter(redate=datetime.date.today()))))
    if user.is_authenticated:
        # 如果用户已经登陆
        user_recommend_movies = list(map(lambda x: x.movie
                                         , list(Top5Recommend.objects.filter(user_id__in=[user.id]))))
        # defautl和recommend随机选取5个， 同时避免了recommend不足5个的情况
        user_recommend_movies = user_recommend_movies + default_recommend_movies
        # print(user_recommend_movies)
        user_recommend_movies = random.sample(user_recommend_movies, 5)
    else:
        # 如果用户没有登陆
        user_recommend_movies = default_recommend_movies
    return user_recommend_movies


class IndexView(View):
    def get(self, request):
        # 用户登陆则推荐电影， 否则推荐默认电影（固定五部）
        # return render(request, 'index.html', {})
        user = request.user
        # de_recommend = list(DefaultPop5Result.objects.filter(redate=datetime.date.today())\
        #     .values('movie__moviename', 'movie__averating', 'movie__description', 'movie__picture'))
        # de_recommend = list(map(lambda x: x.movie
        # , list(Default5Recommend.objects.filter(redate=datetime.date.today()))))
        # user_recommend_movie = None
        # if user.is_authenticated:
        #     # recommend_movie = list(Top5Recomm.objects.filter(user_id__in=[user.id])\
        #     #     .values('movie__moviename', 'movie__averating', 'movie__description', 'movie__picture'))
        #     user_recommend_movie = list(map(lambda x: x.movie
        #                            , list(Top5Recommend.objects.filter(user_id__in=[user.id]))))
        #     # defautl和recommend随机选取5个， 同时避免了recommend不足5个的情况
        #     user_recommend_movie = user_recommend_movie + de_recommend
        #     user_recommend_movie = random.sample(user_recommend_movie, 5)
        # else:
        #     user_recommend_movie = de_recommend


        user_recommend_movie = recommendForUser(request=request)
        user_recommend_movie_dict = list()

        for movie in user_recommend_movie:
            movie = model_to_dict(movie)
            score = int(movie["averating"]+0.5)
            movie["stars"] = [(i<score) for i in range(5)]
            user_recommend_movie_dict.append(movie)

        print(user_recommend_movie_dict)

        all_movieinfo = MovieInfo.objects.all().order_by('-releasedate')
        
        all_movieinfo_dict = list()
        for movie in all_movieinfo:
            movie = model_to_dict(movie)
            score = int(movie["averating"]+0.5)
            movie["stars"] = [(i<score) for i in range(5)]
            all_movieinfo_dict.append(movie)

        top1info = all_movieinfo_dict[0]
        movieinfo = all_movieinfo_dict[9:18]
        movietitle = all_movieinfo_dict[1]
        movielatest = all_movieinfo_dict[1:9]
        return render(request, 'index.html', {
            "top1info": top1info,
            "movieinfo": movieinfo,
            "movietitle": movietitle,
            "movielatest": movielatest,
            "user_recommend_movie": user_recommend_movie_dict,
        })



        # return render(request, 'index.html', {
        #     "moiveinfo": None,
        #     "movietitle": None,
        #     "movielatest": None,
        #     "user_recommend_movie": None,
        # })