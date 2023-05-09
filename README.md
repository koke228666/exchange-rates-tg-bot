# exchange-rates-tg-bot

<img alt="GitHub" src="https://img.shields.io/github/license/VirtualSoftKey/exchange-rates-tg-bot?style=flat-square"> <img alt="GitHub release (latest by date)" src="https://img.shields.io/github/release/VirtualSoftKey/exchange-rates-tg-bot?style=flat-square"><br>
<img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/downloads-pre/VirtualSoftKey/exchange-rates-tg-bot/1.6.2/total?style=flat-square"> <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/downloads-pre/VirtualSoftKey/exchange-rates-tg-bot/2.0.0/total?style=flat-square"> <img alt="GitHub release (latest by date including pre-releases)" src="https://img.shields.io/github/downloads-pre/VirtualSoftKey/exchange-rates-tg-bot/3.0.0.3/total?style=flat-square"><br>
<img alt="GitHub Workflow Status" src="https://img.shields.io/github/actions/workflow/status/VirtualSoftKey/exchange-rates-tg-bot/main.yml?style=flat-square"> <img alt="open issues" src="https://img.shields.io/github/issues-raw/VirtualSoftKey/exchange-rates-tg-bot?style=flat-square">
<br>
<b>Requirements (versions are specified on which the bot was developed and tested):</b>
<ul>
  <li>Python 3.10</li>
  <li>Aiogram 2.25</li>
  <li>uvloop 0.17.0 (not support at Windows)</li>
  <li>ujson 5.7.0</li>
  <li>cchardet 2.1.7</li>
  <li>aiodns 3.0.0</li>
  <li>aiohttp[speedups] 3.8.4</li>
  <li>Requests 2.29.0</li>
  <li>Pandas 2.0.1</li>
</ul>
<b id='en'>ENGLISH VERSION</b><br>Ukrainian <a href="#ua">here</a><br><br>
ERTB – exchange rates telegram bot.<br>
The bot is created to recognize pairs of numbers and currencies in the text, with automatic further conversion to other currencies at current rates. An example of a working bot: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br><br>
<b>An example of bot work</b><br>
Your message:<br>
<pre>5 dollars</pre>
Bot answer:
<pre>🇺🇸5.0 USD<br>
🇪🇺4.13 EUR
🇷🇺365.98 RUB
🇺🇦139.83 UAH</pre><br>
<b>Features of the bot</b>
<table>
  <tr>
    <th>Text recognition languages</th>
    <td>English, Ukrainian, Russian (no longer updated). Polish and Belarusian are coming soon.</td>
  </tr>
  <tr>
    <th>Bot interface languages</th>
    <td>English, Ukrainian, Russian. Polish and Belarusian are coming soon.</td>
  </tr>
  <tr>
    <th>Recognizing and converting national currencies</th>
    <td>161 currencies, gold and silver (in ounces).</td>
  </tr>
  <tr>
    <th>Enhanced recognition of national currencies</th>
    <td>29 national currencies, gold and silver (in ounces).</td>
  </tr>
  <tr>
    <th>Recognizing and converting cryptocurrencies</th>
    <td>ADA, BCH, BNB, BTC, DASH, DOGE, ETC, ETH, LTC, RVN, TRX, XLM, XMR, XRP.<br>
    SOL, MATIC, DOT, SHIB, AVAX, TON are coming soon.</td>
  </tr>
  <tr>
    <th>Enhanced cryptocurrency recognition</th>
    <td>ADA, BCH, BNB, BTC, DASH, DOGE, ETC, ETH, LTC, RVN, TRX, XLM, XMR, XRP</td>
  </tr>
  <tr>
    <th>API for national currencies</th>
    <td><a href="http://data.fixer.io/api/">Fixer.io</a> (once a 24 hour)</td>
  </tr>
  <tr>
    <th>API for cryptocurrencies</th>
    <td><a href="https://api.binance.com/api/v3/">Binance.com</a> (several times a minute)</td>
  </tr>
</table><br>

<b>Running the bot</b><br>
By default, the bot can be run as follows:
<pre>python3 ERTB.py</pre>
You can also enable logging in the terminal:
<pre>python3 ERTB.py -l on</pre>
or
<pre>python3 ERTB.py --logs on</pre><br>
All the arguments for run:
<table>
  <tr>
    <th>Name</th>
    <th>Argument</th>
    <th>Value</th>
    <th>Example</th>
    <th>Default</th>
  </tr>
  <tr>
    <td>Logging messages and errors to the terminal</td>
    <td><code>--logs</code> or <code>-l</code></td>
    <td><code>on</code> or <code>off</code></td>
    <td><code>python3 ERTB.py --logs on</code></td>
    <td><code>off</code></td>
  </tr>
  <tr>
    <td>Adding an administrator for the bot</td>
    <td><code>--admin</code> or <code>-a</code></td>
    <td>user ID</td>
    <td><code>python3 ERTB.py --admin 123456789</code></td>
    <td>none</td>
  </tr>
  <tr>
    <td>Processing received messages on start</td>
    <td><code>--updates</code> or <code>-u</code></td>
    <td><code>on</code> or <code>off</code></td>
    <td><code>python3 ERTB.py --updates on</code></td>
    <td><code>off</code></td>
  </tr>
</table><br>
<b>Commands in Telegram for the user</b><br><br>
<table>
  <tr>
    <th>Command</th>
    <th>Command description</th>
  </tr>
  <tr>
    <td><code>/about</code></td>
    <td>Short information about the authors, version, API, code, and license.</td>
  </tr>
  <tr>
    <td><code>/help</code></td>
    <td>Information about the bot, commands, and settings.</td>
  </tr>
  <tr>
    <td><code>/settings</code></td>
    <td>Setting up a bot in the current chat.</td>
  </tr>
  <tr>
    <td><code>/donate</code></td>
    <td>Link to the donation for developers.</td>
  </tr>
  <tr>
    <td><code>/wrong</code></td>
    <td>A command to report an incorrect recognition of a message by a bot.</td>
  </tr>
</table><br>
<b>Commands in Telegram for administrators</b><br><br>
<table>
  <tr>
    <th>Command</th>
    <th>Command description</th>
  </tr>
  <tr>
    <td>
    <code>/echo</code>
    </td>
    <td>
    Sending messages to all chats.<br>
    Example of use: <code>/echo Test messaging</code><br>
    Users will receive: <code>Test messaging</code>
    </td>
  </tr>
  <tr>
  <td>
  <code>/write</code>
  </td>
  <td>
  Write to a specific chat.<br>
  Example of use:: <code>/write 12345789 Test message</code><br>
  The chat user(s) will receive: <code>Test message</code>
  </td>
  </tr>
  <tr>
    <td><code>/count</code></td>
    <td>Counting the number of active users of the bot. You can write <code>/count short</code> and the count will be kept only for group chats.</td>
  </tr>
  <tr>
    <td><code>/newadmin</code></td>
    <td>Add an administrator. Example: <code>/newadmin 123456789</code></td>
  </tr>
  <tr>
    <td><code>/stats</code></td>
    <td>Number of chats and groups where the bot has been used at least once.</td>
  </tr>
  <tr>
    <td><code>/fullstats</code></td>
    <td>The number of chats and groups in which the bot was used at least once for the all time, 24 hours, week, and month.</td>
  </tr>
  <tr>
    <td><code>/backup</code></td>
    <td>Sends an archive with copies of databases.</td>
  </tr>
  <tr>
    <td><code>/ban</code></td>
    <td>Block a user/group chat by ID. <code>/ban 123456789</code></td>
  </tr>
  <tr>
    <td><code>/unban</code></td>
    <td>Unblock user/group chat by ID. <code>/unban 123456789</code></td>
  </tr>
</table>
<br><br><br>
<b id='ua'>UKRAiNIAN VERSION</b><br>English <a href="#en">here</a><br><br>
ERTB – exchange rates telegram bot.<br>
Бот створений для розпізнавання в тексті пар чисел та валют, з автоматичною наступною конвертацією в інші валюти за актуальними курсами. Приклад працюючого бота: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br><br>
<b>Приклад роботи бота</b><br>
Ваше повідомлення:<br>
<pre>5 баксів</pre>
Відповідь бота:
<pre>🇺🇸5.0 USD<br>
🇪🇺4.13 EUR
🇷🇺365.98 RUB
🇺🇦139.83 UAH</pre><br>
<b>Характеристики бота</b>
<table>
  <tr>
    <th>Мови розпізнавання тексту</th>
    <td>Англійська, українська, російська (більше не оновлюється). Польська та білоруська – скоро.</td>
  </tr>
  <tr>
    <th>Мови інтерфейсу боту</th>
    <td>Англійська, українська, російська. Польська та білоруська – скоро.</td>
  </tr>
  <tr>
    <th>Розпізнавання та конвертація національних валют</th>
    <td>161 валюта, а також золото та срібло (в унціях).</td>
  </tr>
  <tr>
    <th>Покращене розпізнавання національних валют</th>
    <td>29 національних валют, а також золото та срібло (в унціях).</td>
  </tr>
  <tr>
    <th>Розпізнавання та конвертація криптовалют</th>
    <td>ADA, BCH, BNB, BTC, DASH, DOGE, ETC, ETH, LTC, RVN, TRX, XLM, XMR, XRP.<br>
    SOL, MATIC, DOT, SHIB, AVAX, TON – скоро.</td>
  </tr>
  <tr>
    <th>Покращене розпізнавання криптовалют</th>
    <td>ADA, BCH, BNB, BTC, DASH, DOGE, ETC, ETH, LTC, RVN, TRX, XLM, XMR, XRP</td>
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

<b>Запуск боту</b><br>
За замовчуванням бот запускається так:
<pre>python3 ERTB.py</pre>
Також можна увімнкути логування в термінал:
<pre>python3 ERTB.py -l on</pre>
або
<pre>python3 ERTB.py --logs on</pre><br>
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
    <td><code>on</code> або <code>off</code></td>
    <td><code>python3 ERTB.py --logs on</code></td>
    <td><code>on</code></td>
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
    <td><code>on</code> або <code>off</code></td>
    <td><code>python3 ERTB.py --updates on</code></td>
    <td><code>off</code></td>
  </tr>
</table><br>
<b>Команди в Telegram для користувача</b><br><br>
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
  <tr>
    <td><code>/wrong</code></td>
    <td>Команда, щоб повідомити про не правильне розпізнавання ботом повідомлення.</td>
  </tr>
</table><br>
<b>Команди в Telegram для адміністраторів</b><br><br>
<table>
  <tr>
    <th>Команда</th>
    <th>Опис команди</th>
  </tr>
  <tr>
    <td>
    <code>/echo</code>
    </td>
    <td>
    Розсилка повідомлень по всіх чатах.<br>
    Приклад використання: <code>/echo Тестова розсилка</code><br>
    Користувачі отримають: <code>Тестова розсилка</code>
    </td>
  </tr>
  <tr>
  <td>
  <code>/write</code>
  </td>
  <td>
  Написати у конкретний чат.<br>
  Приклад використання: <code>/write 12345789 Тестове повідомлення</code><br>
  Користувач(і) чату отримають: <code>Тестове повідомлення</code>
  </td>
  </tr>
  <tr>
    <td><code>/count</code></td>
    <td>Підрахунок кількості активних користувачів бота. Можна написати <code>/count short</code> і підрахунок буде вестись лише по групових чатах.</td>
  </tr>
  <tr>
    <td><code>/newadmin</code></td>
    <td>Додати адміністратора. Приклад: <code>/newadmin 123456789</code></td>
  </tr>
  <tr>
    <td><code>/stats</code></td>
    <td>Кількість чатів та груп у яких хоча би раз користувались ботом.</td>
  </tr>
  <tr>
    <td><code>/fullstats</code></td>
    <td>Кількість чатів та груп у яких хоча би раз користувались ботом за весь час, добу, тиждень та місяць.</td>
  </tr>
  <tr>
    <td><code>/backup</code></td>
    <td>Надсилає архів з копіями баз даних.</td>
  </tr>
  <tr>
    <td><code>/ban</code></td>
    <td>Заблокувати користувача/груповий чат по ID. <code>/ban 123456789</code></td>
  </tr>
  <tr>
    <td><code>/unban</code></td>
    <td>Розблокувати користувача/груповий чат по ID. <code>/unban 123456789</code></td>
  </tr>
</table>