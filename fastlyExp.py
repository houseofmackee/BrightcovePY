import sys
import base64
import time

if len(sys.argv)>1:
	token = str(base64.b64decode((sys.argv[1]).replace('%3D', '='))).replace('b\'','')
	token = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int('0x'+token[:token.find('_')],0)))
	print('Token expires: ' + token )
else:
	print('Missing token.')
