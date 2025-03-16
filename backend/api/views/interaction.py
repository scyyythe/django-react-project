from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.models.artwork import Art
from api.models.interaction import Comment, Like
from api.serializers.interaction import CommentSerializer, LikeSerializer

class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]  

    def post(self, request, *args, **kwargs):
        user = request.user  
        art_id = request.data.get('art') 
        content = request.data.get('content')  

        if not art_id or not content:
            return Response({"detail": "Art ID and content are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            art = Art.objects.get(id=art_id)  
        except Art.DoesNotExist:
            return Response({"detail": "Artwork not found."}, status=status.HTTP_404_NOT_FOUND)

       
        comment = Comment.objects.create(content=content, user=user, art=art)
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class LikeCreateView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def post(self, request, *args, **kwargs):
        user = request.user
        art_id = request.data.get('art')  

        if not art_id:
            return Response({"detail": "Art ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            art = Art.objects.get(id=art_id)  
            
        except Art.DoesNotExist:
            return Response({"detail": "Artwork not found."}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(user=user, art=art).first()

        if like:
            like.delete()
            return Response({"detail": "You have unliked this artwork."}, status=status.HTTP_200_OK)
        
        else:
            like = Like.objects.create(user=user, art=art)
            return Response(LikeSerializer(like).data, status=status.HTTP_201_CREATED)

