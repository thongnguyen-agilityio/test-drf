from collections import OrderedDict

from drf_core import pagination
from rest_framework.response import Response
from rest_framework.utils.urls import (
    replace_query_param,
    remove_query_param,
)


class CustomPagination(pagination.BasePagination):
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('self', self.request.build_absolute_uri()),
            ('first', self.get_first_link()),
            ('last', self.get_last_link()),
            ('results', data)
        ]))

    def get_first_link(self):
        if self.offset <= 0:
            return None
        url = self.request.build_absolute_uri()
        return remove_query_param(url, self.offset_query_param)

    def get_last_link(self):
        if self.offset + self.limit >= self.count:
            return None
        url = self.request.build_absolute_uri()
        url = replace_query_param(url, self.limit_query_param, self.limit)
        offset = self.count - self.limit
        return replace_query_param(url, self.offset_query_param, offset)

