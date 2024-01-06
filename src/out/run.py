from doindex import Do as do_index
from donull import Do as do_null
from up_net import do as up_net

# compatibility
up_net()

# create file null
do_null().do()
# create index.html for dir
do_index().do()
