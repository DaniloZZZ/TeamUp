mkdir teams

echo ">killing all python processes"
killall -9 python
echo ">starting bot"
python bot.py &
echo ">starting data server"
python server.py &
echo ">starting frontend server"
cd web
npm start >/dev/null &

