curl --request GET "https://www.pref.fukuoka.lg.jp/contents/covid19-hassei.html" | grep '<strong>福岡地域' -A 99 | sed -e 's/<[a-z =:;"%0-9]*>//g' -e 's/<\/[a-z]*>//g' -e '/地域/d' -e '/県外/d' -e '/^$/d '
