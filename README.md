# Pyststg

Search the sensitive text of in git. And this project is written Python language.

## Getting Started

This project is for search sensitive word in the git repository. To use this project so see "Installing" and "Usage" section.

### Prerequisites

This software to use need prepare environment for executing a Python, further need to install bellow packages so written in requirements.txt.

* Click
    - version: 7.0
* GitPython
    - version: 3.0.2

### Installing

To let's search sensitive word, need to install this software your local machine.

However, install this software is easy. Let's check the below command line.

```bash
git clone https://github.com/xSPANGLEx/pyststg.git
cd pyststg
pip install -r requirements.txt
```

### Usage 

To use, just run below commands.

```bash
python main.py {URL}
```

Also, you possible to add new sensitive word patterns.

How to add patterns, so please add new source code into "patterns" directory.
To create source code, reference the below code.

```python
from lib import audit

class Audit(audit.Auditor):

    @property
    def regex_word(self) -> str:
        return r'regex pattern'

    def extend_filter(self, result) -> list:
        return ["filtered line"]
```

## Authors

* **xSPANGLEx**

See also the list of [contributors](https://github.com/xSPANGLEx/pyststg/contributors) who participated in this project.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details
