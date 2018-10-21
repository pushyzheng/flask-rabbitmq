# encoding:utf-8

data = {
    '28934892342':{
            'isAccept': False,
            'result': None
    },
    '8923849234':{
            'isAccept': False,
            'result': None
    }
}

for key in data.keys():
    object = data[key]

    print(object['isAccept'])