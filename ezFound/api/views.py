from django.shortcuts import render
from django.views import View
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.timezone import now

from posts.models import Post, Comment, Message, Location, Category, PostImage
from authen.models import OTP
from account.models import Profile
from api.utils.get import comment as getComment
from api.utils.get import image as getImage

"""
    TODO:
          - Edit Post
"""

@api_view(['GET', 'DELETE'])
def post_get(request, postId):
    """ Get Specific Post """

    if request.method == 'GET':
        try:
            post = Post.objects.get(pk=postId)
            return JsonResponse({
                "statusCode": 200,
                "statusText": "Success",
                "message": "Success",
                "error": False,
                "data": {
                    "id": postId,
                    "title": post.title,
                    "description": post.descriptions,
                    "status": post.status,
                    "categories": [c.name for c in post.category.all()],
                    "location": post.location.name,
                    "user": post.user.username,
                    "create_at": post.create_at,
                    "date": post.date,
                    "comment": getComment(postId),
                    "images": getImage(postId)
                }
            })
        except ObjectDoesNotExist:
            return JsonResponse({
                "statusCode": 404,
                "statusText": "Not Found",
                "message": "Post Not Exist",
                "error": True
            })

    elif request.method == 'DELETE':
        try:
            post = Post.objects.get(pk=postId)
            post.delete_at = now()
            post.save()

            return JsonResponse({
                "statusCode": 200,
                "statusText": "Success",
                "message": "Post Deleted!",
                "error": False
            })

        except ObjectDoesNotExist:
            return JsonResponse({
                "statusCode": 404,
                "statusText": "Not Found",
                "message": "Post Not Exist",
                "error": True
            })

@api_view(['GET'])
def userPost(request, userId):
    """ Get all post of specific user """

    try:
        posts = Post.objects.filter(user_id=userId)
        payload = [{
            "id": p.id,
            "title": p.title,
            "description": p.descriptions,
            "status": p.status,
            "category": [c.name for c in p.category.all()],
            "location": p.location.name,
            "user": p.user.username,
            "create_at": p.create_at,
            "date": p.date,
            "images": getImage(p.id)
        } for p in posts if p.delete_at is None]

        return JsonResponse({
            "statusCode": 200,
            "statusText": "Success",
            "message": "Successt",
            "error": False,
            "data": payload
        })
    except ObjectDoesNotExist:
        return JsonResponse({
            "statusCode": 404,
            "statusText": "Not Found",
            "message": "Post Not Exist",
            "error": True
        })


@api_view(['GET', 'POST'])
def post(request):
    """ Get post for index page and create new post """

    try:
        if request.method == 'GET':
            posts = Post.objects.all()
            payload = [{
                "id": p.id,
                "title": p.title,
                "description": p.descriptions,
                "status": p.status,
                "location": p.location.name,
                "user": p.user.username,
                "create_at": p.create_at,
                "date": p.date
            } for p in posts]

            return JsonResponse({
                "statusCode": 200,
                "statusText": "Success",
                "message": "Successt",
                "error": False,
                "data": payload
            })

        elif request.method == 'POST':
            try:
                # Create Post
                post = Post(
                    title=request.data['title'],
                    descriptions=request.data['descriptions'],
                    status=request.data['status'],
                    date=request.data['date'],
                    user=User.objects.get(pk=request.data['user_id']),
                    location=Location.objects.get(pk=request.data['location_id'])
                )
                
                # Add category to post
                post.save()
                for c in request.data['categories_id']:
                    post.category.add(Category.objects.get(pk=c))
                post.save()

                # Create PostImage
                image = PostImage(
                    image_url=request.data['img'],
                    post=post
                )
                image.save()

                return JsonResponse({
                    "statusCode": 201,
                    "statusText": "Created",
                    "message": "Create Post Successfully",
                    "error": False,
                })

            except KeyError:
                return JsonResponse({
                    "statusCode": 400,
                    "statusText": "Bad Request",
                    "message": "Invalid API Payload",
                    "error": True
            })

    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })


@api_view(['GET'])
def get_location(request, locationId):

    try:
        posts = Post.objects.filter(location=locationId)
        payload = [{
            "id": p.id,
            "title": p.title,
            "description": p.descriptions,
            "status": p.status,
            "category": [c.name for c in p.category.all()],
            "location": p.location.name,
            "user": p.user.username,
            "create_at": p.create_at,
            "date": p.date,
            "images": getImage(p.id)
        } for p in posts if p.delete_at is None]

        return JsonResponse({
            "statusCode": 200,
            "statusText": "Success",
            "message": "Query Success",
            "error": False,
            "data": payload
        })

    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })


@api_view(['GET'])
def get_category(request, categoryId):

    try:
        posts = Post.objects.filter(category=categoryId)
        payload = [{
            "id": p.id,
            "title": p.title,
            "description": p.descriptions,
            "status": p.status,
            "category": [c.name for c in p.category.all()],
            "location": p.location.name,
            "user": p.user.username,
            "create_at": p.create_at,
            "date": p.date,
            "images": getImage(p.id)
        } for p in posts if p.delete_at is None]

        return JsonResponse({
            "statusCode": 200,
            "statusText": "Success",
            "message": "Query Success",
            "error": False,
            "data": payload
        })

    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })


@api_view(['GET'])
def profile(request, userId):
    """ Get Profile Of A User """
    try:
        try:
            user = User.objects.get(pk=userId)
            profile = Profile.objects.get(user_id=userId)
            return JsonResponse({
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "student_id": profile.student_id,
                "phone": profile.phone,
                "profile_img_path": profile.profile_img_path
            })

        except ObjectDoesNotExist:
            return JsonResponse({
                "statusCode": 404,
                "statusText": "Not Found",
                "message": "User Not Exist",
                "error": True
            })
    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })


@api_view(['POST', 'PUT'])
def comment(request):

    try:
        if request.method == 'POST':
            try:
                # Get Object
                user = User.objects.get(pk=request.data['user_id'])
                post = Post.objects.get(pk=request.data['post_id'])

                # Create Comment Object
                comment = Comment(
                    text=request.data['text'],
                    user=user,
                    post=post
                )

                # Create Message Object
                if user.id != post.user_id:
                    message = Message(
                        text=f"{user.first_name} Commented on your post.",
                        post=post,
                        send_by=user,
                        message_to=User.objects.get(pk=post.user_id)
                    )
                    message.save()

                # Save Object
                comment.save()

                # Response
                return JsonResponse({
                    "statusCode": 201,
                    "statusText": "Created",
                    "message": "Comment Posted!",
                    "error": False
                })

            except ObjectDoesNotExist:
                return JsonResponse({
                    "statusCode": 404,
                    "statusText": "Not Found",
                    "message": "Post Or User Not Exist",
                    "error": True
                })

        elif request.method == 'PUT':
            try:
                comment = Comment.objects.get(pk=request.data['comment_id'])
                comment.text = request.data['text']
                comment.save()

                return JsonResponse({
                    "statusCode": 200,
                    "statusText": "Success",
                    "message": "Success",
                    "error": False
                })

            except ObjectDoesNotExist:
                return JsonResponse({
                    "statusCode": 404,
                    "statusText": "Not Found",
                    "message": "Comment Not Exist",
                    "error": True
                })

    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })


@api_view(['DELETE'])
def del_comment(request, commentId):
    try:
        comment = Comment.objects.get(pk=commentId)
        comment.delete_at = now()
        comment.save()

        return JsonResponse({
            "statusCode": 200,
            "statusText": "Success",
            "message": "Comment Deleted!",
            "error": False
        })

    except ObjectDoesNotExist:
        return JsonResponse({
            "statusCode": 404,
            "statusText": "Not Found",
            "message": "Comment Not Exist",
            "error": True
        })

    except:
        return JsonResponse({
            "statusCode": 500,
            "statusText": "Internal Server",
            "message": "Internal Server",
            "error": True
        })