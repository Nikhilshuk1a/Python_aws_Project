import boto3

# Initialize a session using Amazon EC2
ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

# Replace with the IDs of the resources created by your script
vpc_id = 'vpc-008e0d59a4925d5e9'
internet_gateway_id = 'igw-03159cf7b980cb972'
subnet_id = 'subnet-0e38c54a914b16d36'
route_table_id = 'rtb-07f2f70bed5fb67c8'
security_group_id = 'sg-0b9326d67d4144709'

# Terminate all instances within the VPC
print(f'Terminating instances in VPC: {vpc_id}')
instances = ec2.instances.filter(Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}])
for instance in instances:
    instance.terminate()
    instance.wait_until_terminated()
    print(f'Terminated instance: {instance.id}')

# Detach and delete the internet gateway
print(f'Detaching and deleting Internet Gateway: {internet_gateway_id}')
vpc = ec2.Vpc(vpc_id)
vpc.detach_internet_gateway(InternetGatewayId=internet_gateway_id)
internet_gateway = ec2.InternetGateway(internet_gateway_id)
internet_gateway.delete()
print(f'Deleted Internet Gateway: {internet_gateway_id}')

# Disassociate the route table from the subnet
print(f'Disassociating Route Table from Subnet: {subnet_id}')
route_table = ec2.RouteTable(route_table_id)
associations = route_table.associations
for association in associations:
    association.delete()
    print(f'Disassociated Route Table: {route_table_id} from Subnet: {subnet_id}')

# Delete custom routes in the route table
print(f'Deleting custom routes in Route Table: {route_table_id}')
for route in route_table.routes:
    if route.destination_cidr_block != 'local':  # Skip the default local route
        client.delete_route(RouteTableId=route_table_id, DestinationCidrBlock=route.destination_cidr_block)
        print(f'Deleted route: {route.destination_cidr_block}')

# Delete the route table
print(f'Deleting Route Table: {route_table_id}')
# route_table = ec2.RouteTable(route_table_id)
# route_table.delete()

response = client.delete_route_table(
    RouteTableId='rtb-07f2f70bed5fb67c8', # Different way to delete route table as i was getting error before,but later i figured it out.
)

print(response)
print(f'Deleted Route Table: {route_table_id}')

# Delete the security group
print(f'Deleting Security Group: {security_group_id}')
security_group = ec2.SecurityGroup(security_group_id)
security_group.delete()
print(f'Deleted Security Group: {security_group_id}')

# Delete the subnet
print(f'Deleting Subnet: {subnet_id}')
subnet = ec2.Subnet(subnet_id)
subnet.delete()
print(f'Deleted Subnet: {subnet_id}')

# Finally, delete the VPC
print(f'Deleting VPC: {vpc_id}')
# vpc = ec2.Vpc(vpc_id)
# vpc.delete()
print(f'Deleted VPC: {vpc_id}')

response = client.delete_vpc(
    VpcId='vpc-008e0d59a4925d5e9', # Different way to delete VPC as i was getting error before but later i figured it out.
)

print(response)
