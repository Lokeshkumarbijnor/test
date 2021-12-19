"""
 Description: Script to archive files

 Syntax: Run command "archive_file.py -h"

 Param#  R/O Description
     1    R  Full path of the input file(s)
                single file
                   e.g. c:\test.dat
                multiple files using wildcards
                   e.g. c:\test*.dat
                        c:\test*
                multiple files using .list file
                   e.g. c:\test.list
     2    O  Timestamp format (See supported formats)
     3    O  Location where timestamp should be added to the file (See allowed
             values)

     R = Required
     O = Optional

 Supported timestamp formats:
    YYYYMMDDHHMISS
    YYYYMMDDHHMI
    YYYYMMDDHH
    YYYYMMDD
    YYYYMM
    YYYY

    Default is read from the config file

 Allowed location values:
    beginning
    before_extension
    at_the_end

    Default is read from the config file

 Config file: config/archive_file.json
"""
import argparse
import os
import shutil
import config
import os
import logging
import datetime
import misc
# import add_ts

__version__ = '1.1.0'
__author__ = 'Vikram Chauhan'
__date__ = '30-SEP-2017'

# Read config file
config = config.Config(script_name=__file__)


# This is the core function
def do(source_file, ts_format=None):
    # Get logger
    log = logging.getLogger(__name__)

    # Define global err
    global err

    # Normalize paths
    source_file = os.cleanpath(source_file)

    # Write parameters to log file
    log.debug('source file: %s' % source_file)
    log.debug('ts_format: %s' % ts_format)

    # Show if test mode
    if config.test_mode:
        log.info('test_mode: true')

    # Archive folder
    archive_dir = os.path.join(os.get_dir(source_file), 'archive')

    # Try to create archive directory. It's ok if it exists!
    try:
        os.makedirs(archive_dir, exist_ok=True)
    except EnvironmentError as e:
        log.error('error occurred while creating archive folder')
        log.error(e)
        err = 1
    else:
        log.debug('using folder %s' % archive_dir)

    # Start copying
    try:
        if os.get_file_extension(source_file) in ['.list', '.lst']:
            log.debug('source is a list file')

            # Get all the files inside the list file into "files" variable
            files = misc.read_list_file(source_file)

            # Add list file as well
            files.append(source_file)

        elif os.path.isfile(source_file):
            log.debug('source is a single file')

            # Single file
            files = [source_file]
        else:
            # Assume wildcards and process the files
            log.debug('source is a wildcard name or other type')

            source_dir = os.get_dir(source_file)
            source_file = os.path.join(source_dir,
                                       os.get_filename(source_file))
            files = os.ls(source_dir)
            files = misc.match(files, source_file)
    except Exception as e:
        log.error('error occurred while processing source file')
        log.error(e)
        err = 1
    else:
        if len(files) > 0:
            # Loop through all the identified files
            for file in files:
                # Define archive directory and filename
                archive_file = os.path.join(archive_dir,
                                            os.get_filename(file))
                # Now, archive the file
                try:
                    shutil.move(file, archive_file)
                except EnvironmentError as e:
                    log.error('error occurred moving file')
                    log.error(e)
                    err = 1
                # else:
                #     # Add timestamp
                #     log.debug('invoking add_ts')
                #     add_ts.do(source_file=archive_file, ts_format=ts_format,
                #               ts_location='at_the_end')
        else:
            log.warn('no files to process')


# Main function called if script is invoked directly
if __name__ == '__main__':
    # Set command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename',
                        help='full path of the file to be archived')
    parser.add_argument('-t', help='timestamp format')
    args = parser.parse_args()

    # Define logging
    # Append the input file name to the name of the archive log file
    log_name_keyword = os.get_filename(args.filename)
    log = logging.Log(script_name=__file__,
                          log_name_keyword=log_name_keyword)

    # Define err
    err = 0

    # Start logging
    log.start()

    # Invoke main function
    do(source_file=args.filename, ts_format=args.t)

    # End logging
    log.end()

    # Exit
    exit(err)
