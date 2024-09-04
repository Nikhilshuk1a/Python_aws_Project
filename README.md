# Python_Aws_Project
## _Creating and Destroying AWS resources with Python using Boto3 module._
## _AWS EC2 Infrastructure Automation with Boto3_

- *This repository contains a Python script that automates the creation and deletion of AWS EC2 resources using the Boto3 library. The script allows you to easily set up and tear down an entire EC2 infrastructure, including VPC, subnets, Internet Gateway, route tables, security groups, and EC2 instances.*

## Prerequisites

Before running the script, ensure that you have the following:

- **AWS Credentials**: Download *__AWS CLI__* and Ensure your AWS credentials are configured. You can do this by setting up the `~/.aws/credentials` file or by setting the `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
- **Boto3**: The AWS SDK for Python, which can be installed via pip:
  ```bash
  pip install boto3
  ```

# _Script Overview_
 ### 1. Creating Resources

### The script first creates the following resources:

-    **VPC**: A Virtual Private Cloud is created with a specified CIDR block.
-   **Internet Gateway**: An Internet Gateway is created and attached to the VPC, enabling internet access.
-   **Public Subnet**: A public subnet is created within the VPC, placed in a specific availability zone.
-    **Route Table**: A route table is created with a route to the Internet Gateway, and it is associated with the public subnet.
-    **Security Group**: A security group is created with ingress rules for SSH (port 22), HTTP (port 80), and HTTPS (port 443).
-    **EC2 Instances**: A specified number of EC2 instances are created in the public subnet, each associated with the security group.


### 2. Deleting Resources

### The script then handles the deletion of the resources created:

-    **Terminate EC2 Instances**: All instances within the specified VPC are terminated.
-    **Detach and Delete Internet Gateway**: The Internet Gateway is detached from the VPC and then deleted.
-    **Disassociate and Delete Route Table**: The route table is disassociated from the subnet, custom routes are deleted, and the route table is deleted.
-    **Delete Security Group**: The security group is deleted.
-    **Delete Subnet**: The public subnet is deleted.
-    **Delete VPC**: Finally, the VPC itself is deleted.


# _Usage_

- **To use the script, simply execute it in your Python environment. Be sure to update the vpc_id, internet_gateway_id, subnet_id, route_table_id, and security_group_id with the appropriate values for your AWS resources.**

```bash
python your_script.py
```

## Example Output

**As the script runs, it will output the following information:**

- IDs of created resources (VPC, Internet Gateway, Subnet, etc.)
- Status of EC2 instances (Instance ID, State, Public DNS)
- Confirmation messages for resource deletion.

# _Important Considerations_

- **IAM Permissions**: Ensure your AWS credentials have sufficient permissions to create and delete these resources.
- **Resource Limits**: Be mindful of AWS resource limits in your account, such as the number of VPCs or EC2 instances.
- **Costs**: Running these resources may or may not incur AWS charges. Be sure to delete resources when no longer needed.

