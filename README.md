# NSX-T

This is an Automation Framework for NSX-T Automation.


### Dependencies

Apart from dependencies listed in the requirements.txt, User needs to install vsphere-automation-sdk-python also.

More details about the sdk can be found here.

[vsphere-automation-sdk-python](https://github.com/vmware/vsphere-automation-sdk-python)

### Run

`python -m pytest TestNsxTransformer.py -v -s --junitxml=nsxtResult.xml`

This Produces a log file as well as result in a junit xml formatt which can be used for integration in pipeline code.

### Bugs

User can contribute for developement and file bugs which I would fix as sooner as possible. 

Please note this is my Hobby Project. VMWare bears no responsibility.
