from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated

from app.models import Cart
from .serializer import*
from rest_framework.status import *




class RegisterView(APIView):
    permission_class = (IsAuthenticated,)
    def get(self,request):
        if request.user.type == 'Librarian':
            stu=User.objects.filter(type='Member')
            serializer=UserRegisterSerializer(stu,many=True)
            return Response({'data':serializer.data})
        return Response({'message':'No Permission access user'})

    def post(self,request):
        if request.user.type == 'Librarian':
            serializer=UserRegisterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data})
            return Response({'error': serializer.errors})
        return Response({'message':'No Permission access member'})

    def put(self,request):
        if request.user.type == 'Librarian':
            if request.data.get('id'):
                try:
                    stu=User.objects.get(id=request.data.get('id'))
                except:
                    return Response({'message':'please provide valid id'})

                serializer=UserRegisterSerializer(instance=stu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data})
                return Response({'error': serializer.errors})

            return Response({'message':'Please provide user id'})
        else:
            stu=User.objects.get(id=request.user.id)
            serializer=UserRegisterSerializer(instance=stu,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data})
            return Response({'error': serializer.errors})
    def delete(self,request):
        if request.user.type == 'Librarian':
            if request.data.get('id'):
                try:
                    stu=User.objects.get(id=request.data.get('id'))
                except:
                    return Response({'message':'please provide valid id'})
                
                stu.delete()
                return Response({'message':'User delete successfully'})
            return Response({'message':'please provide User Id'})
        return Response({'message':'No Permission access member'})


  
class LoginApiView(APIView):
    permission_class = (AllowAny,)
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message':'login successfully','data':serializer.data},status=HTTP_200_OK)
        return Response({'error':serializer.errors},status=HTTP_400_BAD_REQUEST)

class BookView(APIView):
    permission_class = (IsAuthenticated,)
    def get(self,request):
        stu=Book.objects.all()
        serializer=BookSerializer(stu,many=True)
        return Response({'data':serializer.data})
    
    def post(self,request):
        if request.user.type == 'Librarian':
            serializer=BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data':serializer.data})
            return Response({'error': serializer.errors})

        return Response({'message':'No permission'})

    def put(self,request):
        if request.user.type == 'Librarian':
            if request.data.get('id'):
                try:
                    stu=Book.objects.get(id=request.data.get('id'))
                except:
                    return Response({'message':'please provide valid id'})

                serializer=BookSerializer(instance=stu,data=request.data,partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'data':serializer.data})
                return Response({'error': serializer.errors})

            return Response({'message':'Please provide Book id'})
        return Response({'message':'No permission'})

    def delete(self,request):
        if request.user.type == 'Librarian':
            if request.data.get('id'):
                try:
                    stu=Book.objects.get(id=request.data.get('id'))
                except:
                    return Response({'message':'please provide valid id'})
                
                stu.delete()
                return Response({'message':'Book delete successfully'})
            return Response({'message':'please provide Book Id'})
        return Response({'message':'No Permission'})

class BookRegister(APIView):
    def post(self,request):
        if request.data.get('id'):
            try:
                stu=Book.objects.get(id=request.data.get('id'),status='Available')
            except:
                return Response({'message':'please provide valid id'})
            stu.status='Borrowed'
            Cart.objects.create(user=request.user,book=stu).save()
            stu.save()
            return Response({'message':'Book Borrowed successfully'})
        return Response({'message':'please provide Book id'})
    def delete(self,request):
        if request.data.get('id'):
            try:
                stu=Book.objects.get(id=request.data.get('id'),status='Borrowed')
            except:
                return Response({'message':'please provide valid id'})
            cart=Cart.objects.get(user=request.user,book=stu)
            stu.status='Available'
            stu.save()
            cart.delete()
            return Response({'message':'book return successfully'})
        return Response({'message':'please provide Book id'}) 


                