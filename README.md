## Дипломная работа

# VKinder
Приложение предоставляет простой интерфейс для выбора понравившегося человека.

Используя данные из VK сервис находит людей, подходящих под условия, на основании информации о пользователе из VK:

возраст,
пол,
город,
семейное положение.
У тех людей, которые подошли по требованиям пользователю, получать топ-3 популярных фотографии с аватара. Популярность определяется по количеству лайков и комментариев.

# Входные данные:

Имя пользователя или его id в ВК, для которого мы ищем пару.

если информации недостаточно нужно дополнительно спросить её у пользователя.

# Выходные данные:

JSON-файл с 10 объектами, где у каждого объекта перечислены топ-3 фотографии и ссылка на аккаунт.

# Требование к сервису:

Код программы удовлетворяетPEP8.
Получать токен от пользователя с нужными правами.
Программа декомпозирована на функции/классы/модули/пакеты.
Результат программы записывать в БД.
Люди не должны повторяться при повторном поиске.
Реализовать тесты на базовую функциональность.
Не запрещается использовать внешние библиотеки для vk.

# Дополнительные требования (не обязательны для получения диплома):

В vk максимальная выдача при поиске 1000 человек. Подумать как это ограничение можно обойти.
Добавить возможность ставить/убирать лайк, выбранной фотографии.
Можно усложнить поиск добавив поиск по интересам. Разбор похожих интересов(группы, книги, музыка, интересы) нужно будет провести с помощью анализа текста.
У каждого критерия поиска должны быть свои веса. То есть совпадение по возрасту должны быть важнее общих групп. Интересы по музыке важнее книг. Наличие общих друзей важнее возраста. И так далее.
Добавлять человека в избранный список, используя БД.
Добавлять человека в черный список чтобы он больше не попадался при поиске, используя БД.
К списку фотографий из аватарок добавлять список фотографий, где отмечен пользователь.