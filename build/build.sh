#!/bin/sh

check_make_ok() {
	if [ $? != 0 ]; then
		echo ""
		echo "Make Failed..."
		echo "Please check the messages and fix any problems. If you're still stuck,"
		echo "then please email all the output and as many details as you can to"
		echo "  www.project-laika.com"
		echo ""
		exit 1
	fi
}

f_exit(){
	echo ""
	echo "Optional: Add a non-default 'otheruser' after the command (default is:pi)."
	echo "i.e. sudo ./build.sh otheruser"
	echo ""
	exit
}

echo "Running Installer"
if [ -z $1 ]; then
	HDIR="/home/pi"
	USERID="pi"
	GROUPID="pi"
else
	HDIR=/home/$1
	USERID=`id -n -u $1`
	GROUPID=`id -n -g $1`
fi

#Confirm if install should continue with default Pi user or inform about command-line option.
echo ""
echo "Install Details:"
echo "Home Directory: "$HDIR
echo "User: "$USERID
echo "Group: "$USERID
echo ""
if [ ! -d "$HDIR" ]; then
	echo ""; 
	echo "The home directory does not exist!";f_exit;
fi

if [ x$1 = "xclean" ]; then
	echo -n "laika:   "	; make clean
	exit
fi

if [ x$1 = "xexamples" ]; then
	echo -n "laika:   "	; make examples -B
	exit
fi

if [ x$1 = "xuninstall" ]; then
	echo -n "laika: " ; sudo make uninstall
	echo "laika: [Uninstalled]" 
	exit
fi

echo "Laika Build script"
echo "=================="
echo
echo
echo "Laika Library"

sudo make uninstall
sudo make install
check_make_ok
make examples
check_make_ok
sudo make clean
check_make_ok

echo
echo All Done.
echo ""
echo "NOTE: You can now run the examples: type: cd ../source/examples/py_test"
echo "and then type: python example_1.py"
echo 
echo
