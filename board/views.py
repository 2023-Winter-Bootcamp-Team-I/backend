from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from board.serializers import BoardSerializer


@api_view(['POST'])
def create_board(request):
    serializer = BoardSerializer(data=request.data)
    # is_valid 알아보기
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': '게시글이 성공적으로 생성되었습니다.',
            'data': serializer.data
        }, status.HTTP_201_CREATED)
    return Response({
        'message': '유효하지 않은 입력값입니다.',
        'data': serializer.errors
    }, status.HTTP_400_BAD_REQUEST)
