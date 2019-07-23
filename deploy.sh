if test $# -eq 1
then
	attr=$1
elif test $# -eq 0
then
	attr='-s'
else 

	echo "expect 0 or 1 attributes, but actual got ($attr) attributes"
	attr='-h'
fi

echo "Welcome to ML+ project. \n"
cd ./gradingwebapp/gmugrader/dockerfiles


if test ! -e ./log_build.txt -o $attr = '-b'
then
	echo "To deploy this project, docker-compose and docker CE for linux (Or other versions Docker on difference os) are required."
	echo "\n"
	echo "If not sure, please open another terminal..."
	echo "To check if docker have already install, run 'docker -v', if installed, a version information will appear"
	echo "To check if docker-compose have already install, run 'docker-compose -v', if installed, a version information will appear. If you already have docker and pip, you can run 'pip install docker-compose' to install it\n\n"

	echo "Do you already install docker and docker-compose? (yes/no) \n>"
	read is_Docker

	if test $is_Docker = 'yes'
	then
		echo "You have docker already!"
	else 
		echo "This project required docker for deploy. Now we will leave."
		echo "To install docker, please visit https://docs.docker.com/install and following the guide."
		echo "To install docker-compose, please visit https://docs.docker.com/compose/install/ and following the guide."
		echo "If you try to deploy ML+ on AWS, just use run 'apt install docker' for install docker"
		echo "We actually leave now."
		exit 0
	fi
	echo "Welcome to ML+ project, again. "
	echo "You are try to build/rebuild everything of ML+ now. If you do not want to do that, enter CONTROL+C to stop\n"	
	cd ../gmugrader
	echo "Your currect ALLOWED HOSTS are followings:"
	sed -n "s/ALLOWED_HOSTS.*\[\(.*\\)]/\1/p"  ./settings.py
	echo "\n"
	echo "Does your own address appeared in the above list?(yes\N)\n>"
	read check
	if test $check = 'yes'
	then
		echo "\nYour IP address have appeared already. Start project."
	else
		echo "\nTo build the project, please enter your server's IP address or your own Domain name:\n>"
		read my_address
		sed "s/ALLOWED_HOSTS[[:space:]]*=[[:space:]]*\[/ALLOWED_HOSTS = ['$my_address',/" ./settings.py > ./tem
		mv ./tem ./settings.py
		echo "Your IP address have appeared already. Start project."
	fi
	cd ../../../..
	tar -cvf dmgrader.tar dmgrader
	mv dmgrader.tar ./dmgrader/gradingwebapp/gmugrader/dockerfiles
	cd ./dmgrader/gradingwebapp/gmugrader/dockerfiles
	docker-compose build 
	rm -f dmgrader.tar
	echo "project have been deploy already......"
        echo "start to run project"
	echo $my_address > ./log_build.txt
	docker-compose up 
elif test $attr = '-m'
then
	echo "maintenance mode: please enter you command:"
	read user_command
	$user_command
elif test $attr = '-s'
then
	echo "start\n"
	docker-compose up 
elif test $attr = '-h'
then
	echo "-b	rebuild everything"
	echo "-m	maintenance mode, do anything you like"
	echo "-s	start django"
	echo "nothing	depend on situation...default is start django"
	echo "-h	re echo above messages including this message"
else 
	echo "unexpect attribute. expect -b, -m, -h, -s or [nothing], but received $1"
	echo "-b	rebuild everything"
	echo "-m	maintenance mode, do anything you like"
	echo "-s	start django"
	echo "nothing	depend on situation...default is start django"
	echo "-h	re echo above messages including this message"
fi

