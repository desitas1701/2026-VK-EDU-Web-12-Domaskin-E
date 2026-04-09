class EmptyPage(Exception):
    """The requested page does not exist."""
    pass


class PageNotAnInteger(Exception):
    """The page number is not an integer."""
    pass


class Page:
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def has_next(self):
        return self.number < self.paginator.num_pages

    def has_previous(self):
        return self.number > 1

    def has_other_pages(self):
        return self.paginator.num_pages > 1

    def next_page_number(self):
        if not self.has_next():
            raise EmptyPage("There is no next page")
        return self.number + 1

    def previous_page_number(self):
        if not self.has_previous():
            raise EmptyPage("There is no previous page")
        return self.number - 1

    def start_index(self):
        if self.paginator.count == 0:
            return 0
        return (self.number - 1) * self.paginator.per_page + 1

    def end_index(self):
        if self.paginator.count == 0:
            return 0
        if self.number == self.paginator.num_pages:
            return self.paginator.count
        return self.number * self.paginator.per_page

    def get_page_window(self, window_size=5):
        total_pages = self.paginator.num_pages
        current_pages = self.number

        if window_size < 1:
            return range(0)

        if total_pages <= window_size:
            return range(1, total_pages + 1)

        left = window_size // 2
        right = window_size - left - 1

        start_page = current_pages - left
        end_page = current_pages + right

        if start_page < 1:
            end_page += 1 - start_page
            start_page = 1

        if end_page > total_pages:
            start_page -= end_page - total_pages
            end_page = total_pages

        if start_page < 1:
            start_page = 1

        return range(start_page, end_page + 1)


class Paginator:
    def __init__(self, object_list, per_page=5):
        if not isinstance(per_page, int) or per_page <= 0:
            raise ValueError("per_page must be a positive integer")

        self.object_list = object_list
        self.per_page = per_page
        self.count = len(object_list)

        self.num_pages = 1 if self.count == 0 else (self.count - 1) // per_page + 1
        self.page_range = range(1, self.num_pages + 1)

    def page(self, number):
        try:
            number_int = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger("That page number is not an integer")

        if number_int < 1:
            raise EmptyPage("That page number is less than 1")

        if number_int > self.num_pages:
            raise EmptyPage(f"That page number is greater than {self.num_pages}")

        start = (number_int - 1) * self.per_page
        end = start + self.per_page
        page_objects = self.object_list[start:end]

        return Page(page_objects, number_int, self)

    def get_page(self, number):
        try:
            return self.page(number)
        except PageNotAnInteger:
            return self.page(1)
        except EmptyPage:
            return self.page(self.num_pages)
