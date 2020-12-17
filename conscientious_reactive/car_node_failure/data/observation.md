**car node failure:** node is not able to communicate the idleness value to the car. For example: node 12 have car node failure then it means that node 12 will not communicate what's the the surrounding node idleness, so it will take random action afer coming to this node.

corner node: node 0

edge node: node 2

center node: node 12

# 1 car:

in comparison to proper connection case, idleness value drop by very small amount (4-6)

>corner node is disconnected: behavior remains same

>edge node in disconnected:randomness comes into play and symmetry is broken

>center node is disconnected:behavior remains same

# 2 cars:

in comparison to proper connection case, idleness value remains identical. But it was observed that in some case idleness is sinusodial as well, so corresponding to that we have same behavior in packet loss

>corner node is disconnected: behavior was quite uncertain, sometimes it linearizes after few time steps and sometimes it follows sinusodial behavior

>edge node is disconnected:  asymmetrical again

>center node is disconnected: becomes asymmetrical and wavy nature is there

# 4 cars:

in comparison to proper connection case, idleness value remains identical
>corner node is disconnected: asymmterical behavior with large variations

>edge node is disconnected: very slight variation but almost identical

>center node is disconnected: asymmetrical with large variations in few case but less in other cases

# 6 cars:

in comparison to proper connection case, idleness value remains identical

>corner node is disconnected: very slight variation but almost identical

>edge node is disconnected: very slight variation but almost identical

>center node is disconnected: asymmetrical with large variations in few case but less in other cases

# 10 cars:

in comparison to proper connection case, idleness value remains identical

>corner node is disconnected: asymmetrical with large variations in few case but less in other cases

>edge node is disconnected: very slight variation but almost identical

>center node is disconnected: very slight variation but almost identical