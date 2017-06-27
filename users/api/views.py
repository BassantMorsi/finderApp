import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView
    )


from users.models import User, FindRequest, MissRequest
from .pagination import UserLimitOffsetPagination, UserPageNumberPaginaton

from .serializers import (
    UserListSerializer,
    UserDetailSerializer,
    UserSerializer,
    )
from datetime import datetime as dt
import os
import cv2
from PIL import Image
import numpy as np
import base64

FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))

MISS_FACES_PATH = "{base_path}/faces/miss/".format(
    base_path=os.path.abspath(os.path.dirname(__file__)))


FIND_FACES_PATH = "{base_path}/faces/find/".format(
   base_path=os.path.abspath(os.path.dirname(__file__)))


# maximum distance between face and match
THRESHOLD = 75

# create the cascade classifiers
detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)

# path  faces/testing or faces/training
# imageName == 1...10.userid.userrequest.jpg
# image extension = .userid.userrequest


def get_images_and_labels_helper(path, extension):
    images = []
    labels = []
    temp = []
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith(extension)]
    for image_path in image_paths:
        requestId = os.path.split(image_path)[1].split(".")[1]
        if requestId not in temp:
            temp.append(requestId)
            # Read the image and convert to grayscale
            image_pil = Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')
            # Detect the face in the image
            faces = detector.detectMultiScale(image)
            # If face is detected, append the face to images and the label to labels
            for (x, y, w, h) in faces:
                images.append(image[y: y + h, x: x + w])
                labels.append(int(os.path.split(image_path)[1].split(".")[1]))

    return images, labels


def get_images_and_labels(path, extension):
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    # Append all the absolute image paths in a list image_paths
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(extension)]
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Detect the face in the image
        faces = detector.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(int(os.path.split(image_path)[1].split(".")[0]))
    return images, labels

"""
def image_getter(path, extension):
    images = []
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(extension)]
    for image_path in image_paths:
        image = Image.open(image_path)
        image = np.array(image, 'uint8')
        images.append(image)

    return images
"""

@api_view(['POST'])
def recognize(request):
    data = request.data
    username =data.get('userName', None)
    date = str(data.get('date', None))
    requestType = data.get('type', None)
    user = User.objects.get(userName=username)
    userid = str(user.id)
    msg = {
        'error': 'Sorry there has no any matching yet'
    }

    if requestType == 'f':
        r = FindRequest.objects.get(user=user, date=date)
        fname = r.fName
        gender = r.gender
        requestid = str(r.id)

        # print requestid, userid
        e = '.' + requestid + '.' + userid + '.jpg'
        images, labels = get_images_and_labels(FIND_FACES_PATH, e)
        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.train(images, np.array(labels))
        e1 = userid + '.jpg'
        timages, tlabels = get_images_and_labels_helper(MISS_FACES_PATH, e1)
        collector = cv2.face.StandardCollector_create()
        recognizer.setThreshold(THRESHOLD)
        minConf = 1000
        for timage, tlabel in zip(timages, tlabels):
            recognizer.predict_collect(timage, collector)
            conf = collector.getMinDist()
            # dah bydeny elmin image mismatching ma3 el sora elly batest beha
            pred = collector.getMinLabel()
            if conf < minConf:
                minConf = conf
                labelRequest = tlabel

            print tlabel
            print (conf)
            print (pred)
        requestconf = MissRequest.objects.get(id=labelRequest)
        userconf =requestconf.user
        useridconf = userconf.id
        print (userconf, useridconf)
        rdate = str(requestconf.date)
        rgender = requestconf.gender
        rstatus = requestconf.status
        rfname = requestconf.fName
        print (rdate, rfname, rgender)
        rdatestr = dt.strptime(rdate, '%Y-%m-%d')
        datestr = dt.strptime(date, '%Y-%m-%d')
        print(gender, fname)
        if rdatestr <= datestr and rgender == gender and rfname == fname and rstatus is False:
            os.chdir(os.path.dirname(MISS_FACES_PATH))
            filename = '1.'+str(labelRequest)+'.'+str(useridconf)+'.jpg'
            image_file = open(filename, 'rb').read()
            encoded_string = base64.b64encode(image_file)
            msg = {
                'image': encoded_string
            }

    elif requestType == 'm':
        r = MissRequest.objects.get(user=user, date=date)
        fname = r.fName
        gender = r.gender
        requestid = str(r.id)

        # print requestid, userid
        e = '.' + requestid + '.' + userid + '.jpg'
        images, labels = get_images_and_labels(MISS_FACES_PATH, e)
        recognizer = cv2.face.createLBPHFaceRecognizer()
        recognizer.train(images, np.array(labels))
        e1 = userid + '.jpg'
        timages, tlabels = get_images_and_labels_helper(FIND_FACES_PATH, e1)
        collector = cv2.face.StandardCollector_create()
        recognizer.setThreshold(THRESHOLD)
        minConf = 1000
        for timage, tlabel in zip(timages, tlabels):
            recognizer.predict_collect(timage, collector)
            conf = collector.getMinDist()
            # dah bydeny elmin image mismatching ma3 el sora elly batest beha
            pred = collector.getMinLabel()
            if conf < minConf:
                minConf = conf
                labelRequest = tlabel

            print tlabel
            print (conf)
            print (pred)
        requestconf = MissRequest.objects.get(id=labelRequest)
        userconf = requestconf.user
        useridconf = userconf.id
        print (userconf, useridconf)
        rdate = str(requestconf.date)
        rgender = requestconf.gender
        rstatus = requestconf.status
        rfname = requestconf.fName
        print (rdate, rfname, rgender)
        rdatestr = dt.strptime(rdate, '%Y-%m-%d')
        datestr = dt.strptime(date, '%Y-%m-%d')
        print(gender, fname)
        if rdatestr >= datestr and rgender == gender and rfname == fname and rstatus is False:
            os.chdir(os.path.dirname(FIND_FACES_PATH))
            filename = '1.' + str(labelRequest) + '.' + str(useridconf) + '.jpg'
            image_file = open(filename, 'rb').read()
            encoded_string = base64.b64encode(image_file)
            msg = {
                'image': encoded_string
            }

    return Response(msg)


@api_view(['POST'])
def find_request(request):
    data = request.data
    username = data.get('userName', None)
    date = data.get('date', None)
    strimage1 =data.get('image1', None)
    strimage2 = data.get('image2', None)
    strimage3 = data.get('image3', None)
    strimage4 = data.get('image4', None)
    strimage5 = data.get('image5', None)
    strimage6 = data.get('image6', None)
    strimage7 = data.get('image7', None)
    strimage8 = data.get('image8', None)
    strimage9 = data.get('image9', None)
    strimage10 = data.get('image10', None)
    listOfImages = [strimage1, strimage2, strimage3, strimage4, strimage5, strimage6,
                    strimage7, strimage8, strimage9, strimage10]

    user = User.objects.get(userName=username)

    if FindRequest.objects.filter(user=user, date=date).exists():
        msg = {
            'status': 'You have already sent your request...'
        }
        return Response(msg, status=status.HTTP_404_NOT_FOUND)
    else:
        # create request object
        r = FindRequest(user=user, date=date)
        r.save()
        """print FIND_FACES_PATH
        abspath = os.getcwd() + "/users/api/faces/find/"
        print abspath
        """
        # abspath = os.getcwd()+"/users/api/faces/find/"
        # os.chdir(os.path.dirname(abspath))
        os.chdir(os.path.dirname(FIND_FACES_PATH))
        userid = str(user.id)
        requestid = str(r.id)
        imgNum = 0
        for x in listOfImages:
            imgdata = base64.b64decode(x)
            # imgNum = listOfImages.index(x) + 1
            imgNum = imgNum + 1
            # print imgNum
            filename = str(imgNum) + '.' + requestid + '.' + userid + '.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)

        msg = {
            'status': 'Your request has been sent...'
        }
        return Response(msg)


@api_view(['POST'])
def miss_request(request):
    data = request.data
    username = data.get('userName', None)
    date = data.get('date', None)
    strimage1 =data.get('image1', None)
    strimage2 = data.get('image2', None)
    strimage3 = data.get('image3', None)
    strimage4 = data.get('image4', None)
    strimage5 = data.get('image5', None)
    strimage6 = data.get('image6', None)
    strimage7 = data.get('image7', None)
    strimage8 = data.get('image8', None)
    strimage9 = data.get('image9', None)
    strimage10 = data.get('image10', None)
    listOfImages = [strimage1, strimage2, strimage3, strimage4, strimage5, strimage6,
                    strimage7, strimage8, strimage9, strimage10]

    user = User.objects.get(userName=username)
    if MissRequest.objects.filter(user=user, date=date).exists():
        msg = {
            'status': 'You have already sent your request...'
        }
        return Response(msg, status=status.HTTP_404_NOT_FOUND)
    else:
        r = MissRequest(user=user, date=date)
        r.save()
        # abspath = os.getcwd()+"/users/api/faces/miss/"
        # os.chdir(os.path.dirname(abspath))
        os.chdir(os.path.dirname(MISS_FACES_PATH))
        userid = str(user.id)
        requestid = str(r.id)
        imgNum = 0
        for x in listOfImages:
            imgdata = base64.b64decode(x)
            # imgNum = listOfImages.index(x) + 1
            imgNum = imgNum + 1
            # print imgNum
            filename = str(imgNum) + '.' + requestid + '.' + userid + '.jpg'
            with open(filename, 'wb') as f:
                f.write(imgdata)

        msg = {
            'status': 'Your request has been sent...'
        }
        return Response(msg)



"""
@api_view(['POST'])
def miss_request(request):
    data = request.data
    username = data.get('userName', None)
    date = data.get('date', None)
    strimage =data.get('image1', None)
    user = User.objects.get(userName=username)
    r = MissRequest(user=user, date=date)
    if MissRequest.objects.filter(user=user, date=date).exists():
        msg = {
            'status': 'You have already sent your request...'
        }
        return Response(msg, status=status.HTTP_404_NOT_FOUND)
    else:
        r.save()
        abspath = os.getcwd() + "/users/api/faces/testing/"
        os.chdir(os.path.dirname(abspath))
        userid = str(user.id)
        requestid = str(r.id)
        imgdata = base64.b64decode(strimage)
        filename = 'face'+'.' + requestid + '.' + userid + '.jpg'
        with open(filename, 'wb') as f:
            f.write(imgdata)
        msg = {
            'status': 'Your request has been sent...'
        }
        return Response(msg)
"""

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        # serializer = UserSerializer(data=json.loads(request.body.decode('utf-8')))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    msg = {
        'status': 'error'
    }
    try:
        data = request.data
        username = data.get('userName', None)
        password = data.get('password', None)
        user = User.objects.get(userName=username, password=password)
    except User.DoesNotExist:
        return Response(msg, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# serializer = UserLoginSerializer(data=request.data)
# serializer = UserSerializer(data=json.loads(request.body.decode('utf-8')))
""" queryset = User.objects.all()
    data = request.data
    usename = data.get('userName', None)
    password = data.get('password', None)
    if queryset.filter(userName=usename,password=password).exist():
            return Response()
"""

#post bas ma3mola be get we7sha ya3ny first version

"""
def detail(request, username, password, email, mobile):
    num_results = User.objects.filter(userName=username).count()
    if num_results == 0:
        user = User()
        user.userName = str(username)
        user.password = str(password)
        user.email = str(email)
        user.mobile = str(mobile)
        user.save()
        return HttpResponse("{'userName':'"+str(username)+"','password':'"+str(password)+"','email':'"+str(email)+"','mobile':'"+str(mobile)+"'}")

    else:
        return HttpResponse("{'status':'already exists'}")
"""


@api_view(['GET']) #deh m3 kelment request t5aleny a3raf asta5dem Response enha return JSON
def detail(request, username, password, email, mobile):
    num_results = User.objects.filter(userName=username).count()
    if num_results == 0:
        user = User()
        user.userName = str(username)
        user.password = str(password)
        user.email = str(email)
        user.mobile = str(mobile)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        msg ={
            'status': 'exists'
        }
        return Response(msg)









class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = UserPageNumberPaginaton

    #PageNumberPagination

class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_field = 'userName'




