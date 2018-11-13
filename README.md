# tochirp
This is a simple converter that converts a CSV file into a format that CHIRP can understand

To get the help file, run with the -h option

See below for example

> % ./tochirp.py -h
> usage: tochirp.py [-h] [--input INPUT] [--output OUTPUT]
>                  [--parser {wia,default}]
>                  [--prefix-filter {vk3,vk2,vk1,vk4,vk5,custom,none}]
>                  [--band-filter {2m,70cm,2m-70cm,none}]
>                  
>
>CHIRP CSV Converter version(1.0.0 rv1)
>  Copyright Enzo Reyes (License GPLv3)
>
>optional arguments:
> -h, --help            show this help message and exit
> --input INPUT         The Input CSV to convert
> --output OUTPUT       the output CSV in CHIRP format
> --parser {wia,default}
> .  CSV Input type
>  --prefix-filter {vk3,vk2,vk1,vk4,vk5,custom,none}
> .  Filter for Repeater Prefix
> --band-filter {2m,70cm,2m-70cm,none}
                        Band filter

>Example usage:
>....    ./tochirp.py --input foo.csv --output bar.csv --parser wia --prefix-filter vk2 --band-filter 70cm
