from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from kanban_comments.api.serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from kanban_comments.api.permissions import IsBoardMember, IsCommentCreatorOrBoardOwner
from kanban_tasks.models import Task
from kanban_comments.models import Comment


class CommentView(APIView):
    def get_permissions(self):
        if self.request.method == "DELETE":
            permission_classes = [IsAuthenticated, IsCommentCreatorOrBoardOwner]
        elif self.request.method == "PATCH":
            permission_classes = [IsAuthenticated, IsCommentCreatorOrBoardOwner]
        else:
            permission_classes = [IsAuthenticated, IsBoardMember]

        return [permission() for permission in permission_classes]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        self.check_object_permissions(request, task.board)

        comments = Comment.objects.filter(task=task).select_related("author__profile")

        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)
    
    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)

        self.check_object_permissions(request, task.board)

        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save(
            author=request.user,
            task=task
        )

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED
        )

    def patch(self, request, task_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)

        self.check_object_permissions(request, comment)

        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, task_id, comment_id):
        comment = get_object_or_404(Comment, id=comment_id, task_id=task_id)

        self.check_object_permissions(request, comment)

        comment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)