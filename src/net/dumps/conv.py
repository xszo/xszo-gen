def proxy(out) -> None:
    out.write(
        """[custom]
ruleset=DIRECT,[]FINAL
custom_proxy_group=Node`select`[]DIRECT`[]REJECT
add_emoji=false

clash_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
loon_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
mellow_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
quan_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
quanx_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
singbox_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
sssub_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
surfboard_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null
surge_rule_base=https://cdn.jsdelivr.net/gh/xszo/etc@etc/null

rename=^(JMS-\\d+).(c\\d+s[123])\\..*@$1 $2 US
rename=^(JMS-\\d+).(c\\d+s4)\\..*@$1 $2 JP
rename=^(JMS-\\d+).(c\\d+s5)\\..*@$1 $2 NL
rename=^(JMS-\\d+).(c\\d+s\\d+)\\..*@$1 $2
"""
    )
