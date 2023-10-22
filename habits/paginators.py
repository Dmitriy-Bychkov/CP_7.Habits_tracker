from rest_framework.pagination import PageNumberPagination


class HabitsPaginator(PageNumberPagination):
    """ Пагинатор для вывода информации на странице по 5 записей """

    page_size = 5
    page_query_param = 'page_size'
    max_page_size = 5
