if [ ! -z "$(ls -A ./)" ]; then
    echo -n "WARNING: Directory not empty. Continue? [Y/n] "
    read RUN_NOT_EMPTY

    if !([ -z $RUN_NOT_EMPTY ] || [ $RUN_NOT_EMPTY = "y" ] || [ $RUN_NOT_EMPTY = "Y" ]); then
        echo "Stopping."
        exit
    fi
fi

wget https://github.com/Ted-Barrett/easycloudflareddns/archive/main.tar.gz
tar -xf main.tar.gz --strip-components 1 && rm main.tar.gz

echo -n "Would you like to run the setup now? [Y/n] "
read RUNSETUP

if [ -z $RUNSETUP ] || [ $RUNSETUP = "y" ] || [ $RUNSETUP = "Y" ]; then
    python3 createconfig.py
else
    echo "Stopping."
fi
