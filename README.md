
## Requirements for the program

* Make sure you have Python installed, by using the command `python --version`
* If python is not installed on your system, visit  *python.org* to install the python version compatible with your system.
* Make sure you have the Boto3 SDK installed for Python, by using this command `pip show boto3`
* If boto3 is not installed, install it using this command `pip install boto3`
* Create an AWS account if you don't already have one, and obtain your access key id and secret access key for the account.
* Enter your access key information in a file named `S5-S3.conf`. Refer below for the expected configuration file format. 

## How to run the program

* Please make sure you place your S5-S3.conf file in the same directory as the s5_shell.py file
* The config follows this structure - 

```
[default]
aws_access_key_id = YOUR_ACCESS_KEY_ID
aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

```
* To run the script, type  `python s5_shell.py`
* If you are using python3, type `python3 s5_shell.py`
* Once the AWS S3 Storage shell (S5) is initiated, begin to enter commands to navigate your S3 storage.
* If you are unsure as to which commands to use and their expected format, type `help` to view the user manual.
* To exit the shell, type `quit` or `exit`

## Limitations of the program

* The shell doesn't incorporate non-Cloud related commands at the moment (bash/Powershell/command prompt). The functionality to pass non-Cloud related commands to the session's shell (bash/zsh/Powershell) has not been incorporated in the program currently.
* This functionality is in the scope of future improvements/developments to this program.
* The `list` operation currently doesn't function if the full path of the S3 location is provided. As an example, in the root directory, a command like - 
```
S5> list /demo-bucket-01
```
doesn't seem to respond. 
* On the contrary, the `list` command functions correctly, if the user performs chlocn into the directory that they wish to see the contents of and provides the command with no path specification. As an example, in the root directory, a prompt like - 
```
S5> chlocn /demo-bucket-01
```
followed by 
```
S5> list
```
* This prompt displays the contents of, in this case, /demo-bucket-01, successfully. 
* Hence, the `list` command can be seen as partly functioning.

## Important Information

* Please refer to the Documentatation.pdf file to view specific testing case screenshots for the shell functionality.
