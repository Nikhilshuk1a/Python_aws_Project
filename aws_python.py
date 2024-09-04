import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Create a VPC
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')
vpc.wait_until_available()
print(f'Created VPC: {vpc.id}')

# Enable DNS support
vpc.modify_attribute(EnableDnsSupport={'Value': True})
vpc.modify_attribute(EnableDnsHostnames={'Value': True})

# Create an Internet Gateway and attach it to the VPC
internet_gateway = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=internet_gateway.id)
print(f'Created Internet Gateway: {internet_gateway.id}')

# Create a public subnet
public_subnet = ec2.create_subnet(CidrBlock='10.0.1.0/24', VpcId=vpc.id, AvailabilityZone='us-west-2a')
print(f'Created Public Subnet: {public_subnet.id}')

# Create a route table and a public route
route_table = vpc.create_route_table()
route = route_table.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    GatewayId=internet_gateway.id
)
print(f'Created Route Table: {route_table.id}')

# Associate the route table with the subnet
route_table.associate_with_subnet(SubnetId=public_subnet.id)
print(f'Associated Route Table with Subnet: {public_subnet.id}')

# Create a security group
security_group = ec2.create_security_group(
    GroupName='MySG',
    Description='My security group',
    VpcId=vpc.id
)
security_group.authorize_ingress(
    IpPermissions=[
        {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, # giving access to port 22 for ssh
        {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, # giving access to port 80 for http
        {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}, # giving access to port 443 for https
    ]
)
print(f'Created Security Group: {security_group.id}')

# Function to create instances
def create_instances(instance_count):
    instances = ec2.create_instances(
        ImageId='ami-0aff18ec83b712f05',  # Replace with your desired AMI ID
        MinCount=instance_count,
        MaxCount=instance_count,
        InstanceType='t2.micro',  # Choose your instance type
        KeyName='keypair',  # Replace with your key pair name
        NetworkInterfaces=[{
            'SubnetId': public_subnet.id,
            'DeviceIndex': 0,
            'AssociatePublicIpAddress': True,
            'Groups': [security_group.group_id]
        }],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': f'Server {i+1}'} for i in range(instance_count)]
            }
        ],
        Placement={
            'AvailabilityZone': 'us-west-2a'
        }
    )
    return instances

# Number of instances to create
num_instances = 1

# Create the instances
instances = create_instances(num_instances)
print(f'Created {num_instances} EC2 instances')

# Print details of the created instances
for instance in instances:
    print(f'Instance ID: {instance.id}')
    print(f'State: {instance.state}')
    print(f'Public DNS: {instance.public_dns_name}')
    print(f'Instance Type: {instance.instance_type}')
