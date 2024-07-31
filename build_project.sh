printf '......\nEstablishing GMU ML+ Control, Standby......\n......\n'

printf "Welcome to ML+ project. \n\n\n"
address=`find -type d -name "dockerfiles"`
cd $address

if test ! -e ./log_build.txt
then 
	database=1
else
	database=0
fi

# Welcome to ML+ !
printf "To deploy this project, docker-compose and Docker CE for linux (Or other versions Docker on difference os) are required.\n"
printf "If not sure, please open another terminal...\n"
printf "To check if docker have already install, run 'docker -v', if installed, a version information will appear\n"
printf "To check if docker-compose have already install, run 'docker-compose -v', if installed, a version information will appear. If you already have docker and pip, you can run 'pip install docker-compose' to install it\n\n"
printf "Do you already install BOTH Docker and docker-compose? (yes/N) \n>"
read is_Docker
printf "\n"

# ASK if User have Docker and docker-compose already. if they don't add it, tell user how to install them and exit. 

if test $is_Docker = 'yes'
then
	printf "\n\nYou have docker already!"
else 
	printf "\n\nThis project required docker for deploy. Now we will leave.\n"
	printf "To install docker, please visit https://docs.docker.com/install and following the guide.\n"
	printf "To install docker-compose, please visit https://docs.docker.com/compose/install/ and following the guide.\n"
	printf "If you try to deploy ML+ on AWS, just use run 'apt install docker' for install docker\n"
	printf "After that, we need add your user into group by following command (see https://docs.docker.com/install/linux/linux-postinstall/#manage-docker-as-a-non-root-user) :"
	printf "\nsudo usermod -aG docker \$USER\n"
	printf "And then start docker daemon, by following command (see https://docs.docker.com/config/daemon/systemd/) :"
	printf "\nsudo systemctl start docker\n"
	printf "\n\nWe actually leave now. Good luck for your new Docker\n\n"
	exit 0
fi


printf "GMU ML+ Servers Established\n"
printf "You are try to build/rebuild everything of ML+ now. If you do not want to do that, enter CONTROL+C to stop\n"	
printf "START TO MAKE SOME SETTING......STANDBY\n"	

#### Start to set something....

### Start to set settings.py

## Start to set IP

# read server's out ip address, or use user's own ip. 
cd ../gmugrader

ip_address=`curl ifconfig.me` 


#check if our own ip added in the allowed host? do nothing : add external ip inside. 
sed "s/'$ip_address',//g" ./settings.py > ./tem
sed -i "s/ALLOWED_HOSTS[[:space:]]*=[[:space:]]*\[/ALLOWED_HOSTS = ['$ip_address',/" ./tem 

printf "\n\nYour currect ALLOWED HOSTS are followings:\n"
sed -n "s/ALLOWED_HOSTS.*\[\(.*\\)]/\1/p"  ./tem
printf "\nYour external IP Address is : $ip_address\n"
printf "Does your wish to add new IP in the above list?(yes\N)\n>"
read check_IP
printf "\n"

if test $check_IP = 'yes'
then
	printf "Please enter the IP address you wish to add:\n"
	read my_address
	sed -i "s/'$my_address',//g" ./tem
	sed -i "s/ALLOWED_HOSTS[[:space:]]*=[[:space:]]*\[/ALLOWED_HOSTS = ['$my_address',/" ./tem 
	printf "Your IP address have been added already. \nStart edit Database.\n"
else
	printf "Your IP address have appeared already. \nStart edit Database.\n"
fi

ip_list=`sed -n "s/ALLOWED_HOSTS.*\[\(.*\\)]/\1/p"  ./tem`

printf 'IP setting Finished.'
## FINISH set IP

## Set Database
# Database ONLY SET ONCE!!!!
if [ "$database" = 1 ]
then
	printf '\n\nStart to setting Database......\n'
	printf 'Following things are your original settings, will all removed after setting.\n'
	printf 'Your Database Name is:\n'
	sed -n "s/^[[:space:]]*'NAME'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem
	printf '\nYour Database User Name is:\n'
	sed -n "s/^[[:space:]]*'USER'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem
	printf '\nYour Database User Password is:\n'
	# No, we never want that!
	sed -n "s/^[[:space:]]*'PASSWORD'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem
	#printf '<Not_My_Password>\n\n'

	#printf "Do your wish to change Database's NAME, USER, and PASSWORD?(yes\N)\n>"
	#read check_DB
	#printf "\n"

	#if test $check_DB = 'yes'
	#then
	printf '\n\nNow we start to set your Database. Please input your Database name, Username and Password\n'
	printf 'Database name:\n'
	read db_dbname
	printf 'Database User name:\n'
	read db_username
	stty -echo
	echo "Database User $db_username PASSWORD: "
	read db_password
	stty echo
	printf "\n"

	sed -i "s/'NAME'[[:space:]]*:[[:space:]]*'.*',/'NAME': '$db_dbname',/g" ./tem
	sed -i "s/'USER'[[:space:]]*:[[:space:]]*'.*',/'USER': '$db_username',/g" ./tem
	sed -i "s/'PASSWORD'[[:space:]]*:[[:space:]]*'.*',/'PASSWORD': '$db_password',/g" ./tem

	#else
	#	printf "\n\nYou do not want to change DB settings. Start to Setting port.\n"

	#fi
fi
db_new_name=`sed -n "s/^[[:space:]]*'NAME'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem`
db_new_user=`sed -n "s/^[[:space:]]*'USER'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem`
db_new_password=`sed -n "s/^[[:space:]]*'NAME'[[:space:]]*:[[:space:]]'\(.*\)',/\1/p"  ./tem`
### Finish setting setting.py. Store it. DB need other file to set, hold on. 
mv ./tem ./settings.py

## Continue setting DB, in docker-compose.yml
cd ../dockerfiles
# Fake ending, just make things look better....
# To make output look good, I give up the logic. 
printf 'Database setting finished.\n\n'

## Setting port first. 
printf 'Now we start to setting port.'
printf 'Your Old port is:\n'
sed -n "s/[[:space:]]*-[[:space:]]*\"\([0-9]\+\):[0-9]\+\"/\1/p"  ./docker-compose.yml
printf 'Do you want to setting a new outside port?(yes\N)\n>\n'
read check_Port
printf "\n"


if test $check_Port = 'yes'
then
	printf 'Which port do your like best? Input the port your like in following:\n'
	read my_port
	sed -i "s/\"[0-9]\+:8000\"/\"$my_port:8000\"/g" ./docker-compose.yml
else
	printf 'No setting applied on port.\n'
fi

port=`sed -n "s/[[:space:]]*-[[:space:]]*\"\([0-9]\+\):[0-9]\+\"/\1/p"  ./docker-compose.yml`

## Finish setting Port

if [ "$database" = 1 ]
then
	sed -i "s/POSTGRES_USER=.*$/POSTGRES_USER=$db_username/g" ./docker-compose.yml
	sed -i "s/POSTGRES_PASSWORD=.*$/POSTGRES_PASSWORD=$db_password/g" ./docker-compose.yml
	sed -i "s/POSTGRES_DB=.*$/POSTGRES_DB=$db_dbname/g" ./docker-compose.yml
fi

## Finish setting database

## Finish setting docker-compose.yml

#### Finish setting
printf "Finish setting.\n"


## Start Build

printf "\n\n\n\nEstablish Project Control, Standby....\n"

cd ../../../..
tar -cvf dmgrader.tar dmgrader
mv dmgrader.tar ./dmgrader/gradingwebapp/gmugrader/dockerfiles
cd ./dmgrader/gradingwebapp/gmugrader/dockerfiles
docker-compose build 
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
docker-compose run web python manage.py collectstatic --noinput
rm -f dmgrader.tar
printf "project have been deploy already......\n"

currect_time=`date`
my_id=`uname -a`



printf "Last build/rebuild time: $currect_time\nLast build/rebuild user: $my_id\n\nSettings of last rebuild:\nAllowed_IPs = [$ip_list]\n
Database:\n\tIS_SETED_LAST_TIME:$database\n\tNAME:$db_new_name\n\tUSER:$db_new_user\n\tPASSWORD:$db_new_password\n" > ./log_build.txt


docker-compose up -d










