import requests
import pygal

from pygal.style import SolidColorStyle as sol
from operator import itemgetter


# Создание вызова API и сохранение ответа:
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print("Status code: ", r.status_code)

# Оработка информации о каждой статье:
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[:30]:
    # создание отдельного вызова API для каждой статьи:
    url = ('https://hacker-news.firebaseio.com/v0/item/' +
           str(submission_id) + '.json')
    submission_r = requests.get(url)
    print(submission_r.status_code)
    response_dict = submission_r.json()

    submission_dict = {
        'title': response_dict['title'],
        'link': 'http://news.ycombinator.com/item?id=' + str(submission_id),
        'comments': response_dict.get('descendants', 0)
        }
    submission_dicts.append(submission_dict)

submission_dicts = sorted(submission_dicts,
                          key=itemgetter('comments'),
                          reverse=True)
# for submission_dict in submission_dicts:
#     print("\nTitle: ", submission_dict['title'])
#     print("Discussion link: ", submission_dict['link'])
#     print("Comments: ", submission_dict['comments'])

# print(submission_dicts)

titles, plot_dicts = [], []
for sb_dict in submission_dicts:
    titles.append(sb_dict['title'])
    plot_dict = {
        'value': sb_dict['comments'],
        'label': sb_dict['title'],
        'xlink': sb_dict['link'],
        }
    plot_dicts.append(plot_dict)

my_style = sol()
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 22
my_config.label_font_size = 12
my_config.major_label_font_size = 16
my_config.truncate_label = 13
my_config.show_y_guides = False
my_config.width = 1000
my_config.y_title = 'Number of comments'

chart = pygal.Bar(my_config, style=my_style)
chart.title = 'Most commented hacker-news'
chart.x_labels =titles
chart.add('', plot_dicts)
chart.render_to_file('hacker_news.svg')
