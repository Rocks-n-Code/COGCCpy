# COGCCpy

[![License](http://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/rocks_n_code/COGCCpy/blob/master/license)


This is a distribution for pulling data from Colorado Oil and Gas Conservation Commission (COGCC).  This package is not authored, or maintained, by COGCC or the State of Colorado.

Currently it can be used for production data and formation tops.


### Installation

```bash
$ pip install COGCCpy
```

### Production Example

```bash
from COGCCpy import production

apis = ['05-013-40002','0501305023']
prod = production(apis)

#Preview
prod.df.head()
```

### Formation Tops Example

```bash
from COGCCpy import formation_tops

apis = ['0501306049','05-013-06457']
tops = formation_tops(apis)
tops.df.head()
```

##License

MIT