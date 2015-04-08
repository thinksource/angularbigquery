#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from apiclient.errors import HttpError
import bqclient
import httplib2
import logging
import os
import simplejson as json
from google.appengine.api import memcache
import webapp2
from oauth2client import appengine
import bigquery
import jinja2
import logging

# from google.appengine.ext import webapp
# from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp.template import render
# from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.client import OAuth2WebServerFlow
# CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
# application, including client_id and client_secret, which are found
# on the API Access tab on the Google APIs
# Console <http://code.google.com/apis/console>
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
    ,extensions=['jinja2.ext.autoescape']
    ,variable_start_string='[['
    ,variable_end_string=']]'
   ,autoescape=True)
# BILLING_PROJECT_ID for a project where you and your users
#   are viewing members.  This is where the bill will be sent.
#   During the limited availability preview, there is no bill.
# Replace the BILLING_PROJECT_ID value with the Client ID value
# from your project, the same numeric value you used in client_secrets.json
BILLING_PROJECT_ID = "foretribebigquery"
project_id = "foretribebigquery"
DATASET = "testdata"
TABLE = "zip_code"
service_id="876306077634-k467esemosu36lgs9h1aarmbrh2hg3us.apps.googleusercontent.com"
service_email="876306077634-k467esemosu36lgs9h1aarmbrh2hg3us@developer.gserviceaccount.com"
QUERY = "SELECT area_codes,timezone, primary_city,longitude,estimated_population, latitude, county FROM [testdata.zip_code] LIMIT 1000"
key="key.pem"
#decorator = oauth2decorator_from_clientsecrets(CLIENT_SECRETS,'https://www.googleapis.com/auth/bigquery')
#decorator=flow_from_clientsecrets(CLIENT_SECRETS, scope='https://www.googleapis.com/auth/bigquery')
decorator=OAuth2WebServerFlow(client_id='876306077634-k467esemosu36lgs9h1aarmbrh2hg3us.apps.googleusercontent.com',
                           client_secret='MIICdQIBADANBgkqhkiG9w0BAQEFAASCAl8wggJbAgEAAoGBALDCbL17RP+J3q1A\nqTzmm2vo2mJzI2bUffsaLhXm+jVkgt9Wu2ZNOdreiIpG2XuFOo+J6oHDvhU7WAKw\n6xqmf+HF0jPnaWeXD+LVQMAEgB/P99D2Cl9dQEHC91vxJbSl7G440z5+036jV0CZ\nhmUrgbK8V8ca1LrGX3IQhtOnztexAgMBAAECgYBIFHDNcAg6AJnaosSgvhVhEsqD\nXRpxo3NgQ1PJwLAFt+AafT7cP9+43ghmAvBLC5BO2lnT4uOPuuxv5H9rFbyNwlNb\nwrAgTW4LUpJlW7Xl2s2FonyMeNW9TyL2LLwFeJnj0lisTBk/TBaM3YoYmIFEezX2\n/8CKAk7AHa2eNs2yMQJBANrC16mBbyOBammHkiKiDiRNcJTYtFDNshTbO9C00TFU\npMAXkoBja/CBtzsOG2xUuO0Ms0imlEyrUACN/m02dA0CQQDO2TzmE7LuUXkw1/n9\n2Gvq6ZC0s885meHBK2khrL748+UiNd2WON1+S2XKpXsQQ3yY8nM4sKhSIol+KY2Q\nYtU1AkAwYXMMu+F2esKsAB2jpy91e+LwKFUIodVGo43BBJxXSp79FLmDx3kxwZ5i\nYyZReRNE6dAkuyKFKkYROVYRlT9pAkA+zWJaEL0Q8pezJr/2PJF3f3a6BqXyPTB3\n7/A5kzNgbtyw6F3g0F8fi1DamCenJnZcEbC+E5TnaykHryIWJovJAkA8VnT7IkPl\n5SjnH63EGM6RzvCKi+JrLNXW0nH9rnOtLd/SczN9TSR0tMG/dutgY1YOBuyMTgqA\nonm6A5Nd5YNa',
                           scope='https://www.googleapis.com/auth/bigquery')
                           # ,redirect_uri='http://example.com/auth_return')

decorator = appengine.OAuth2DecoratorFromClientSecrets(
  'client_secret.json',
  scope='https://www.googleapis.com/auth/bigquery')
http = httplib2.Http()
client=bigquery.get_client(project_id, service_account=service_email, private_key_file=key,  readonly=True)

bq = bqclient.BigQueryClient(http, decorator)

class MainHandler(webapp2.RequestHandler):
    def _bq2geo(self, bqdata):
        """geodata output for region maps must be in the format region, value.
           Assume the BigQuery query output is in this format and get names from schema.
        """
        logging.info(bqdata)
        #columnNameGeo = bqdata['schema']['fields'][0]['name']
        #columnNameVal = bqdata['schema']['fields'][1]['name']
        #logging.info("Column Names=%s, %s" % (columnNameGeo, columnNameVal))
        #geodata = { 'cols': ({'id':columnNameGeo, 'label':columnNameGeo, 'type':'string'},
        #  {'id':columnNameVal, 'label':columnNameVal, 'type':'number'})}
        #geodata['rows'] = [];
        #logging.info(geodata)
        #for row in bqdata['rows']:
        #    newrow = ({'c':[]})
        #    newrow['c'].append({'v': 'US-'+row['f'][0]['v']})
        #    newrow['c'].append({'v':row['f'][1]['v']})
        #    geodata['rows'].append(newrow)
        #logging.info('FINAL GEODATA---')
        #logging.info(geodata)
        return json.dumps(bqdata)

	def _bqdata(self, bqdata):
		logging.info(bqdata)
		return json.dumps(bqdata)

    # @decorator.oauth_required
    def get(self):
        # logging.info('Last mod time: %s' % bq.getLastModTime(
        #     project_id, DATASET, TABLE))
        data = {'query': QUERY}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        #template = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(data))


class JsonHandler(webapp2.RequestHandler):

    def get(self):

        job_id, _results = client.query(QUERY)
        # complete,row_count=client.check_job(job_id)
        results=client.get_query_rows(job_id, offset=0, limit=1000)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(results))

    def post(self, httperror=None):
        jsonstring=self.request.body
        jsonobject = json.loads(jsonstring)

        query=jsonobject["query"]
        if query=="" or query is None:
            pass
        else:
            QUERY=query
        try:
            job_id, _results = client.query(QUERY.strip())
            # complete,row_count=client.check_job(job_id)
            results=client.get_query_rows(job_id, offset=0, limit=1000)
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(json.dumps(results))
        except HttpError,e:

            logging.info(QUERY)
            logging.info(e.content.strip())
            self.response.status=e.resp.status
            jsonobj=json.loads(e.content.strip())
            error={"resp":e.resp,"content":e.content.strip(), "message":jsonobj["error"]["message"]}
            self.response.out.write(json.dumps(error))
            

class DelHandler(webapp2.RedirectHandler):

    def get(self):
        pass


app = webapp2.WSGIApplication([
   ('/', MainHandler),('/json', JsonHandler)
], debug=True)

def main():
   app

if __name__ == '__main__':
    main()