# sciprt's written by SoledaD208, email: not.soledad@gmail.com
# script get national IP from http://www.ipaddresslocation.org, permit all these IP with minimum policy (enable ssh only)
# block all the foreign traffic
# script create 2 new chains in Iptables: VIETNAM-INPUT and NOT-VIETNAM-INPUT:
# accept just ssh protocol in VIETNAM-INPUT chain
# all these foreign traffic jump to NOT-VIETNAM-INPUT chain and block by default
# if have internal networks, you should create more chain for these networks, or add smt like this to iptables config file:
# -A INPUT -i internallIf -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

import re
import shutil
import requests

# Create payload to get IP
payload = {'country': 'VN', 'prefix': '', 'output': 'cidr'}

# Send request to http://www.ipaddresslocation.org
r = requests.post('http://www.ipaddresslocation.org/ip_ranges/get_ranges.php', data=payload)
confIpt = raw_input("config iptbles? ")
if confIpt == 'y' or confIpt == 'Y' or confIpt == 'Yes' or confIpt == 'YES':
    # backup config file
    shutil.copyfile('/etc/sysconfig/iptables', '/etc/sysconfig/iptables.bak')
    print 'current iptables config file is backuped to iptables.bak'
    while True:
        sshInput = raw_input("Which's ssh port? ")
        try:
            ssh = int(sshInput)
        except ValueError:
            print("That's not an int!")
            continue
        else:
            break
    tempF = open('iptablesv5','r')
    tempRules = tempF.readlines()
    tempF.close()
    for i in re.findall(''' (.+)<br />''', r._content, re.I):
        tempRules.insert(6,'-A INPUT -s ' + i + ' -j VIETNAM-INPUT\n')
        tempRules.insert(6,'-A FORWARD -s ' + i + ' -j VIETNAM-INPUT\n')
        ipt = file('iptables', 'wt')
    rules = "".join(tempRules)
    rules = rules.replace('--dport 22', '--dport ' + sshInput)
    ipt.write(rules)
    ipt.close()
else:
    exit()