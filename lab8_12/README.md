Цель работы: показать построение мини‑веб‑приложения для мониторинга курсов валют в архитектуре MVC с хранением данных в SQLite (in‑memory), маршрутизацией на http.server и рендерингом HTML через
    Jinja2.
1) Модели и связи (lab9/models):
      - Author — имя/группа с валидацией непустых строк.
      - User — id (int>0), name (>=2 символов).
      - Currency — id, num_code/char_code (3 символа, upper), name, value (float>0), nominal (int>0); вычисление курса за единицу.
      - UserCurrency — связь user_id↔currency_id, оба >0.
      - Связи в БД: таблица user_currency с внешними ключами на user.id и currency.id, обеспечивающими ссылочную целостность.
2) Структура проекта:
      - lab9/myapp.py — точка входа, HTTP‑маршруты, подготовка контекста, запуск HTTPServer, инициализация данных.
      - lab9/controllers/databasecontroller.py — работа с SQLite (создание таблиц, CRUD для user/currency/user_currency).
      - lab9/controllers/currencycontroller.py, usercontroller.py — бизнес‑логика над БД.
      - lab9/templates/*.html — представления Jinja2 (главная, автор, список валют, список пользователей, страница пользователя).
      - lab9/tests.py — модульные тесты с unittest и unittest.mock.
3) CRUD и SQL‑примеры (из lab9/controllers/databasecontroller.py):
      - Create: INSERT INTO user(name) VALUES (?); / INSERT INTO currency(num_code,char_code,name,value,nominal) VALUES(?,?,?,?,?);
      - Read: SELECT * FROM currency; и SELECT c.* FROM currency c JOIN user_currency uc ON uc.currency_id = c.id WHERE uc.user_id = ?;
      - Update: UPDATE currency SET value = ? WHERE char_code = ?;
      - Delete: DELETE FROM user_currency WHERE currency_id = ?; затем DELETE FROM currency WHERE id = ?; 
4) Реализация CRUD в интерфейсе:
      - Добавление валюты через форму на / (/currency/add?num_code=...).
      - Просмотр и обновление курсов на /currencies (форма отправляет GET /currency/update с парами ?USD=90.1).
      - Удаление валюты — ссылки /currency/delete?id=....
      - Подписка/отписка пользователя на валюту — /user/subscribe?user_id=..&currency_id=.. и /user/unsubscribe?.... 
5) ![Снимок экрана 2025-12-14 в 6.10.22 PM.png](../%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-12-14%20%D0%B2%206.10.22%E2%80%AFPM.png)
![Снимок экрана 2025-12-14 в 6.10.38 PM.png](../%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-12-14%20%D0%B2%206.10.38%E2%80%AFPM.png)
![Снимок экрана 2025-12-14 в 6.11.36 PM.png](../%D0%A1%D0%BD%D0%B8%D0%BC%D0%BE%D0%BA%20%D1%8D%D0%BA%D1%80%D0%B0%D0%BD%D0%B0%202025-12-14%20%D0%B2%206.11.36%E2%80%AFPM.png)
6) Тесты (lab9/tests.py):
      - Использование unittest.mock.MagicMock в TestCurrencyController для проверки вызовов к БД.
      - Юнит‑тесты валидаторов модели Currency и работы DatabaseController (создание/обновление/удаление, связи подписок).
      - Результат прогона python3 -m unittest lab9/tests.py: 7 tests, OK (0.001s).
7) Выводы:
      - MVC соблюдён: модели — только данные/валидация, контроллеры — бизнес‑логика и доступ к БД, представления — Jinja2‑шаблоны, маршруты — в AppServer.
      - SQLite в памяти упрощает развёртывание и тестирование, внешние ключи включены (PRAGMA foreign_keys = ON) для целостности подписок.
      - Маршрутизация на http.server через do_GET с обработкой параметров parse_qs; рендеринг шаблонов через общий Environment и единый метод _render_template.
      - CRUD‑операции покрыты примерами SQL и отражены в UI (добавление/обновление/удаление валют, подписки пользователей).
