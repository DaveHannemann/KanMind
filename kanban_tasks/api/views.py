from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from kanban_tasks.models import Task
from kanban_tasks.api.serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kanban_tasks.api.permissions import IsBoardMember, IsTaskCreatorOrBoardOwner
from kanban_board.models import Board


class TaskView(APIView):
    """
    API endpoint for managing tasks.

    GET:
        Returns all tasks visible to the user.

        Optional filters:
        - assigned_to_me
        - reviewing

    POST:
        Create a new task within a board.

    PATCH:
        Update an existing task.

    DELETE:
        Delete a task (only creator or board owner).
    """

    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsTaskCreatorOrBoardOwner]
        else:
            permission_classes = [IsAuthenticated, IsBoardMember]
        return [permission() for permission in permission_classes]
    

    def get(self, request):
        tasks = Task.objects.with_related().filter(board__members=request.user)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        board = get_object_or_404(Board, id=request.data.get("board"))
        self.check_object_permissions(request, board)

        serializer = TaskSerializer(data=request.data, context={"board": board})
        serializer.is_valid(raise_exception=True)

        task = serializer.save(creator=request.user, board=board)
        task = Task.objects.with_related().get(id=task.id)

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
    
    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task.board)

        serializer = TaskSerializer(task, data=request.data, partial=True, context={"board": task.board})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        self.check_object_permissions(request, task)

        task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AssignedTasksView(APIView):

    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request):
        tasks = Task.objects.with_related().filter(assignee=request.user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
class ReviewerTasksView(APIView):

    permission_classes = [IsAuthenticated, IsBoardMember]

    def get(self, request):
        tasks = Task.objects.with_related().filter(reviewer=request.user)

        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)