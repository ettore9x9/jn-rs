#! /usr/bin/env python
"""
.. module:: text
    :platform: Unix
    :synopsis: Python module to store the user interface texts.

.. moduleauthor:: Ettore Sani

"""

title = R"""              _      _       _                                   _
           __| |_ __(_)_   _(_)_ __   __ _   _ __ ___   ___   __| | ___
          / _` | '__| \ \ / / | '_ \ / _` | | '_ ` _ \ / _ \ / _` |/ _ \
=========| (_| | |  | |\ V /| | | | | (_| | | | | | | | (_) | (_| |  __/=======
          \__,_|_|  |_| \_/ |_|_| |_|\__, | |_| |_| |_|\___/ \__,_|\___|
                                     |___/                              
   
Choose one of the following driving modality:"""


modalities = """    1 - Autonomous driving
    2 - Free drive
    3 - Driver assistance




    q - for quit
"""


info = """INFO-------------------------------------
| Last command = 
|
|
|                        """


wasd = """    w - Increase linear speed
    s - Decrease linear speed
    a - Increase ang. speed (left)
    d - Decrease ang. speed (right)
    z - Stop angular speed
    x - Stop linear speed

    b - Back to drive modalities"""