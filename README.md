# NestedDict
Use nested dict easily. You can explode your dict, 
get schema, get easily a "deep" value ...
# Examples
```python
from src.nestedict import Nested
d = {
'lvl_1' : {
    'lvl_2' : {
        'lvl_3_1' : [
                {'lvl_3_1' : 1},2.3
                ]
            }
        }
}
nested = Nested(d,sep='.')
nested['lvl_1.lvl_2']
# output : {'lvl_3_1' : [{'lvl_3_1' : 1},2.3]}
nested.max_deep()
# output : 3
nested.min_deep()
# output : 1
nested.explode()
# output : {"lvl_1.lvl_2.lvl_3_1" : [{'lvl_3_1' : 1},2.3]}
nested.dtypes(to_string=True)
# output : {"lvl_1.lvl_2.lvl_3_1" : 'list'}
nested.explode_plus()
#output : {"lvl_1.lvl_2.lvl_3_1.0.lvl_3_1": 1,"lvl_1.lvl_2.lvl_3_1.1": 2.3}
nested.dtypes_plus(to_string=True)
#output : {"lvl_1.lvl_2.lvl_3_1.0.lvl_3_1": 'int', "lvl_1.lvl_2.lvl_3_1.1" : 'float'}

```

