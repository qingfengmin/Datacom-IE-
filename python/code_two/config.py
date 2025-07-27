comist = {
        'cpu-usage':{'command':'dis cpu ','re':'CPU\s+Usage\s+:.*?%'},
        'ospf': {'command': 'display ospf peer ', 're': 'State.*?:\s+(\w+)\s+'},
        'power':{'command':'dis power ','re':'Supply|NotSupply|Sleep|NO'},
        'lacp':{'command':' dis eth-trunk ','re':'O.*:\s+(up|down)'},
        'memory':{'command':'dis memory ','re':'M\w+\s\w+\s\w+:\s+(\d+%)'},
        'fan':{'command':'display fan ','re':'Normal'}}


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
# 注意如果你使用的是RPC方式,不用复制到config标签
