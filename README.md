cssmanager - пробний редактор css файлів в реальному часі.
==========
**Обмеження - недає вибрати і редагувати selector котрий не присутній на сторінці.**
________

Для роботи потрібен пакет `cssutils` (`pip install cssutils`)

Встановлення: папку cssmanager копіюємо в директорію проекта

Додаємо менеджер в INSTALLED_APPS в файлі settings.py проекту:


    INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.sites',
    'cssmanager',
     ...
    )

`CSSMANAGER_ROOTDIR = STATIC_ROOT` - верхня директорія, яка доступна для менеджера

Одноразово потрібно виконати `manage.py collectstatic`.

Додаємо URLs в urls.py проекту:

  `url(r'^cssmanager/', include('cssmanager.urls')),`

Далі в верху файла base.html прописуємо 

`{% load cssmanager %}` 

в тег `<head>....</head>` додаємо:

    <script src="http://code.jquery.com/jquery-latest.js"></script>
    {% cssmanager_css %}
    {% cssmanager_js %}

в кінці базового шаблону перед тегом `</body>`  додаємо

    {% if user.is_authenticated %}
    {% include 'pan.html' %}
    {% endif %}

замість `{% if user.is_authenticated %}` може бути `{% if user.is_staff %} `або `{% if user.is_superuser %}`
