# coding=utf-8
from rest_framework import status
from rest_framework.response import Response as RestResponse

def Response(success=True, message=[], content={}, status=200,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
	return RestResponse(
		{
	        'success': success,
	        'message': message,
	        'content': content
	    }, status=200,
                 template_name=None, headers=None,
                 exception=False, content_type=None
    )
