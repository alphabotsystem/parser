source /run/secrets/alpha-service/key
if [[ $PRODUCTION_MODE == "1" ]]
then
	python app/parser.py
else
	python -u app/parser.py
fi