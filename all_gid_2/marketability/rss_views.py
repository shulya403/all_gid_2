from .models import TxtRatings
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords



class RateFeed(Feed):
    title = "Гид покупателя. Рейтинги. Мониторы, Ноутбуки, Принтеры и МФУ, ИБП, "
    description = "Рейтинги. Top самых популярных моделей в России. Обзоры и подборки. Лучшие Мониторы, Ноутбуки, Принтеры и МФУ, ИБП, "
    link = "https://allgid.ru"
    category_dict = {
        'Nb': {
            "categories_name_singular": "Ноутбук",
            "categories_name_plural": "Ноутбуки"
        }
    }
    language = "ru"

    def items(self):
        return TxtRatings.objects.all().values("cat").distinct()

    def item_title(self, item):
        return "Выбор покупателя. Рейтинг по продажам в России. " + self.category_dict[item["cat"]]["categories_name_singular"] + "."

    def item_description(self, item):
        return self.category_dict[item["cat"]]["categories_name_plural"] + ": Top самых популярных модлей в России."

    def item_link(self, item):
        return "https://allgid.ru/rate/" + item["cat"] + "/"


