from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from posts.models import Post, Scrapper
from posts.serializers import PostSerializer, ScrapperSerializer

@csrf_exempt
def post_list(request):
    posts = Post.objects.all().reverse()
    serializer = PostSerializer(posts, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except post.DoesNotExist:
        return JsonResponse("Not yet")
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return JsonResponse(serializer.data)

@csrf_exempt
def login(request):
    data = JSONParser().parse(request)
    username = data['user_id']
    request.session['username'] = username
    return JsonResponse("login success", safe=False)

def logout(request):
   try:
      del request.session['username']
   except:
      pass
   return JsonResponse("You are logged out.", safe=False)

def my(request):
    if request.session.has_key('username'):
        username = request.session['username']
        posts = Post.objects.filter(author=username)
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse("You should login first", safe=False)

@csrf_exempt
def post_create(request):
    if request.session.has_key('username'):
        if request.method == "POST":
            data = JSONParser().parse(request)
            post = Post.objects.create(title=data["title"], content=data["content"], author=request.session['username'])
            data["author"] = request.session['username']
            serializer = PostSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse("You should login first", safe=False)

@csrf_exempt
def post_update(request):
    if request.session.has_key('username'):
        if request.method == "POST":
            print(request.session['username'])
            data = JSONParser().parse(request)
            post = Post.objects.get(id=data['target_id'])
            if post.author == request.session['username']:
                if 'title' in data:
                    post.title = data["title"]
                else:
                    data['title'] = post.title
                if 'content' in data:
                    post.content = data["content"]
                else:
                    data['content'] = post.content
                post.save()
                data["author"] = request.session['username']
                serializer = PostSerializer(post, data=data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data)
                return JsonResponse(serializer.errors, status=400)
            else:
                return JsonResponse("It's not yours to update!", safe=False)
    else:
        return JsonResponse("You should login first", safe=False)

@csrf_exempt
def post_delete(request):
    if request.session.has_key('username'):
        if request.method == "POST":
            data = JSONParser().parse(request)
            post = Post.objects.get(id=data['target_id'])
            if post.author == request.session['username']:
                post.delete()
                return JsonResponse("Delete succeess", safe=False)
            else:
                return JsonResponse("It's not yours to delete!", safe=False)
    else:
        return JsonResponse("You should login first", safe=False)

@csrf_exempt
def post_scrap(request):
    if request.method =="POST":
        data = JSONParser().parse(request)
        target_id = data['target_id']
        print(type(target_id))
        target_post = Post.objects.get(id=target_id)
        print(target_post.scrapped)
        already_scrapped = Scrapper.objects.filter(scrapped_by=request.session['username'])
        for item in already_scrapped:
            if item.post.id == int(target_id):
                return JsonResponse("Already scrapped the post", safe=False)
        scrapper = Scrapper.objects.create(post=target_post, scrapped_by=request.session['username'])
        scrapper.save()
        target_post.scrapped = target_post.scrapped + 1
        target_post.save()
        my_scrap = Scrapper.objects.filter(scrapped_by=request.session['username'])
        serializer = ScrapperSerializer(my_scrap, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        my_scrap = Scrapper.objects.filter(scrapped_by=request.session['username'])
        my_scrap_list = []
        for item in my_scrap:
            my_scrap_list.append(item.post)
        serializer = PostSerializer(my_scrap_list, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def unscrap(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        target_id = data['target_id']
        print(type(target_id))
        target_post = Post.objects.get(id=target_id)
        print(target_post.scrapped)
        already_scrapped = Scrapper.objects.filter(scrapped_by=request.session['username'])
        for item in already_scrapped:
            if item.post.id == int(target_id):
                item.delete()
                target_post.scrapped = target_post.scrapped - 1
                target_post.save()
                my_scrap = Scrapper.objects.filter(scrapped_by=request.session['username'])
                serializer = ScrapperSerializer(my_scrap, many=True)
                return JsonResponse(serializer.data, safe=False)
        return JsonResponse("You have not even scrapped the post", safe=False)
    else:
        return JsonResponse("make sure that method is 'POST'", safe=False)