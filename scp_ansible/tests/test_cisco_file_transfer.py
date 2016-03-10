from DEVICE_CREDS import my_device

def test_setup_initial_state(ansible_module):	
	'''
	Transfer initial file to remote device
	'''
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt'
		enable_scp='true',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)

def test_file_already_exists(ansible_module):
	'''
	make sure file already exists and not 'changed'
	'''
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)
	
	for host, result in module_out.items():
		assert result['changed'] is False
		assert result['msg'] == 'File exists and has correct MD5'

def test_xfer_file(ansible_module):
	'''
	Transfer a new file to the remote device
	'''
	#will disable scp after test
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt'
		enable_scp='true',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)

	for host, result in module_out.items():
		assert result['changed'] is True
		assert result['msg'] == 'File successfully transfered to remote device'
	
def test_verify_file(ansible_module):
	'''
	Verify the new file on the remote device
	'''
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)
	
	for host, result in module_out.items():
		assert result['changed'] is False
		assert result['msg'] == 'File exists and has correct MD5'

def test_xfer_and_scp_enable(ansible_module):
	'''
	Transfer a new file to the remote device
	ansible module must enable scp for this work
	'''
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt',
		enable_scp = 'true',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)
	
	for host, result in module_out.items():
		assert result['changed'] is True
		assert result['msg'] == 'File successfully transfered to remote device'	

def test_overwrite(ansible_module):
	'''
	verify overwrite when file already exists results in an error
	'''
	ansible_args=dict(
		source_file="/home/kbyers/scp_sidecar/tests/cisco_logging.txt",
		dest_file='cisco_logging.txt',
		enable_scp= 'true',
		overwrite = 'false',
	)
	ansible_args.update(my_device)
	module_out=ansible_module.cisco_file_transfer(**ansible_args)
	
	for host, result in module_out.items():
		assert result['changed'] is False
		assert result['msg'] == 'File already exists and overwrite set to false'
