#!/usr/bin/python

__version__="1.0.0 rv1"

import sys
import csv
import argparse
import math

#COMMON SYMBOLS
__greeting__ = 'CHIRP CSV Converter version('+ __version__+')\n  Copyright Enzo Reyes (License GPLv3) \n\n'
__chirp_header__ = 'Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL'

#BAND CONSTANT
__10M__  = '10M'
__6M__   = '6M'
__2M__   = '2M'
__70CM__ = '70CM'
__23CM__ = '23CM'
__ALL__ = '*'


def wia_converter(prefix, band, inputCSV, output_csv):
    first_line = True
    note_row = 12
    line_count = 0

    prefix_found = False
    band_found = False

    #Read through the CSV and filter the data out, into this array
    selected_entries = []
    with open(inputCSV) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            line_count = line_count + 1
            if first_line:
                first_line = False
                continue
            #print(row)
            if  not row[0]  and row[note_row]:
                #print('Info Line at ' + str(line_count) + '-> '+ row[note_row])
                info_note = row[note_row]
                parsed_info = info_note[2:-2]
                if len(parsed_info) < 5:
                    prefix_found = False
                    band_found = False
                    continue
                seperated_info = parsed_info.split(";")
                band_section = seperated_info[0]
                mode_section = seperated_info[1]
                prefix_section = seperated_info[2]
                #print ('Section Band: '+band_section+' ||  Mode: '+mode_section+' || Prefix '+prefix_section)
                if band[band_section] == True:
                    band_found = True
                else:
                    band_found = False

                if prefix_section == prefix:
                    prefix_found = True
                else:
                    prefix_found = False
                continue
            if prefix_found and band_found:
                #print('Found Selected Information at line ' + str(line_count))
                selected_entries.append(row)

    #define constants for the conversion
    __output_col__         = 0
    __input_col__          = 1
    __repeater_name_col__  = 2
    __location_col__       = 4
    __tone_col__           = 11         

       

    print ('Converting '+str(len(selected_entries))+' entries')
    output_conversion = open(output_csv, "w")
    output_conversion.write(__chirp_header__+'\n')
    entry_location = 0
    for item in selected_entries:
        
        outpt_freq = item[__output_col__]
        input_freq = item[__input_col__]
        name = item[__repeater_name_col__]

        offset_output =  float(input_freq) - float(outpt_freq) 
        offset_output = math.ceil(offset_output*100)/100
        if item[__tone_col__] == '-':
            tone = '88.5' #Complains if Empty add dumy value
        else:
            tone = item[__tone_col__]

        #Work out the correct offset for the repeater 
        if offset_output < 0: 
            offset_sign = '-'
            offset_output = offset_output * -1
        else:
            offset_sign = '+' 

        #Clamp the offset to 0.6 not 0.61 or 0.59

        if offset_output < 0.6 and offset_output > 0.58:
           offset_output = 0.6
        elif  offset_output > 0.6 and offset_output< 0.65 :
            offset_output = 0.6

        csv_out = str(entry_location) +','+name+','+str(outpt_freq)+','+offset_sign+','+ str(offset_output) +',,'+tone+','+tone+',23,NN,FM,5.00,,,,,,\n'  
        output_conversion.write(csv_out)
        entry_location = entry_location + 1
    output_conversion.flush()
    output_conversion.close()
    print('Conversion completed')
    return

def main(args):
    print (__greeting__)
    #print (args)

    band_plan_filter = {};

    #Create a truth table of permitted bands
    band_plan_filter[__10M__] = False
    band_plan_filter[__2M__] = False
    band_plan_filter[__6M__] = False
    band_plan_filter[__70CM__] = False
    band_plan_filter[__23CM__] = False
    band_plan_filter[__ALL__] = False

    print_helpline_and_exit = False
    #Check Arguments
    if args.prefix_filter == None:
        print ('Please select a prefix filter')
        print_helpline_and_exit = True
    if args.input  == None:
        print ('Please enter an input CSV')
        print_helpline_and_exit = True
    if args.output == None:
        print ('Please enter an output file to write to')
        print_helpline_and_exit = True
    if args.parser == None:
        print ('Please select a CSV parser')
        print_helpline_and_exit = True
    if args.band_filter == None:
        print ('Please select a prefix filter')
        print_helpline_and_exit = True

    if print_helpline_and_exit == True:
        print('Please see options use -h when executing (example: ./tochirp.py -h)')
        return

    #Convert arguments
    input_file = args.input[0]
    output_file = args.output[0]
    parser = args.parser[0]
    prefix_filter = args.prefix_filter[0].upper()
    band_filter = args.band_filter[0]

    if band_filter == "2m":
        band_plan_filter[__2M__] = True
    if band_filter == "70cm":
        band_plan_filter[__70CM__] = True
    if band_filter =="2m-70cm":
        band_plan_filter[__70CM__] = True
        band_plan_filter[__2M__] = True

    #Print status
    print ('Using '+ input_file +' as input')
    print ('Exporting to ' + output_file)
    print ('Using the following parser '+parser)
    print ('Filtering on prefix '+prefix_filter)
    print ('Filtering bands '+ band_filter)

    
    if parser == 'wia':
        wia_converter(prefix_filter,band_plan_filter,input_file, output_file)


if __name__ == "__main__":
    example_text = '''Example usage: 
    ./tochirp.py --input foo.csv --output bar.csv --parser wia --prefix-filter vk2 --band-filter 70cm 
    '''
    parser = argparse.ArgumentParser(description = __greeting__ , epilog=example_text, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--input',  nargs=1, help='The Input CSV to convert', action="store")
    parser.add_argument('--output', nargs=1, help='the output CSV in CHIRP format', action="store")
    parser.add_argument('--parser', nargs=1, help='CSV Input type', action="store", choices=['wia','default'])
    parser.add_argument('--prefix-filter', nargs=1, help='Filter for Repeater Prefix', action="store", choices=['vk3','vk2','vk1','vk4','vk5','custom','none'])
    parser.add_argument('--band-filter', nargs=1, help='Band filter', action="store", choices=['2m','70cm','2m-70cm','none'])
    args = parser.parse_args()
    main(args)