Member Names:
Deepak Reddy Nayani
Karthik Aravapalli
Nikhil Chandra Nirukonda

Bucket Names:
input bucket name : ndk-proj2
output bucket name : ndk-proj2output

DB table name : ndk-proj2-table

Download and install AWS CLI
https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Go to terminal, and run “aws configure”, then type in the AWS_ACCESS_KEY, AWS_SECRET_KEY & REGION
Git Clone the repository and cd into it.

https://github.com/deepaknayani22/CSE546_Project2.git

AWS_REGION = "us-east-1"
aws_access_key_id = "AAAAAAAAAAAAAAAAAAAA"
aws_secret_access_key = "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"
Access keys provided in the report and not added to read me as it is going to be pushed to github and is a security risk.

Make the following changes (if using the TAs code)
In Dockerfile, add a line “COPY encoding /home/app/”
In requirements.txt, change ffmpeg to python-ffmpeg

Download and install Docker and Docker Desktop for deploying the image.
Run the following commands:
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 458362110587.dkr.ecr.us-east-1.amazonaws.com
docker build -t proj2-docker-lambda .
docker tag proj2-docker-lambda:latest 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest
docker push 458362110587.dkr.ecr.us-east-1.amazonaws.com/proj2-docker-lambda:latest

Run python3 uploadDB.py (should not be required as the table is already populated)

- Follow the instructions in https://canvas.asu.edu/courses/141245/assignments/3780879 to install the OpenStack devstack.
- Add triggers to the input SQS queue and input S3 input bucket. Follow the same thing for the output queue and output bucket. 
- We can either use the OpenStack dashboard (Horizon) or the OpenStack command-line interface (CLI) to connect to the OpenStack environment.
- To create the Ubuntu VM, click on "Launch Instance" or use the "nova boot" command on the CLI. 
- Configure the VM, - name, flavor (CPU, RAM, and disk specifications), Ubuntu OS image, VNIC, and optional settings like security groups or key pairs. Now, launch instance. 
- Assign a floating public IP address to the created instance and use the key pair key to establish an SSH connection with the instance. - Copy the script to the home directory and install boto3 and awscli. Execute the script to monitor the SQS messages.
- Run workload.py on your local machine.

Run python3 workload.py to upload the videos in the test folder into the S3 bucket.
