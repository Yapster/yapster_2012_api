from rest_framework.response import Response as RestResponse


def Response(success=True, message=[], content={}, status=200,
             template_name=None, headers=None,
             exception=False, content_type=None):
    return RestResponse(
        {
            'success': success,
            'message': message,
            'content': content
        }, status=status,
        template_name=template_name, headers=headers,
        exception=exception, content_type=content_type
    )
