from django.utils.deprecation import MiddlewareMixin


class MyMiddle(MiddlewareMixin):
    def process_request(self, request):
        print('get参数为：', request.GET.get('a'))
