class Filtering(object):
    def do_filter(self, value, queryset):
        pass


class FilterCategoeryByName(Filtering):
    def do_filter(self, value, queryset):
        return queryset.filter(name__contains=value)


class FilterCategoryById(Filtering):
    def do_filter(self, value, queryset):
        return queryset.filter(id__contains=value)


class FacadeCategoryFilter(object):
    def __init__(self, queryset):
        self.queryset = queryset
        self.filter_name = FilterCategoeryByName()
        self.filter_id = FilterCategoryById()

    def filter_by_name(self, value):
        self.queryset = self.filter_name.do_filter(value, self.queryset)

    def filter_by_id(self, value):
        self.queryset = self.filter_id.do_filter(value, self.queryset)

    def get_result(self):
        return self.queryset

