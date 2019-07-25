echo "Welcome to ML+ project."
echo "Establishing GMU ML+ Control, Standby......"
echo "Before we start, let us make decision."
echo "Function List:"
echo "	B - rebuild everything"
echo "	M - make django migrations for database "
echo "	S - stop project server"
echo "	R - run project"
echo "	U - uninstall all things...."
echo "	LOG - show log of build/rebuild record"
echo "	ADMIN - make new ADMIN account"
echo "	DJANGO - enter any django command you like"
echo "	FREE - enter any COMMAND you like" #(e.g. sudo rm -rf)
echo "	<Anything_else> - leave"
printf "What are you want to do? Input the choice, remember this is a case sensitive mutiple choice problem\n>"
read choice
printf "\n"

if test $choice = 'B'
then
	sh ./build_project.sh
elif test $choice = 'M'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	docker-compose run web python manage.py makemigrations
	docker-compose run web python manage.py migrate
elif test $choice = 'S'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	docker-compose stop
elif test $choice = 'R'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	docker-compose up -d
elif test $choice = 'U'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	docker-compose stop 
	docker-compose rm
elif test $choice = 'LOG'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	cat log_build.txt 
elif test $choice = 'ADMIN'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	docker-compose run web python manage.py createsuperuser 
elif test $choice = 'DJANGO'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	printf "Give what you want to do for django.\n>python manage.py "
	read user_django_command
	printf "\n"
	docker-compose run web python manage.py $user_django_command
elif test $choice = 'FREE'
then
	cd ./gradingwebapp/gmugrader/dockerfiles
	echo "FREE mode, better understand what you want to do"
	printf "Give what you want to do for computer, you can do anything you wished.\n>"
	read user_command
	printf "\n"
	$user_command
else
	echo "Unexpect choice.Script exit"
	exit 0
fi

