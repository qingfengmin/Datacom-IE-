comist = {
        'cpu-usage':{'command':'dis cpu ','re':'CPU\s+Usage\s+:.*?%'},
        'ospf': {'command': 'display ospf peer ', 're': 'State.*?:\s+(\w+)\s+'},
        'power':{'command':'dis power ','re':'Supply|NotSupply|Sleep|NO'},
        'lacp':{'command':' dis eth-trunk ','re':'O.*:\s+(up|down)'},
        'memory':{'command':'dis memory ','re':'M\w+\s\w+\s\w+:\s+(\d+%)'},
        'fan':{'command':'display fan ','re':'Normal'}}

#这里的正则表达式可能需要进行一些区分,真机和模拟器的正则表达式有一定的差别
netxml ={
"vlan":
"""
        <config>
          <vlan xmlns="http://www.huawei.com/netconf/vrp" content-version="1.0" format-version="1.0">
            <vlans>
              <vlan operation="merge">
                <vlanId>100</vlanId>
                <vlanType>common</vlanType>
                <vlanName>VLAN100</vlanName>
              </vlan>
            </vlans>
          </vlan>
        </config>
"""
}#这是Huawei5700设置日志主机的xml
#这里的netconf xml是一个测试,在真机设备上可以运行,作用是创建vlan100

user_info = {
        'ssh':{
                'username':'python',
                'password':'Huawei@123',
                'hostname':'10.1.0.6',
                'port':22
        },
        'net_user':{
                'username':'netconf',
                'password':'Huawei@123',
                'host':'10.1.0.6',
                'port':830,
                'hostkey_verify':False,
                'allow_agent':False,
                'look_for_keys':False,
                'device_params':{
                        'name':'huawei'
                }
        }

}
