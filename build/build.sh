#!/bin/sh

check_make_ok() {
  if [ $? != 0 ]; then
    echo ""
    echo "Make Failed..."
    echo "Please check the messages and fix any problems. If you're still stuck,"
    echo "then please email all the output and as many details as you can to"
    echo "  project-laika.com"
    echo ""
    exit 1
  fi
}

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
  sudo rm -f /etc/udev/rules.d/99-lklibftdi.rules
  sudo rm -f /home/pi/.local/lib/python2.7/site-packages/laika -R
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

echo [Install FTDI udev Rule]
sudo cp ../rules/99-lklibftdi.rules /etc/udev/rules.d/99-lklibftdi.rules

echo [Install Python Modules to /home/pi/.local/lib/python2.7/site-packages]
sudo cp -R ../source/py_api/laika /home/pi/.local/lib/python2.7/site-packages

echo
echo All Done.
echo ""
echo "NOTE: You can now run the examples: browse to source/examples/py_test and type: python example_1.py"
echo 
echo
