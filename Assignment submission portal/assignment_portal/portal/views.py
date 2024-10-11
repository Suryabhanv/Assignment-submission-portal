# portal/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User, Assignment
from .serializers import UserSerializer, AssignmentSerializer

@api_view(['POST'])
def register(request):
    data = request.data
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username, password=password)
        return Response({'message': 'Login successful', 'user_id': user.id, 'is_admin': user.is_admin})
    except User.DoesNotExist:
        return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

"""@api_view(['POST'])
def upload_assignment(request):
    user_id = request.data.get('user_id')
    task = request.data.get('task')
    admin_username = request.data.get('admin')

    try:
        user = User.objects.get(id=user_id)
        admin = User.objects.get(username=admin_username, is_admin=True)
        assignment = Assignment.objects.create(user=user, task=task, admin=admin)
        return Response(AssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response({'message': 'Invalid user or admin'}, status=status.HTTP_400_BAD_REQUEST)"""



from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Assignment
from .serializers import AssignmentSerializer

@api_view(['POST'])
def upload_assignment(request):
    user_id = request.data.get('user_id')
    task = request.data.get('task')
    admin_username = request.data.get('admin')

    try:
        # Ensure the user exists
        user = User.objects.get(id=user_id)
        
        # Ensure the admin exists and is an admin
        admin = User.objects.get(username=admin_username, is_admin=True)

        # If both exist, create the assignment
        assignment = Assignment.objects.create(user=user, task=task, admin=admin)
        return Response(AssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)
    
    except User.DoesNotExist:
        # Check if the user or admin was the problem
        if not User.objects.filter(id=user_id).exists():
            return Response({'message': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(username=admin_username, is_admin=True).exists():
            return Response({'message': 'Invalid admin'}, status=status.HTTP_400_BAD_REQUEST)



"""from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment
from .serializers import AssignmentSerializer

@api_view(['GET'])
def get_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        return Response(AssignmentSerializer(assignment).data, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({'message': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)"""


# portal/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment
from .serializers import AssignmentSerializer

@api_view(['GET'])
def get_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({'message': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def list_admins(request):
    admins = User.objects.filter(is_admin=True)
    serializer = UserSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def view_assignments(request, admin_id):
    try:
        admin = User.objects.get(id=admin_id, is_admin=True)
        assignments = Assignment.objects.filter(admin=admin)
        serializer = AssignmentSerializer(assignments, many=True)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'message': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def accept_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.status = 'Accepted'
        assignment.save()
        return Response({'message': 'Assignment accepted'})
    except Assignment.DoesNotExist:
        return Response({'message': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def reject_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.status = 'Rejected'
        assignment.save()
        return Response({'message': 'Assignment rejected'})
    except Assignment.DoesNotExist:
        return Response({'message': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)


from django.contrib.auth import authenticate
from rest_framework.decorators import api_view

@api_view(['GET'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid user or admin"}, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth import authenticate

@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        return Response({"message": "Login successful"}, status=200)
    else:
        return Response({"message": "Invalid user or admin"}, status=400)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def admin_login_view(request):
    # Your logic for admin login
    if request.method == "POST":
        # Assuming some login validation happens here
        return JsonResponse({"message": "Admin login successful"}, status=200)



# portal/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Assignment
from .serializers import AssignmentSerializer

@api_view(['GET'])
def get_assignment(request, assignment_id):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        # Now we check if the admin exists
        if not assignment.admin:
            return Response({'message': 'Admin not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Assignment.DoesNotExist:
        return Response({'message': 'Assignment not found'}, status=status.HTTP_404_NOT_FOUND)



from django.shortcuts import render

def upload_assignment_form(request):
    return render(request, 'upload_form.html')



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Assignment
from .serializers import AssignmentSerializer

@api_view(['POST'])
def upload_assignment(request):
    user_id = request.data.get('user_id')
    task = request.data.get('task')
    admin_username = request.data.get('admin')
    uploaded_file = request.FILES.get('file')  # Handle file upload

    try:
        # Ensure the user exists
        user = User.objects.get(id=user_id)

        # Ensure the admin exists and is an admin
        admin = User.objects.get(username=admin_username, is_admin=True)

        # If both exist, create the assignment
        assignment = Assignment.objects.create(user=user, task=task, admin=admin, file=uploaded_file)
        return Response(AssignmentSerializer(assignment).data, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'message': 'Invalid user or admin'}, status=status.HTTP_400_BAD_REQUEST)
