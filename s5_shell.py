#!/usr/bin/env python3
#
#  Libraries and Modules
#
import configparser
import os 
import sys 
import pathlib
import boto3
from botocore.exceptions import ClientError
import s3Functions as s3f
from pathlib import Path

#
#  Student Name: Khushi Rajput
#  Student ID: 1103687
#


# Initialize current_location variable
current_location = "/"

#
#   Function to print help options/user manual of commands accpeted by the shell
#
def printHelp():

    print("Welcome to AWS S3 Storage Shell (S5) help.")
    print("Shell commands - ")
    print("")
    print("locs3cp: copy a local file to a S3 location.")
    print("format: 'locs3cp <full or relative pathname of local object> /<bucket_name>/<full or relative pathname of the S3 object> ' ")
    print("")
    print("create_bucket: create a bucket in the S3 space following naming conventions.")
    print("format: 'create_bucket /<bucket_name>' ")
    print("")
    print("cwlocn: Display the current working directory.")
    print("format: 'cwlocn' ")
    print("")
    print("list: List all contents of the current directory.")
    print("format: 'list' or 'list /' or 'list <full or relative pathname>' ")
    print("")
    print("chlocn: Change the current working dorectory in the S3 space.")
    print("format: 'chlocn /<bucket_name' or 'chlocn <full or relative pathname' ")
    print("")
    print("quit/exit: Exit the AWS S3 Storage Shell (S5).")
    print("format: 'quit' or 'exit' ")

#
#   Function to copy a local file to a S3 location
#   Success: returns 0, Command prompt
#   Failure: return 1, Error message
#
def locs3cp(user_input):
    try:
        global current_location

        # check for correct input format
        tokens = user_input.split(' ')
        if(len(tokens) < 3):
            print('Incorrect input format. Missing local file path or S3 file path. Enter "help". ')
            return 1
        
        # check if command is being executed inside a bucket, if in root print error
        if(current_location == "/"):
            print("You must first create a bucket or 'chlocn' into an existing one before you can use this command.")
            return 1
        
        # check if local file path is correct and file exists
        local_path = Path(tokens[1])
        if(local_path.is_file() == False):
            print('Incorrect local file path. File at \'' + str(local_path) + '\' does not exist.')
            return 1

        #   check if input format is including / before the bucket name
        if(tokens[2].startswith("/") == False):
            print('Incorrect cloud path. The path to the S3 location must be in the format - /<bucket_name>/<full or relative path to S3 location> ')
            return 1

        cloud_path_list = list(Path(tokens[2]).parts)
        bucket_name = str(cloud_path_list[1])

        # check if specified bucket exists or not
        if(s3f.bucket_exists(s3_res, bucket_name) == False):
            print('Incorrect Bucket in S3 space \'' + current_location+bucket_name + '\' does not exist.')
            return 1

        # check if cloud path is correct and exists
        cloud_path = Path(tokens[2])
        if(len(Path(tokens[2]).parts) > 3):
            if(s3f.cloud_folder_path_exists(s3_res, cloud_path, bucket_name) == False):
                print('Incorrect cloud path. The cloud path \'' + str(cloud_path) + '\' could not be found. ')
                return 1
        
        # copy the local file to cloud location 
        cloud_folder = "\\".join(str(cloud_path).split("\\")[2:])
        s3_res.Bucket(bucket_name).upload_file(local_path, cloud_folder)
        
    except Exception as CopyError:
        print("Unsuccesful Copy Operation - ", CopyError)
        return 1
    
    return 0

#
#   Function to create a new bucket at the S3 location specified
#   Success: returns 0, Command prompt
#   Failure: return 1, Error message
#
def create_bucket(user_input):
    try:
        global current_location
        tokens = user_input.split(" ")

        #   check for correct user input
        if(len(tokens) != 2):
            print('Incorrect input format or missing bucket name. Expected format - "create_bucket /<bucket_name>"')
            return 1
        
        #   check if bucket name is provided with leading slash to indicate root
        if(tokens[1].startswith("/") == False):
            print("Incorrect input format. Verify with expected format - 'create_bucket /<bucket_name>'")
            return 1
        
        #   check if command is being used in root
        if(current_location != '/'):
            print('Cannot create bucket if you are not in the root directory.')
            return 1
        
        #   get bucket name and check if it already exists
        bucket_name = tokens[1].split('/')[1]
        if(s3f.bucket_exists(s3_res, bucket_name) == True):
            print('Bucket with name \'' + str(bucket_name) + '\' already exists.')
            return 1

        #   create the bucket in the root directory. 
        s3_res.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={'LocationConstraint': 'ca-central-1'})
    
    except Exception as CreateBucketError:
        print("Unsuccesful Create Bucket Operation - ", CreateBucketError)
        return 1
    
    return 0

#
#   Function to change current working directory
#   Success: returns 0, command prompt
#   Failure: return 1, Error message
#
def chlocn(user_input):
    try:
        global current_location
        tokens = user_input.split(" ")

        #   check for correct user input 
        if(len(tokens) != 2):
            print("Incorrect input format or missing folder information. Expected format - 'chlocn /<bucket_name or full/relative path to directory> ' ")
            return 1
        
        if(tokens[1].startswith('/') and len(tokens[1]) == 1):
            current_location = '/'
            return 0
        elif(tokens[1].startswith('/')):
            cloud_path = tokens[1][1:]
        elif(tokens[1].startswith('.')):
            cloud_path = tokens[1]
        else:
            print('Incorrect input format. Verify with expected format - "chlocn <bucket_name or full/relative pathname of new directory>" ')
            return 1
        
        # Create a path list
        path_list = list()
        if(current_location != '/'):
            path_list = list(Path(current_location).parts[1:])
        if(cloud_path == '/'):
            current_location = '/'
            return 0
        else:
            if(cloud_path.startswith('/')):
                path_list = list()
            for item in Path(cloud_path).parts:
                if(item == '..' and len(path_list) > 0):
                    path_list.pop()
                elif(item.count('.') == len(item) and len(item) > 2):
                    print('Cannot change folder, \'' + str(item) + '\' is not a valid directory')
                    return 1
                elif(item != '/'):
                    path_list.append(item)
        
        path = '/' + '/'.join(path_list)
        current_location = path

    except Exception as ChlocnError:
        print('Unsuccesful Chlocn Operation - ', ChlocnError)
        return 1
    
    return 0

#
#   Function to print the current working directory
#   Success: returns 0, Print the new working directory
#   Failure: return 1, Error message
#
def cwlocn():
    global current_location
    print(current_location)
    return 0

#
#   Function to list all contents of the specified directory
#   Success: returns 0, print the location's content
#   Failure: return 1, Error message
#
def list_contents(user_input):
    try:
        global current_location
        tokens = user_input.split(" ")

        #   print buckets in root when in root, or print contents of current location in S3 space
        if(len(tokens) == 1):
            if(current_location == '/'):
               s3f.list_buckets(s3)
            else: 
                bucket_name = str(list(Path(current_location).parts)[1])
                s3f.print_objects(s3_res, current_location, bucket_name)

        #   print buckets in root, regardless of current directory
        if(len(tokens) == 2 and tokens[1] == '/'):
            s3f.list_buckets(s3)

        #   print contents of specified path - not implemented
                
    except Exception as ListError:
        print('Unsuccesful List Operation - ', ListError)
        return 1

    return 0

#
#   Function to exit the shell
#
def exit_shell():
    print('Exiting AWS S3 Storage Shell (S5)...')
    sys.exit(0)


#
#  Find AWS access key id and secret access key information
#  from configuration file
#  NOTE: Please include the S5-S3.conf in the same directory as this script, with information about your AWS account
#

config = configparser.ConfigParser()
config.read("S5-S3.conf")
aws_access_key_id = config['default']['aws_access_key_id']
aws_secret_access_key = config['default']['aws_secret_access_key']

#
#  Preliminary welcome message for user
#
print ( "Welcome to the AWS S3 Storage Shell (S5)" )

try:
#
#  Establish an AWS session
#
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
#
#  Set up client and resources
#
    s3 = session.client('s3')
    s3_res = session.resource('s3')

    print ( "You are now connected to your S3 storage")

#
#  S5 shell infinite loop till exit
#
    while True:
        user_input = input("S5> ").strip().lower()

        if user_input.startswith("list"):
            #
            # Calling functions to list all contents in the S3 location
            #
            list_contents(user_input)

        
        elif user_input.startswith("locs3cp"):
            #
            # Calling function to create a new bucket
            #
            locs3cp(user_input)

        elif user_input.startswith("create_bucket"):
            #
            # Calling function to create a new bucket
            #
            create_bucket(user_input)

        elif user_input.startswith("chlocn"):
            #
            # Calling fucntion to change current working directory
            #
            chlocn(user_input)

        elif user_input.startswith("cwlocn"):
            #
            # Calling fucntion to display current directory
            #
            cwlocn()

        elif user_input == "quit" or user_input == "exit":
            #
            # Exiting the shell
            #
            exit_shell()

        elif user_input == "help":
            #
            # Display information about the commands to guide the user
            #
            printHelp()

        else:
            #
            # Display help options to guide the user
            #
            print("Invalid command. Please enter 'help' to learn more about the commands you can use, or exit/quit the shell.")


#
#   If AWS credentials cannot be authenticated, print error message
#
except ClientError:
    print ("You could not be connected to your S3 storage")
    print ("Please review procedures for authenticating your account on AWS S3")


