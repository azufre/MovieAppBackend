
import json
from authentication.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Movie, RateReview

# Create your tests here.
class MovieApiViewTestCase(APITestCase):

    url_movie = reverse('movie')
    movie_title = "THE MATRIX 2"

    def setUp(self):

        self.user = User.objects.create_user(
            email = "bobwhite@gmail.com",
            username = "bobwhite",
            password = "Abc123..",
            first_name = "Bob",
            last_name = "White",
            phone = "+50578251453"
        )

        self.movie = Movie.objects.create(
            title = "THE MATRIX 2",
            year = 2003,
            rated = "R (Sci-Fi Violence|Brief Language)",
            released_on = "2021-05-05",
            genre = "Action, Sci Fi",
            director = "Andy Wachowski, Larry Wachowski",
            plot = "Neo (Keanu Reeves) believes that Morpheus (Laurence Fishburne), an elusive figure considered to be the most dangerous man alive, can answer his question -- What is the Matrix? ",
            audience_score = 0,
            owner = self.user,
        )

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_movie_list_authenticated(self):

        response = self.client.get(self.url_movie)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url_movie)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_movie_create_authenticated(self):

        data = {
            "title": "THE MATRIX",
            "year": 1991,
            "rated": "R (Sci-Fi Violence|Brief Language)",
            "released_on": "2021-05-05",
            "genre": "Action, Sci Fi",
            "director": "Andy Wachowski, Larry Wachowski",
            "plot": "Neo (Keanu Reeves) believes that Morpheus (Laurence Fishburne), an elusive figure considered to be the most dangerous man alive, can answer his question -- What is the Matrix? ",
            "audience_score":0
            }

        response = self.client.post(self.url_movie, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movie_update_authenticated(self):

        self.movie.director = 'robert deniro'
 
        response = self.client.put(reverse('movieDetail', kwargs={'pk':self.movie.pk}), self.movie.__dict__)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_get_authenticated(self):
 
        response = self.client.get(reverse('movieDetail', kwargs={'pk':self.movie.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_delete_authenticated(self):
 
        response = self.client.delete(reverse('movieDetail', kwargs={'pk':self.movie.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_movie_filter_authenticated(self):
 
        response = self.client.get(self.url_movie + f'?title={self.movie_title}')
        
        self.assertTrue(response.data)

    def test_movie_filter_authenticated_fail(self):

        title_no_exist = 'la macarena'    
        response = self.client.get(self.url_movie + f'?title={title_no_exist}')
        
        self.assertFalse(response.data)


class RateReviewApiView(APITestCase):
    
    url_ratereview = reverse('ratereview')
    url_ratereviewDetail = reverse('ratereviewDetail')

    def setUp(self):

        self.user = User.objects.create_user(
            email = "bobwhite@gmail.com",
            username = "bobwhite",
            password = "Abc123..",
            first_name = "Bob",
            last_name = "White",
            phone = "+50578251453"
        )

        self.user2 = User.objects.create_user(
            email = "bobwhite2@gmail.com",
            username = "bobwhite2",
            password = "Abc123..",
            first_name = "Lucas",
            last_name = "White",
            phone = "+50579251455"
        )

        self.movie = Movie.objects.create(
            title = "THE MATRIX 2",
            year = 2003,
            rated = "R (Sci-Fi Violence|Brief Language)",
            released_on = "2021-05-05",
            genre = "Action, Sci Fi",
            director = "Andy Wachowski, Larry Wachowski",
            plot = "Neo (Keanu Reeves) believes that Morpheus (Laurence Fishburne), an elusive figure considered to be the most dangerous man alive, can answer his question -- What is the Matrix? ",
            audience_score = 0,
            owner = self.user,
        )

        self.ratereview = RateReview.objects.create(            
            movie =  self.movie,
            stars = 5,
            rewiew =  'Nice movie',
            owner = self.user2  
        )

        self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    def setUpAuthEnvToUser2(self):

        self.token = Token.objects.create(user=self.user2)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_ratereview_list_authenticated(self):

        response = self.client.get(self.url_ratereview)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ratereview_list_un_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url_ratereview)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ratereview_filter_authenticated(self):
 
        response = self.client.get(self.url_ratereview + f'?idmovie={self.movie.pk}')
        
        self.assertTrue(response.data)

    def test_ratereview_filter_authenticated_fail(self):

        movie_id_wrong = '561655156ghf'    
        response = self.client.get(self.url_ratereview + f'?idmovie={movie_id_wrong}')
        
        self.assertFalse(response.data)

    def test_ratereview_create_authenticated(self):

        data = {
            'movie':  self.movie.pk,
            'stars': 4,
            'rewiew':  'Not bad movie',
            }

        response = self.client.put(self.url_ratereviewDetail, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ratereview_create_authenticated_fail_ratereview_already_exist(self):

        data = {
            'movie':  self.movie.pk,
            'stars': 4,
            'rewiew':  'Not bad movie',
            }

        self.setUpAuthEnvToUser2()

        response = self.client.put(self.url_ratereviewDetail, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)