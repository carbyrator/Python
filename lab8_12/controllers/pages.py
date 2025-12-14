"""Рендеринг HTML-шаблонов через Jinja2."""

from typing import Any, Dict

from jinja2 import Environment

from models import App, Author


class PageController:
    """Отвечает за подготовку контекста и рендеринг шаблонов."""

    def __init__(
        self, env: Environment, app: App, author: Author, last_update_getter
    ):
        """
        Инициализирует контроллер представления.

        Args:
            env: Инстанс окружения Jinja2.
            app: Описание приложения.
            author: Автор приложения.
            last_update_getter: Callable, возвращающий строку времени обновления.
        """
        self.env = env
        self.app = app
        self.author = author
        self._last_update_getter = last_update_getter

    def render(
        self, template_name: str, extra_context: Dict[str, Any] | None = None
    ) -> str:
        """
        Рендерит шаблон с базовым и дополнительным контекстом.

        Args:
            template_name: Имя файла шаблона.
            extra_context: Дополнительные переменные для контекста.

        Returns:
            Сгенерированная HTML-строка.
        """
        context = {
            "app_name": self.app.name,
            "app_version": self.app.version,
            "author_name": self.author.name,
            "author_group": self.author.group,
            "page_title": "Мониторинг валют",
            "last_update": self._last_update_getter(),
        }
        if extra_context:
            context.update(extra_context)
        template = self.env.get_template(template_name)
        return template.render(**context)
