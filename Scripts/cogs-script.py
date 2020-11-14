#!"C:\Users\Beck\Desktop\Projects\Sullybot (Python)\Scripts\python.exe"
# EASY-INSTALL-ENTRY-SCRIPT: 'Cogs==0.4.4','console_scripts','cogs'
__requires__ = 'Cogs==0.4.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('Cogs==0.4.4', 'console_scripts', 'cogs')()
    )
