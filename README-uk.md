# exchange-rates-tg-bot

## IMPORTANT INFORMATION

Цей репозиторій більше <b>НЕ ПІДТРИМУЄТЬСЯ</b>. Подальші оновлення бота відбувається з закритим вихідним кодом.<br><br>
ОРИГІНАЛЬНИЙ бот від розробників тут: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a>. Всі інші боти це не офіційні форки, ми не гарантуємо безпеку ваших даних, якщо ви користуєтесь іншими ботами.
<hr>

ERTB – exchange rates telegram bot.<br>
Бот створений для розпізнавання в тексті пар чисел та валют, з автоматичною наступною конвертацією в інші валюти за актуальними курсами. Приклад працюючого бота: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br>
<hr>
<h3>Навігація</h3>
<ol>
  <li><a href="#example">Приклад роботи</a></li>
  <li><a href="#features">Характеристики бота</a></li>
  <li><a href="#before">Що зробити перед першим запуском?</a></li>
  <li><a href="#running">Як запустити бот?</a></li>
  <li><a href="#commands">Команди у Telegram</a>:
    <ol>
      <li><a href="#commands-user">для пересічного користувача</a></li>
      <li><a href="#commands-admin">для адміністратора</a></li>
    </ol>
  </li>
</ol><br>
<hr id="example">
<h3>Приклад роботи бота</h3>
Ваше повідомлення:<br>
<pre>5 баксів</pre>
Відповідь бота:
<pre>5.0 USD<br>
4.13 EUR
365.98 RUB
139.83 UAH</pre>
Інакше повідомлення:<br>
<pre>Я купив акції по двадцять п'ять доларів, тепер вони коштують 43 долари.</pre>
Відповідь бота
<pre>25.00 USD<br>
22.90 EUR
19.67 GBP<br>
0.000813843 BTC
0.012757250 ETH<br>
======
43.00 USD<br>
39.39 EUR
33.84 GBP<br>
0.001399810 BTC
0.021942470 ETH</pre><br>
<hr id="features">
<h3>Характеристики бота</h3>
<table>
  <tr>
    <th>Мови інтерфейсу боту</th>
    <td>
    <ul>
    <li><b>Англійська</b></li>
    <li><b>Білоруська</b></li>
    <li><b>Німецька</b></li>
    <li><b>Польська</b></li>
    <li><b>Португальська (бразильська)</b></li>
    <li><b>російська</b></li>
    <li><b>Українська</b></li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Мови, які підтримує W2N<br>
    ("Двадцять п'ять гривень" буде розпізнано як "25 UAH")</th>
    <td>
    <ul>
    <li><b>Англійська</b></li>
    <li><b>Білоруська</b></li>
    <li><b>Німецька</b></li>
    <li><b>російська</b></li>
    <li><b>Українська</b></li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Розпізнавання та конвертація національних валют</th>
    <td>161 валюта, а також золото та срібло (в унціях).</td>
  </tr>
  <tr>
    <th>Покращене розпізнавання національних валют</th>
    <td>
    <ul>
    <li><b>Англійська</b> – 47, а також золото та срібло (в унціях)</li>
    <li><b>Білоруська</b> – 59, а також золото та срібло (в унціях)</li>
    <li><b>Німецька</b> – 161, а також золото та срібло (в унціях)</li>
    <li><b>російська</b> <i>(підтримку закінчено)</i> – 25, а також золото та срібло (в унціях)</li>
    <li><b>Українська</b> – 50, а також золото та срібло (в унціях)</li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Розпізнавання та конвертація криптовалют</th>
    <td>ADA, AVAX, BCH, BNB, BTC, DASH, DOGE, DOT, ETC, ETH, LTC, MATIC, RVN, SHIB, SOL, TRX, XLM, XMR, XRP.</td>
  </tr>
  <tr>
    <th>Покращене розпізнавання криптовалют</th>
    <td>ADA, AVAX, BCH, BNB, BTC, DASH, DOGE, DOT, ETC, ETH, LTC, MATIC, RVN, SHIB, SOL, TRX, XLM, XMR, XRP.</td>
  </tr>
  <tr>
    <th>API національних валют валют</th>
    <td><a href="http://data.fixer.io/api/">Fixer.io</a> (раз у добу)</td>
  </tr>
  <tr>
    <th>API криптовалютвалют</th>
    <td><a href="https://api.binance.com/api/v3/">Binance.com</a> (декілька разів за хвилину)</td>
  </tr>
</table><br>
<hr id="before">
<h3>Перед запуском боту</h3>
Якщо ви завантажили код з розділу <code>"Releases"</code>, то відкрийте файл <code>Token.py</code> та заповніть відповідні змінні. Якщо ви скачали код з головної сторінки, або у вас відсутній файл <code>Token.py</code>, то створіть файл з таким іменим розмістіть поруч з <code>ERTB.py</code>. Потім заповніть його таким чином:<br>
<table>
  <tr>
    <th>Назва змінної</th>
    <th>Значення змінної</th>
    <th>Приклад</th>
    <th>Де взяти</th>
  </tr>
  <tr>
  <td><code>botToken</code></td>
  <td>Токен вашого бота, який ви використовуватимете для автентифікації свого бота та надання йому доступу до API телеграму.</td>
  <td><code>botToken="1234567890:BBCkM9ooUa4NKGa8asdGdsa1iB4qwqZTqlc"</code></td>
  <td>В Telegram у бота <a href="https://t.me/BotFather">@BotFather</a></td>
  </tr>
  <tr>
  <td><code>apiKey</code></td>
  <td>Ключ для <a href="https://fixer.io/">Fixer.io</a>, щоб користуватись API національних валют.</td>
  <td><code>apiKey="2597f6f5j2f0fc8bf228c7f798ghgkleb"</code></td>
  <td>На <a href="https://apilayer.com/marketplace/fixer-api#pricing">цій</a> сторінці сайту.</td>
  </tr>
  <tr>
  <td><code>botUsername</code></td>
  <td>Юзернейм бота, такий який ви налаштували в <a href="https://t.me/BotFather">@BotFather</a></td>
  <td><code>botUsername = "test_bot"</code></td>
  <td>В Telegram у бота <a href="https://t.me/BotFather">@BotFather</a></td>
  </tr>
<table><br>
<hr id="running">
<h3>Запуск бота</h3>
За замовчуванням бот запускається так:
<pre>python3 ERTB.py</pre>
Також можна увімнкути логування в термінал:
<pre>python3 ERTB.py -l 1</pre>
або
<pre>python3 ERTB.py --logs 1</pre><br>
Всі аргументи для запуску:
<table>
  <tr>
    <th>Назва</th>
    <th>Аргумент</th>
    <th>Значення</th>
    <th>Приклад</th>
    <th>За замовчуванням</th>
  </tr>
  <tr>
    <td>Логування у термінал</td>
    <td><code>--logs</code> або <code>-l</code></td>
    <td><code>1</code> або <code>0</code></td>
    <td><code>python3 ERTB.py --logs on</code></td>
    <td><code>0</code></td>
  </tr>
  <tr>
    <td>Додати адміністратора для боту</td>
    <td><code>--admin</code> або <code>-a</code></td>
    <td>ID юзера</td>
    <td><code>python3 ERTB.py --admin 123456789</code></td>
    <td>відсутнє</td>
  </tr>
  <tr>
    <td>Опрацювання повідомлень, що надійшли від API Телеграму при старті бота</td>
    <td><code>--updates</code> або <code>-u</code></td>
    <td><code>1</code> або <code>0</code></td>
    <td><code>python3 ERTB.py --updates 1</code></td>
    <td><code>0</code></td>
  </tr>
</table><br>
<hr id="commands">
<h3 id="commands-user">Команди в Telegram для користувача</h3>
<table>
  <tr>
    <th>Команда</th>
    <th>Опис команди</th>
  </tr>
  <tr>
    <td><code>/about</code></td>
    <td>Коротка інформація про авторів, версія, API, код та ліцензію.</td>
  </tr>
  <tr>
    <td><code>/help</code></td>
    <td>Довідка про бота, користування командами та налаштуваннями.</td>
  </tr>
  <tr>
    <td><code>/settings</code></td>
    <td>Налаштування бота у поточному чаті.</td>
  </tr>
  <tr>
    <td><code>/donate</code></td>
    <td>Посилання на донат для розробників.</td>
  </tr>
</table><br>
<h3 id="commands-admin">Команди в Telegram для адміністраторів</h3>
<table>
  <tr>
    <th>Команда</th>
    <th>Опис команди</th>
    <th>Приклад використання</th>
    <th>Результат</th>
  </tr>
  <tr>
    <td>
    <code>/echo</code>
    </td>
    <td>
      Розсилка повідомлень по всіх чатах. Підтримує HTML-розмітку.
    </td>
    <td>
    <code>/echo Тестова розсилка з &lt;a href="google.com"&gt;посиланням&lt;/a&gt;.</code>
    </td>
    <td>
    <code>Тестова розсилка з <a href="google.com">посиланням</a>.</code>
    </td>
  </tr>
  <tr>
    <td>
    <code>/write</code>
    </td>
    <td>
      Написати у конкретний чат. Підтримує HTML-розмітку.
    </td>
    <td>
    <code>/write 12345789 Тестова розсилка з &lt;a href="google.com"&gt;посиланням&lt;/a&gt;.</code>
    </td>
    <td>
    <code>Тестова розсилка з <a href="google.com">посиланням</a>.</code>
    </td>
  </tr>
  <tr>
    <td><code>/count</code></td>
    <td>Підрахунок кількості активних користувачів бота. Параметр <code>short</code> означає, що підрахунок буде вестись лише по групових чатах.</td>
    <td><code>/count</code> or <code>/count short</code></td>
    <td><code>The number of members of group chats: 396306</code></td>
  </tr>
  <tr>
    <td><code>/newadmin</code></td>
    <td>Додати адміністратора.</td>
    <td><code>/newadmin 123456789</code></td>
    <td>Буде доданий новий адмін.</td>
  </tr>
  <tr>
    <td><code>/amount</code></td>
    <td>Кількість чатів та груп у яких хоча би раз користувались ботом за весь час, добу, тиждень та місяць.</td>
    <td><code>/amount</code></td>
    <td><p>For all the time:<br>PM: 32235<br>Groups: 11938<br><br>In 24 hours:<br>PM: 549<br>Groups: 998<br><br>In a week:<br><br>PM: 1662<br>Groups: 1928<br>In 30 days:<br>PM: 3522<br>Groups: 2859</p></td>
  </tr>
  <tr>
    <td><code>/plotamount</code></td>
    <td>Графік кількості чатів та груп у яких хоча би раз користувались ботом за весь час, добу, тиждень та місяць з розбивкою по днях.</td>
    <td><code>/plotamount</code></td>
    <td>Графіки</td>
  </tr>
  <tr>
    <td><code>/stats</code></td>
    <td>Статистика по використанню бота користувачами за день, тиждень та місяць.</td>
    <td><code>/amount</code></td>
    <td><p>Bot activity:<br><br>Today: 6095<br>In the last week: 101781<br>In this month: 299825<br><br>Unique users:<br><br>Today: 1985<br>In the last week: 12802<br>In the last month: 23628</p></td>
  </tr>
  <tr>
    <td><code>/plotstats</code></td>
    <td>Графіки по статистиці використання бота за різні проміжки часу.</td>
    <td><code>/plotstats</code></td>
    <td>Графіки</td>
  </tr>
  <tr>
    <td><code>/backup</code></td>
    <td>Надсилає архів з копіями баз даних.</td>
    <td><code>/backup</code></td>
    <td>Архів з бекапами баз данних.</td>
  </tr>
  <tr>
    <td><code>/chats</code></td>
    <td>Надсилає файл зі списком ID всіх чатів (групових та приватних)</td>
    <td><code>/chats</code></td>
    <td>Файл зі списком ID всіх чатів (групових та приватних).</td>
  </tr>
  <tr>
    <td><code>/ban</code></td>
    <td>Заблокувати користувача/груповий чат по ID.</td>
    <td><code>/ban 123456789</code></td>
    <td><code>User/group successfully blocked.</code></td>
  </tr>
  <tr>
    <td><code>/unban</code></td>
    <td>Розблокувати користувача/груповий чат по ID.</td>
    <td><code>/unban 123456789</code></td>
    <td><code>User/group has been successfully unblocked.</code></td>
  </tr>
</table>
