# Copyright 2014, Schuberg Philis B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#  nagios.py
#
# Utility class to perform the interfacing to Nagios (e.g. the boilerplate for building Nagios
# plugin compliant response strings (status + performance data).
#
# See http://nagiosplug.sourceforge.net/developer-guidelines.html

import sys

class Nagios:
    """
    Support routines for Python based Nagios plugins
    """

    def __init__(self,check_name):
        self.service = check_name

        # Fill a 2-way reponse map to map codes to text and vice versa
        self.response_map = {}
        self.return_code = 3
        self._add_response ( 0, "OK" )
        self._add_response ( 1, "WARNING" )
        self._add_response ( 2, "CRITICAL" )
        self._add_response ( 3, "UNKNOWN" )
        self.perfdata = ""
        self.status = "No statusdata available"

    def _add_response ( self, code, text ):
        self.response_map [ code ] = text
        self.response_map [ text ] = code

    def AddPerfData ( self,name,value ):
        if len ( self.perfdata ) > 0:
            self.perfdata += " "
        self.perfdata += name + "=" + str(value)

    def SetStatus ( self, message ):
        self.status = message

    def AppendStatus ( self, message ):
	if len(self.status) > 0:
           self.status+=", "
        self.status+=message

    def SetExitCode (self,code):
        try:
            code=int(code)
        except ValueError:
            code=self.response_map[code]

        if self.return_code == 3 or code > self.return_code:
            self.return_code = code

    def BuildResponseAndExit ( self, code=None, message=None):

        if code != None:
            self.SetExitCode ( code )

        if message != None:
            self.SetStatus ( message )

        text = self.service + " " + str(self.response_map[self.return_code]) + ": " + self.status
        if len(self.perfdata) > 0:
            text += "|" +self.perfdata
        print text
        sys.exit ( self.return_code )


if __name__ == "__main__":
    nagios = Nagios("TEST")
    nagios.BuildResponseAndExit ( "UNKNOWN", "All is well!" )
