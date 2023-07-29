# exchange-rates-tg-bot
ERTB – exchange rates telegram bot.<br>
The bot is created to recognize pairs of numbers and currencies in the text, with automatic further conversion to other currencies at current rates. An example of a working bot: <a href="https://t.me/exchange_rates_vsk_bot">ERTB</a><br>
<hr>
<h3>Navigation</h3>
<ol>
  <li><a href="#example">An example of bot work</a></li>
  <li><a href="#features">Features of the bot</a></li>
  <li><a href="#before">Before running the bot</a></li>
  <li><a href="#running">How to run a bot?</a></li>
  <li><a href="#commands">Commands for Telegram</a>:
    <ol>
      <li><a href="#commands-user">for user</a></li>
      <li><a href="#commands-admin">for admin</a></li>
    </ol>
  </li>
</ol><br>
<hr id="example">
<h3>An example of bot work</h3>
Your message:<br>
<pre>5 dollars</pre>
Bot answer:
<pre>🇺🇸5.0 USD<br>
🇪🇺4.13 EUR
🇺🇦139.83 UAH</pre>
Another message:<br>
<pre>I bought the stock for twenty five dollars, and now it's 43 dollars.</pre>
Bot answer:
<pre>🇺🇸25.00 USD<br>
🇪🇺22.90 EUR
🇬🇧19.67 GBP<br>
0.000813843 BTC
0.012757250 ETH<br>
======
🇺🇸43.00 USD<br>
🇪🇺39.39 EUR
🇬🇧33.84 GBP<br>
0.001399810 BTC
0.021942470 ETH</pre><br>
<hr id="features">
<h3>Features of the bot</h3>
<table>
  <tr>
    <th>Bot interface languages</th>
    <td>
    <ul>
    <li><b>Belarusian</b> (coming soon)</li>
    <li><b>Czech</b> (coming soon)</li>
    <li><b>English</b></li>
    <li><b>German</b> (coming soon)</li>
    <li><b>Polish</b></li>
    <li><b>Russian</b></li>
    <li><b>Ukrainian</b></li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Languages for the W2N<br>
    <i>('Twenty-five dollars' is recognized as '$25')</i></th>
    <td>
    <ul>
    <li><b>English</b></li>
    <li><b>German</b> (coming soon)</li>
    <li><b>Polish</b> (coming soon)</li>
    <li><b>Russian</b></li>
    <li><b>Ukrainian</b></li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Recognizing and converting national currencies</th>
    <td>161 currencies, gold and silver (in ounces).</td>
  </tr>
  <tr>
    <th>Enhanced recognition of national currencies</th>
    <td>
    <ul>
    <li><b>English</b> – 47 and gold and silver (in ounces)</li>
    <li><b>German</b> (coming soon)</li>
    <li><b>Polish</b> (coming soon)</li>
    <li><b>Russian</b> <i>(no longer support)</i> – 24 and gold and silver (in ounces)</li>
    <li><b>Ukrainian</b> – 50 and gold and silver (in ounces)</li>
    </ul>
    </td>
  </tr>
  <tr>
    <th>Recognizing and converting cryptocurrencies</th>
    <td>ADA, AVAX, BCH, BNB, BTC, DASH, DOGE, DOT, ETC, ETH, LTC, MATIC, RVN, SHIB, SOL, TRX, XLM, XMR, XRP.</td>
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
<hr id="before">
<h3>Before running the bot</h3>
If you downloaded the code from the <code>"Releases"</code> page, then open the file <code>Token.py</code> and fill in the corresponding variables. If you downloaded the code from the main page, or you do not have the <code>Token.py</code> file, then create a file with that name and place it next to <code>ERTB.py</code>. Then fill it out as below:<br>
<table>
  <tr>
    <th>Name of the variable</th>
    <th>The value of the variable</th>
    <th>Example</th>
    <th>Where to get it</th>
  </tr>
  <tr>
  <td><code>botToken</code></td>
  <td>Your bot's token, which you will use to authenticate your bot and give it access to the Telegram API.</td>
  <td><code>botToken="1234567890:BBCkM9ooUa4NKGa8asdGdsa1iB4qwqZTqlc"</code></td>
  <td>In Telegram, at the bot <a href="https://t.me/BotFather">@BotFather</a></td>
  </tr>
  <tr>
  <td><code>apiKey</code></td>
  <td>A key for <a href="https://fixer.io/">Fixer.io</a> to use the national currency API.</td>
  <td><code>apiKey="2597f6f5j2f0fc8bf228c7f798ghgkleb"</code></td>
  <td>On <a href="https://apilayer.com/marketplace/fixer-api#pricing">this</a> page of the website.</td>
  </tr>
  <tr>
  <td><code>botUsername</code></td>
  <td>The bot's username is the one you set up in <a href="https://t.me/BotFather">@BotFather</a></td>
  <td><code>botUsername = "test_bot"</code></td>
  <td>In Telegram, at the bot <a href="https://t.me/BotFather">@BotFather</a></td>
  </tr>
<table><br>
<hr id="running">
<h3>Running the bot</h3>
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
    <td><code>1</code> or <code>0</code></td>
    <td><code>python3 ERTB.py --logs 1</code></td>
    <td><code>0</code></td>
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
    <td><code>1</code> or <code>0</code></td>
    <td><code>python3 ERTB.py --updates 1</code></td>
    <td><code>0</code></td>
  </tr>
</table><br>
<hr id="commands">
<h3 id="commands-user">Commands in Telegram for the user</h3>
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
</table><br>
<h3 id="commands-admin">Commands in Telegram for administrators</h3>
<table>
  <tr>
    <th>Command</th>
    <th>Command description</th>
    <th>Example</th>
    <th>Result</th>
  </tr>
  <tr>
    <td>
    <code>/echo</code>
    </td>
    <td>
      Sending messages to all chats. Supporting HTML.
    </td>
    <td>
    <code><xmp>/echo Test messaging with <a href="google.com">link</a>.</xmp></code>
    </td>
    <td>
    <code>Test messaging with <a href="google.com">link</a>.</code>
    </td>
  </tr>
  <tr>
    <td>
    <code>/write</code>
    </td>
    <td>
      Write to a specific chat. Supporting HTML.
    </td>
    <td>
      <code><xmp>/echo Test messaging with <a href="google.com">link</a>.</xmp></code>
    </td>
    <td>
    <code>Test messaging with <a href="google.com">link</a>.</code>
    </td>
  </tr>
  <tr>
    <td><code>/count</code></td>
    <td>Counting the number of active users of the bot. The <code>short</code> parameter means that the count will be made only for group chats.</td>
    <td><code>/count</code> or <code>/count short</code></td>
    <td><code>The number of members of group chats: 396306</code></td>
  </tr>
  <tr>
    <td><code>/newadmin</code></td>
    <td>Add an administrator.</td>
    <td><code>/newadmin 123456789</code></td>
    <td>A new admin will be added.</td>
  </tr>
  <tr>
    <td><code>/amount</code></td>
    <td>The number of chats and groups in which the bot was used at least once for the full time, day, week, and month.</td>
    <td><code>/amount</code></td>
    <td><code>For all the time:<br>PM: 32235<br>Groups: 11938<br><br>In 24 hours:<br>PM: 549<br>Groups: 998<br><br>In a week:<br><br>PM: 1662<br>Groups: 1928<br>In 30 days:<br>PM: 3522<br>Groups: 2859</code></td>
  </tr>
  <tr>
    <td><code>/plotamount</code></td>
    <td>A graph of the number of chats and groups in which the bot was used at least once for the entire time, day, week, and month, by day.</td>
    <td><code>/plotamount</code></td>
    <td>Charts</td>
  </tr>
  <tr>
    <td><code>/backup</code></td>
    <td>Sends an archive with copies of databases.</td>
    <td><code>/backup</code></td>
    <td>Archive with database backups.</td>
  </tr>
  <tr>
    <td><code>/ban</code></td>
    <td>Block a user/group chat by ID.</td>
    <td><code>/ban 123456789</code></td>
    <td><code>User/group successfully blocked.</code></td>
  </tr>
  <tr>
    <td><code>/unban</code></td>
    <td>Unblock a user/group chat by ID.</td>
    <td><code>/unban 123456789</code></td>
    <td><code>User/group has been successfully unblocked.</code></td>
  </tr>
</table>
<br>