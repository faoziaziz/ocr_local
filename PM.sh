#!/bin/bash

#script untuk restart aplikasi

date

var=$(ps axu | grep -v grep | grep "python3 ocrgrit_png.py")
        if [ ! -z "$var" ];
                then echo "found";
        else
            while true
            do
                python3 ocrgrit_png.py|more
                sleep 10
            done
fi

